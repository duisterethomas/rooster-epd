from copy import deepcopy
from time import sleep
from json import dumps

from PySide6.QtCore import QRect, QTime
from PySide6.QtWidgets import QFrame, QDialog, QDialogButtonBox

from rooster_epd_ui import Ui_Sjabloon, Ui_Rooster_EPD_sjablonen

class sjabloonFrame(QFrame, Ui_Sjabloon):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Add a minimum time check
        self.startTime.timeChanged.connect(lambda: self.endTime.setMinimumTime(self.startTime.time()))
        
        # Add a max length check
        self.lesuur.textChanged.connect(lambda: self.onderwerpen.setMaxLength(12-len(self.lesuur.text())))
        
        # Delete the template when verwijder is clicked
        self.verwijderButton.clicked.connect(lambda: self.setParent(None))
        self.verwijderButton.clicked.connect(lambda: self.deleteLater())
        
class sjablonenWindow(QDialog, Ui_Rooster_EPD_sjablonen):
    def __init__(self, parent = None, save : dict = None, pico = None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Set the text of the buttonbox buttons
        self.buttonBox.button(QDialogButtonBox.Save).setText("Opslaan")
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("Annuleren")
        
        self.save = save
        self.pico = pico
        
        self.count = 0
        self.templates = {}
        
        # Get the layout in the scroll area
        self.scrolllayout = self.scrollAreaWidgetContents.layout()
        
        # Connect buttons to functions
        self.nieuwButton.clicked.connect(self.addTemplate)
        self.buttonBox.accepted.connect(self.saveTemplates)
        
        # Add templates if needed
        if len(save["templates"]) > 0:
            for template in sorted(self.save["templates"].keys()):
                self.addTemplate(self.save["templates"][template])
        
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
    
    # Add a template
    def addTemplate(self, template):
        # Add the new template
        template_name = f"template{self.count}"
        self.templates[template_name] = sjabloonFrame(self.scrollAreaWidgetContents)
        self.templates[template_name].setObjectName(template_name)
        self.templates[template_name].verwijderButton.clicked.connect(lambda _ = None, temp_name = template_name: self.templates.pop(temp_name))
        self.templates[template_name].verwijderButton.clicked.connect(lambda:self.scrolllayout.update())
        self.templates[template_name].verwijderButton.clicked.connect(self.checkSaveDisable)
        self.templates[template_name].startTime.timeChanged.connect(self.checkSaveDisable)
        self.templates[template_name].endTime.timeChanged.connect(self.checkSaveDisable)
        self.templates[template_name].onderwerpen.textChanged.connect(self.checkSaveDisable)
        self.templates[template_name].locaties.textChanged.connect(self.checkSaveDisable)
        self.templates[template_name].lesuur.textChanged.connect(self.checkSaveDisable)
        self.templates[template_name].naam.textChanged.connect(self.checkSaveDisable)
        
        # Fill in the info if it was imported form the save
        if type(template) == dict:
            self.templates[template_name].naam.setText(template["name"])
            
            starttime = QTime()
            starttime.setHMS(template["startTime"][0], template["startTime"][1], 0)
            self.templates[template_name].startTime.setTime(starttime)
            
            endtime = QTime()
            endtime.setHMS(template["endTime"][0], template["endTime"][1], 0)
            self.templates[template_name].endTime.setTime(endtime)
            
            self.templates[template_name].onderwerpen.setText(template["subjects"])
            self.templates[template_name].locaties.setText(template["locations"])
            self.templates[template_name].lesuur.setText(template["timeSlotName"])
        
        self.scrolllayout.insertWidget(self.scrolllayout.count() - 1, self.templates[template_name])
        self.count += 1
        
        # Check if save button should be disabled
        self.checkSaveDisable()
    
    # Check if every template has a name and if there are changes
    def checkSaveDisable(self):
        template_names = []
        disable = False
        self.new_templates = {}
        
        for widget in self.scrollAreaWidgetContents.children():
            if widget.objectName().startswith("template"):
                if widget.naam.text() == "" or widget.naam.text() in template_names:
                    disable = True
                else:
                    template_names.append(widget.naam.text())
                
                self.new_templates[widget.naam.text()] = {"name": widget.naam.text(),
                                                          "startTime": (widget.startTime.time().hour(), widget.startTime.time().minute()),
                                                          "endTime": (widget.endTime.time().hour(), widget.endTime.time().minute()),
                                                          "subjects": widget.onderwerpen.text(),
                                                          "locations": widget.locaties.text(),
                                                          "timeSlotName": widget.lesuur.text()}
        
        self.buttonBox.button(QDialogButtonBox.Save).setDisabled(disable or self.new_templates == self.save["templates"])

    # Save the templates
    def saveTemplates(self):
        self.save["templates"] = deepcopy(self.new_templates)
        
        # Save the save
        self.sendToPico(f"dump {dumps(self.save)}")