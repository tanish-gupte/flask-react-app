import rsa 

public_key, private_key = rsa.newkeys(1024) # generates a key with long nos

print("public_key: ", public_key)
print("private_key :", private_key)

# write

with open("public_key.pem", "wb") as f:
    f.write(public_key.save_pkcs1("PEM"))

with open("private_key.pem", "wb") as f:
    f.write(private_key.save_pkcs1("PEM"))


# read

with open("public_key.pem", "rb") as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read())

with open("private_key.pem", "rb") as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read())

msg = "From Crypto Helper Fn"

encrypted_msg = rsa.encrypt(msg.encode(), public_key)
print("encrypted_msg ", encrypted_msg)

# write
with open("encrypted.message", "wb") as f:
    f.write(encrypted_msg)
    print("encrypted_msg: ", encrypted_msg)

with open("encrypted.message", "rb") as f:
    encrypted = f.read()
    print("encrypted :", encrypted)