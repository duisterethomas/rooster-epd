from zermelo import Client
from pickle import dump

from PySide6.QtWidgets import QDialog, QDialogButtonBox

from rooster_epd_ui import Ui_Rooster_epd_setup

# The functionality of the setup window
class setupWindow(QDialog, Ui_Rooster_epd_setup):
    def __init__(self, parent = None, save_dict : dict = None, firstTimeSetup = False):
        super().__init__(parent)
        self.setupUi(self)
        
        self.save_dict = save_dict
        
        # Reset the token if token is "ERROR"
        if self.save_dict["token"] == "ERROR": self.save_dict["token"] = ""
        
        # Connect the buttons to functions
        self.buttonBox.accepted.connect(self.saveClicked)
        
        # Connect the changes to check if save button must be disabled
        self.koppelcode.textChanged.connect(self.checkSaveDisabled)
        self.schoolnaam.textChanged.connect(self.checkSaveDisabled)
        
        # Disable the save button
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(True)
        
        # Disable the cancel button if first time setup
        self.buttonBox.button(QDialogButtonBox.Cancel).setDisabled(firstTimeSetup)
        
        if "school" in save_dict.keys():
            # Set the schoolnaam text
            self.schoolnaam.setText(save_dict["school"])
    
    # Check if the save button must be disabled
    def checkSaveDisabled(self):
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(len(self.koppelcode.text()) == 0 or len(self.schoolnaam.text()) == 0)
    
    def saveClicked(self):
        # Get the schoolnaam
        self.save_dict["school"] = self.schoolnaam.text()
    
        # Get and save a new zermelo token
        try:
            self.save_dict["token"] = Client(self.save_dict["school"]).authenticate(self.koppelcode.text())["access_token"]
        except ValueError:
            self.save_dict["token"] = "ERROR"
        
        # Save the save_dict
        with open("rooster-epd.data", "wb") as save_file:
            dump(self.save_dict, save_file)
        
        # Close the ui
        self.close()