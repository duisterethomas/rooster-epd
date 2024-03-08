from pickle import dump
from math import floor

from PySide6.QtCore import QTime
from PySide6.QtWidgets import QDialog, QDialogButtonBox

from rooster_epd_ui import Ui_Rooster_epd_tijden

class tijdenWindow(QDialog, Ui_Rooster_epd_tijden):
    def __init__(self, parent = None, save_dict : dict = None, firstTimeSetup = False):
        super().__init__(parent)
        self.setupUi(self)
        
        self.save_dict = save_dict
        
        # Connect buttons to functions
        self.buttonBox.accepted.connect(self.saveTijden)
        
        # Change the minimum time of the eindTijd when beginTijd is changed
        self.beginTijd.timeChanged.connect(lambda: self.eindTijd.setMinimumTime(self.beginTijd.time().addSecs(60)))
        
        if firstTimeSetup:
            # Disable the cancel button if first time setup
            self.buttonBox.button(QDialogButtonBox.Cancel).setDisabled(True)
        else:
            # Connect the changes to check if the save button must be disabled
            self.beginTijd.timeChanged.connect(self.checkSaveDisabled)
            self.eindTijd.timeChanged.connect(self.checkSaveDisabled)
        
            # Disable the save button
            self.buttonBox.button(QDialogButtonBox.Save).setDisabled(True)
        
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
    
    # Check if the save button must be disabled
    def checkSaveDisabled(self):
        self.begintijd = self.beginTijd.time().hour()*60 + self.beginTijd.time().minute()
        self.eindtijd = self.eindTijd.time().hour()*60 + self.eindTijd.time().minute()
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(self.begintijd == self.save_dict["begintijd"] and self.eindtijd == self.save_dict["eindtijd"])

    def saveTijden(self):
        self.save_dict["begintijd"] = self.beginTijd.time().hour()*60 + self.beginTijd.time().minute()
        self.save_dict["eindtijd"] = self.eindTijd.time().hour()*60 + self.eindTijd.time().minute()
        with open("rooster-epd.data", "wb") as save_file:
            dump(self.save_dict, save_file)