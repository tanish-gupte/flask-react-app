# from cryptography.fernet import Fernet

# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives import serialization


import rsa

class Cryptography:
    def __init__(self):
        pass

    def generate_keys (self):
        public_key, private_key = rsa.newkeys(1024) # generates a key with long nos

        print("public_key: ", public_key)
        print("private_key :", private_key)

        # write
        with open("public_key.pem", "wb") as f:
            f.write(public_key.save_pkcs1("PEM"))

        with open("private_key.pem", "wb") as f:
            f.write(private_key.save_pkcs1("PEM"))

    def load_keys (self):
        with open("public_key.pem", "rb") as f:
            public_key = rsa.PublicKey.load_pkcs1(f.read())

        with open("private_key.pem", "rb") as f:
            private_key = rsa.PrivateKey.load_pkcs1(f.read())    

        return public_key, private_key

    def encrypt_data (self, data, key):
        encrypted_msg = rsa.encrypt(data.encode(), key) # will take public key
        print("encrypted_msg ", encrypted_msg)    

# class Cryptography:
#     def __init__(self):
#         pass

#     def generatePrivateAndPublicPem(self):
#         private_key = rsa.generate_private_key(
#             public_exponent=65537,
#             key_size=2048,
#         )

#         public_key = private_key.public_key()

#         private_pem = private_key.private_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PrivateFormat.PKCS8,
#             encryption_algorithm=serialization.NoEncryption(),
#         )

#         public_pem = public_key.public_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PublicFormat.SubjectPublicKeyInfo,
#         )

#         with open("private.pem", "wb") as key_file:
#             key_file.write(private_pem)

#         with open("public.pem", "wb") as key_file:
#             key_file.write(public_pem)

#         print("private_pem", private_pem)
#         print("public_pem", public_pem)

#         encryptedData = public_key.encrypt(
#             message,
#             padding.OAEP(
#             mgf=padding.MGF1(algorithm=hashes.SHA256()),
#             algorithm=hashes.SHA256(),
#             label=None
#             )
#         )
#         return 
     

# cryptography = Cryptography()   
# publicAndPrivatePem = cryptography.generatePrivateAndPublicPem()

