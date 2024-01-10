from zermelo import Client
from os.path import exists
import time

cl = Client("csghetstreek")

if exists("token.txt"):
    token = open("token.txt", "r").read()
else:
    token = cl.authenticate(input("Koppel code: "))["access_token"]
    with open("token.txt", "w") as f:
        f.write(token)

user = cl.get_user(token)
print(user)

appointments = cl.get_appointments(token, time.time()-36000, time.time()+36000)
print(appointments)