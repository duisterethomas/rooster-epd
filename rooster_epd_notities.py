from pickle import dump

from PySide6.QtWidgets import QDialog

from rooster_epd_ui import Ui_Rooster_epd_notities

class notitiesWindow(QDialog, Ui_Rooster_epd_notities):
    def __init__(self, save_dict : dict):
        super().__init__()
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

    # Save the notities
    def saveNotities(self):
        self.save_dict["notities"] = (self.maandag.text(),
                                      self.dinsdag.text(),
                                      self.woensdag.text(),
                                      self.donderdag.text(),
                                      self.vrijdag.text(),
                                      self.zaterdag.text(),
                                      self.zondag.text())

        with open("rooster-epd.data", "wb") as save_file:
            dump(self.save_dict, save_file)