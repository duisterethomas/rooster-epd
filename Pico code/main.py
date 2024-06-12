from zermelo_api import Client
from ntp import set_time

from math import ceil
import network
import json
import time

from machine import Pin

# Set led pin
led = Pin("LED", Pin.OUT)

# Turn on led
led.on()

# Load the save file
try:
    with open("save.json", "r") as file:
        save = json.load(file)
except OSError:  # open failed
    save = {"wlan": {},
            "school": "",
            "token": "",
            "starttime": 510,
            "endtime": 970,
            "notes": ("", "", "", "", "", "", ""),
            "appointments": []}
    
    with open("save.json", "w") as file:
        json.dump(save, file)

# Get a list of all available networks
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
networks = wlan.scan() # list with tupples with 6 fields ssid, bssid, channel, RSSI, security, hidden

networks.sort(key=lambda x:x[3], reverse=True) # sorted on RSSI (3)

# Connect to network if in list
for w in networks:
    ssid = w[0].decode()
    
    if ssid in save["wlan"].keys():
        wlan.connect(ssid, save["wlan"][ssid])
        
        print(f'Connecting to {ssid}')
        
        timeout = 10
        while not wlan.isconnected() and timeout != 0:
            time.sleep(1)
            timeout -= 1
            
        if wlan.isconnected():
            print("Connected!")
            break
        else:
            print("Connection failed")

# Test if token is valid
if not save["token"]:
    print("Zermelo nog niet gekoppeld")
else:
    try:
        # Dummy request to check if token is active
        Client(save["school"]).get_user(save["token"])
    except ValueError:
        print("Token invalid: koppel zermelo opnieuw")

# Set the time
set_time()

# Get the appointments
local_time = time.localtime()
starttimestamp = round(time.time() - (local_time[3] * 60 * 60) - (local_time[4] * 60) - local_time[5])
endtimestamp = round(time.time() + ((24 - local_time[3]) * 60 * 60) + ((60 - local_time[4]) * 60) + (60 - local_time[5]))

appointments = Client(save["school"]).get_appointments(save["token"], str(starttimestamp), str(endtimestamp))

print(appointments)

# Turn off led
led.off()