from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QSizePolicy, QStatusBar, QWidget, QDialogButtonBox, QTimeEdit, QDateEdit, QMenu, QMenuBar, QScrollArea, QFrame, QVBoxLayout, QSpacerItem, QToolButton, QTextBrowser
from PySide6.QtGui import QAction, QFont, QIcon

# The main UI
class Ui_Rooster_EPD(object):
    def setupUi(self, Rooster_EPD):
        if not Rooster_EPD.objectName():
            Rooster_EPD.setObjectName(u"Rooster_EPD")
        Rooster_EPD.resize(251, 121)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Rooster_EPD.sizePolicy().hasHeightForWidth())
        Rooster_EPD.setSizePolicy(sizePolicy)
        Rooster_EPD.setMinimumSize(QSize(251, 121))
        Rooster_EPD.setMaximumSize(QSize(251, 121))
        self.actionTijden_instellen = QAction(Rooster_EPD)
        self.actionTijden_instellen.setObjectName(u"actionTijden_instellen")
        self.actionZermelo_koppelen = QAction(Rooster_EPD)
        self.actionZermelo_koppelen.setObjectName(u"actionZermelo_koppelen")
        self.actionRefresh_ports = QAction(Rooster_EPD)
        self.actionRefresh_ports.setObjectName(u"actionRefresh_ports")
        self.actionNotities_bewerken = QAction(Rooster_EPD)
        self.actionNotities_bewerken.setObjectName(u"actionNotities_bewerken")
        self.actionAfspraken_bewerken = QAction(Rooster_EPD)
        self.actionAfspraken_bewerken.setObjectName(u"actionAfspraken_bewerken")
        self.actionControleren_op_updates = QAction(Rooster_EPD)
        self.actionControleren_op_updates.setObjectName(u"actionControleren_op_updates")
        self.actionGithub_repository = QAction(Rooster_EPD)
        self.actionGithub_repository.setObjectName(u"actionGithub_repository")
        self.actionWiFi_netwerken = QAction(Rooster_EPD)
        self.actionWiFi_netwerken.setObjectName(u"actionWiFi_netwerken")
        self.actionForceer_pico_update = QAction(Rooster_EPD)
        self.actionForceer_pico_update.setObjectName(u"actionForceer_pico_update")
        self.centralwidget = QWidget(Rooster_EPD)
        self.centralwidget.setObjectName(u"centralwidget")
        self.synchroniserenButton = QPushButton(self.centralwidget)
        self.synchroniserenButton.setObjectName(u"synchroniserenButton")
        self.synchroniserenButton.setGeometry(QRect(10, 40, 231, 24))
        self.verbindenButton = QPushButton(self.centralwidget)
        self.verbindenButton.setObjectName(u"verbindenButton")
        self.verbindenButton.setGeometry(QRect(10, 10, 231, 24))
        Rooster_EPD.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Rooster_EPD)
        self.statusbar.setObjectName(u"statusbar")
        Rooster_EPD.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(Rooster_EPD)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 251, 33))
        self.menuSettings = QMenu(self.menuBar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuBewerken = QMenu(self.menuBar)
        self.menuBewerken.setObjectName(u"menuBewerken")
        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName(u"menuHelp")
        Rooster_EPD.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuBewerken.menuAction())
        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.menuSettings.addAction(self.actionZermelo_koppelen)
        self.menuSettings.addAction(self.actionWiFi_netwerken)
        self.menuSettings.addAction(self.actionTijden_instellen)
        self.menuBewerken.addAction(self.actionNotities_bewerken)
        self.menuBewerken.addAction(self.actionAfspraken_bewerken)
        self.menuHelp.addAction(self.actionGithub_repository)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionControleren_op_updates)
        self.menuHelp.addAction(self.actionForceer_pico_update)

        self.retranslateUi(Rooster_EPD)

        QMetaObject.connectSlotsByName(Rooster_EPD)
    # setupUi

    def retranslateUi(self, Rooster_EPD):
        Rooster_EPD.setWindowTitle(QCoreApplication.translate("Rooster_EPD", u"Rooster-EPD", None))
        self.actionTijden_instellen.setText(QCoreApplication.translate("Rooster_EPD", u"Tijden instellen", None))
        self.actionZermelo_koppelen.setText(QCoreApplication.translate("Rooster_EPD", u"Zermelo koppelen", None))
        self.actionRefresh_ports.setText(QCoreApplication.translate("Rooster_EPD", u"Refresh ports", None))
        self.actionNotities_bewerken.setText(QCoreApplication.translate("Rooster_EPD", u"Notities bewerken", None))
        self.actionAfspraken_bewerken.setText(QCoreApplication.translate("Rooster_EPD", u"Afspraken bewerken", None))
        self.actionControleren_op_updates.setText(QCoreApplication.translate("Rooster_EPD", u"Controleren op updates", None))
        self.actionGithub_repository.setText(QCoreApplication.translate("Rooster_EPD", u"Github repository", None))
        self.actionWiFi_netwerken.setText(QCoreApplication.translate("Rooster_EPD", u"Wi-Fi netwerken", None))
        self.actionForceer_pico_update.setText(QCoreApplication.translate("Rooster_EPD", u"Forceer pico update", None))
        self.synchroniserenButton.setText(QCoreApplication.translate("Rooster_EPD", u"Synchroniseren", None))
        self.verbindenButton.setText(QCoreApplication.translate("Rooster_EPD", u"Verbinden", None))
        self.menuSettings.setTitle(QCoreApplication.translate("Rooster_EPD", u"Instellingen", None))
        self.menuBewerken.setTitle(QCoreApplication.translate("Rooster_EPD", u"Bewerken", None))
        self.menuHelp.setTitle(QCoreApplication.translate("Rooster_EPD", u"Help", None))
    # retranslateUi

# The update UI
class Ui_Rooster_EPD_update(object):
    def setupUi(self, Rooster_EPD_update):
        if not Rooster_EPD_update.objectName():
            Rooster_EPD_update.setObjectName(u"Rooster_EPD_update")
        Rooster_EPD_update.resize(401, 321)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Rooster_EPD_update.sizePolicy().hasHeightForWidth())
        Rooster_EPD_update.setSizePolicy(sizePolicy)
        Rooster_EPD_update.setMinimumSize(QSize(401, 321))
        Rooster_EPD_update.setMaximumSize(QSize(401, 321))
        self.buttonBox = QDialogButtonBox(Rooster_EPD_update)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(0, 280, 401, 41))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.No|QDialogButtonBox.StandardButton.Yes)
        self.buttonBox.setCenterButtons(True)
        self.label = QLabel(Rooster_EPD_update)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 381, 31))
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.version = QLabel(Rooster_EPD_update)
        self.version.setObjectName(u"version")
        self.version.setGeometry(QRect(10, 40, 381, 21))
        self.version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.releaseNotes = QTextBrowser(Rooster_EPD_update)
        self.releaseNotes.setObjectName(u"releaseNotes")
        self.releaseNotes.setGeometry(QRect(10, 90, 381, 161))
        self.releaseNotes.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.label_3 = QLabel(Rooster_EPD_update)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 70, 381, 16))
        self.label_4 = QLabel(Rooster_EPD_update)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 260, 361, 16))
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.retranslateUi(Rooster_EPD_update)
        self.buttonBox.accepted.connect(Rooster_EPD_update.accept)
        self.buttonBox.rejected.connect(Rooster_EPD_update.reject)

        QMetaObject.connectSlotsByName(Rooster_EPD_update)
    # setupUi

    def retranslateUi(self, Rooster_EPD_update):
        Rooster_EPD_update.setWindowTitle(QCoreApplication.translate("Rooster_EPD_update", u"Update beschikbaar!", None))
        self.label.setText(QCoreApplication.translate("Rooster_EPD_update", u"Er is een update beschikbaar!", None))
        self.version.setText(QCoreApplication.translate("Rooster_EPD_update", u"VX.X.X -> VX.X.X", None))
        self.label_3.setText(QCoreApplication.translate("Rooster_EPD_update", u"Release notes:", None))
        self.label_4.setText(QCoreApplication.translate("Rooster_EPD_update", u"Wil je nu naar GitHub gaan om de update te downloaden?", None))
    # retranslateUi

# The setup UI
class Ui_Rooster_EPD_setup(object):
    def setupUi(self, Rooster_EPD_setup):
        if not Rooster_EPD_setup.objectName():
            Rooster_EPD_setup.setObjectName(u"Rooster_EPD_setup")
        Rooster_EPD_setup.resize(271, 111)
        Rooster_EPD_setup.setMinimumSize(QSize(271, 111))
        Rooster_EPD_setup.setMaximumSize(QSize(271, 111))
        self.buttonBox = QDialogButtonBox(Rooster_EPD_setup)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 70, 251, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)
        self.buttonBox.setCenterButtons(True)
        self.label_schoolnaam = QLabel(Rooster_EPD_setup)
        self.label_schoolnaam.setObjectName(u"label_schoolnaam")
        self.label_schoolnaam.setGeometry(QRect(10, 10, 71, 21))
        self.label_schoolnaam.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_koppelcode = QLabel(Rooster_EPD_setup)
        self.label_koppelcode.setObjectName(u"label_koppelcode")
        self.label_koppelcode.setGeometry(QRect(10, 40, 71, 21))
        self.label_koppelcode.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.schoolnaam = QLineEdit(Rooster_EPD_setup)
        self.schoolnaam.setObjectName(u"schoolnaam")
        self.schoolnaam.setGeometry(QRect(90, 10, 171, 22))
        self.koppelcode = QLineEdit(Rooster_EPD_setup)
        self.koppelcode.setObjectName(u"koppelcode")
        self.koppelcode.setGeometry(QRect(90, 40, 171, 22))

        self.retranslateUi(Rooster_EPD_setup)
        self.buttonBox.accepted.connect(Rooster_EPD_setup.accept)
        self.buttonBox.rejected.connect(Rooster_EPD_setup.reject)

        QMetaObject.connectSlotsByName(Rooster_EPD_setup)
    # setupUi

    def retranslateUi(self, Rooster_EPD_setup):
        Rooster_EPD_setup.setWindowTitle(QCoreApplication.translate("Rooster_EPD_setup", u"Zermelo koppelen", None))
        self.label_schoolnaam.setText(QCoreApplication.translate("Rooster_EPD_setup", u"Schoolnaam:", None))
        self.label_koppelcode.setText(QCoreApplication.translate("Rooster_EPD_setup", u"Koppelcode:", None))
    # retranslateUi

# The wifi UI
class Ui_Rooster_EPD_wifi(object):
    def setupUi(self, Rooster_EPD_wifi):
        if not Rooster_EPD_wifi.objectName():
            Rooster_EPD_wifi.setObjectName(u"Rooster_EPD_wifi")
        Rooster_EPD_wifi.resize(261, 311)
        Rooster_EPD_wifi.setMinimumSize(QSize(261, 201))
        Rooster_EPD_wifi.setMaximumSize(QSize(261, 16777215))
        self.buttonBox = QDialogButtonBox(Rooster_EPD_wifi)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(0, 260, 261, 41))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)
        self.buttonBox.setCenterButtons(True)
        self.scrollArea = QScrollArea(Rooster_EPD_wifi)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(-1, 0, 261, 261))
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 249, 261))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.nieuwButton = QPushButton(self.scrollAreaWidgetContents)
        self.nieuwButton.setObjectName(u"nieuwButton")

        self.verticalLayout.addWidget(self.nieuwButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Rooster_EPD_wifi)
        self.buttonBox.accepted.connect(Rooster_EPD_wifi.accept)
        self.buttonBox.rejected.connect(Rooster_EPD_wifi.reject)

        QMetaObject.connectSlotsByName(Rooster_EPD_wifi)
    # setupUi

    def retranslateUi(self, Rooster_EPD_wifi):
        Rooster_EPD_wifi.setWindowTitle(QCoreApplication.translate("Rooster_EPD_wifi", u"Wi-Fi netwerken", None))
        self.nieuwButton.setText(QCoreApplication.translate("Rooster_EPD_wifi", u"Nieuw Wi-Fi netwerk", None))
    # retranslateUi

# The wifi frame
class Ui_Wifi(object):
    def setupUi(self, Wifi):
        if not Wifi.objectName():
            Wifi.setObjectName(u"Wifi")
        Wifi.resize(231, 71)
        Wifi.setMinimumSize(QSize(231, 71))
        Wifi.setMaximumSize(QSize(231, 71))
        Wifi.setFrameShape(QFrame.Shape.StyledPanel)
        self.ssid = QLineEdit(Wifi)
        self.ssid.setObjectName(u"ssid")
        self.ssid.setGeometry(QRect(10, 10, 171, 22))
        self.password = QLineEdit(Wifi)
        self.password.setObjectName(u"password")
        self.password.setGeometry(QRect(10, 40, 171, 22))
        self.password.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.verwijderButton = QPushButton(Wifi)
        self.verwijderButton.setObjectName(u"verwijderButton")
        self.verwijderButton.setGeometry(QRect(190, 10, 31, 51))
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditDelete))
        self.verwijderButton.setIcon(icon)
        QWidget.setTabOrder(self.ssid, self.password)
        QWidget.setTabOrder(self.password, self.verwijderButton)

        self.retranslateUi(Wifi)

        QMetaObject.connectSlotsByName(Wifi)
    # setupUi

    def retranslateUi(self, Wifi):
        Wifi.setWindowTitle(QCoreApplication.translate("Wifi", u"Frame", None))
        self.ssid.setPlaceholderText(QCoreApplication.translate("Wifi", u"SSID", None))
        self.password.setPlaceholderText(QCoreApplication.translate("Wifi", u"Wachtwoord", None))
        self.verwijderButton.setText("")
    # retranslateUi

# The tijden UI
class Ui_Rooster_EPD_tijden(object):
    def setupUi(self, Rooster_EPD_tijden):
        if not Rooster_EPD_tijden.objectName():
            Rooster_EPD_tijden.setObjectName(u"Rooster_EPD_tijden")
        Rooster_EPD_tijden.resize(211, 111)
        Rooster_EPD_tijden.setMinimumSize(QSize(211, 111))
        Rooster_EPD_tijden.setMaximumSize(QSize(211, 111))
        Rooster_EPD_tijden.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.buttonBox = QDialogButtonBox(Rooster_EPD_tijden)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 70, 191, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)
        self.buttonBox.setCenterButtons(True)
        self.beginTijd = QTimeEdit(Rooster_EPD_tijden)
        self.beginTijd.setObjectName(u"beginTijd")
        self.beginTijd.setGeometry(QRect(110, 10, 81, 22))
        self.eindTijd = QTimeEdit(Rooster_EPD_tijden)
        self.eindTijd.setObjectName(u"eindTijd")
        self.eindTijd.setGeometry(QRect(110, 40, 81, 22))
        self.label = QLabel(Rooster_EPD_tijden)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 91, 21))
        self.label.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.label_2 = QLabel(Rooster_EPD_tijden)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 40, 91, 21))
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.retranslateUi(Rooster_EPD_tijden)
        self.buttonBox.accepted.connect(Rooster_EPD_tijden.accept)
        self.buttonBox.rejected.connect(Rooster_EPD_tijden.reject)

        QMetaObject.connectSlotsByName(Rooster_EPD_tijden)
    # setupUi

    def retranslateUi(self, Rooster_EPD_tijden):
        Rooster_EPD_tijden.setWindowTitle(QCoreApplication.translate("Rooster_EPD_tijden", u"Tijden instellen", None))
        self.label.setText(QCoreApplication.translate("Rooster_EPD_tijden", u"Begin eerste uur:", None))
        self.label_2.setText(QCoreApplication.translate("Rooster_EPD_tijden", u"Eind laatste uur:", None))
    # retranslateUi

# The notities UI
class Ui_Rooster_EPD_notities(object):
    def setupUi(self, Rooster_EPD_notities):
        if not Rooster_EPD_notities.objectName():
            Rooster_EPD_notities.setObjectName(u"Rooster_EPD_notities")
        Rooster_EPD_notities.resize(231, 261)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Rooster_EPD_notities.sizePolicy().hasHeightForWidth())
        Rooster_EPD_notities.setSizePolicy(sizePolicy)
        Rooster_EPD_notities.setMinimumSize(QSize(231, 261))
        Rooster_EPD_notities.setMaximumSize(QSize(231, 261))
        self.buttonBox = QDialogButtonBox(Rooster_EPD_notities)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 220, 211, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)
        self.buttonBox.setCenterButtons(True)
        self.maandag = QLineEdit(Rooster_EPD_notities)
        self.maandag.setObjectName(u"maandag")
        self.maandag.setGeometry(QRect(80, 10, 141, 22))
        self.maandag.setMaxLength(18)
        self.maandag.setClearButtonEnabled(True)
        self.dinsdag = QLineEdit(Rooster_EPD_notities)
        self.dinsdag.setObjectName(u"dinsdag")
        self.dinsdag.setGeometry(QRect(80, 40, 141, 22))
        self.dinsdag.setMaxLength(18)
        self.dinsdag.setClearButtonEnabled(True)
        self.woensdag = QLineEdit(Rooster_EPD_notities)
        self.woensdag.setObjectName(u"woensdag")
        self.woensdag.setGeometry(QRect(80, 70, 141, 22))
        self.woensdag.setMaxLength(18)
        self.woensdag.setClearButtonEnabled(True)
        self.donderdag = QLineEdit(Rooster_EPD_notities)
        self.donderdag.setObjectName(u"donderdag")
        self.donderdag.setGeometry(QRect(80, 100, 141, 22))
        self.donderdag.setMaxLength(18)
        self.donderdag.setClearButtonEnabled(True)
        self.vrijdag = QLineEdit(Rooster_EPD_notities)
        self.vrijdag.setObjectName(u"vrijdag")
        self.vrijdag.setGeometry(QRect(80, 130, 141, 22))
        self.vrijdag.setMaxLength(18)
        self.vrijdag.setClearButtonEnabled(True)
        self.zaterdag = QLineEdit(Rooster_EPD_notities)
        self.zaterdag.setObjectName(u"zaterdag")
        self.zaterdag.setGeometry(QRect(80, 160, 141, 22))
        self.zaterdag.setMaxLength(18)
        self.zaterdag.setClearButtonEnabled(True)
        self.zondag = QLineEdit(Rooster_EPD_notities)
        self.zondag.setObjectName(u"zondag")
        self.zondag.setGeometry(QRect(80, 190, 141, 22))
        self.zondag.setMaxLength(18)
        self.zondag.setClearButtonEnabled(True)
        self.labelMaandag = QLabel(Rooster_EPD_notities)
        self.labelMaandag.setObjectName(u"labelMaandag")
        self.labelMaandag.setGeometry(QRect(0, 10, 71, 21))
        self.labelMaandag.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.labelDinsdag = QLabel(Rooster_EPD_notities)
        self.labelDinsdag.setObjectName(u"labelDinsdag")
        self.labelDinsdag.setGeometry(QRect(0, 40, 71, 21))
        self.labelDinsdag.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.labelWoensdag = QLabel(Rooster_EPD_notities)
        self.labelWoensdag.setObjectName(u"labelWoensdag")
        self.labelWoensdag.setGeometry(QRect(0, 70, 71, 21))
        self.labelWoensdag.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.labelDonderdag = QLabel(Rooster_EPD_notities)
        self.labelDonderdag.setObjectName(u"labelDonderdag")
        self.labelDonderdag.setGeometry(QRect(0, 100, 71, 21))
        self.labelDonderdag.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.labelVrijdag = QLabel(Rooster_EPD_notities)
        self.labelVrijdag.setObjectName(u"labelVrijdag")
        self.labelVrijdag.setGeometry(QRect(0, 130, 71, 21))
        self.labelVrijdag.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.labelZaterdag = QLabel(Rooster_EPD_notities)
        self.labelZaterdag.setObjectName(u"labelZaterdag")
        self.labelZaterdag.setGeometry(QRect(0, 160, 71, 21))
        self.labelZaterdag.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.labelZondag = QLabel(Rooster_EPD_notities)
        self.labelZondag.setObjectName(u"labelZondag")
        self.labelZondag.setGeometry(QRect(0, 190, 71, 21))
        self.labelZondag.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.retranslateUi(Rooster_EPD_notities)
        self.buttonBox.accepted.connect(Rooster_EPD_notities.accept)
        self.buttonBox.rejected.connect(Rooster_EPD_notities.reject)

        QMetaObject.connectSlotsByName(Rooster_EPD_notities)
    # setupUi

    def retranslateUi(self, Rooster_EPD_notities):
        Rooster_EPD_notities.setWindowTitle(QCoreApplication.translate("Rooster_EPD_notities", u"Notities bewerken", None))
        self.labelMaandag.setText(QCoreApplication.translate("Rooster_EPD_notities", u"Maandag:", None))
        self.labelDinsdag.setText(QCoreApplication.translate("Rooster_EPD_notities", u"Dinsdag:", None))
        self.labelWoensdag.setText(QCoreApplication.translate("Rooster_EPD_notities", u"Woensdag:", None))
        self.labelDonderdag.setText(QCoreApplication.translate("Rooster_EPD_notities", u"Donderdag:", None))
        self.labelVrijdag.setText(QCoreApplication.translate("Rooster_EPD_notities", u"Vrijdag:", None))
        self.labelZaterdag.setText(QCoreApplication.translate("Rooster_EPD_notities", u"Zaterdag:", None))
        self.labelZondag.setText(QCoreApplication.translate("Rooster_EPD_notities", u"Zondag:", None))
    # retranslateUi

# The afspraken ui
class Ui_Rooster_EPD_afspraken(object):
    def setupUi(self, Rooster_EPD_afspraken):
        if not Rooster_EPD_afspraken.objectName():
            Rooster_EPD_afspraken.setObjectName(u"Rooster_EPD_afspraken")
        Rooster_EPD_afspraken.resize(471, 281)
        Rooster_EPD_afspraken.setMinimumSize(QSize(471, 171))
        Rooster_EPD_afspraken.setMaximumSize(QSize(471, 16777215))
        self.buttonBox = QDialogButtonBox(Rooster_EPD_afspraken)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(0, 240, 471, 41))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)
        self.buttonBox.setCenterButtons(True)
        self.scrollArea = QScrollArea(Rooster_EPD_afspraken)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(-1, 0, 471, 241))
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 459, 241))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.nieuwButton = QToolButton(self.scrollAreaWidgetContents)
        self.nieuwButton.setObjectName(u"nieuwButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nieuwButton.sizePolicy().hasHeightForWidth())
        self.nieuwButton.setSizePolicy(sizePolicy)
        self.nieuwButton.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.nieuwButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)

        self.verticalLayout.addWidget(self.nieuwButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Rooster_EPD_afspraken)
        self.buttonBox.accepted.connect(Rooster_EPD_afspraken.accept)
        self.buttonBox.rejected.connect(Rooster_EPD_afspraken.reject)

        QMetaObject.connectSlotsByName(Rooster_EPD_afspraken)
    # setupUi

    def retranslateUi(self, Rooster_EPD_afspraken):
        Rooster_EPD_afspraken.setWindowTitle(QCoreApplication.translate("Rooster_EPD_afspraken", u"Afspraken bewerken", None))
        self.nieuwButton.setText(QCoreApplication.translate("Rooster_EPD_afspraken", u"Nieuwe afspraak", None))
    # retranslateUi

# The afspraak frame
class Ui_Afspraak(object):
    def setupUi(self, Afspraak):
        if not Afspraak.objectName():
            Afspraak.setObjectName(u"Afspraak")
        Afspraak.resize(441, 71)
        Afspraak.setMinimumSize(QSize(441, 71))
        Afspraak.setMaximumSize(QSize(441, 71))
        Afspraak.setFrameShape(QFrame.Shape.StyledPanel)
        self.lesuur = QLineEdit(Afspraak)
        self.lesuur.setObjectName(u"lesuur")
        self.lesuur.setGeometry(QRect(250, 10, 41, 22))
        self.lesuur.setMaxLength(5)
        self.line = QFrame(Afspraak)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(100, 10, 21, 51))
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.onderwerpen = QLineEdit(Afspraak)
        self.onderwerpen.setObjectName(u"onderwerpen")
        self.onderwerpen.setGeometry(QRect(120, 10, 121, 22))
        self.onderwerpen.setMaxLength(12)
        self.locaties = QLineEdit(Afspraak)
        self.locaties.setObjectName(u"locaties")
        self.locaties.setGeometry(QRect(120, 40, 121, 22))
        self.locaties.setMaxLength(12)
        self.verwijderButton = QPushButton(Afspraak)
        self.verwijderButton.setObjectName(u"verwijderButton")
        self.verwijderButton.setGeometry(QRect(310, 40, 121, 24))
        self.startTime = QTimeEdit(Afspraak)
        self.startTime.setObjectName(u"startTime")
        self.startTime.setGeometry(QRect(10, 10, 91, 22))
        self.endTime = QTimeEdit(Afspraak)
        self.endTime.setObjectName(u"endTime")
        self.endTime.setGeometry(QRect(10, 40, 91, 22))
        self.datum = QDateEdit(Afspraak)
        self.datum.setObjectName(u"datum")
        self.datum.setGeometry(QRect(310, 10, 121, 22))
        self.line_2 = QFrame(Afspraak)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(290, 0, 21, 71))
        self.line_2.setFrameShadow(QFrame.Shadow.Plain)
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        QWidget.setTabOrder(self.startTime, self.endTime)
        QWidget.setTabOrder(self.endTime, self.onderwerpen)
        QWidget.setTabOrder(self.onderwerpen, self.locaties)
        QWidget.setTabOrder(self.locaties, self.lesuur)
        QWidget.setTabOrder(self.lesuur, self.datum)
        QWidget.setTabOrder(self.datum, self.verwijderButton)

        self.retranslateUi(Afspraak)

        QMetaObject.connectSlotsByName(Afspraak)
    # setupUi

    def retranslateUi(self, Afspraak):
        Afspraak.setWindowTitle(QCoreApplication.translate("Afspraak", u"Frame", None))
        self.lesuur.setPlaceholderText(QCoreApplication.translate("Afspraak", u"Uur", None))
        self.onderwerpen.setPlaceholderText(QCoreApplication.translate("Afspraak", u"Onderwerp(en)", None))
        self.locaties.setPlaceholderText(QCoreApplication.translate("Afspraak", u"Locatie(s)", None))
        self.verwijderButton.setText(QCoreApplication.translate("Afspraak", u"Verwijder", None))
    # retranslateUi

# The sjablonen ui
class Ui_Rooster_EPD_sjablonen(object):
    def setupUi(self, Rooster_EPD_sjablonen):
        if not Rooster_EPD_sjablonen.objectName():
            Rooster_EPD_sjablonen.setObjectName(u"Rooster_EPD_sjablonen")
        Rooster_EPD_sjablonen.resize(471, 281)
        Rooster_EPD_sjablonen.setMinimumSize(QSize(471, 171))
        Rooster_EPD_sjablonen.setMaximumSize(QSize(471, 16777215))
        self.buttonBox = QDialogButtonBox(Rooster_EPD_sjablonen)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(0, 240, 471, 41))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Save)
        self.buttonBox.setCenterButtons(True)
        self.scrollArea = QScrollArea(Rooster_EPD_sjablonen)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(-1, 0, 471, 241))
        self.scrollArea.setFrameShape(QFrame.Shape.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 459, 241))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.nieuwButton = QPushButton(self.scrollAreaWidgetContents)
        self.nieuwButton.setObjectName(u"nieuwButton")

        self.verticalLayout.addWidget(self.nieuwButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Rooster_EPD_sjablonen)
        self.buttonBox.accepted.connect(Rooster_EPD_sjablonen.accept)
        self.buttonBox.rejected.connect(Rooster_EPD_sjablonen.reject)

        QMetaObject.connectSlotsByName(Rooster_EPD_sjablonen)
    # setupUi

    def retranslateUi(self, Rooster_EPD_sjablonen):
        Rooster_EPD_sjablonen.setWindowTitle(QCoreApplication.translate("Rooster_EPD_sjablonen", u"Sjablonen bewerken", None))
        self.nieuwButton.setText(QCoreApplication.translate("Rooster_EPD_sjablonen", u"Nieuw sjabloon", None))
    # retranslateUi

# The sjabloon frame
class Ui_Sjabloon(object):
    def setupUi(self, Sjabloon):
        if not Sjabloon.objectName():
            Sjabloon.setObjectName(u"Sjabloon")
        Sjabloon.resize(441, 71)
        Sjabloon.setMinimumSize(QSize(441, 71))
        Sjabloon.setMaximumSize(QSize(441, 71))
        Sjabloon.setFrameShape(QFrame.Shape.StyledPanel)
        self.lesuur = QLineEdit(Sjabloon)
        self.lesuur.setObjectName(u"lesuur")
        self.lesuur.setGeometry(QRect(250, 10, 41, 22))
        self.lesuur.setMaxLength(5)
        self.line = QFrame(Sjabloon)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(100, 10, 21, 51))
        self.line.setFrameShadow(QFrame.Shadow.Plain)
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.onderwerpen = QLineEdit(Sjabloon)
        self.onderwerpen.setObjectName(u"onderwerpen")
        self.onderwerpen.setGeometry(QRect(120, 10, 121, 22))
        self.onderwerpen.setMaxLength(12)
        self.locaties = QLineEdit(Sjabloon)
        self.locaties.setObjectName(u"locaties")
        self.locaties.setGeometry(QRect(120, 40, 121, 22))
        self.locaties.setMaxLength(12)
        self.verwijderButton = QPushButton(Sjabloon)
        self.verwijderButton.setObjectName(u"verwijderButton")
        self.verwijderButton.setGeometry(QRect(310, 40, 121, 24))
        self.startTime = QTimeEdit(Sjabloon)
        self.startTime.setObjectName(u"startTime")
        self.startTime.setGeometry(QRect(10, 10, 91, 22))
        self.endTime = QTimeEdit(Sjabloon)
        self.endTime.setObjectName(u"endTime")
        self.endTime.setGeometry(QRect(10, 40, 91, 22))
        self.line_2 = QFrame(Sjabloon)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(290, 0, 21, 71))
        self.line_2.setFrameShadow(QFrame.Shadow.Plain)
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.naam = QLineEdit(Sjabloon)
        self.naam.setObjectName(u"naam")
        self.naam.setGeometry(QRect(310, 10, 121, 22))
        QWidget.setTabOrder(self.startTime, self.endTime)
        QWidget.setTabOrder(self.endTime, self.onderwerpen)
        QWidget.setTabOrder(self.onderwerpen, self.locaties)
        QWidget.setTabOrder(self.locaties, self.lesuur)
        QWidget.setTabOrder(self.lesuur, self.naam)
        QWidget.setTabOrder(self.naam, self.verwijderButton)

        self.retranslateUi(Sjabloon)

        QMetaObject.connectSlotsByName(Sjabloon)
    # setupUi

    def retranslateUi(self, Sjabloon):
        Sjabloon.setWindowTitle(QCoreApplication.translate("Sjabloon", u"Frame", None))
        self.lesuur.setPlaceholderText(QCoreApplication.translate("Sjabloon", u"Uur", None))
        self.onderwerpen.setPlaceholderText(QCoreApplication.translate("Sjabloon", u"Onderwerp(en)", None))
        self.locaties.setPlaceholderText(QCoreApplication.translate("Sjabloon", u"Locatie(s)", None))
        self.verwijderButton.setText(QCoreApplication.translate("Sjabloon", u"Verwijder", None))
        self.naam.setPlaceholderText(QCoreApplication.translate("Sjabloon", u"Naam", None))
    # retranslateUi