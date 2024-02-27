from serial import Serial, SerialException
from pickle import load, dump
from zermelo import Client
from os.path import exists
from copy import deepcopy
from glob import glob
import sys

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QMainWindow, QApplication

from rooster_epd_ui import *
from rooster_epd_worker import Worker

from rooster_epd_setup import setupWindow
from rooster_epd_tijden import tijdenWindow
from rooster_epd_notities import notitiesWindow
from rooster_epd_afspraken import afsprakenWindow

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
        ports = glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = Serial(port)
            s.close()
            result.append(port)
        except (OSError, SerialException):
            pass
    return result

class mainWindow(QMainWindow, Ui_Rooster_epd):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Check if save data exist
        if exists("rooster-epd.data"):
            # Open and load the save_dict
            with open("rooster-epd.data", "rb") as save_file:
                self.save_dict : dict = load(save_file)
            
            try:
                # Dummy request to check if token is active
                Client(self.save_dict["school"]).get_user(self.save_dict["token"])
                
            except ValueError:
                # Generate new token if token inactive
                self.vandaag.setDisabled(True)
                self.morgen.setDisabled(True)
                self.zermeloKoppelenClicked()
                
            # Add notities to save_dict if it doesn't exist
            if "notities" not in self.save_dict.keys():
                self.save_dict["notities"] = ("", "", "", "", "", "", "")
                
            # Add afspraken to save_dict if it doesn't exist
            if "afspraken" not in self.save_dict.keys():
                self.save_dict["afspraken"] = []
                
            # Add afspraken to save_dict if it doesn't exist
            if "sjablonen" not in self.save_dict.keys():
                self.save_dict["sjablonen"] = []
            
        else:
            # First time setup
            
            # Create a new save_dict
            self.save_dict = {"school": "",
                              "token": "",
                              "begintijd": 510,
                              "eindtijd": 970,
                              "port": "",
                              "notities": ("", "", "", "", "", "", ""),
                              "afspraken": [],
                              "sjablonen": []}
            
            # Open the setup window
            self.zermeloKoppelenClicked()
            self.tijdenInstellenClicked()
            
        # Connect the buttons to functions
        self.actionZermelo_koppelen.triggered.connect(self.zermeloKoppelenClicked)
        self.actionTijden_instellen.triggered.connect(self.tijdenInstellenClicked)
        self.actionNotities_bewerken.triggered.connect(self.notitiesBewerkenClicked)
        self.actionAfspraken_bewerken.triggered.connect(self.afsprakenBewerkenClicked)
        self.actionRefresh_ports.triggered.connect(self.refreshPorts)
        self.vandaag.clicked.connect(self.vandaagClicked)
        self.morgen.clicked.connect(self.morgenClicked)
        self.pico_port.currentTextChanged.connect(self.portSelected)

        self.refreshPorts()
    
    def zermeloKoppelenClicked(self):
        prev_token = deepcopy(self.save_dict)["token"]
        dlg = setupWindow(self.save_dict)
        dlg.exec()
                
        if self.save_dict["token"] == "":
            self.statusbar.showMessage("Koppel met zermelo om verder te gaan")
        elif self.save_dict["token"] != prev_token:
            self.statusbar.showMessage("Zermelo gekoppeld")
    
    def tijdenInstellenClicked(self):
        dlg = tijdenWindow(self.save_dict)
        dlg.exec()
    
    def notitiesBewerkenClicked(self):
        dlg = notitiesWindow(self.save_dict)
        dlg.exec()
    
    def afsprakenBewerkenClicked(self):
        dlg = afsprakenWindow(self.save_dict)
        dlg.exec()
    
    def refreshPorts(self):
        # Get the available ports
        available_ports = serial_ports()
        
        # Add the available ports to the dropdown
        self.pico_port.clear()
        self.pico_port.addItem("<select port>")
        for available_port in available_ports:
            self.pico_port.addItem(available_port)
        
        # Check if there is a port selected
        self.vandaag.setDisabled(self.pico_port.currentText() == "<select port>" or self.save_dict["token"] == "")
        self.morgen.setDisabled(self.pico_port.currentText() == "<select port>" or self.save_dict["token"] == "")
        
        # Set the selected port to the saved port if available
        if self.save_dict["port"] in available_ports:
            self.pico_port.setCurrentText(self.save_dict["port"])
    
    def portSelected(self):
        # Check if there is a port selected
        self.vandaag.setDisabled(self.pico_port.currentText() == "<select port>" or self.save_dict["token"] == "")
        self.morgen.setDisabled(self.pico_port.currentText() == "<select port>" or self.save_dict["token"] == "")
        
        # Save the port
        if self.pico_port.currentText() != "<select port>":
            self.save_dict["port"] = self.pico_port.currentText()
            with open("rooster-epd.data", "wb") as save_file:
                dump(self.save_dict, save_file)
    
    def vandaagClicked(self):
        self.updateEpd(False)
        
    def morgenClicked(self):
        self.updateEpd(True)
    
    def updateEpd(self, morgen):
        self.thread = QThread()
        self.worker = Worker(self, self.save_dict, morgen)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

# Create a QApplication
app = QApplication(sys.argv)

# Open the main ui
win = mainWindow()
win.show()
sys.exit(app.exec())