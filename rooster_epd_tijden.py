from json import dumps
from math import floor
from time import sleep

from PySide6.QtCore import QTime
from PySide6.QtWidgets import QDialog, QDialogButtonBox

from rooster_epd_ui import Ui_Rooster_EPD_tijden

class tijdenWindow(QDialog, Ui_Rooster_EPD_tijden):
    def __init__(self, parent=None, save: dict = None, pico=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Set the text of the buttonbox buttons
        self.buttonBox.button(QDialogButtonBox.Save).setText("Opslaan")
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("Annuleren")
        
        self.save = save
        self.pico = pico
        
        # Connect buttons to functions
        self.buttonBox.accepted.connect(self.saveTijden)
        
        # Change the minimum time of the eindTijd when beginTijd is changed
        self.beginTijd.timeChanged.connect(lambda: self.eindTijd.setMinimumTime(self.beginTijd.time().addSecs(60)))
        
        # Connect the changes to check if the save button must be disabled
        self.beginTijd.timeChanged.connect(self.checkSaveDisabled)
        self.eindTijd.timeChanged.connect(self.checkSaveDisabled)
    
        # Disable the save button
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(True)
        
        # Calculate the begin and eind hour and minute
        begin_hour = int(floor(save["starttime"]/60))
        begin_minute = int(save["starttime"] - (begin_hour * 60))
        
        eind_hour = int(floor(save["endtime"]/60))
        eind_minute = int(save["endtime"] - (eind_hour * 60))
        
        # Set begin tijd
        q_time = QTime()
        q_time.setHMS(begin_hour, begin_minute, 0, 0)
        self.beginTijd.setTime(q_time)
        
        # Set eind tijd
        q_time = QTime()
        q_time.setHMS(eind_hour, eind_minute, 0, 0)
        self.eindTijd.setTime(q_time)
    
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
        self.begintijd = self.beginTijd.time().hour()*60 + self.beginTijd.time().minute()
        self.eindtijd = self.eindTijd.time().hour()*60 + self.eindTijd.time().minute()
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(self.begintijd == self.save["starttime"] and self.eindtijd == self.save["endtime"])

    def saveTijden(self):
        self.save["starttime"] = self.beginTijd.time().hour()*60 + self.beginTijd.time().minute()
        self.save["endtime"] = self.eindTijd.time().hour()*60 + self.eindTijd.time().minute()
        
        # Save the save
        self.sendToPico(f"dump {dumps(self.save)}")