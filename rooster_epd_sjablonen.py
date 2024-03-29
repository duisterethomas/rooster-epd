from copy import deepcopy
from pickle import dump

from PySide6.QtCore import QRect
from PySide6.QtWidgets import QFrame, QDialog, QDialogButtonBox

from rooster_epd_ui import Ui_Sjabloon, Ui_Rooster_epd_sjablonen

class sjabloonFrame(QFrame, Ui_Sjabloon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Add a minimum time check
        self.startTime.timeChanged.connect(lambda: self.endTime.setMinimumTime(self.startTime.time()))
        
        # Add a max length check
        self.lesuur.textChanged.connect(lambda: self.onderwerpen.setMaxLength(12-len(self.lesuur.text())))
        
        # Delete the sjabloon when verwijder is clicked
        self.verwijderButton.clicked.connect(lambda: self.setParent(None))
        self.verwijderButton.clicked.connect(lambda: self.deleteLater())
        
class sjablonenWindow(QDialog, Ui_Rooster_epd_sjablonen):
    def __init__(self, parent = None, save_dict : dict = None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Set the text of the buttonbox buttons
        self.buttonBox.button(QDialogButtonBox.Save).setText("Opslaan")
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("Annuleren")
        
        self.save_dict = save_dict
        
        self.count = 0
        self.sjablonen = {}
        
        # Get the layout in the scroll area
        self.scrolllayout = self.scrollAreaWidgetContents.layout()
        
        # Connect buttons to functions
        self.nieuwButton.clicked.connect(self.addSjabloon)
        self.buttonBox.accepted.connect(self.saveSjablonen)
        
        # Add sjablonen if needed
        if len(save_dict["sjablonen"]) > 0:
            for sjabloon in self.save_dict["sjablonen"].keys():
                self.addSjabloon(self.save_dict["sjablonen"][sjabloon])
        
        # Check if save button should be disabled
        self.checkSaveDisable()
    
    # Resize the ui if the window is resized
    def resizeEvent(self, event):
        QDialog.resizeEvent(self, event)
        self.scrollArea.setGeometry(QRect(-1, 0, 396, event.size().height()-40))
        self.buttonBox.setGeometry(QRect(0, event.size().height()-41, 396, 41))
    
    # Add a sjabloon
    def addSjabloon(self, sjabloon):
        # Add the new sjabloon
        sjabloon_naam = f"sjabloon{self.count}"
        self.sjablonen[sjabloon_naam] = sjabloonFrame(self.scrollAreaWidgetContents)
        self.sjablonen[sjabloon_naam].setObjectName(sjabloon_naam)
        self.sjablonen[sjabloon_naam].verwijderButton.clicked.connect(lambda _ = None, sjab_naam = sjabloon_naam: self.sjablonen.pop(sjab_naam))
        self.sjablonen[sjabloon_naam].verwijderButton.clicked.connect(lambda:self.scrolllayout.update())
        self.sjablonen[sjabloon_naam].verwijderButton.clicked.connect(self.checkSaveDisable)
        self.sjablonen[sjabloon_naam].startTime.timeChanged.connect(self.checkSaveDisable)
        self.sjablonen[sjabloon_naam].endTime.timeChanged.connect(self.checkSaveDisable)
        self.sjablonen[sjabloon_naam].onderwerpen.textChanged.connect(self.checkSaveDisable)
        self.sjablonen[sjabloon_naam].locaties.textChanged.connect(self.checkSaveDisable)
        self.sjablonen[sjabloon_naam].lesuur.textChanged.connect(self.checkSaveDisable)
        self.sjablonen[sjabloon_naam].naam.textChanged.connect(self.checkSaveDisable)
        
        # Fill in the info if it was imported form the save
        if type(sjabloon) == dict:
            self.sjablonen[sjabloon_naam].naam.setText(sjabloon["name"])
            self.sjablonen[sjabloon_naam].startTime.setTime(sjabloon["startTime"])
            self.sjablonen[sjabloon_naam].endTime.setTime(sjabloon["endTime"])
            self.sjablonen[sjabloon_naam].onderwerpen.setText(sjabloon["subjects"])
            self.sjablonen[sjabloon_naam].locaties.setText(sjabloon["locations"])
            self.sjablonen[sjabloon_naam].lesuur.setText(sjabloon["timeSlotName"])
        
        self.scrolllayout.insertWidget(self.scrolllayout.count() - 1, self.sjablonen[sjabloon_naam])
        self.count += 1
        
        # Check if save button should be disabled
        self.checkSaveDisable()
    
    # Check if every template has a name and if there are changes
    def checkSaveDisable(self):
        sjabloon_names = []
        disable = False
        self.new_sjablonen = {}
        
        for widget in self.scrollAreaWidgetContents.children():
            if widget.objectName().startswith("sjabloon"):
                if widget.naam.text() == "" or widget.naam.text() in sjabloon_names:
                    disable = True
                else:
                    sjabloon_names.append(widget.naam.text())
                
                self.new_sjablonen[widget.naam.text()] = {"name": widget.naam.text(),
                                                          "startTime": widget.startTime.time(),
                                                          "endTime": widget.endTime.time(),
                                                          "subjects": widget.onderwerpen.text(),
                                                          "locations": widget.locaties.text(),
                                                          "timeSlotName": widget.lesuur.text()}
        
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(disable or self.new_sjablonen == self.save_dict["sjablonen"])

    # Save the sjablonen
    def saveSjablonen(self):
        self.save_dict["sjablonen"] = deepcopy(self.new_sjablonen)

        with open("rooster-epd.data", "wb") as save_file:
            dump(self.save_dict, save_file)