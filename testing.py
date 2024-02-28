import bcrypt
import pybase64

password = input()
password = bytes(password, "utf-8")
b64password = pybase64.b64encode(password)
print(b64password)

hashedpassword = "$2b$14$s25kEBuH8.Njoplw4.kXTu7rLHEJ2y4dZOEucZLF2PfwljvuyE8ca"
hashedpassword = bytes(hashedpassword,"utf-8")
print("previous")
print(hashedpassword)
hashed = bcrypt.hashpw(password, bcrypt.gensalt(14))
print("new")
print(hashed)

if bcrypt.checkpw(password, hashedpassword):
    print("MAJA AAGAYA")