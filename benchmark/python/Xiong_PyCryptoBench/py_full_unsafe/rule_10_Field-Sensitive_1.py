from cryptography.hazmat.primitives.asymmetric import rsa


class BaseRunner(object):

    def __init__(self, argument):
        self.argument = argument


runner_object = BaseRunner(rsa.generate_private_key)
private_key = runner_object.argument(
    public_exponent=65537,
    key_size=512,
)
print(private_key)
