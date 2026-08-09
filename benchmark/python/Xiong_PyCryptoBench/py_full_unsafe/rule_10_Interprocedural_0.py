from cryptography.hazmat.primitives.asymmetric import rsa


def call_method(argument):
    private_key = argument(
        public_exponent=65537,
        key_size=512,
    )
    print(private_key)


def starting_method():
    call_method(rsa.generate_private_key)


starting_method()
