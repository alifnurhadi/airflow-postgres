from cryptography.fernet import Fernet

# Generate a new Fernet key
key = Fernet.generate_key()

# Print or store the key
print(key.decode())  # Decoding to make it human-readable if needed
