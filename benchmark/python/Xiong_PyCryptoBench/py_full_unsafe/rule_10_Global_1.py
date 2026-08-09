from cryptography.hazmat.primitives.asymmetric import rsa

x = rsa.generate_private_key


def starting_method():
    global x
    private_key = x(
        public_exponent=65537,
        key_size=512,
    )
    print(private_key)


starting_method()
