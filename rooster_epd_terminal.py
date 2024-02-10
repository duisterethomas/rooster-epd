from zermelo import Client
from os.path import exists
from copy import deepcopy
from time import sleep
from pickle import load, dump
import datetime
import serial
import glob
import sys

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def send_to_pico(command):
    pico.write(f"{command}\r".encode())
    
    recieved = pico.read_until().strip()
    while not recieved:
        sleep(0.1)
        recieved = pico.read_until().strip()
    
    print(recieved.decode())
    
    return recieved.decode()

available_ports = serial_ports()

# Check if save data exist
if exists("rooster-epd.data"):
    # Open and load the save_dict
    with open("rooster-epd.data", "rb") as save_file:
        save_dict = load(save_file)
    
    # Create the zermelo client
    cl = Client(save_dict["school"])
    
    # Check if the port is available
    if save_dict["port"] not in available_ports:
        # List the available ports
        print('Available ports:')
        for available_port in enumerate(available_ports):
            print(f"{available_port[0]}. {available_port[1]}")
        
        # Save the available port
        save_dict["port"] = available_ports[int(input("Port: "))]
        
        # Save the save_dict
        with open("rooster-epd.data", "wb") as save_file:
            dump(save_dict, save_file)
else:
    # Create a new save_dict
    save_dict = {}
    
    # Get and save the school name
    save_dict["school"] = input("School: ")
    
    # Create the zermelo client
    cl = Client(save_dict["school"])
    
    # Get and a new zermelo token
    save_dict["token"] = cl.authenticate(input("Koppel code: "))["access_token"]
    
    # Set the pico port
    # List the available ports
    print('Available ports:')
    for available_port in enumerate(available_ports):
        print(f"{available_port[0]}. {available_port[1]}")
    
    # Save the available port
    save_dict["port"] = available_ports[int(input("Port: "))]
    
    # Save the save_dict
    with open("rooster-epd.data", "wb") as save_file:
        dump(save_dict, save_file)

# Connect and initialize the pico epd
pico = serial.Serial(port=save_dict["port"], parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1)
pico.flush()
send_to_pico("init")

# Get the user code
usercode = cl.get_user(save_dict["token"])["response"]["data"][0]["code"]

# Get the current week and day
today = datetime.date.today()
isocal = datetime.date.isocalendar(today)
# Request: yyyyww
# yyyy = year: {isocal[0]}
# ww = weeknumber: {"0"*(isocal[1]<10)}{isocal[1]}
# If weeknum < 10 add zero: {"0"*isocal[1]<10}
enrollments = cl.get_liveschedule(save_dict["token"], f"{isocal[0]}{"0"*(isocal[1]<10)}{isocal[1]}", usercode)

# Get the lessons of today
lessons : list = enrollments['response']['data'][0]['appointments']
lessons_today = []
for lesson in lessons:
    # Check the day number: 1 = monday...
    if datetime.datetime.fromtimestamp(lesson['start']).isoweekday() == today.isoweekday():
        lessons_today.append(deepcopy(lesson))

# Show it on the epd
for lesson in lessons_today:
    # Get the start and end time in datetime format
    lesson_starttime = datetime.datetime.fromtimestamp(lesson['start'])
    lesson_endtime = datetime.datetime.fromtimestamp(lesson['end'])
    
    # Set the colour
    # If cancelled: red (r), else: black (b)
    if lesson['cancelled']: colour = "r"
    else: colour = "b"
    
    # Set the block position and size
    # 510 is 08:30 in minutes
    # 970 is 16:10 in minutes - 510 is 460
    ystartpos = round(((lesson_starttime.hour * 60) + lesson_starttime.minute - 510) / 460 * 298)
    yendpos = round(((lesson_endtime.hour * 60) + lesson_endtime.minute - 510) / 460 * 298) - 2
    ysize = yendpos - ystartpos
    send_to_pico(f"rect{colour}000{"0"*((ystartpos<100)+(ystartpos<10))}{ystartpos}152{"0"*((ysize<100)+(ysize<10))}{ysize}0")
    
    # Set the timestamps + positions
    starttimestamp = lesson_starttime.strftime('%H:%M').removeprefix("0")
    if len(starttimestamp) < 5: starttimestamp = " " + starttimestamp
    starttimestamp_ypos = ystartpos + 4
    send_to_pico(f"text{colour}003{"0"*((starttimestamp_ypos<100)+(starttimestamp_ypos<10))}{starttimestamp_ypos}{starttimestamp}")
    
    endtimestamp = lesson_endtime.strftime('%H:%M').removeprefix("0")
    if len(endtimestamp) < 5: endtimestamp = " " + endtimestamp
    endtimestamp_ypos = yendpos - 11
    send_to_pico(f"text{colour}003{"0"*((endtimestamp_ypos<100)+(endtimestamp_ypos<10))}{endtimestamp_ypos}{endtimestamp}")
    
    # Set the subjects + position
    if len(lesson['subjects']) != 0:
        for subject in enumerate(lesson['subjects']):
            if subject[0] == 0:
                subjects = subject[1].upper()
            else:
                subjects += f",{subject[1].upper()}"
        subject_ypos = ystartpos + 4
        send_to_pico(f"text{colour}050{"0"*((subject_ypos<100)+(subject_ypos<10))}{subject_ypos}{subjects}")
    
    # Set the locations + position
    if len(lesson['locations']) != 0:
        for location in enumerate(lesson['locations']):
            if location[0] == 0:
                locations = location[1]
            else:
                locations += f",{location[1]}"
        location_ypos = ystartpos + 16
        send_to_pico(f"text{colour}050{"0"*((location_ypos<100)+(location_ypos<10))}{location_ypos}{locations}")
    
    # Set the hour + position
    hour : str = lesson['startTimeSlotName'].upper()
    hour_ypos = ystartpos + 4
    hour_xpos = 149 - (len(hour) * 8)
    send_to_pico(f"text{colour}{"0"*((hour_xpos<100)+(hour_xpos<10))}{hour_xpos}{"0"*((hour_ypos<100)+(hour_ypos<10))}{hour_ypos}{hour}")

# Show the result
send_to_pico("show")
pico.close()