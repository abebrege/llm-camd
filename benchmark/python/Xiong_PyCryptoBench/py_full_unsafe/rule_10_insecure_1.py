from cryptography.hazmat.primitives.asymmetric import dsa

private_key = dsa.generate_private_key(key_size=1024)
print(private_key)
