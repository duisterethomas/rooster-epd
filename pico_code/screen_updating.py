import network
import time
from json import load, dump
from machine import Pin

from epd_2in9_b import EPD_2in9_B
from ntp import set_time
from zermelo_api import Client


def connect(timeout: int):
    # Load the save file
    try:
        with open('save.json', 'r') as file:
            save = load(file)
    except OSError:  # open failed
        save = None
    
    # Get a list of all available networks
    networks = wlan.scan() # list with tupples with 6 fields ssid, bssid, channel, RSSI, security, hidden

    networks.sort(key=lambda x: x[3]) # sorted on RSSI (3)

    # Connect to network if in list
    for w in networks:
        ssid = w[0].decode()
        
        if ssid in save['wlan'].keys():
            wlan.connect(ssid, save['wlan'][ssid])
            
            print(f'Connecting to {ssid}')
            
            while not wlan.isconnected() and timeout > 0:
                time.sleep(0.5)
                timeout -= 0.5
                led.toggle()
                
                if wlan.status() == network.STAT_WRONG_PASSWORD:
                    print('Wrong wifi password')
                    break
                elif wlan.status() == network.STAT_NO_AP_FOUND:
                    print('Wifi not found')
                    break
                elif wlan.status() == network.STAT_CONNECT_FAIL:
                    print('Wifi error')
                    break
                
            if wlan.isconnected():
                print('Connected!')
                led.on()
                break
            else:
                led.off()
    
    if wlan.isconnected():
        # Test if token is valid
        if not save['token']:
            print('Zermelo nog niet gekoppeld')
        else:
            try:
                # Dummy request to check if token is active
                Client(save['school']).get_user(save['token'])
            except ValueError:
                print('Token invalid: koppel zermelo opnieuw')

        # Set the time
        print('Get the current time with NTP')
        set_time()


def disconnect():
    wlan.disconnect()


def sync():
    # Load the save file
    try:
        with open('save.json', 'r') as file:
            save = load(file)
    except OSError:  # open failed
        save = None
    
    # Turn on led
    led.on()
    
    if wlan.isconnected():
        # Get the appointments
        print('Get the appointments')
        local_time = time.localtime(time.time() + save['time_offset'])

        starttimestamp = round(time.time() + save['time_offset'] - (local_time[3] * 3600) - (local_time[4] * 60) - local_time[5])
        endtimestamp = starttimestamp + 86400
        weekday = local_time[6]

        lessons_today = []

        # Get the lessons of today
        appointments = Client(save['school']).get_appointments(save['token'], str(starttimestamp - save['time_offset']), str(endtimestamp - save['time_offset']))
        lessons: list = appointments['response']['data']
        
        # Sort the lessons list based on last modified and created
        lessons.sort(key=lambda x: (x['lastModified'], x['created']), reverse=True)
        
        handled_instances = []
        for lesson in lessons:
            # Add the lesson to lessons_today if not already in there based on the appointment instance
            if lesson['appointmentInstance'] not in handled_instances:
                handled_instances.append(lesson['appointmentInstance'])
                
                # Preprocess some of the data
                lesson['start'] = time.localtime(lesson['start'] + save['time_offset'])
                lesson['end'] = time.localtime(lesson['end'] + save['time_offset'])
                lesson['startTimeSlotName'] = lesson['startTimeSlotName'].upper()
                lesson['endTimeSlotName'] = lesson['endTimeSlotName'].upper()
                
                for i in range(len(lesson['subjects'])):
                    lesson['subjects'][i] = lesson['subjects'][i].upper()
                
                lessons_today.append(lesson.copy())
        
        # Add the appointments to lessons_today
        for appointment in save['appointments']:
            appointmenttimestamp = time.mktime((appointment['date'][0], appointment['date'][1], appointment['date'][2], appointment['startTime'][0], appointment['startTime'][1], 0, 0, 0)) + save['time_offset']
            
            if starttimestamp <= appointmenttimestamp < endtimestamp:
                lesson = {'start': time.localtime((appointment['startTime'][0] * 3600) + (appointment['startTime'][1] * 60)),
                          'end': time.localtime((appointment['endTime'][0] * 3600) + (appointment['endTime'][1] * 60)),
                          'cancelled': False,
                          'subjects': [appointment['subjects']],
                          'locations': [appointment['locations']],
                          'startTimeSlotName': appointment['timeSlotName'],
                          'endTimeSlotName': appointment['timeSlotName']}
                
                lessons_today.append(lesson.copy())
            
            # Automatically remove old appointments
            elif appointmenttimestamp < starttimestamp:
                save['appointments'].remove(appointment)
                
                with open('save.json', 'w') as file:
                    dump(save, file)

        # Print the lessons of today
        print(lessons_today)
        
        # Set the max size based on if there is a note
        if save['notes'][weekday] == '': max_size = 298
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
            ystartpos = round(((lesson_starttime[3] * 60) + lesson_starttime[4] - save['starttime']) / (save['endtime'] - save['starttime']) * max_size)
            yendpos = round(((lesson_endtime[3] * 60) + lesson_endtime[4] - save['starttime']) / (save['endtime'] - save['starttime']) * max_size) - 2
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
            starttimestamp = f'{' ' if lesson_starttime[3] < 10 else ''}{lesson_starttime[3]}:{'0' if lesson_starttime[4] < 10 else ''}{lesson_starttime[4]}'
            
            # Set the ypos
            starttimestamp_ypos = ystartpos + 4
            
            # If starttimestamp y pos is greater than or equal to 0 draw the start timestamp on the epd
            if starttimestamp_ypos >= 0:
                epd.imagered.text(starttimestamp, 3, starttimestamp_ypos, colour)
                epd.imageblack.text(starttimestamp, 3, starttimestamp_ypos, colour)
            
            # Set the endtimestamp + position
            endtimestamp = f'{' ' if lesson_endtime[3] < 10 else ''}{lesson_endtime[3]}:{'0' if lesson_endtime[4] < 10 else ''}{lesson_endtime[4]}'
            
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
                        subjects += f',{subject[1]}'
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
                        locations += f',{location[1]}'
                
                # Set the location_ypos to the endtimestamp_ypos if endtimestamp_ypos is smaller than ystartpos + 16
                location_ypos = min(ystartpos + 16, endtimestamp_ypos)
                
                # If the location y pos is greater than or equal to 0 draw the location on the epd
                if location_ypos >= 0:
                    epd.imagered.text(locations, 50, location_ypos, colour)
                    epd.imageblack.text(locations, 50, location_ypos, colour)
            
            # Set the hour name
            if lesson['startTimeSlotName'] != lesson['endTimeSlotName'] and lesson['startTimeSlotName'] and lesson['endTimeSlotName']:
                hour: str = f"{lesson['startTimeSlotName']}-{lesson['endTimeSlotName']}"
            elif lesson['startTimeSlotName']:
                hour: str = lesson['startTimeSlotName']
            elif lesson['endTimeSlotName']:
                hour: str = lesson['endTimeSlotName']
            else:
                hour = ""
            
             # Set the hour position and draw it if it isn't empty
            if hour:
                hour_ypos = ystartpos + 4
                hour_xpos = 149 - (len(hour) * 8)
                
                # if the hour position is greater than or equal to 0 draw the hour
                if hour_ypos >= 0 and hour_xpos >= 0:
                    epd.imagered.text(hour, hour_xpos, hour_ypos, colour)
                    epd.imageblack.text(hour, hour_xpos, hour_ypos, colour)

        # Draw the note if it isn't empty
        if save['notes'][weekday] != '':
            epd.imagered.text(save['notes'][weekday], 2, 288, 0xff)
            epd.imageblack.text(save['notes'][weekday], 2, 288, 0xff)

        # Display it
        epd.display()

    # Turn off led
    led.off()


def handle_command(data: str):
    # Sync command
    if data == 'sync':
        # Connect to wifi if not already
        if not wlan.isconnected():
            connect(30)
        
        # Sync the display
        sync()
        
        print('done')
    
    # Unknown command recieved
    else:
        print(f'Unknown command: {data}')
        
        print('done')


# Set led pin
led = Pin('LED', Pin.OUT)

# Init the epd
epd = EPD_2in9_B()

# Activate wlan
wlan = network.WLAN(network.STA_IF)
wlan.active(True)