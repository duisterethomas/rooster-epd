from serial import Serial, PARITY_EVEN, STOPBITS_ONE
from datetime import datetime, date, time
from zermelo import Client
from copy import deepcopy
from time import sleep

from PySide6.QtCore import QObject, Signal

# Thread for updating the epd
class Worker(QObject):
    finished = Signal()
    
    def __init__(self, ui_self, save_dict : dict, morgen : bool, offline : bool):
        super(Worker, self).__init__()
        self.ui_self = ui_self
        self.save_dict = save_dict
        self.morgen = morgen
        self.offline = offline
    
    # Function to send commands to the pico
    def send_to_pico(self, command):
        self.pico.write(f"{command}\r".encode())
        
        recieved = self.pico.read_until().strip()
        while not recieved:
            sleep(0.1)
            recieved = self.pico.read_until().strip()
        
        print(recieved.decode())
        
        return recieved.decode()
    
    def run(self):
        # Disable the UI and show message
        self.ui_self.centralwidget.setDisabled(True)
        self.ui_self.menuBar.setDisabled(True)
        
        # Connect and initialize the pico epd
        self.pico = Serial(port=self.save_dict["port"], parity=PARITY_EVEN, stopbits=STOPBITS_ONE, timeout=1)
        self.pico.flush()
        recv = self.send_to_pico("init")
        self.ui_self.statusbar.showMessage(recv)

        # Get the current week and day
        today = date.today()
        isocal = date.isocalendar(today)
        year = isocal[0]
        week = isocal[1]
        weekday = today.isoweekday()
        
        # If morgen add 1 day
        if self.morgen:
            if weekday == 7:
                weekday = 1
                if week == 52:
                    week == 1
                    year += 1
                else:
                    week += 1
            else:
                weekday += 1
        
        lessons_today = []
        
        if not self.offline:
            # Get the zermelo client
            cl = Client(self.save_dict["school"])
            
            # Get the usercode
            usercode = cl.get_user(self.save_dict["token"])["response"]["data"][0]["code"]
            
            # Request: yyyyww
            # yyyy = year: {isocal[0]}
            # ww = weeknumber: {"0"*(isocal[1]<10)}{isocal[1]}
            # If weeknum < 10 add zero: {"0"*isocal[1]<10}
            enrollments = cl.get_liveschedule(self.save_dict["token"], f"{year}{"0"*(week<10)}{week}", usercode)

            # Get the lessons of today
            lessons : list = enrollments['response']['data'][0]['appointments']
            for lesson in lessons:
                # Preprocess some of the data
                lesson['start'] = datetime.fromtimestamp(lesson['start'])
                lesson['end'] = datetime.fromtimestamp(lesson['end'])
                lesson['startTimeSlotName'] = lesson['startTimeSlotName'].upper()
                for i in range(len(lesson["subjects"])):
                    lesson['subjects'][i] = lesson['subjects'][i].upper()
                
                # Check the day number: 1 = monday...
                if lesson['start'].isoweekday() == weekday:
                    lessons_today.append(deepcopy(lesson))
        
        # Add the afspraken to lessons_today
        for afspraak in self.save_dict["afspraken"]:
            if date(afspraak["date"].year(), afspraak["date"].month(), afspraak["date"].day()).isoweekday() == weekday:
                lesson = {}
                lesson["start"] = time(afspraak["startTime"].hour(), afspraak["startTime"].minute(), 0, 0)
                lesson["end"] = time(afspraak["endTime"].hour(), afspraak["endTime"].minute(), 0, 0)
                lesson["cancelled"] = False
                lesson["subjects"] = [afspraak["subjects"]]
                lesson["locations"] = [afspraak["locations"]]
                lesson['startTimeSlotName'] = afspraak["timeSlotName"]
                
                lessons_today.append(deepcopy(lesson))

        # Set the max size base don if there is a note
        if self.save_dict["notities"][weekday-1] == "": max_size = 298
        else: max_size = 286
        
        # Show it on the epd
        for lesson in lessons_today:
            # Get the start and end time in datetime format
            lesson_starttime = lesson['start']
            lesson_endtime = lesson['end']
            
            # Set the colour
            # If cancelled: red (r), else: black (b)
            if lesson['cancelled']: colour = "r"
            else: colour = "b"
            
            # Set the block position and size
            # (Lesson starttime in minutes - first lesson starttime) / (Last lesson endtime - First lesson starttime) * max_size
            # (Lesson endtime in minutes - first lesson starttime) / (Last lesson endtime - First lesson starttime) * max_size - 2
            ystartpos = round(((lesson_starttime.hour * 60) + lesson_starttime.minute - self.save_dict["begintijd"]) / (self.save_dict["eindtijd"] - self.save_dict["begintijd"]) * max_size)
            yendpos = round(((lesson_endtime.hour * 60) + lesson_endtime.minute - self.save_dict["begintijd"]) / (self.save_dict["eindtijd"] - self.save_dict["begintijd"]) * max_size) - 2
            ysize = yendpos - ystartpos
            
            # If the startpos and size are greater than or equal to 0 draw a rectangle on the epd
            if ystartpos >= 0 and ysize >= 0:
                # Draw a white filled rectangle on the epd to overwrite possible previous data
                recv = self.send_to_pico(f"rectw000{"0"*((ystartpos<100)+(ystartpos<10))}{ystartpos}152{"0"*((ysize<100)+(ysize<10))}{ysize}1")
                self.ui_self.statusbar.showMessage(recv)
                
                # Draw a rectangle outline
                recv = self.send_to_pico(f"rect{colour}000{"0"*((ystartpos<100)+(ystartpos<10))}{ystartpos}152{"0"*((ysize<100)+(ysize<10))}{ysize}0")
                self.ui_self.statusbar.showMessage(recv)
            
            lineystartpos = ystartpos + 3
            lineyendpos = yendpos - 4
            
            # If the startpos and endpos are greater than or equal to 0 draw a line on the epd
            if lineystartpos >= 0 and lineyendpos >= 0:
                recv = self.send_to_pico(f"line{colour}046{"0"*((lineystartpos<100)+(lineystartpos<10))}{lineystartpos}046{"0"*((lineyendpos<100)+(lineyendpos<10))}{lineyendpos}")
                self.ui_self.statusbar.showMessage(recv)
            
            # Set the starttimestamp + position
            starttimestamp = lesson_starttime.strftime('%H:%M').removeprefix("0")
            
            # Add a space if the hour is only one digit long
            if len(starttimestamp) < 5: starttimestamp = " " + starttimestamp
            starttimestamp_ypos = ystartpos + 4
            
            # If starttimestamp y pos is greater than or equal to 0 draw the start timestamp on the epd
            if starttimestamp_ypos >= 0:
                recv = self.send_to_pico(f"text{colour}003{"0"*((starttimestamp_ypos<100)+(starttimestamp_ypos<10))}{starttimestamp_ypos}{starttimestamp}")
                self.ui_self.statusbar.showMessage(recv)
            
            # Set the endtimestamp + position
            endtimestamp = lesson_endtime.strftime('%H:%M').removeprefix("0")
            
            # Add a space if the hour is only one digit long
            if len(endtimestamp) < 5: endtimestamp = " " + endtimestamp
            endtimestamp_ypos = yendpos - 11
            
            # If endtimestamp y pos is greater than or equal to 0 draw the end timestamp on the epd
            if endtimestamp_ypos >= 0:
                recv = self.send_to_pico(f"text{colour}003{"0"*((endtimestamp_ypos<100)+(endtimestamp_ypos<10))}{endtimestamp_ypos}{endtimestamp}")
                self.ui_self.statusbar.showMessage(recv)
            
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
                    recv = self.send_to_pico(f"text{colour}050{"0"*((subject_ypos<100)+(subject_ypos<10))}{subject_ypos}{subjects}")
                    self.ui_self.statusbar.showMessage(recv)
            
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
                    recv = self.send_to_pico(f"text{colour}050{"0"*((location_ypos<100)+(location_ypos<10))}{location_ypos}{locations}")
                    self.ui_self.statusbar.showMessage(recv)
            
            # Set the hour + position
            hour : str = lesson['startTimeSlotName']
            hour_ypos = ystartpos + 4
            hour_xpos = 149 - (len(hour) * 8)
            
            # if the hour position is greater than or equal to 0 draw the hour
            if hour_ypos >= 0 and hour_xpos >= 0:
                recv = self.send_to_pico(f"text{colour}{"0"*((hour_xpos<100)+(hour_xpos<10))}{hour_xpos}{"0"*((hour_ypos<100)+(hour_ypos<10))}{hour_ypos}{hour}")
                self.ui_self.statusbar.showMessage(recv)

        # Draw the note if it isn't empty
        if self.save_dict["notities"][weekday-1] != "":
            recv = self.send_to_pico(f"textb002288{self.save_dict["notities"][weekday-1]}")
            self.ui_self.statusbar.showMessage(recv)
        
        # Show the result
        recv = self.send_to_pico("show")
        self.ui_self.statusbar.showMessage(recv)
        self.pico.close()
        
        # Enable the UI and clear the message
        self.ui_self.centralwidget.setDisabled(False)
        self.ui_self.menuBar.setDisabled(False)
        self.ui_self.statusbar.clearMessage()
        
        # Send finished signal
        self.finished.emit()