from copy import deepcopy
from datetime import date
from json import dumps
from time import sleep

from PySide6.QtCore import QRect, QDate, QTime
from PySide6.QtWidgets import QFrame, QDialog, QDialogButtonBox
from PySide6.QtGui import QAction

from rooster_epd_ui import Ui_Afspraak, Ui_Rooster_EPD_afspraken

from rooster_epd_sjablonen import sjablonenWindow

class afspraakFrame(QFrame, Ui_Afspraak):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Add a minimum time check
        self.startTime.timeChanged.connect(lambda: self.endTime.setMinimumTime(self.startTime.time()))
        
        # Add a max length check
        self.lesuur.textChanged.connect(lambda: self.onderwerpen.setMaxLength(12-len(self.lesuur.text())))
        
        # Delete the appointment when verwijder is clicked
        self.verwijderButton.clicked.connect(lambda: self.setParent(None))
        self.verwijderButton.clicked.connect(lambda: self.deleteLater())
        
        # Set minimum date
        today = date.today()
        min_date = QDate()
        min_date.setDate(today.year, today.month, today.day)
        self.datum.setMinimumDate(min_date)
        
class afsprakenWindow(QDialog, Ui_Rooster_EPD_afspraken):
    def __init__(self, parent=None, save: dict = None, pico=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Set the text of the buttonbox buttons
        self.buttonBox.button(QDialogButtonBox.Save).setText("Opslaan")
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("Annuleren")
        
        # Copy the save to self.save
        self.save = save
        self.pico = pico
        
        # Set required initial values for variables
        self.count = 0
        self.appointments = {}
        self.templates = []
        
        # Get the layout in the scroll area
        self.scrolllayout = self.scrollAreaWidgetContents.layout()
        
        # Connect buttons to functions
        self.nieuwButton.clicked.connect(self.addAppointment)
        self.buttonBox.accepted.connect(self.saveAppointments)
        
        # Add all the templates to the template combobox
        self.refreshTemplates()
        
        # Add afspraken if needed
        today = date.today()
        
        if self.save["appointments"]:
            for appointment in self.save["appointments"]:
                if date(appointment["date"][0], appointment["date"][1], appointment["date"][2]) >= today:
                    self.addAppointment(appointment)
                else:
                    # Auto remove old appointments
                    save["appointments"].remove(appointment)
        
        # Save the save
        self.sendToPico(f"dump {dumps(self.save)}")
        
        # Check if save button should be disabled
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
    
    # Resize the ui if the window is resized
    def resizeEvent(self, event):
        QDialog.resizeEvent(self, event)
        self.scrollArea.setGeometry(QRect(-1, 0, 471, event.size().height()-40))
        self.buttonBox.setGeometry(QRect(0, event.size().height()-41, 471, 41))
    
    # Open the sjablonen bewerken ui
    def openSjablonenBewerken(self):
        dlg = sjablonenWindow(self, self.save, self.pico)
        dlg.exec()
        
        # Refresh the template list
        self.refreshTemplates()
    
    # Refresh the template buttons
    def refreshTemplates(self):
        for template in self.templates:
            template.deleteLater()
            
        self.templates = [QAction(text="Sjablonen bewerken", parent=self.nieuwButton)]
        self.templates[0].triggered.connect(self.openSjablonenBewerken)
        
        for template in sorted(self.save["templates"].keys()):
            self.templates.append(QAction(text=template, parent=self.nieuwButton))
            self.templates[-1].triggered.connect(lambda _ = None, templ = template: self.addAppointment(self.save["templates"][templ]))
        
        self.nieuwButton.addActions(self.templates)
    
    # Add an afspraak
    def addAppointment(self, appointment=None):
        appointment_name = f"appointment{self.count}"
        self.appointments[appointment_name] = afspraakFrame(self.scrollAreaWidgetContents)
        self.appointments[appointment_name].setObjectName(appointment_name)
        self.appointments[appointment_name].verwijderButton.clicked.connect(lambda _ = None, afspr_naam = appointment_name: self.appointments.pop(afspr_naam))
        self.appointments[appointment_name].verwijderButton.clicked.connect(lambda: self.scrolllayout.update())
        self.appointments[appointment_name].verwijderButton.clicked.connect(self.checkSaveDisable)
        self.appointments[appointment_name].startTime.timeChanged.connect(self.checkSaveDisable)
        self.appointments[appointment_name].endTime.timeChanged.connect(self.checkSaveDisable)
        self.appointments[appointment_name].onderwerpen.textChanged.connect(self.checkSaveDisable)
        self.appointments[appointment_name].locaties.textChanged.connect(self.checkSaveDisable)
        self.appointments[appointment_name].lesuur.textChanged.connect(self.checkSaveDisable)
        self.appointments[appointment_name].datum.dateChanged.connect(self.checkSaveDisable)
        
        # Fill in the info if it was imported form the save
        if type(appointment) == dict:
            if "date" in appointment.keys():
                qdate = QDate()
                qdate.setDate(appointment["date"][0], appointment["date"][1], appointment["date"][2])
                self.appointments[appointment_name].datum.setDate(qdate)
                
            starttime = QTime()
            starttime.setHMS(appointment["startTime"][0], appointment["startTime"][1], 0)
            self.appointments[appointment_name].startTime.setTime(starttime)
            
            endtime = QTime()
            endtime.setHMS(appointment["endTime"][0], appointment["endTime"][1], 0)
            self.appointments[appointment_name].endTime.setTime(endtime)
            
            self.appointments[appointment_name].onderwerpen.setText(appointment["subjects"])
            self.appointments[appointment_name].locaties.setText(appointment["locations"])
            self.appointments[appointment_name].lesuur.setText(appointment["timeSlotName"])
        
        self.scrolllayout.insertWidget(self.scrolllayout.count() - 1, self.appointments[appointment_name])
        self.count += 1
        
        # Check if save button should be disabled
        self.checkSaveDisable()
    
    # Check if every template has a name and if there are changes
    def checkSaveDisable(self):
        self.new_appointments = []
        
        for widget in self.scrollAreaWidgetContents.children():
            if widget.objectName().startswith("appointment"):
                appointment = {"date": (widget.datum.date().year(), widget.datum.date().month(), widget.datum.date().day()),
                               "startTime": (widget.startTime.time().hour(), widget.startTime.time().minute()),
                               "endTime": (widget.endTime.time().hour(), widget.endTime.time().minute()),
                               "subjects": widget.onderwerpen.text(),
                               "locations": widget.locaties.text(),
                               "timeSlotName": widget.lesuur.text()}
                
                self.new_appointments.append(deepcopy(appointment))
        
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(self.new_appointments == self.save["appointments"])

    # Save the afspraken
    def saveAppointments(self):
        self.save["appointments"] = deepcopy(self.new_appointments)
        
        # Save the save
        self.sendToPico(f"dump {dumps(self.save)}")