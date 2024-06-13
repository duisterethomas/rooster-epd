from epd_2in9_b import EPD_2in9_B
from zermelo_api import Client
from ntp import set_time

import network
import json
import time

from machine import Pin

# Set led pin
led = Pin("LED", Pin.OUT)

# Init the epd
epd = EPD_2in9_B()

# Turn on led
led.on()

# Load the save file
try:
    with open("save.json", "r") as file:
        save = json.load(file)
except OSError:  # open failed
    save = {"wlan": {},
            "time_offset": 2,
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
print("Get the current time with NTP")
set_time()

# Get the appointments
print("Get the appointments")
local_time = time.localtime()

starttimestamp = round(time.time() - (local_time[3] * 60 * 60) - (local_time[4] * 60) - local_time[5])
endtimestamp = round(time.time() + ((24 - local_time[3]) * 60 * 60) + ((60 - local_time[4]) * 60) + (60 - local_time[5]))
weekday = local_time[6]

lessons_today = []

# Get the lessons of today
if wlan.isconnected():
    appointments = Client(save["school"]).get_appointments(save["token"], str(starttimestamp), str(endtimestamp))

    lessons : list = appointments['response']['data']
    for lesson in lessons:
        # Preprocess some of the data
        lesson['start'] = time.localtime(lesson['start'] + (save["time_offset"] * 60 * 60))
        lesson['end'] = time.localtime(lesson['end'] + (save["time_offset"] * 60 * 60))
        lesson['startTimeSlotName'] = lesson['startTimeSlotName'].upper()
        
        for i in range(len(lesson["subjects"])):
            lesson['subjects'][i] = lesson['subjects'][i].upper()
        
        lessons_today.append(lesson.copy())

# Add the afspraken to lessons_today
#for afspraak in save["afspraken"]:
#    if afspraak["date"] == None:
#        lesson = {}
#        lesson["start"] = time.localtime(afspraak["startTime"])
#        lesson["end"] = time.localtime(afspraak["endTime"])
#        lesson["cancelled"] = False
#        lesson["subjects"] = [afspraak["subjects"]]
#        lesson["locations"] = [afspraak["locations"]]
#        lesson['startTimeSlotName'] = afspraak["timeSlotName"]
#        
#        lessons_today.append(deepcopy(lesson))

# Set the max size based on if there is a note
if save["notes"][weekday] == "": max_size = 298
else: max_size = 286

# Init the layers
epd.imageblack.fill(0x00)
epd.imagered.fill(0xff)

# Show it on the epd
for lesson in lessons_today:
    # Get the start and end time in datetime format
    lesson_starttime = lesson['start']
    lesson_endtime = lesson['end']
    
    # Set the appointment colour
    if lesson['cancelled']: colour = 0x00
    else: colour = 0xff
    
    # Set the block position and size
    # (Lesson starttime in minutes - first lesson starttime) / (Last lesson endtime - First lesson starttime) * max_size
    # (Lesson endtime in minutes - first lesson starttime) / (Last lesson endtime - First lesson starttime) * max_size - 2
    ystartpos = round(((lesson_starttime[3] * 60) + lesson_starttime[4] - save["starttime"]) / (save["endtime"] - save["starttime"]) * max_size)
    yendpos = round(((lesson_endtime[3] * 60) + lesson_endtime[4] - save["starttime"]) / (save["endtime"] - save["starttime"]) * max_size) - 2
    ysize = yendpos - ystartpos
    
    # If the startpos and size are greater than or equal to 0 draw a rectangle on the epd
    if ystartpos >= 0 and ysize >= 0:
        # Draw a white filled rectangle on the epd to overwrite possible previous data
        epd.imagered.rect(0, ystartpos, 152, ysize, 0xff, 1)
        epd.imageblack.rect(0, ystartpos, 152, ysize, 0x00, 1)
        
        # Draw a rectangle outline
        epd.imagered.rect(0, ystartpos, 152, ysize, colour, 0)
        epd.imageblack.rect(0, ystartpos, 152, ysize, colour, 0)
    
    lineystartpos = ystartpos + 3
    lineyendpos = yendpos - 4
    
    # If the startpos and endpos are greater than or equal to 0 draw a line on the epd
    if lineystartpos >= 0 and lineyendpos >= 0:
        epd.imagered.line(46, lineystartpos, 46, lineyendpos, colour)
        epd.imageblack.line(46, lineystartpos, 46, lineyendpos, colour)
    
    # Set the starttimestamp + position
    starttimestamp = f"{" " if lesson_starttime[3] < 10 else ""}{lesson_starttime[3]}:{"0" if lesson_starttime[4] < 10 else ""}{lesson_starttime[4]}"
    
    # Set the ypos
    starttimestamp_ypos = ystartpos + 4
    
    # If starttimestamp y pos is greater than or equal to 0 draw the start timestamp on the epd
    if starttimestamp_ypos >= 0:
        epd.imagered.text(starttimestamp, 3, starttimestamp_ypos, colour)
        epd.imageblack.text(starttimestamp, 3, starttimestamp_ypos, colour)
    
    # Set the endtimestamp + position
    endtimestamp = f"{" " if lesson_endtime[3] < 10 else ""}{lesson_endtime[3]}:{"0" if lesson_endtime[4] < 10 else ""}{lesson_endtime[4]}"
    
    # Set the ypos
    endtimestamp_ypos = yendpos - 11
    
    # If endtimestamp y pos is greater than or equal to 0 draw the end timestamp on the epd
    if endtimestamp_ypos >= 0:
        epd.imagered.text(endtimestamp, 3, endtimestamp_ypos, colour)
        epd.imageblack.text(endtimestamp, 3, endtimestamp_ypos, colour)
    
    # Set the subjects + position
    if len(lesson['subjects']) != 0:
        for subject in enumerate(lesson['subjects']):
            if subject[0] == 0:
                subjects = subject[1]
            else:
                subjects += f",{subject[1]}"
        subject_ypos = ystartpos + 4
        
        # If the subject y pos is greater than or equal to 0 draw the subject on the epd
        if subject_ypos >= 0:
            epd.imagered.text(subjects, 50, subject_ypos, colour)
            epd.imageblack.text(subjects, 50, subject_ypos, colour)
    
    # Set the locations + position
    if len(lesson['locations']) != 0:
        for location in enumerate(lesson['locations']):
            if location[0] == 0:
                locations = location[1]
            else:
                locations += f",{location[1]}"
        
        # Set the location_ypos to the endtimestamp_ypos if endtimestamp_ypos is smaller than ystartpos + 16
        location_ypos = min(ystartpos + 16, endtimestamp_ypos)
        
        # If the location y pos is greater than or equal to 0 draw the location on the epd
        if location_ypos >= 0:
            epd.imagered.text(locations, 50, location_ypos, colour)
            epd.imageblack.text(locations, 50, location_ypos, colour)
    
    # Set the hour + position
    hour : str = lesson['startTimeSlotName']
    hour_ypos = ystartpos + 4
    hour_xpos = 149 - (len(hour) * 8)
    
    # if the hour position is greater than or equal to 0 draw the hour
    if hour_ypos >= 0 and hour_xpos >= 0:
        epd.imagered.text(hour, hour_xpos, hour_ypos, colour)
        epd.imageblack.text(hour, hour_xpos, hour_ypos, colour)

# Draw the note if it isn't empty
if save["notes"][weekday] != "":
    epd.imagered.text(save["notes"][weekday], 2, 288, 0xff)
    epd.imageblack.text(save["notes"][weekday], 2, 288, 0xff)

# Display it
epd.display()

# Turn off led
led.off()