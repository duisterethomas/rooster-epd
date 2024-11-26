from zermelo import Client
from time import sleep
from json import dumps

from PySide6.QtWidgets import QDialog, QDialogButtonBox

from rooster_epd_ui import Ui_Rooster_EPD_setup

# The functionality of the setup window
class setupWindow(QDialog, Ui_Rooster_EPD_setup):
    def __init__(self, parent = None, save : dict = None, pico = None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Set the text of the buttonbox buttons
        self.buttonBox.button(QDialogButtonBox.Save).setText("Opslaan")
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("Annuleren")
        
        self.save = save
        self.pico = pico
        
        # Reset the token if token is "ERROR"
        if self.save["token"] == "ERROR": self.save["token"] = ""
        
        # Connect the buttons to functions
        self.buttonBox.accepted.connect(self.saveClicked)
        
        # Connect the changes to check if save button must be disabled
        self.koppelcode.textChanged.connect(self.checkSaveDisabled)
        self.schoolnaam.textChanged.connect(self.checkSaveDisabled)
        
        # Disable the save button
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(True)
        
        if "school" in save.keys():
            # Set the schoolnaam text
            self.schoolnaam.setText(save["school"])
    
    # Function to send a command to the pico
    def sendToPico(self, command):
        self.pico.write(f"{command}\r".encode())
        
        recieved = self.pico.read_until().strip().decode()
        while recieved != "done":
            if recieved:
                print(recieved)
            
            sleep(0.1)
            recieved = self.pico.read_until().strip().decode()
    
    # Check if the save button must be disabled
    def checkSaveDisabled(self):
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(len(self.koppelcode.text()) == 0 or len(self.schoolnaam.text()) == 0)
    
    def saveClicked(self):
        # Get the schoolnaam
        self.save["school"] = self.schoolnaam.text()
    
        # Get and save a new zermelo token
        try:
            self.save["token"] = Client(self.save["school"]).authenticate(self.koppelcode.text())["access_token"]
        except ValueError:
            self.save["token"] = "ERROR"
        
        # Save the save
        self.sendToPico(f"dump {dumps(self.save)}")
        
        # Close the ui
        self.close()