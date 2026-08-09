from cryptography.hazmat.primitives.asymmetric import rsa

x = rsa


def starting_method():
    global x
    private_key = x.generate_private_key(
        public_exponent=65537,
        key_size=512,
    )
    print(private_key)


starting_method()
