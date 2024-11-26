from copy import deepcopy
from time import sleep
from json import dumps

from PySide6.QtWidgets import QDialog, QDialogButtonBox

from rooster_epd_ui import Ui_Rooster_EPD_notities

class notitiesWindow(QDialog, Ui_Rooster_EPD_notities):
    def __init__(self, parent = None, save : dict = None, pico = None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Set the text of the buttonbox buttons
        self.buttonBox.button(QDialogButtonBox.Save).setText("Opslaan")
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("Annuleren")
        
        self.save = save
        self.pico = pico
        
        # Connect buttons to functions
        self.buttonBox.accepted.connect(self.saveNotities)
        
        # Set the previous notes in all the line edits
        self.maandag.setText(save["notes"][0])
        self.dinsdag.setText(save["notes"][1])
        self.woensdag.setText(save["notes"][2])
        self.donderdag.setText(save["notes"][3])
        self.vrijdag.setText(save["notes"][4])
        self.zaterdag.setText(save["notes"][5])
        self.zondag.setText(save["notes"][6])
        
        # Add a check if the save button should be disabled
        self.maandag.textChanged.connect(self.checkSaveDisable)
        self.dinsdag.textChanged.connect(self.checkSaveDisable)
        self.woensdag.textChanged.connect(self.checkSaveDisable)
        self.donderdag.textChanged.connect(self.checkSaveDisable)
        self.vrijdag.textChanged.connect(self.checkSaveDisable)
        self.zaterdag.textChanged.connect(self.checkSaveDisable)
        self.zondag.textChanged.connect(self.checkSaveDisable)
        
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

    def checkSaveDisable(self):
        self.new_notities = [self.maandag.text(),
                             self.dinsdag.text(),
                             self.woensdag.text(),
                             self.donderdag.text(),
                             self.vrijdag.text(),
                             self.zaterdag.text(),
                             self.zondag.text()]
        
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(self.new_notities == self.save["notes"])
    
    # Save the notities
    def saveNotities(self):
        self.save["notes"] = deepcopy(self.new_notities)
        
        # Save the save
        self.sendToPico(f"dump {dumps(self.save)}")