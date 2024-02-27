from copy import deepcopy
from datetime import date
from pickle import dump

from PySide6.QtCore import QRect, QDate
from PySide6.QtWidgets import QFrame, QDialog, QDialogButtonBox

from rooster_epd_ui import Ui_Sjabloon, Ui_Rooster_epd_sjablonen, Ui_Afspraak, Ui_Rooster_epd_afspraken

class sjabloonFrame(QFrame, Ui_Sjabloon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Add a minimum time check
        self.startTime.timeChanged.connect(self.setMinTime)
        
        # Delete the sjabloon when verwijder is clicked
        self.verwijderButton.clicked.connect(lambda:self.deleteLater())
    
    def setMinTime(self):
        self.endTime.setMinimumTime(self.startTime.time())
        
class sjablonenWindow(QDialog, Ui_Rooster_epd_sjablonen):
    def __init__(self, save_dict : dict):
        super().__init__()
        self.setupUi(self)
        
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
            for sjabloon in save_dict["sjablonen"]:
                self.addSjabloon(sjabloon)
    
    # Resize the ui if the window is resized
    def resizeEvent(self, event):
        QDialog.resizeEvent(self, event)
        self.scrollArea.setGeometry(QRect(-1, 0, 396, event.size().height()-40))
        self.buttonBox.setGeometry(QRect(0, event.size().height()-41, 396, 41))
    
    # Add a sjabloon
    def addSjabloon(self, sjabloon = None):
        sjabloon_naam = f"sjabloon{self.count}"
        self.sjablonen[sjabloon_naam] = sjabloonFrame(self.scrollAreaWidgetContents)
        self.sjablonen[sjabloon_naam].setObjectName(sjabloon_naam)
        self.sjablonen[sjabloon_naam].verwijderButton.clicked.connect(lambda:self.sjablonen.pop(sjabloon_naam))
        self.sjablonen[sjabloon_naam].verwijderButton.clicked.connect(lambda:self.scrolllayout.update())
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
    
    def checkSaveDisable(self):
        sjabloon_names = []
        disable = False
        for widget in self.scrollAreaWidgetContents.children():
            if widget.objectName().startswith("sjabloon"):
                if widget.naam.text() == "" or widget.naam.text() in sjabloon_names:
                    disable = True
                else:
                    sjabloon_names.append(widget.naam.text())
        
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(disable)

    # Save the sjablonen
    def saveSjablonen(self):
        self.save_dict["sjablonen"] = []
        
        for widget in self.scrollAreaWidgetContents.children():
            if widget.objectName().startswith("sjabloon"):
                sjabloon = {}
                sjabloon["name"] = widget.naam.text()
                sjabloon["startTime"] = widget.startTime.time()
                sjabloon["endTime"] = widget.endTime.time()
                sjabloon["subjects"] = widget.onderwerpen.text()
                sjabloon["locations"] = widget.locaties.text()
                sjabloon["timeSlotName"] = widget.lesuur.text()
                
                self.save_dict["sjablonen"].append(deepcopy(sjabloon))

        with open("rooster-epd.data", "wb") as save_file:
            dump(self.save_dict, save_file)

class afspraakFrame(QFrame, Ui_Afspraak):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.startTime.timeChanged.connect(self.setMinTime)
        
        self.verwijderButton.clicked.connect(lambda:self.deleteLater())
        
        # Set minimum date
        today = date.today()
        min_date = QDate()
        min_date.setDate(today.year, today.month, today.day)
        self.datum.setMinimumDate(min_date)
    
    def setMinTime(self):
        self.endTime.setMinimumTime(self.startTime.time())
        
class afsprakenWindow(QDialog, Ui_Rooster_epd_afspraken):
    def __init__(self, save_dict : dict):
        super().__init__()
        self.setupUi(self)
        
        self.save_dict = save_dict
        
        self.count = 0
        self.afspraken = {}
        
        # Get the layout in the scroll area
        self.scrolllayout = self.scrollAreaWidgetContents.layout()
        
        # Connect buttons to functions
        self.nieuwButton.clicked.connect(self.addAfspraak)
        self.buttonBox.accepted.connect(self.saveAfspraken)
        
        # Add afspraken if needed
        if len(self.save_dict["afspraken"]) > 0:
            for afspraak in self.save_dict["afspraken"]:
                self.addAfspraak(afspraak)
    
    # Resize the ui if the window is resized
    def resizeEvent(self, event):
        QDialog.resizeEvent(self, event)
        self.scrollArea.setGeometry(QRect(-1, 0, 396, event.size().height()-40))
        self.buttonBox.setGeometry(QRect(0, event.size().height()-41, 396, 41))
    
    # Add an afspraak
    def addAfspraak(self, afspraak = None):
        afspraak_naam = f"afspraak{self.count}"
        self.afspraken[afspraak_naam] = afspraakFrame(self.scrollAreaWidgetContents)
        self.afspraken[afspraak_naam].setObjectName(afspraak_naam)
        self.afspraken[afspraak_naam].verwijderButton.clicked.connect(lambda:self.afspraken.pop(afspraak_naam))
        self.afspraken[afspraak_naam].verwijderButton.clicked.connect(lambda:self.scrolllayout.update())
        
        # Fill in the info if it was imported form the save
        if type(afspraak) == dict:
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