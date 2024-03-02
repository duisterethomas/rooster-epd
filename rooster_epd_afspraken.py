from copy import deepcopy
from datetime import date
from pickle import dump

from PySide6.QtCore import QRect, QDate
from PySide6.QtWidgets import QFrame, QDialog
from PySide6.QtGui import QAction

from rooster_epd_ui import Ui_Afspraak, Ui_Rooster_epd_afspraken

from rooster_epd_sjablonen import sjablonenWindow

class afspraakFrame(QFrame, Ui_Afspraak):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Add a minimum time check
        self.startTime.timeChanged.connect(lambda:self.endTime.setMinimumTime(self.startTime.time()))
        
        # Add a max length check
        self.lesuur.textChanged.connect(lambda:self.onderwerpen.setMaxLength(12-len(self.lesuur.text())))
        
        # Delete the sjabloon when verwijder is clicked
        self.verwijderButton.clicked.connect(lambda:self.deleteLater())
        
        # Set minimum date
        today = date.today()
        min_date = QDate()
        min_date.setDate(today.year, today.month, today.day)
        self.datum.setMinimumDate(min_date)
        
class afsprakenWindow(QDialog, Ui_Rooster_epd_afspraken):
    def __init__(self, save_dict : dict):
        super().__init__()
        self.setupUi(self)
        
        # Copy the save_dict to self.save_dict
        self.save_dict = save_dict
        
        # Set required initial values for variables
        self.count = 0
        self.afspraken = {}
        self.sjablonen = []
        
        # Get the layout in the scroll area
        self.scrolllayout = self.scrollAreaWidgetContents.layout()
        
        # Connect buttons to functions
        self.nieuwButton.clicked.connect(self.addAfspraak)
        self.buttonBox.accepted.connect(self.saveAfspraken)
        
        # Add all the templates to the template combobox
        self.refreshTemplates()
        
        # Add afspraken if needed
        if len(self.save_dict["afspraken"]) > 0:
            for afspraak in self.save_dict["afspraken"]:
                self.addAfspraak(afspraak)
    
    # Resize the ui if the window is resized
    def resizeEvent(self, event):
        QDialog.resizeEvent(self, event)
        self.scrollArea.setGeometry(QRect(-1, 0, 396, event.size().height()-40))
        self.buttonBox.setGeometry(QRect(0, event.size().height()-41, 396, 41))
    
    # Open the sjablonen bewerken ui
    def openSjablonenBewerken(self):
        dlg = sjablonenWindow(self.save_dict)
        dlg.exec()
        
        # Refresh the template list
        self.refreshTemplates()
    
    # Refresh the template buttons
    def refreshTemplates(self):
        for sjabloon in self.sjablonen:
            sjabloon.deleteLater()
            
        self.sjablonen = [QAction(text="Sjablonen bewerken", parent=self.nieuwButton)]
        self.sjablonen[0].triggered.connect(self.openSjablonenBewerken)
        
        for sjabloon in self.save_dict["sjablonen"].keys():
            self.sjablonen.append(QAction(text=sjabloon, parent=self.nieuwButton))
            self.sjablonen[-1].triggered.connect(lambda:self.addAfspraak(self.save_dict["sjablonen"][sjabloon]))
        
        self.nieuwButton.addActions(self.sjablonen)
        
    
    # Add an afspraak
    def addAfspraak(self, afspraak = None):
        afspraak_naam = f"afspraak{self.count}"
        self.afspraken[afspraak_naam] = afspraakFrame(self.scrollAreaWidgetContents)
        self.afspraken[afspraak_naam].setObjectName(afspraak_naam)
        self.afspraken[afspraak_naam].verwijderButton.clicked.connect(lambda:self.afspraken.pop(afspraak_naam))
        self.afspraken[afspraak_naam].verwijderButton.clicked.connect(lambda:self.scrolllayout.update())
        
        # Fill in the info if it was imported form the save
        if type(afspraak) == dict:
            if "date" in afspraak.keys():
                self.afspraken[afspraak_naam].datum.setDate(afspraak["date"])
            self.afspraken[afspraak_naam].startTime.setTime(afspraak["startTime"])
            self.afspraken[afspraak_naam].endTime.setTime(afspraak["endTime"])
            self.afspraken[afspraak_naam].onderwerpen.setText(afspraak["subjects"])
            self.afspraken[afspraak_naam].locaties.setText(afspraak["locations"])
            self.afspraken[afspraak_naam].lesuur.setText(afspraak["timeSlotName"])
        
        self.scrolllayout.insertWidget(self.scrolllayout.count() - 1, self.afspraken[afspraak_naam])
        self.count += 1

    # Save the afspraken
    def saveAfspraken(self):
        self.save_dict["afspraken"] = []
        
        for widget in self.scrollAreaWidgetContents.children():
            if widget.objectName().startswith("afspraak"):
                afspraak = {}
                afspraak["date"] = widget.datum.date()
                afspraak["startTime"] = widget.startTime.time()
                afspraak["endTime"] = widget.endTime.time()
                afspraak["subjects"] = widget.onderwerpen.text()
                afspraak["locations"] = widget.locaties.text()
                afspraak["timeSlotName"] = widget.lesuur.text()
                
                self.save_dict["afspraken"].append(deepcopy(afspraak))

        with open("rooster-epd.data", "wb") as save_file:
            dump(self.save_dict, save_file)