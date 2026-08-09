from __future__ import annotations
import os
from dataclasses import dataclass
import requests

DEFAULT_TIMEOUT = 300
MAX_RETRIES = 5
MAX_OUTPUT_TOKENS = 32000

@dataclass(frozen=True)
class ModelSpec:
    provider: str
    model_id: str
    api_key_env: str = ""
    base_url: str = ""

MODELS: dict[str, ModelSpec] = {
    "opus": ModelSpec("anthropic", "claude-opus-5", "CLAUDE_API_KEY"),
    "sonnet": ModelSpec("anthropic", "claude-sonnet-5", "CLAUDE_API_KEY"),
    "gpt-5.1": ModelSpec("openai", "gpt-5.1", "OPENAI_API_KEY"),
    "gpt-5": ModelSpec("openai", "gpt-5", "OPENAI_API_KEY"),
    "deepseek": ModelSpec(
        "deepseek", "deepseek-reasoner", "DEEPSEEK_API_KEY", "https://api.deepseek.com/v1"
    ),
    "kimi-k2": ModelSpec(
        "moonshot", "kimi-k2-thinking", "MOONSHOT_API_KEY", "https://api.moonshot.ai/v1"
    ),
    "qwen3": ModelSpec("ollama", "qwen3:8b", base_url="http://localhost:11434"),
}

_DEFAULT_KEY_ENV = {
    "anthropic": "CLAUDE_API_KEY",
    "openai": "OPENAI_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "moonshot": "MOONSHOT_API_KEY",
}
_DEFAULT_BASE_URL = {
    "deepseek": "https://api.deepseek.com/v1",
    "moonshot": "https://api.moonshot.ai/v1",
    "ollama": "http://localhost:11434",
}


def get_model(name: str, timeout: int = DEFAULT_TIMEOUT) -> Model:
    spec = MODELS.get(name)
    if spec is None:
        if ":" not in name:
            raise ValueError(
                f"Unknown model '{name}'. Choose one of: {', '.join(list_models())}, "
                "or pass 'provider:model_id'."
            )
        provider, model_id = name.split(":", 1)
        if provider not in _DEFAULT_KEY_ENV and provider != "ollama":
            raise ValueError(f"Unknown provider '{provider}' in model '{name}'.")
        spec = ModelSpec(
            provider,
            model_id,
            _DEFAULT_KEY_ENV.get(provider, ""),
            _DEFAULT_BASE_URL.get(provider, ""),
        )
    return Model(name, spec, timeout)

def list_models() -> list[str]:
    return list(MODELS)

def _api_key(spec: ModelSpec) -> str:
    key = os.getenv(spec.api_key_env) or os.getenv("API_KEY")
    if not key:
        raise RuntimeError(f"{spec.api_key_env} is not set. Please set it in the .env file.")
    return key

def _build(spec: ModelSpec, timeout: int):
    if spec.provider == "anthropic":
        return _Anthropic(spec, timeout)
    if spec.provider == "openai":
        return _OpenAICompatible(spec, timeout, reasoning_effort="high")
    if spec.provider in ("deepseek", "moonshot"):
        return _OpenAICompatible(spec, timeout)
    if spec.provider == "ollama":
        return _Ollama(spec, timeout)
    raise ValueError(f"Unknown provider: {spec.provider}")

class Model:
    def __init__(self, name: str, spec: ModelSpec, timeout: int = DEFAULT_TIMEOUT):
        self.name = name
        self.spec = spec
        self._call = _build(spec, timeout)

    def complete(self, prompt: str) -> str:
        return self._call(prompt)

class _Anthropic:
    def __init__(self, spec: ModelSpec, timeout: int):
        import anthropic

        self._model_id = spec.model_id
        self._client = anthropic.Anthropic(
            api_key=_api_key(spec), timeout=timeout, max_retries=MAX_RETRIES
        )

    def __call__(self, prompt: str) -> str:
        with self._client.messages.stream(
            model=self._model_id,
            max_tokens=MAX_OUTPUT_TOKENS,
            thinking={"type": "adaptive"},
            output_config={"effort": "high"},
            messages=[{"role": "user", "content": prompt}],
        ) as stream:
            message = stream.get_final_message()
        if message.stop_reason == "refusal":
            raise RuntimeError("Request was declined by the model's safety classifiers.")
        return "".join(block.text for block in message.content if block.type == "text")

class _OpenAICompatible:
    def __init__(self, spec: ModelSpec, timeout: int, reasoning_effort: str = ""):
        from openai import OpenAI

        self._model_id = spec.model_id
        self._reasoning_effort = reasoning_effort
        self._client = OpenAI(
            api_key=_api_key(spec),
            base_url=spec.base_url or None,
            timeout=timeout,
            max_retries=MAX_RETRIES,
        )

    def __call__(self, prompt: str) -> str:
        kwargs = {"reasoning_effort": self._reasoning_effort} if self._reasoning_effort else {}
        response = self._client.chat.completions.create(
            model=self._model_id,
            max_completion_tokens=MAX_OUTPUT_TOKENS,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )
        return response.choices[0].message.content or ""

class _Ollama:
    def __init__(self, spec: ModelSpec, timeout: int):
        self._model_id = spec.model_id
        self._endpoint = f"{spec.base_url.rstrip('/')}/api/chat"
        self._timeout = timeout

    def __call__(self, prompt: str) -> str:
        try:
            response = requests.post(
                self._endpoint,
                json={
                    "model": self._model_id,
                    "messages": [{"role": "user", "content": prompt}],
                    "think": True,
                    "stream": False,
                    "options": {"temperature": 0, "num_predict": MAX_OUTPUT_TOKENS},
                },
                timeout=self._timeout,
            )
            response.raise_for_status()
            return response.json()["message"]["content"].strip()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama API call failed: {str(e)}")
