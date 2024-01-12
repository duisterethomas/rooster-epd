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

usercode = cl.get_user(token)["response"]["data"][0]["code"]
enrollments = cl.get_liveschedule(token, "202403", usercode) # Requests week 03 of the year 2024
lessons = enrollments['response']['data'][0]['appointments']
print(lessons)

with open("test.json", "w") as f:
    f.write(str(lessons))