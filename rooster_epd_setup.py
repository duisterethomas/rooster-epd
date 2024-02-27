from zermelo import Client
from pickle import dump

from PySide6.QtWidgets import QDialog, QDialogButtonBox

from rooster_epd_ui import Ui_Rooster_epd_setup

# The functionality of the setup window
class setupWindow(QDialog, Ui_Rooster_epd_setup):
    def __init__(self, save_dict : dict):
        super().__init__()
        self.setupUi(self)
        
        self.save_dict = save_dict
        
        # Connect the buttons to functions
        self.buttonBox.accepted.connect(self.saveClicked)
        
        # Connect the changes to check if save button must be disabled
        self.koppelcode.textChanged.connect(self.checkSaveDisabled)
        self.schoolnaam.textChanged.connect(self.checkSaveDisabled)
        
        # Disable the save button
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(True)
        
        if "school" in save_dict.keys():
            # Set the schoolnaam text
            self.schoolnaam.setText(save_dict["school"])
    
    # Check if save button must be disabled
    def checkSaveDisabled(self):
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(len(self.koppelcode.text()) == 0 or len(self.schoolnaam.text()) == 0)
    
    def saveClicked(self):
        # Get the schoolnaam
        self.save_dict["school"] = self.schoolnaam.text()
    
        # Get and a new zermelo token
        self.save_dict["token"] = Client(self.save_dict["school"]).authenticate(self.koppelcode.text())["access_token"]
    
        # Save the save_dict
        with open("rooster-epd.data", "wb") as save_file:
            dump(self.save_dict, save_file)
        
        # Close the ui
        self.close()