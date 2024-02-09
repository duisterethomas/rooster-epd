from pickle import load, dump
from zermelo import Client
from os.path import exists
from copy import deepcopy
from time import sleep
import datetime
import serial
import glob
import sys

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize, QObject, Signal, QThread
from PySide6.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton, QSizePolicy, QStatusBar, QWidget, QMainWindow, QApplication

class Ui_Rooster_epd(object):
    def setupUi(self, Rooster_epd):
        if not Rooster_epd.objectName():
            Rooster_epd.setObjectName(u"Rooster_epd")
        Rooster_epd.resize(271, 91)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Rooster_epd.sizePolicy().hasHeightForWidth())
        Rooster_epd.setSizePolicy(sizePolicy)
        Rooster_epd.setMinimumSize(QSize(271, 91))
        Rooster_epd.setMaximumSize(QSize(271, 91))
        self.centralwidget = QWidget(Rooster_epd)
        self.centralwidget.setObjectName(u"centralwidget")
        self.update_epd = QPushButton(self.centralwidget)
        self.update_epd.setObjectName(u"update_epd")
        self.update_epd.setGeometry(QRect(180, 40, 81, 24))
        self.pico_port = QComboBox(self.centralwidget)
        self.pico_port.setObjectName(u"pico_port")
        self.pico_port.setGeometry(QRect(90, 10, 171, 22))
        self.label_pico_port = QLabel(self.centralwidget)
        self.label_pico_port.setObjectName(u"label_pico_port")
        self.label_pico_port.setGeometry(QRect(10, 10, 81, 16))
        Rooster_epd.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Rooster_epd)
        self.statusbar.setObjectName(u"statusbar")
        Rooster_epd.setStatusBar(self.statusbar)

        self.retranslateUi(Rooster_epd)

        QMetaObject.connectSlotsByName(Rooster_epd)
    # setupUi

    def retranslateUi(self, Rooster_epd):
        Rooster_epd.setWindowTitle(QCoreApplication.translate("Rooster_epd", u"Rooster epd", None))
        self.update_epd.setText(QCoreApplication.translate("Rooster_epd", u"Update epd", None))
        self.label_pico_port.setText(QCoreApplication.translate("Rooster_epd", u"Pico port:", None))
    # retranslateUi

class Ui_Rooster_epd_setup(object):
    def setupUi(self, Rooster_epd_setup):
        if not Rooster_epd_setup.objectName():
            Rooster_epd_setup.setObjectName(u"Rooster_epd_setup")
        Rooster_epd_setup.resize(271, 101)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Rooster_epd_setup.sizePolicy().hasHeightForWidth())
        Rooster_epd_setup.setSizePolicy(sizePolicy)
        Rooster_epd_setup.setMinimumSize(QSize(271, 101))
        Rooster_epd_setup.setMaximumSize(QSize(271, 101))
        self.centralwidget = QWidget(Rooster_epd_setup)
        self.centralwidget.setObjectName(u"centralwidget")
        self.save = QPushButton(self.centralwidget)
        self.save.setObjectName(u"save")
        self.save.setGeometry(QRect(180, 70, 81, 24))
        self.koppelcode = QLineEdit(self.centralwidget)
        self.koppelcode.setObjectName(u"koppelcode")
        self.koppelcode.setGeometry(QRect(90, 10, 171, 22))
        self.schoolnaam = QLineEdit(self.centralwidget)
        self.schoolnaam.setObjectName(u"schoolnaam")
        self.schoolnaam.setGeometry(QRect(90, 40, 171, 22))
        self.label_koppelcode = QLabel(self.centralwidget)
        self.label_koppelcode.setObjectName(u"label_koppelcode")
        self.label_koppelcode.setGeometry(QRect(10, 10, 81, 21))
        self.label_schoolnaam = QLabel(self.centralwidget)
        self.label_schoolnaam.setObjectName(u"label_schoolnaam")
        self.label_schoolnaam.setGeometry(QRect(10, 40, 81, 16))
        Rooster_epd_setup.setCentralWidget(self.centralwidget)

        self.retranslateUi(Rooster_epd_setup)

        QMetaObject.connectSlotsByName(Rooster_epd_setup)
    # setupUi

    def retranslateUi(self, Rooster_epd_setup):
        Rooster_epd_setup.setWindowTitle(QCoreApplication.translate("Rooster_epd_setup", u"Rooster epd", None))
        self.save.setText(QCoreApplication.translate("Rooster_epd_setup", u"Save", None))
        self.label_koppelcode.setText(QCoreApplication.translate("Rooster_epd_setup", u"Koppelcode:", None))
        self.label_schoolnaam.setText(QCoreApplication.translate("Rooster_epd_setup", u"Schoolnaam:", None))
    # retranslateUi

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

# Function to send commands to the pico
def send_to_pico(command):
    pico.write(f"{command}\r".encode())
    
    recieved = pico.read_until().strip()
    while not recieved:
        sleep(0.1)
        recieved = pico.read_until().strip()
    
    print(recieved.decode())
    
    return recieved.decode()

# Thread for updating the epd
class Worker(QObject):
    finished = Signal()
    
    def run(self):
        global ui_self
        global pico
        global cl
        
        # Disable the button and show message
        ui_self.update_epd.setEnabled(False)
        ui_self.statusbar.showMessage("Updating epd...")
        
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
        
        # Enable the button and show message
        ui_self.update_epd.setEnabled(True)
        ui_self.statusbar.showMessage("Done", 10)

class mainWindow(QMainWindow, Ui_Rooster_epd):
    def __init__(self, parent=None):
        global available_ports
        global save_dict
        
        super().__init__(parent)
        self.setupUi(self)
        
        # Connect the buttons to functions
        self.update_epd.clicked.connect(self.updateEpdClicked)
        
        # Add the available ports to the dropdown
        self.pico_port.addItem("")
        for available_port in available_ports:
            self.pico_port.addItem(available_port)
        
        # Set the selected port to the saved port if available
        if save_dict["port"] in available_ports:
            self.pico_port.setCurrentIndex(available_ports.index(available_port))
        
    def saveClicked(self):
        with open("rooster-epd.data", "wb") as save_file:
            dump(save_dict, save_file)
    
    def updateEpdClicked(self):
        global ui_self
        
        ui_self = self
    
        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        
class setupWindow(QMainWindow, Ui_Rooster_epd_setup):
    def __init__(self, parent=None):
        global save_dict
        
        super().__init__(parent)
        self.setupUi(self)
        
        # Connect the buttons to functions
        self.save.clicked.connect(self.saveClicked)
        
        self.koppelcode.textChanged.connect(self.checkSaveDisabled)
        self.schoolnaam.textChanged.connect(self.checkSaveDisabled)
        
        # Disable the save button
        self.save.setDisabled(True)
        
        if False:
            # Set the schoolnaam text
            self.schoolnaam.setText(save_dict["school"])
        else:
            # Create a new save_dict
            save_dict = {}
    
    def checkSaveDisabled(self):
        self.save.setDisabled(self.koppelcode.text and self.schoolnaam.text)
    
    def saveClicked(self):
        # Get the schoolnaam
        save_dict["school"] = self.schoolnaam.text
        
        # Create the zermelo client
        cl = Client(save_dict["school"])
    
        # Get and a new zermelo token
        save_dict["token"] = cl.authenticate(self.koppelcode.text)["access_token"]
    
        # Save the save_dict
        with open("rooster-epd.data", "wb") as save_file:
            dump(save_dict, save_file)
        
        # Close the ui
        self.close()
    
    def closeEvent(self, event):
        global setup_closed
        setup_closed = True

available_ports = serial_ports()

app = QApplication(sys.argv)

setup_closed = False

# Check if save data exist
if exists("rooster-epd.data"):
    # Open and load the save_dict
    with open("rooster-epd.data", "rb") as save_file:
        save_dict = load(save_file)
    
    # Create the zermelo client
    cl = Client(save_dict["school"])
    
else:
    win = setupWindow()
    win.show()
    app.exec()

if not setup_closed:
    win = mainWindow()
    win.show()
    sys.exit(app.exec())