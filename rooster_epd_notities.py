from copy import deepcopy
from pickle import dump

from PySide6.QtWidgets import QDialog, QDialogButtonBox

from rooster_epd_ui import Ui_Rooster_epd_notities

class notitiesWindow(QDialog, Ui_Rooster_epd_notities):
    def __init__(self, parent = None, save_dict : dict = None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.save_dict = save_dict
        
        # Connect buttons to functions
        self.buttonBox.accepted.connect(self.saveNotities)
        
        # Set the previous notes in all the line edits
        self.maandag.setText(save_dict["notities"][0])
        self.dinsdag.setText(save_dict["notities"][1])
        self.woensdag.setText(save_dict["notities"][2])
        self.donderdag.setText(save_dict["notities"][3])
        self.vrijdag.setText(save_dict["notities"][4])
        self.zaterdag.setText(save_dict["notities"][5])
        self.zondag.setText(save_dict["notities"][6])
        
        # Add a check if the save button should be disabled
        self.maandag.textChanged.connect(self.checkSaveDisable)
        self.dinsdag.textChanged.connect(self.checkSaveDisable)
        self.woensdag.textChanged.connect(self.checkSaveDisable)
        self.donderdag.textChanged.connect(self.checkSaveDisable)
        self.vrijdag.textChanged.connect(self.checkSaveDisable)
        self.zaterdag.textChanged.connect(self.checkSaveDisable)
        self.zondag.textChanged.connect(self.checkSaveDisable)
        
        self.checkSaveDisable()

    def checkSaveDisable(self):
        self.new_notities = (self.maandag.text(),
                             self.dinsdag.text(),
                             self.woensdag.text(),
                             self.donderdag.text(),
                             self.vrijdag.text(),
                             self.zaterdag.text(),
                             self.zondag.text())
        
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(self.new_notities == self.save_dict["notities"])
    
    # Save the notities
    def saveNotities(self):
        self.save_dict["notities"] = deepcopy(self.new_notities)
        with open("rooster-epd.data", "wb") as save_file:
            dump(self.save_dict, save_file)