from datetime import datetime, date, timezone
from json import load, dump
from os.path import expanduser, isfile
from PIL import Image, ImageDraw, ImageFont
from sys import argv
from waveshare_epd import epd2in13g
from zermelo import Client

# Initializing the epd
print('Initializing EPD')
epd = epd2in13g.EPD()
epd.init()

# Initialize the font
font = ImageFont.truetype(expanduser('~/rooster-epd/om_thick_plain.ttf'), 8)

if isfile(expanduser('~/rooster-epd/save.json')):
    # Load the save file
    print('Loading save file')
    with open(expanduser('~/rooster-epd/save.json'), 'r') as file:
        save = load(file)
else:
    # Generate new save file
    print('Generating new save file')
    save = {"templates": {},
            "starttime": 0,
            "endtime": 0,
            "token": "",
            "school": "",
            "notes": ["",
                      "",
                      "",
                      "",
                      "",
                      "",
                      ""],
            "appointments": []}

    with open(expanduser('~/rooster-epd/save.json'), 'w') as file:
            dump(save, file)

# Get the date
if len(argv) > 1:
    # Get the date from the command line arguments
    sync_date = date.fromisoformat(argv[1])
else:
    # Else use current date
    sync_date = date.today()

print(f'Getting appointments from {sync_date}')

# Convert the date to timestamps, week day and week number
start_timestamp = round(datetime.combine(sync_date, datetime.min.time()).timestamp())
end_timestamp = start_timestamp + 86400
weekday = sync_date.weekday()
week = sync_date.isocalendar().week

# Get all lessons of this week
usercode = Client(save['school']).get_user(token=save['token'])['response']['data'][0]['code']
appointments = Client(save['school']).get_liveschedule(token=save['token'], week=f'{sync_date.year}{"0" * (week < 10)}{week}', usercode=usercode)
lessons: list = appointments['response']['data'][0]['appointments']

# Get the lessons of today
lessons_today = []
for lesson in lessons:
    # Add the lesson to lessons_today if appointmentInstance isn't null and it is for today
    if lesson['appointmentInstance'] and start_timestamp <= lesson['start'] < end_timestamp:
        # Preprocess some of the data
        lesson['start'] = datetime.fromtimestamp(lesson['start'])
        lesson['end'] = datetime.fromtimestamp(lesson['end'])
        lesson['startTimeSlotName'] = lesson['startTimeSlotName'].upper()
        lesson['endTimeSlotName'] = lesson['endTimeSlotName'].upper()
        
        for i in range(len(lesson['subjects'])):
            lesson['subjects'][i] = lesson['subjects'][i].upper()
        
        lessons_today.append(lesson.copy())

# Add custom appointments to lessons_today
for appointment in save['appointments']:
    appointmenttimestamp = datetime(appointment['date'][0], appointment['date'][1], appointment['date'][2], appointment['startTime'][0], appointment['startTime'][1]).timestamp()
    
    if start_timestamp <= appointmenttimestamp < end_timestamp:
        lesson = {'start': datetime.fromtimestamp((appointment['startTime'][0] * 3600) + (appointment['startTime'][1] * 60), timezone.utc),
                  'end': datetime.fromtimestamp((appointment['endTime'][0] * 3600) + (appointment['endTime'][1] * 60), timezone.utc),
                  'cancelled': False,
                  'appointmentType': 'custom',
                  'subjects': [appointment['subjects']],
                  'locations': [appointment['locations']],
                  'startTimeSlotName': appointment['timeSlotName'],
                  'endTimeSlotName': appointment['timeSlotName']}
        
        lessons_today.append(lesson.copy())
    
    # Automatically remove old appointments
    elif appointmenttimestamp < start_timestamp:
        save['appointments'].remove(appointment)
        
        with open(expanduser('~/rooster-epd/save.json'), 'w') as file:
            dump(save, file)

# Print the lessons of today
print(lessons_today)

# Set the max size based on if there is a note
if save['notes'][weekday]: max_size = 240
else: max_size = 252

# Create new image
Himage = Image.new('RGB', (epd.width, epd.height), epd.WHITE)
draw = ImageDraw.Draw(Himage)

# Show the schedule on the epd
for lesson in lessons_today:
    # Get the start and end time in datetime format
    lesson_starttime = lesson['start']
    lesson_endtime = lesson['end']
    
    # Set the appointment colour
    if lesson['cancelled']: colour = epd.RED
    elif lesson['appointmentType'] == 'exam': colour = epd.YELLOW
    else: colour = epd.BLACK
    
    # Set the block position and size
    # (Lesson starttime in minutes - first lesson starttime) / (Last lesson endtime - First lesson starttime) * max_size
    # (Lesson endtime in minutes - first lesson starttime) / (Last lesson endtime - First lesson starttime) * max_size - 2
    ystartpos = round(((lesson_starttime.hour * 60) + lesson_starttime.minute - save['starttime']) / (save['endtime'] - save['starttime']) * max_size)
    yendpos = round(((lesson_endtime.hour * 60) + lesson_endtime.minute - save['starttime']) / (save['endtime'] - save['starttime']) * max_size) - 2
    
    # If the startpos and endpos are greater than or equal to 0 draw a rectangle on the epd
    if ystartpos >= 0 and yendpos >= 0:
        # Draw a white filled rectangle with black outline
        draw.rectangle((0, ystartpos, 121, yendpos), fill=epd.WHITE, outline=colour)
    
    lineystartpos = ystartpos + 3
    lineyendpos = yendpos - 3
    
    # If the startpos and endpos are greater than or equal to 0 draw a line on the epd
    if lineystartpos >= 0 and lineyendpos >= 0:
        draw.line((45, lineystartpos, 45, lineyendpos), fill=colour)
    
    # Set the starttimestamp y pos
    top_text_ypos = ystartpos + 4
    
    # If starttimestamp y pos is greater than or equal to 0 draw the start timestamp on the epd
    if top_text_ypos >= 0:
        draw.text((2, top_text_ypos), f'{" " if lesson_starttime.hour < 10 else ""}{lesson_starttime.hour}:{"0" if lesson_starttime.minute < 10 else ""}{lesson_starttime.minute}', fill=colour, font=font)
    
    # Set the endtimestamp y pos
    endtimestamp_ypos = yendpos - 9
    
    # If endtimestamp y pos is greater than or equal to 0 draw the end timestamp on the epd
    if endtimestamp_ypos >= top_text_ypos + 8:
        draw.text((2, endtimestamp_ypos), f'{" " if lesson_endtime.hour < 10 else ""}{lesson_endtime.hour}:{"0" if lesson_endtime.minute < 10 else ""}{lesson_endtime.minute}', fill=colour, font=font)
    
    # Set the subjects + position
    if len(lesson['subjects']) != 0:
        for subject in enumerate(lesson['subjects']):
            if subject[0] == 0:
                subjects = subject[1]
            else:
                subjects += f',{subject[1]}'
        
        # If the y pos is greater than or equal to 0 draw the subject on the epd
        if top_text_ypos >= 0:
            draw.text((49, top_text_ypos), subjects, fill=colour, font=font)
    
    # Set the locations + position
    if len(lesson['locations']) != 0:
        for location in enumerate(lesson['locations']):
            if location[0] == 0:
                locations = location[1]
            else:
                locations += f',{location[1]}'
        
        # Set the location_ypos to the endtimestamp_ypos if endtimestamp_ypos is smaller than ystartpos + 16
        locations_ypos = min(ystartpos + 16, endtimestamp_ypos)
        
        # If the location y pos is greater than or equal to 0 draw the location on the epd
        if locations_ypos >= top_text_ypos + 8:
            draw.text((49, locations_ypos), locations, fill=colour, font=font)
        else:
            draw.text((49 + (len(subjects) * 8), locations_ypos), f'-{locations}', fill=colour, font=font)
    
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
        hour_xpos = 119 - (len(hour) * 8)
        
        # if the hour position is greater than or equal to 0 draw the hour
        if top_text_ypos >= 0 and hour_xpos >= 0:
            draw.text((hour_xpos, top_text_ypos), hour, fill=colour, font=font)

# Draw the note if it isn't empty
if save['notes'][weekday] != '':
    draw.text((2, 242), save['notes'][weekday], fill=epd.BLACK, font=font)

# Display the image
epd.display(epd.getbuffer(Himage))