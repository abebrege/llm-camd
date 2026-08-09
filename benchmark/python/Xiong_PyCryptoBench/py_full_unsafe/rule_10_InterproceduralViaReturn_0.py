from cryptography.hazmat.primitives.asymmetric import rsa


def call_method():

    def starting_method():
        rsa.generate_private_key(
            public_exponent=65537,
            key_size=512,
        )

    return starting_method


call_method()()
