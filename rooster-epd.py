from zermelo import Client
from os.path import exists
from copy import deepcopy
from time import sleep
import datetime
import serial

def send_to_pico(command):
    pico.write(f"{command}\r".encode())
    
    recieved = pico.read_until().strip()
    while not recieved:
        sleep(0.1)
        recieved = pico.read_until().strip()
    
    print(recieved.decode())
    
    return recieved.decode()

cl = Client("csghetstreek")

if exists("token.txt"):
    token = open("token.txt", "r").read()
else:
    token = cl.authenticate(input("Koppel code: "))["access_token"]
    with open("token.txt", "w") as f:
        f.write(token)

# Get the user code
usercode = cl.get_user(token)["response"]["data"][0]["code"]

# Get the current week
today = datetime.date.today()
isocal = datetime.date.isocalendar(today)
# If weeknum below 10 add zero: {"0"*isocal[1]<10}
#enrollments = cl.get_liveschedule(token, f"{isocal[0]}{"0"*(isocal[1]<10)}{isocal[1]}", usercode)
enrollments = cl.get_liveschedule(token, "202343", usercode) ### Temp for debugging

# Get the lessons of today
lessons : list = enrollments['response']['data'][0]['appointments']
lessons_today = []
for lesson in lessons:
    #if datetime.datetime.fromtimestamp(lesson['start']).isoweekday() == today.isoweekday():
    if datetime.datetime.fromtimestamp(lesson['start']).isoweekday() == 1:### Temp for debugging
        lessons_today.append(deepcopy(lesson))

# Show it on the epd
pico = serial.Serial(port="COM5", parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1)
pico.flush()
send_to_pico("init")

for lesson in enumerate(lessons_today):
    ypos = lesson[0] * 32
    lesson_ypos = ypos + 12
    lesson_subject : str = lesson[1]['subjects'][0]
    
    # Set the right colour
    if lesson[1]['cancelled']: colour = "r"
    else: colour = "b"

    send_to_pico(f"rect{colour}000{"0"*((ypos<100)+(ypos<10))}{ypos}1520300")
    send_to_pico(f"text{colour}010{"0"*((lesson_ypos<100)+(lesson_ypos<10))}{lesson_ypos}{lesson_subject.upper()}")

send_to_pico("show")
pico.close()