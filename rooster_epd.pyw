import sys
from copy import deepcopy
from datetime import datetime
from json import loads, dumps
from os import listdir
from os.path import exists, abspath, join
from time import sleep, localtime, time
from webbrowser import open_new_tab

from serial import Serial, SerialException, PARITY_EVEN, STOPBITS_ONE
from zermelo import Client

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QMainWindow, QApplication, QDialog

from rooster_epd_ui import Ui_Rooster_EPD, Ui_Rooster_EPD_over
from rooster_epd_worker import Worker

from rooster_epd_setup import setupWindow
from rooster_epd_tijden import tijdenWindow
from rooster_epd_wifi import wifiWindow
from rooster_epd_notities import notitiesWindow
from rooster_epd_afspraken import afsprakenWindow

# Version constant
VERSION = 'V2.1.0'

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = abspath(".")

    return join(base_path, relative_path)

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
    elif sys.platform.startswith('linux'):
        if exists('/dev/serial/by-id'):
            ports = listdir('/dev/serial/by-id')
        else:
            ports = []
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            if sys.platform.startswith('linux'):
                s = Serial(f'/dev/serial/by-id/{port}')
            else:
                s = Serial(port)
            s.close()
            result.append(port)
        except (OSError, SerialException):
            pass
    
    return result

class mainWindow(QMainWindow, Ui_Rooster_EPD):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Init save
        self.save = None
        
        # Connect the buttons to functions
        self.actionGithub_repository.triggered.connect(lambda: open_new_tab("https://github.com/duisterethomas/rooster-epd"))
        self.actionOver_Rooster_epd.triggered.connect(self.overClicked)
        self.actionZermelo_koppelen.triggered.connect(self.zermeloKoppelenClicked)
        self.actionTijden_instellen.triggered.connect(self.tijdenInstellenClicked)
        self.actionWiFi_netwerken.triggered.connect(self.wifiNetwerkenClicked)
        self.actionNotities_bewerken.triggered.connect(self.notitiesBewerkenClicked)
        self.actionAfspraken_bewerken.triggered.connect(self.afsprakenBewerkenClicked)
        self.verbindenButton.clicked.connect(self.verbindenClicked)
        self.synchroniserenButton.clicked.connect(self.synchroniserenClicked)
    	
        # Try to connect to the Pico
        self.verbindenClicked()
        
        # Put the focus on the window
        self.activateWindow()
    
    
    # Function to send a command to the pico with threading
    def sendToPicoThreaded(self, command):
        self.menuBewerken.setDisabled(True)
        self.menuSettings.setDisabled(True)
        self.synchroniserenButton.setDisabled(True)
        
        self.thread = QThread()
        self.worker = Worker(self.pico, command)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        self.thread.finished.connect(lambda: self.menuBewerken.setDisabled(False))
        self.thread.finished.connect(lambda: self.menuSettings.setDisabled(False))
        self.thread.finished.connect(lambda: self.synchroniserenButton.setDisabled(False))
        
        self.thread.finished.connect(lambda: self.statusbar.showMessage(""))
        
        self.thread.start()
    
    
    def verbindenClicked(self):
        # Get the available ports
        available_ports = serial_ports()
        
        recieved = ""
        
        for port in available_ports:
            try:
                # Connect to the port
                if sys.platform.startswith('linux'):
                    self.pico = Serial(port=f'/dev/serial/by-id/{port}', parity=PARITY_EVEN, stopbits=STOPBITS_ONE, timeout=1)
                else:
                    self.pico = Serial(port=port, parity=PARITY_EVEN, stopbits=STOPBITS_ONE, timeout=1) 
        
                self.pico.flush()
                
                # Detect if it is the pico
                self.pico.write("ping\r".encode())
                
                timeout = time() + 2
        
                recieved = self.pico.read_until().strip().decode()
                while recieved != "rooster_epd" and time() < timeout:
                    if recieved:
                        print(recieved)
                        last_recieved = recieved
                    
                    sleep(0.1)
                    recieved = self.pico.read_until().strip().decode()
                
                # If it is the pico break the loop
                if recieved == "rooster_epd":
                    break
                        
            except SerialException:
                pass
                
        if recieved == "rooster_epd":
            # Check the current version
            self.pico.write("vchk\r".encode())
            
            recieved = self.pico.read_until().strip().decode()
            while recieved != "done":
                if recieved:
                    print(recieved)
                    last_recieved = recieved
                
                sleep(0.1)
                recieved = self.pico.read_until().strip().decode()
            
            # Update the pico if it isn't on the latest version
            if last_recieved != VERSION:
                # Get a list of the current files
                self.pico.write("list\r".encode())
                
                pico_files = []
                
                recieved = self.pico.read_until().strip().decode()
                while recieved != "done":
                    if recieved:
                        pico_files.append(recieved)
                        
                        print(recieved)
                        last_recieved = recieved
                    
                    sleep(0.1)
                    recieved = self.pico.read_until().strip().decode()
                
                # Get a list of the new files
                new_files = listdir(resource_path('pico_code'))
                
                # Delete all the unnecessary files from the pico
                for file in pico_files:
                    if file not in new_files:
                        # Don't delete the save file
                        if file != "save.json":
                            self.pico.write(f"fdel {file}\r".encode())
                            
                            recieved = self.pico.read_until().strip().decode()
                            while recieved != "done":
                                if recieved:
                                    print(recieved)
                                    last_recieved = recieved
                                
                                sleep(0.1)
                                recieved = self.pico.read_until().strip().decode()
                
                # Update the files
                for file in new_files:
                    # main.py can't be updated automatically
                    if file != "main.py":
                        self.pico.write(f"upls {file}\r".encode())
                        
                        # Write the file
                        with open(resource_path(f'pico_code/{file}'), 'r') as file:
                            for line in file:
                                # Add an X to the start of every line to indicate the start of the line
                                line = f"X{line.removesuffix('\n')}"
                                self.pico.write(f"{line}\r".encode())
                        
                        # End the upload
                        self.pico.write("uple\r".encode())
                        
                        recieved = self.pico.read_until().strip().decode()
                        while recieved != "done":
                            if recieved:
                                print(recieved)
                                last_recieved = recieved
                            
                            sleep(0.1)
                            recieved = self.pico.read_until().strip().decode()
            
            self.statusbar.showMessage("Connection established", 3)
            
            # Disable the verbinden button
            self.verbindenButton.setDisabled(True)
            
            # Enable all the buttons
            self.menuBewerken.setDisabled(False)
            self.menuSettings.setDisabled(False)
            self.synchroniserenButton.setDisabled(False)
            
            # Load the save data from the pico
            self.pico.write("load\r".encode())
            
            recieved = self.pico.read_until().strip().decode()
            while recieved != "done":
                if recieved:
                    print(recieved)
                    last_recieved = recieved
                
                sleep(0.1)
                recieved = self.pico.read_until().strip().decode()
            
            # Generate save file if it doesn't exist
            if last_recieved == "fail":
                self.save = {'wlan': {},
                             'time_offset': 3600,
                             'school': '',
                             'token': '',
                             'starttime': 510,
                             'endtime': 970,
                             'notes': ('', '', '', '', '', '', ''),
                             'appointments': [],
                             'templates': {}}
            else:
                self.save = loads(last_recieved)
            
            # Automatically set the time zone offset
            self.save["time_offset"] = localtime().tm_gmtoff
            
            # Save the save
            self.sendToPicoThreaded(f"dump {dumps(self.save)}")
            
            # Detect if the Zermelo token is still active
            try:
                Client(self.save["school"]).get_user(self.save["token"])
            except ValueError:
                self.zermeloKoppelenClicked()
        else:
            self.statusbar.showMessage("Connection failed", 3)
            
            # Enable the verbinden button
            self.verbindenButton.setDisabled(False)
            
            # Disable all the buttons
            self.menuBewerken.setDisabled(True)
            self.menuSettings.setDisabled(True)
            self.synchroniserenButton.setDisabled(True)
    
    
    def synchroniserenClicked(self):
        self.statusbar.showMessage("Syncing...", -1)
        self.sendToPicoThreaded("sync")
    
    
    def overClicked(self):
        dlg = overWindow(self)
        dlg.exec()
    
    
    def zermeloKoppelenClicked(self):
        prev_token = deepcopy(self.save)["token"]
        dlg = setupWindow(self, self.save, self.pico)
        dlg.exec()
        
        # Open the window again if an error occured while generating a token
        while self.save["token"] == "ERROR":
            self.zermeloKoppelenClicked()
        
        # If the token has changed show "Zermelo gekoppeld" in the status bar
        if self.save["token"] != prev_token:
            self.statusbar.showMessage("Zermelo gekoppeld")
    
    
    def wifiNetwerkenClicked(self):
        dlg = wifiWindow(self, self.save, self.pico)
        dlg.exec()
    
    
    def tijdenInstellenClicked(self):
        dlg = tijdenWindow(self, self.save, self.pico)
        dlg.exec()
    
    
    def notitiesBewerkenClicked(self):
        dlg = notitiesWindow(self, self.save, self.pico)
        dlg.exec()
    
    
    def afsprakenBewerkenClicked(self):
        # Auto sort the appointments
        self.save["appointments"].sort(key=lambda d: datetime(d["date"][0], d["date"][1], d["date"][2], d["startTime"][0], d["startTime"][1]).timestamp())
        
        # Open the popup
        dlg = afsprakenWindow(self, self.save, self.pico)
        dlg.exec()


# The about screen
class overWindow(QDialog, Ui_Rooster_EPD_over):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Put the version number on the about screen
        self.version.setText(VERSION)


# Create a QApplication
app = QApplication(sys.argv)

# Open the main ui
win = mainWindow()
win.show()
sys.exit(app.exec())