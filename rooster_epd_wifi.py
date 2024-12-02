from copy import deepcopy
from json import dumps
from time import sleep

from PySide6.QtCore import QRect
from PySide6.QtWidgets import QFrame, QDialog, QDialogButtonBox

from rooster_epd_ui import Ui_Wifi, Ui_Rooster_EPD_wifi

class wifiFrame(QFrame, Ui_Wifi):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Delete the template when verwijder is clicked
        self.verwijderButton.clicked.connect(lambda: self.setParent(None))
        self.verwijderButton.clicked.connect(lambda: self.deleteLater())

class wifiWindow(QDialog, Ui_Rooster_EPD_wifi):
    def __init__(self, parent=None, save: dict = None, pico=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Set the text of the buttonbox buttons
        self.buttonBox.button(QDialogButtonBox.StandardButton.Save).setText("Opslaan")
        self.buttonBox.button(QDialogButtonBox.StandardButton.Cancel).setText("Annuleren")
        
        self.save = save
        self.pico = pico
        
        self.count = 0
        self.networks = {}
        
        # Get the layout in the scroll area
        self.scrolllayout = self.scrollAreaWidgetContents.layout()
        
        # Connect buttons to functions
        self.nieuwButton.clicked.connect(lambda: self.addNetwork())
        self.buttonBox.accepted.connect(self.saveWifi)
        
        # Add networks if needed
        if save["wlan"]:
            for network in self.save["wlan"].keys():
                self.addNetwork(network, self.save["wlan"][network])
        
        # Check if save button should be disabled
        self.checkSaveDisable()
    
    # Function to send a command to the pico
    def sendToPico(self, command):
        self.pico.write(f"{command}\r".encode())
        
        recieved = self.pico.read_until().strip().decode()
        while recieved != "done":
            if recieved:
                print(recieved)
            
            sleep(0.1)
            recieved = self.pico.read_until().strip().decode()
    
    # Resize the ui if the window is resized
    def resizeEvent(self, event):
        QDialog.resizeEvent(self, event)
        self.scrollArea.setGeometry(QRect(-1, 0, 396, event.size().height()-40))
        self.buttonBox.setGeometry(QRect(0, event.size().height()-41, 396, 41))
    
    # Add a network
    def addNetwork(self, ssid: str = "", password: str = ""):
        # Add the new template
        network_name = f"network{self.count}"
        self.networks[network_name] = wifiFrame(self.scrollAreaWidgetContents)
        self.networks[network_name].setObjectName(network_name)
        self.networks[network_name].verwijderButton.clicked.connect(lambda _ = None, temp_name = network_name: self.networks.pop(temp_name))
        self.networks[network_name].verwijderButton.clicked.connect(lambda:self.scrolllayout.update())
        self.networks[network_name].verwijderButton.clicked.connect(self.checkSaveDisable)
        self.networks[network_name].ssid.textChanged.connect(self.checkSaveDisable)
        self.networks[network_name].password.textChanged.connect(self.checkSaveDisable)
        
        # Fill in the info if it was imported from the save
        self.networks[network_name].ssid.setText(ssid)
        self.networks[network_name].password.setText(password)
        
        self.scrolllayout.insertWidget(self.scrolllayout.count() - 1, self.networks[network_name])
        self.count += 1
        
        # Check if save button should be disabled
        self.checkSaveDisable()

    def checkSaveDisable(self):
        disable = False
        self.new_wlan = {}
        
        for widget in self.scrollAreaWidgetContents.children():
            if widget.objectName().startswith("network"):
                if widget.ssid.text() in self.new_wlan.keys():
                    disable = True
                else:
                    self.new_wlan[widget.ssid.text()] = widget.password.text()
        
        self.buttonBox.button(QDialogButtonBox.StandardButton.Save).setDisabled(self.new_wlan == self.save["wlan"])
    
    # Save the wifi
    def saveWifi(self):
        self.save["wlan"] = deepcopy(self.new_wlan)
        
        # Save the save
        self.sendToPico(f"dump {dumps(self.save)}")