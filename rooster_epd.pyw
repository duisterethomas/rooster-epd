from pickle import load, dump
from zermelo import Client
from os.path import exists
from copy import deepcopy
from time import sleep
from math import floor
import datetime
import serial
import glob
import sys

from PySide6.QtCore import QObject, Signal, QThread, QTime
from PySide6.QtWidgets import QMainWindow, QApplication, QDialog, QDialogButtonBox

from rooster_epd_ui import Ui_Rooster_epd, Ui_Rooster_epd_setup, Ui_Rooster_epd_tijden

# List available serial ports function
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

# Thread for updating the epd
class Worker(QObject):
    finished = Signal()
    
    def __init__(self, ui_self, morgen):
        self.ui_self = ui_self
        self.morgen = morgen
    
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
        # Disable the button and show message
        self.ui_self.vandaag.setEnabled(False)
        self.ui_self.morgen.setEnabled(False)
        self.ui_self.pico_port.setEnabled(False)
        
        # Connect and initialize the pico epd
        self.pico = serial.Serial(port=save_dict["port"], parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1)
        self.pico.flush()
        recv = self.send_to_pico("init")
        self.ui_self.statusbar.showMessage(recv)

        # Get the current week and day
        today = datetime.date.today()
        isocal = datetime.date.isocalendar(today)
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
        
        # Get the usercode
        usercode = cl.get_user(save_dict["token"])["response"]["data"][0]["code"]
        
        # Request: yyyyww
        # yyyy = year: {isocal[0]}
        # ww = weeknumber: {"0"*(isocal[1]<10)}{isocal[1]}
        # If weeknum < 10 add zero: {"0"*isocal[1]<10}
        enrollments = cl.get_liveschedule(save_dict["token"], f"{year}{"0"*(week<10)}{week}", usercode)

        # Get the lessons of today
        lessons : list = enrollments['response']['data'][0]['appointments']
        lessons_today = []
        for lesson in lessons:
            # Check the day number: 1 = monday...
            if datetime.datetime.fromtimestamp(lesson['start']).isoweekday() == weekday:
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
            # (Lesson starttime in minutes - first lesson starttime) / (First lesson starttime - Last lesson endtime) * 298
            # (Lesson endtime in minutes - first lesson starttime) / (First lesson starttime - Last lesson endtime) * 298 - 2
            ystartpos = round(((lesson_starttime.hour * 60) + lesson_starttime.minute - save_dict["begintijd"]) / (save_dict["begintijd"] - save_dict["eindtijd"]) * 298)
            yendpos = round(((lesson_endtime.hour * 60) + lesson_endtime.minute - save_dict["begintijd"]) / (save_dict["begintijd"] - save_dict["eindtijd"]) * 298) - 2
            ysize = yendpos - ystartpos
            recv = self.send_to_pico(f"rect{colour}000{"0"*((ystartpos<100)+(ystartpos<10))}{ystartpos}152{"0"*((ysize<100)+(ysize<10))}{ysize}0")
            self.ui_self.statusbar.showMessage(recv)
            
            # Set the timestamps + positions
            starttimestamp = lesson_starttime.strftime('%H:%M').removeprefix("0")
            if len(starttimestamp) < 5: starttimestamp = " " + starttimestamp
            starttimestamp_ypos = ystartpos + 4
            recv = self.send_to_pico(f"text{colour}003{"0"*((starttimestamp_ypos<100)+(starttimestamp_ypos<10))}{starttimestamp_ypos}{starttimestamp}")
            self.ui_self.statusbar.showMessage(recv)
            
            endtimestamp = lesson_endtime.strftime('%H:%M').removeprefix("0")
            if len(endtimestamp) < 5: endtimestamp = " " + endtimestamp
            endtimestamp_ypos = yendpos - 11
            recv = self.send_to_pico(f"text{colour}003{"0"*((endtimestamp_ypos<100)+(endtimestamp_ypos<10))}{endtimestamp_ypos}{endtimestamp}")
            self.ui_self.statusbar.showMessage(recv)
            
            # Set the subjects + position
            if len(lesson['subjects']) != 0:
                for subject in enumerate(lesson['subjects']):
                    if subject[0] == 0:
                        subjects = subject[1].upper()
                    else:
                        subjects += f",{subject[1].upper()}"
                subject_ypos = ystartpos + 4
                recv = self.send_to_pico(f"text{colour}050{"0"*((subject_ypos<100)+(subject_ypos<10))}{subject_ypos}{subjects}")
                self.ui_self.statusbar.showMessage(recv)
            
            # Set the locations + position
            if len(lesson['locations']) != 0:
                for location in enumerate(lesson['locations']):
                    if location[0] == 0:
                        locations = location[1]
                    else:
                        locations += f",{location[1]}"
                location_ypos = ystartpos + 16
                recv = self.send_to_pico(f"text{colour}050{"0"*((location_ypos<100)+(location_ypos<10))}{location_ypos}{locations}")
                self.ui_self.statusbar.showMessage(recv)
            
            # Set the hour + position
            hour : str = lesson['startTimeSlotName'].upper()
            hour_ypos = ystartpos + 4
            hour_xpos = 149 - (len(hour) * 8)
            recv = self.send_to_pico(f"text{colour}{"0"*((hour_xpos<100)+(hour_xpos<10))}{hour_xpos}{"0"*((hour_ypos<100)+(hour_ypos<10))}{hour_ypos}{hour}")
            self.ui_self.statusbar.showMessage(recv)

        # Show the result
        recv = self.send_to_pico("show")
        self.ui_self.statusbar.showMessage(recv)
        self.pico.close()
        
        # Enable the button and show message
        self.ui_self.vandaag.setEnabled(True)
        self.ui_self.morgen.setEnabled(True)
        self.ui_self.pico_port.setEnabled(True)
        self.ui_self.statusbar.clearMessage()
        
        # Send finished signal
        self.finished.emit()
        
class setupWindow(QDialog, Ui_Rooster_epd_setup):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Connect the buttons to functions
        self.buttonBox.accepted.connect(self.saveClicked)
        
        # Connect the changes to check if save button must be disabled
        self.koppelcode.textChanged.connect(self.checkSaveDisabled)
        self.schoolnaam.textChanged.connect(self.checkSaveDisabled)
        
        # Disable the save button
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(True)
        
        if "school" in save_dict.keys():
            # Set the schoolnaam text
            self.schoolnaam.setText(save_dict["school"])
    
    # Check if save button must be disabled
    def checkSaveDisabled(self):
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(len(self.koppelcode.text()) == 0 or len(self.schoolnaam.text()) == 0)
    
    def saveClicked(self):
        # Get the schoolnaam
        save_dict["school"] = self.schoolnaam.text()
        
        # Create the zermelo client
        cl = Client(save_dict["school"])
    
        # Get and a new zermelo token
        save_dict["token"] = cl.authenticate(self.koppelcode.text())["access_token"]
    
        # Save the save_dict
        with open("rooster-epd.data", "wb") as save_file:
            dump(save_dict, save_file)
        
        # Close the ui
        self.close()

class tijdenWindow(QDialog, Ui_Rooster_epd_tijden):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Connect buttons to functions
        self.buttonBox.accepted.connect(self.saveTijden)
        
        # Connect the changes to check if save button must be disabled
        self.beginTijd.timeChanged.connect(self.checkSaveDisabled)
        self.eindTijd.timeChanged.connect(self.checkSaveDisabled)
        
        # Calculate the begin and eind hour and minute
        begin_hour = int(floor(save_dict["begintijd"]/60))
        begin_minute = int(save_dict["begintijd"] - (begin_hour * 60))
        
        eind_hour = int(floor(save_dict["eindtijd"]/60))
        eind_minute = int(save_dict["eindtijd"] - (eind_hour * 60))
        
        # Set begin tijd
        q_time = QTime()
        q_time.setHMS(begin_hour, begin_minute, 0, 0)
        self.beginTijd.setTime(q_time)
        
        # Set eind tijd
        q_time = QTime()
        q_time.setHMS(eind_hour, eind_minute, 0, 0)
        self.eindTijd.setTime(q_time)
        
        # Check if save button must be disabled
        self.begintijd = self.beginTijd.time().hour()*60 + self.beginTijd.time().minute()
        self.eindtijd = self.eindTijd.time().hour()*60 + self.eindTijd.time().minute()
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(self.begintijd >= self.eindtijd)
    
    # Check if save button must be disabled
    def checkSaveDisabled(self):
        self.begintijd = self.beginTijd.time().hour()*60 + self.beginTijd.time().minute()
        self.eindtijd = self.eindTijd.time().hour()*60 + self.eindTijd.time().minute()
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(self.begintijd >= self.eindtijd)

    def saveTijden(self):
        save_dict["begintijd"] = self.begintijd
        save_dict["eindtijd"] = self.eindtijd
        with open("rooster-epd.data", "wb") as save_file:
            dump(save_dict, save_file)

class mainWindow(QMainWindow, Ui_Rooster_epd):
    def __init__(self, parent=None):
        global save_dict
        global cl
        
        super().__init__(parent)
        self.setupUi(self)
        
        # Check if save data exist
        if exists("rooster-epd.data"):
            # Open and load the save_dict
            with open("rooster-epd.data", "rb") as save_file:
                save_dict = load(save_file)
            
            # Create the zermelo client
            cl = Client(save_dict["school"])
            
            try:
                # Dummy request to check if token is active
                cl.get_user(save_dict["token"])
                
            except ValueError:
                # Generate new token if token inactive
                self.vandaag.setDisabled(True)
                self.morgen.setDisabled(True)
                self.zermeloKoppelenClicked()
            
        else:
            # First time setup
            
            # Create a new save_dict
            save_dict = {"school": "", "token": "", "starttime": 510, "endtime": 970, "port": ""}
            
            # Open the setup window
            self.zermeloKoppelenClicked()
            self.tijdenInstellenClicked()
            
        # Connect the buttons to functions
        self.actionZermelo_koppelen.triggered.connect(self.zermeloKoppelenClicked)
        self.actionTijden_instellen.triggered.connect(self.tijdenInstellenClicked)
        self.vandaag.clicked.connect(self.vandaagClicked)
        self.morgen.clicked.connect(self.morgenClicked)
        self.pico_port.currentTextChanged.connect(self.portSelected)
        
        # Add the available ports to the dropdown
        self.pico_port.addItem("<select port>")
        for available_port in available_ports:
            self.pico_port.addItem(available_port)
        
        # Check if there is a port selected
        self.vandaag.setDisabled(self.pico_port.currentText() == "<select port>" or save_dict["token"] == "")
        self.morgen.setDisabled(self.pico_port.currentText() == "<select port>" or save_dict["token"] == "")
        
        # Set the selected port to the saved port if available
        if save_dict["port"] in available_ports:
            self.pico_port.setCurrentText(save_dict["port"])
    
    def zermeloKoppelenClicked(self):
        prev_token = deepcopy(save_dict)["token"]
        dlg = setupWindow()
        dlg.exec()
                
        if save_dict["token"] == "":
            self.statusbar.showMessage("Koppel met zermelo om verder te gaan")
        elif save_dict["token"] != prev_token:
            self.statusbar.showMessage("Zermelo gekoppeld")
    
    def tijdenInstellenClicked(self):
        dlg = tijdenWindow()
        dlg.exec()
    
    def portSelected(self):
        # Check if there is a port selected
        self.vandaag.setDisabled(self.pico_port.currentText() == "<select port>" or save_dict["token"] == "")
        self.morgen.setDisabled(self.pico_port.currentText() == "<select port>" or save_dict["token"] == "")
        
        # Save the port
        if self.pico_port.currentText() != "<select port>":
            with open("rooster-epd.data", "wb") as save_file:
                dump(save_dict, save_file)
    
    def vandaagClicked(self):
        self.updateEpd(False)
        
    def morgenClicked(self):
        self.updateEpd(True)
    
    def updateEpd(self, morgen):
        self.thread = QThread()
        self.worker = Worker(self, morgen)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

# Get the available ports
available_ports = serial_ports()

# Create a QApplication
app = QApplication(sys.argv)

# Open the main ui
win = mainWindow()
win.show()
sys.exit(app.exec())