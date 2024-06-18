from serial import Serial, SerialException, PARITY_EVEN, STOPBITS_ONE
from webbrowser import open_new_tab
from time import sleep, localtime
from json import loads, dumps
from zermelo import Client
from os.path import exists
from copy import deepcopy
from os import listdir
import sys

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QMainWindow, QApplication, QDialog

from rooster_epd_ui import Ui_Rooster_epd, Ui_Rooster_epd_over
from rooster_epd_worker import Worker

from rooster_epd_setup import setupWindow
from rooster_epd_tijden import tijdenWindow
from rooster_epd_wifi import wifiWindow
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

class mainWindow(QMainWindow, Ui_Rooster_epd):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Init save
        self.save = None
        
        # Check if previous port is saved
        if exists("prev_port.txt"):
            with open("prev_port.txt", "r") as file:
                self.selected_port = file.read()
        else:
            self.selected_port = ""
            with open("prev_port.txt", "w") as file:
                file.write(self.selected_port)
        
        # Connect the buttons to functions
        self.actionGithub_repository.triggered.connect(lambda: open_new_tab("https://github.com/duisterethomas/rooster-epd"))
        self.actionOver_Rooster_epd.triggered.connect(self.overClicked)
        self.actionZermelo_koppelen.triggered.connect(self.zermeloKoppelenClicked)
        self.actionTijden_instellen.triggered.connect(self.tijdenInstellenClicked)
        self.actionWiFi_netwerken.triggered.connect(self.wifiNetwerkenClicked)
        self.actionNotities_bewerken.triggered.connect(self.notitiesBewerkenClicked)
        self.actionAfspraken_bewerken.triggered.connect(self.afsprakenBewerkenClicked)
        self.actionRefresh_ports.triggered.connect(self.refreshPorts)
        self.connect_button.clicked.connect(self.connectClicked)
        self.sync.clicked.connect(self.syncClicked)
        self.pico_port.currentTextChanged.connect(self.portSelected)
    	
        # Put all the available ports in the ports dropdown
        self.refreshPorts()
        
        # Put the focus on the window
        self.activateWindow()
    
    # Function to send a command to the pico with threading
    def sendToPicoThreaded(self, command):
        self.menuBewerken.setDisabled(True)
        self.menuSettings.setDisabled(True)
        self.pico_port.setDisabled(True)
        self.connect_button.setDisabled(True)
        self.sync.setDisabled(True)
        
        self.thread = QThread()
        self.worker = Worker(self.pico, command)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        self.thread.finished.connect(lambda: self.menuBewerken.setDisabled(False))
        self.thread.finished.connect(lambda: self.menuSettings.setDisabled(False))
        self.thread.finished.connect(lambda: self.pico_port.setDisabled(False))
        self.thread.finished.connect(lambda: self.connect_button.setDisabled(False))
        self.thread.finished.connect(lambda: self.sync.setDisabled(False))
        
        self.thread.finished.connect(lambda: self.statusbar.showMessage(""))
        
        self.thread.start()
    
    def connectClicked(self):
        # Connect to the pico
        if sys.platform.startswith('linux'):
            self.pico = Serial(port=f'/dev/serial/by-id/{self.selected_port}', parity=PARITY_EVEN, stopbits=STOPBITS_ONE, timeout=1)
        else:
            self.pico = Serial(port=self.selected_port, parity=PARITY_EVEN, stopbits=STOPBITS_ONE, timeout=1)
        self.pico.flush()
        
        self.menuBewerken.setDisabled(False)
        self.actionZermelo_koppelen.setDisabled(False)
        self.actionWiFi_netwerken.setDisabled(False)
        self.actionTijden_instellen.setDisabled(False)
        self.sync.setDisabled(False)
        
        # Load the save data from the pico
        self.pico.write("load\r".encode())
        
        recieved = self.pico.read_until().strip().decode()
        while recieved != "done":
            if recieved:
                print(recieved)
                last_recieved = recieved
            
            sleep(0.1)
            recieved = self.pico.read_until().strip().decode()
        
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
    
    def checkConnectButtonDisable(self):
        self.connect_button.setDisabled(self.pico_port.currentText() == "<select port>")
    
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
        dlg = afsprakenWindow(self, self.save, self.pico)
        dlg.exec()
    
    def refreshPorts(self):
        # Get the available ports
        available_ports = serial_ports()
        
        # Add the available ports to the dropdown
        self.pico_port.clear()
        self.pico_port.addItem("<select port>")
        self.pico_port.addItems(available_ports)
        
        # Check if the upload buttons should be disabled
        self.checkConnectButtonDisable()
        
        # Set the selected port to the saved port if available
        if self.selected_port in available_ports:
            self.pico_port.setCurrentText(self.selected_port)
            self.pico_port.update()
            
            self.connectClicked()
        
        else:
            self.menuBewerken.setDisabled(True)
            self.actionZermelo_koppelen.setDisabled(True)
            self.actionWiFi_netwerken.setDisabled(True)
            self.actionTijden_instellen.setDisabled(True)
            self.sync.setDisabled(True)
    
    def portSelected(self):
        # Check if the upload buttons should be disabled
        self.checkConnectButtonDisable()
        
        # Save the port
        if self.pico_port.currentText() != "<select port>":
            self.selected_port = self.pico_port.currentText()
            
            with open("prev_port.txt", "w") as file:
                file.write(self.selected_port)
    
    def syncClicked(self):
        self.statusbar.showMessage("Syncing...", -1)
        self.sendToPicoThreaded("sync")
        
# The about screen
class overWindow(QDialog, Ui_Rooster_epd_over):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Put the version number on the about screen
        self.version.setText("V2.0.0")

# Create a QApplication
app = QApplication(sys.argv)

# Open the main ui
win = mainWindow()
win.show()
sys.exit(app.exec())