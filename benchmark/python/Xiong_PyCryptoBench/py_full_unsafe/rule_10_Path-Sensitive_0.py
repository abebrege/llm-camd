from cryptography.hazmat.primitives.asymmetric import rsa
if True:
    if str(input("Accept Path?")).lower() == "yes":
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=512,
        )
        print(private_key)
    else:
        print("Didn't accept path")
