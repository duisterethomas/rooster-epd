from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt
from PySide6.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton, QSizePolicy, QStatusBar, QWidget, QDialogButtonBox, QTimeEdit, QDateEdit, QMenu, QMenuBar, QScrollArea, QFrame, QVBoxLayout, QSpacerItem, QToolButton
from PySide6.QtGui import QAction, QFont

# The main UI
class Ui_Rooster_epd(object):
    def setupUi(self, Rooster_epd):
        if not Rooster_epd.objectName():
            Rooster_epd.setObjectName(u"Rooster_epd")
        Rooster_epd.resize(251, 111)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Rooster_epd.sizePolicy().hasHeightForWidth())
        Rooster_epd.setSizePolicy(sizePolicy)
        Rooster_epd.setMinimumSize(QSize(251, 111))
        Rooster_epd.setMaximumSize(QSize(251, 111))
        self.actionTijden_instellen = QAction(Rooster_epd)
        self.actionTijden_instellen.setObjectName(u"actionTijden_instellen")
        self.actionZermelo_koppelen = QAction(Rooster_epd)
        self.actionZermelo_koppelen.setObjectName(u"actionZermelo_koppelen")
        self.actionRefresh_ports = QAction(Rooster_epd)
        self.actionRefresh_ports.setObjectName(u"actionRefresh_ports")
        self.actionNotities_bewerken = QAction(Rooster_epd)
        self.actionNotities_bewerken.setObjectName(u"actionNotities_bewerken")
        self.actionAfspraken_bewerken = QAction(Rooster_epd)
        self.actionAfspraken_bewerken.setObjectName(u"actionAfspraken_bewerken")
        self.actionOver_Rooster_epd = QAction(Rooster_epd)
        self.actionOver_Rooster_epd.setObjectName(u"actionOver_Rooster_epd")
        self.actionGithub_repository = QAction(Rooster_epd)
        self.actionGithub_repository.setObjectName(u"actionGithub_repository")
        self.centralwidget = QWidget(Rooster_epd)
        self.centralwidget.setObjectName(u"centralwidget")
        self.pico_port = QComboBox(self.centralwidget)
        self.pico_port.setObjectName(u"pico_port")
        self.pico_port.setGeometry(QRect(70, 10, 171, 22))
        self.label_pico_port = QLabel(self.centralwidget)
        self.label_pico_port.setObjectName(u"label_pico_port")
        self.label_pico_port.setGeometry(QRect(10, 10, 51, 21))
        self.label_pico_port.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.sync = QPushButton(self.centralwidget)
        self.sync.setObjectName(u"sync")
        self.sync.setGeometry(QRect(160, 40, 81, 24))
        self.connect_button = QPushButton(self.centralwidget)
        self.connect_button.setObjectName(u"connect_button")
        self.connect_button.setGeometry(QRect(70, 40, 81, 24))
        Rooster_epd.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Rooster_epd)
        self.statusbar.setObjectName(u"statusbar")
        Rooster_epd.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(Rooster_epd)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 251, 22))
        self.menuSettings = QMenu(self.menuBar)
        self.menuSettings.setObjectName(u"menuSettings")
        self.menuBewerken = QMenu(self.menuBar)
        self.menuBewerken.setObjectName(u"menuBewerken")
        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName(u"menuHelp")
        Rooster_epd.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuBewerken.menuAction())
        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.menuSettings.addAction(self.actionZermelo_koppelen)
        self.menuSettings.addAction(self.actionTijden_instellen)
        self.menuSettings.addSeparator()
        self.menuSettings.addAction(self.actionRefresh_ports)
        self.menuBewerken.addAction(self.actionNotities_bewerken)
        self.menuBewerken.addAction(self.actionAfspraken_bewerken)
        self.menuHelp.addAction(self.actionGithub_repository)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionOver_Rooster_epd)

        self.retranslateUi(Rooster_epd)

        QMetaObject.connectSlotsByName(Rooster_epd)
    # setupUi

    def retranslateUi(self, Rooster_epd):
        Rooster_epd.setWindowTitle(QCoreApplication.translate("Rooster_epd", u"Rooster epd", None))
        self.actionTijden_instellen.setText(QCoreApplication.translate("Rooster_epd", u"Tijden instellen", None))
        self.actionZermelo_koppelen.setText(QCoreApplication.translate("Rooster_epd", u"Zermelo koppelen", None))
        self.actionRefresh_ports.setText(QCoreApplication.translate("Rooster_epd", u"Refresh ports", None))
        self.actionNotities_bewerken.setText(QCoreApplication.translate("Rooster_epd", u"Notities bewerken", None))
        self.actionAfspraken_bewerken.setText(QCoreApplication.translate("Rooster_epd", u"Afspraken bewerken", None))
        self.actionOver_Rooster_epd.setText(QCoreApplication.translate("Rooster_epd", u"Over Rooster epd", None))
        self.actionGithub_repository.setText(QCoreApplication.translate("Rooster_epd", u"Github repository", None))
        self.label_pico_port.setText(QCoreApplication.translate("Rooster_epd", u"Pico port:", None))
        self.sync.setText(QCoreApplication.translate("Rooster_epd", u"Sync", None))
        self.connect_button.setText(QCoreApplication.translate("Rooster_epd", u"Connect", None))
        self.menuSettings.setTitle(QCoreApplication.translate("Rooster_epd", u"Instellingen", None))
        self.menuBewerken.setTitle(QCoreApplication.translate("Rooster_epd", u"Bewerken", None))
        self.menuHelp.setTitle(QCoreApplication.translate("Rooster_epd", u"Help", None))
    # retranslateUi

# The about UI
class Ui_Rooster_epd_over(object):
    def setupUi(self, Rooster_epd_over):
        if not Rooster_epd_over.objectName():
            Rooster_epd_over.setObjectName(u"Rooster_epd_over")
        Rooster_epd_over.resize(141, 81)
        self.buttonBox = QDialogButtonBox(Rooster_epd_over)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(0, 50, 141, 31))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close)
        self.buttonBox.setCenterButtons(True)
        self.label = QLabel(Rooster_epd_over)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 141, 31))
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.version = QLabel(Rooster_epd_over)
        self.version.setObjectName(u"version")
        self.version.setGeometry(QRect(0, 30, 141, 21))
        self.version.setAlignment(Qt.AlignCenter)

        self.retranslateUi(Rooster_epd_over)
        self.buttonBox.accepted.connect(Rooster_epd_over.accept)
        self.buttonBox.rejected.connect(Rooster_epd_over.reject)

        QMetaObject.connectSlotsByName(Rooster_epd_over)
    # setupUi

    def retranslateUi(self, Rooster_epd_over):
        Rooster_epd_over.setWindowTitle(QCoreApplication.translate("Rooster_epd_over", u"Rooster epd", None))
        self.label.setText(QCoreApplication.translate("Rooster_epd_over", u"Rooster epd", None))
        self.version.setText(QCoreApplication.translate("Rooster_epd_over", u"V", None))
    # retranslateUi

# The setup UI
class Ui_Rooster_epd_setup(object):
    def setupUi(self, Rooster_epd_setup):
        if not Rooster_epd_setup.objectName():
            Rooster_epd_setup.setObjectName(u"Rooster_epd_setup")
        Rooster_epd_setup.resize(271, 111)
        Rooster_epd_setup.setMinimumSize(QSize(271, 111))
        Rooster_epd_setup.setMaximumSize(QSize(271, 111))
        self.buttonBox = QDialogButtonBox(Rooster_epd_setup)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 70, 251, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)
        self.label_schoolnaam = QLabel(Rooster_epd_setup)
        self.label_schoolnaam.setObjectName(u"label_schoolnaam")
        self.label_schoolnaam.setGeometry(QRect(10, 10, 71, 21))
        self.label_schoolnaam.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_koppelcode = QLabel(Rooster_epd_setup)
        self.label_koppelcode.setObjectName(u"label_koppelcode")
        self.label_koppelcode.setGeometry(QRect(10, 40, 71, 21))
        self.label_koppelcode.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.schoolnaam = QLineEdit(Rooster_epd_setup)
        self.schoolnaam.setObjectName(u"schoolnaam")
        self.schoolnaam.setGeometry(QRect(90, 10, 171, 22))
        self.koppelcode = QLineEdit(Rooster_epd_setup)
        self.koppelcode.setObjectName(u"koppelcode")
        self.koppelcode.setGeometry(QRect(90, 40, 171, 22))

        self.retranslateUi(Rooster_epd_setup)
        self.buttonBox.accepted.connect(Rooster_epd_setup.accept)
        self.buttonBox.rejected.connect(Rooster_epd_setup.reject)

        QMetaObject.connectSlotsByName(Rooster_epd_setup)
    # setupUi

    def retranslateUi(self, Rooster_epd_setup):
        Rooster_epd_setup.setWindowTitle(QCoreApplication.translate("Rooster_epd_setup", u"Zermelo koppelen", None))
        self.label_schoolnaam.setText(QCoreApplication.translate("Rooster_epd_setup", u"Schoolnaam:", None))
        self.label_koppelcode.setText(QCoreApplication.translate("Rooster_epd_setup", u"Koppelcode:", None))
    # retranslateUi

# The tijden UI
class Ui_Rooster_epd_tijden(object):
    def setupUi(self, Tijden):
        if not Tijden.objectName():
            Tijden.setObjectName(u"Tijden")
        Tijden.resize(201, 111)
        Tijden.setMinimumSize(QSize(201, 111))
        Tijden.setMaximumSize(QSize(201, 111))
        Tijden.setLayoutDirection(Qt.LeftToRight)
        self.buttonBox = QDialogButtonBox(Tijden)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 70, 181, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)
        self.beginTijd = QTimeEdit(Tijden)
        self.beginTijd.setObjectName(u"beginTijd")
        self.beginTijd.setGeometry(QRect(120, 10, 61, 22))
        self.eindTijd = QTimeEdit(Tijden)
        self.eindTijd.setObjectName(u"eindTijd")
        self.eindTijd.setGeometry(QRect(120, 40, 61, 22))
        self.label = QLabel(Tijden)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 101, 21))
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_2 = QLabel(Tijden)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 40, 101, 21))
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.retranslateUi(Tijden)
        self.buttonBox.accepted.connect(Tijden.accept)
        self.buttonBox.rejected.connect(Tijden.reject)

        QMetaObject.connectSlotsByName(Tijden)
    # setupUi

    def retranslateUi(self, Tijden):
        Tijden.setWindowTitle(QCoreApplication.translate("Tijden", u"Tijden instellen", None))
        self.label.setText(QCoreApplication.translate("Tijden", u"Begin eerste uur:", None))
        self.label_2.setText(QCoreApplication.translate("Tijden", u"Eind laatste uur:", None))
    # retranslateUi
    
# The notities UI
class Ui_Rooster_epd_notities(object):
    def setupUi(self, Rooster_epd_notities):
        if not Rooster_epd_notities.objectName():
            Rooster_epd_notities.setObjectName(u"Rooster_epd_notities")
        Rooster_epd_notities.resize(231, 261)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Rooster_epd_notities.sizePolicy().hasHeightForWidth())
        Rooster_epd_notities.setSizePolicy(sizePolicy)
        Rooster_epd_notities.setMinimumSize(QSize(231, 261))
        Rooster_epd_notities.setMaximumSize(QSize(231, 261))
        self.buttonBox = QDialogButtonBox(Rooster_epd_notities)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 220, 211, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)
        self.maandag = QLineEdit(Rooster_epd_notities)
        self.maandag.setObjectName(u"maandag")
        self.maandag.setGeometry(QRect(80, 10, 141, 22))
        self.maandag.setMaxLength(18)
        self.maandag.setClearButtonEnabled(True)
        self.dinsdag = QLineEdit(Rooster_epd_notities)
        self.dinsdag.setObjectName(u"dinsdag")
        self.dinsdag.setGeometry(QRect(80, 40, 141, 22))
        self.dinsdag.setMaxLength(18)
        self.dinsdag.setClearButtonEnabled(True)
        self.woensdag = QLineEdit(Rooster_epd_notities)
        self.woensdag.setObjectName(u"woensdag")
        self.woensdag.setGeometry(QRect(80, 70, 141, 22))
        self.woensdag.setMaxLength(18)
        self.woensdag.setClearButtonEnabled(True)
        self.donderdag = QLineEdit(Rooster_epd_notities)
        self.donderdag.setObjectName(u"donderdag")
        self.donderdag.setGeometry(QRect(80, 100, 141, 22))
        self.donderdag.setMaxLength(18)
        self.donderdag.setClearButtonEnabled(True)
        self.vrijdag = QLineEdit(Rooster_epd_notities)
        self.vrijdag.setObjectName(u"vrijdag")
        self.vrijdag.setGeometry(QRect(80, 130, 141, 22))
        self.vrijdag.setMaxLength(18)
        self.vrijdag.setClearButtonEnabled(True)
        self.zaterdag = QLineEdit(Rooster_epd_notities)
        self.zaterdag.setObjectName(u"zaterdag")
        self.zaterdag.setGeometry(QRect(80, 160, 141, 22))
        self.zaterdag.setMaxLength(18)
        self.zaterdag.setClearButtonEnabled(True)
        self.zondag = QLineEdit(Rooster_epd_notities)
        self.zondag.setObjectName(u"zondag")
        self.zondag.setGeometry(QRect(80, 190, 141, 22))
        self.zondag.setMaxLength(18)
        self.zondag.setClearButtonEnabled(True)
        self.label = QLabel(Rooster_epd_notities)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 10, 71, 21))
        self.label.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_2 = QLabel(Rooster_epd_notities)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(0, 40, 71, 21))
        self.label_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_3 = QLabel(Rooster_epd_notities)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(0, 70, 71, 21))
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_4 = QLabel(Rooster_epd_notities)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(0, 100, 71, 21))
        self.label_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_5 = QLabel(Rooster_epd_notities)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(0, 130, 71, 21))
        self.label_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_6 = QLabel(Rooster_epd_notities)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(0, 160, 71, 21))
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_7 = QLabel(Rooster_epd_notities)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(0, 190, 71, 21))
        self.label_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.retranslateUi(Rooster_epd_notities)
        self.buttonBox.accepted.connect(Rooster_epd_notities.accept)
        self.buttonBox.rejected.connect(Rooster_epd_notities.reject)

        QMetaObject.connectSlotsByName(Rooster_epd_notities)
    # setupUi

    def retranslateUi(self, Rooster_epd_notities):
        Rooster_epd_notities.setWindowTitle(QCoreApplication.translate("Rooster_epd_notities", u"Notities bewerken", None))
        self.label.setText(QCoreApplication.translate("Rooster_epd_notities", u"Maandag:", None))
        self.label_2.setText(QCoreApplication.translate("Rooster_epd_notities", u"Dinsdag:", None))
        self.label_3.setText(QCoreApplication.translate("Rooster_epd_notities", u"Woensdag:", None))
        self.label_4.setText(QCoreApplication.translate("Rooster_epd_notities", u"Donderdag;", None))
        self.label_5.setText(QCoreApplication.translate("Rooster_epd_notities", u"Vrijdag:", None))
        self.label_6.setText(QCoreApplication.translate("Rooster_epd_notities", u"Zaterdag:", None))
        self.label_7.setText(QCoreApplication.translate("Rooster_epd_notities", u"Zondag:", None))
    # retranslateUi

# The afspraken ui
class Ui_Rooster_epd_afspraken(object):
    def setupUi(self, Rooster_epd_afspraken):
        if not Rooster_epd_afspraken.objectName():
            Rooster_epd_afspraken.setObjectName(u"Rooster_epd_afspraken")
        Rooster_epd_afspraken.resize(396, 281)
        Rooster_epd_afspraken.setMinimumSize(QSize(396, 171))
        Rooster_epd_afspraken.setMaximumSize(QSize(396, 16777215))
        self.buttonBox = QDialogButtonBox(Rooster_epd_afspraken)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(0, 240, 396, 41))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)
        self.scrollArea = QScrollArea(Rooster_epd_afspraken)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(-1, 0, 396, 241))
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 379, 241))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.nieuwButton = QToolButton(self.scrollAreaWidgetContents)
        self.nieuwButton.setObjectName(u"nieuwButton")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nieuwButton.sizePolicy().hasHeightForWidth())
        self.nieuwButton.setSizePolicy(sizePolicy)
        self.nieuwButton.setPopupMode(QToolButton.MenuButtonPopup)
        self.nieuwButton.setToolButtonStyle(Qt.ToolButtonTextOnly)

        self.verticalLayout.addWidget(self.nieuwButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Rooster_epd_afspraken)
        self.buttonBox.accepted.connect(Rooster_epd_afspraken.accept)
        self.buttonBox.rejected.connect(Rooster_epd_afspraken.reject)

        QMetaObject.connectSlotsByName(Rooster_epd_afspraken)
    # setupUi

    def retranslateUi(self, Rooster_epd_afspraken):
        Rooster_epd_afspraken.setWindowTitle(QCoreApplication.translate("Rooster_epd_afspraken", u"Afspraken bewerken", None))
        self.nieuwButton.setText(QCoreApplication.translate("Rooster_epd_afspraken", u"Nieuwe afspraak", None))
    # retranslateUi

# The afspraak frame
class Ui_Afspraak(object):
    def setupUi(self, Afspraak):
        if not Afspraak.objectName():
            Afspraak.setObjectName(u"Afspraak")
        Afspraak.resize(361, 71)
        Afspraak.setMinimumSize(QSize(361, 71))
        Afspraak.setMaximumSize(QSize(361, 71))
        Afspraak.setFrameShape(QFrame.StyledPanel)
        self.lesuur = QLineEdit(Afspraak)
        self.lesuur.setObjectName(u"lesuur")
        self.lesuur.setGeometry(QRect(210, 10, 41, 22))
        self.lesuur.setMaxLength(5)
        self.line = QFrame(Afspraak)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(60, 10, 21, 51))
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setFrameShape(QFrame.VLine)
        self.onderwerpen = QLineEdit(Afspraak)
        self.onderwerpen.setObjectName(u"onderwerpen")
        self.onderwerpen.setGeometry(QRect(80, 10, 121, 22))
        self.onderwerpen.setMaxLength(12)
        self.locaties = QLineEdit(Afspraak)
        self.locaties.setObjectName(u"locaties")
        self.locaties.setGeometry(QRect(80, 40, 121, 22))
        self.locaties.setMaxLength(12)
        self.verwijderButton = QPushButton(Afspraak)
        self.verwijderButton.setObjectName(u"verwijderButton")
        self.verwijderButton.setGeometry(QRect(271, 39, 81, 24))
        self.startTime = QTimeEdit(Afspraak)
        self.startTime.setObjectName(u"startTime")
        self.startTime.setGeometry(QRect(10, 10, 51, 22))
        self.endTime = QTimeEdit(Afspraak)
        self.endTime.setObjectName(u"endTime")
        self.endTime.setGeometry(QRect(10, 40, 51, 22))
        self.datum = QDateEdit(Afspraak)
        self.datum.setObjectName(u"datum")
        self.datum.setGeometry(QRect(270, 10, 81, 22))
        self.line_2 = QFrame(Afspraak)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(250, 0, 21, 71))
        self.line_2.setFrameShadow(QFrame.Plain)
        self.line_2.setFrameShape(QFrame.VLine)
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
        self.lesuur.setPlaceholderText(QCoreApplication.translate("Afspraak", u"Lesuur", None))
        self.onderwerpen.setPlaceholderText(QCoreApplication.translate("Afspraak", u"Onderwerp(en)", None))
        self.locaties.setPlaceholderText(QCoreApplication.translate("Afspraak", u"Locatie(s)", None))
        self.verwijderButton.setText(QCoreApplication.translate("Afspraak", u"Verwijder", None))
    # retranslateUi

# The sjablonen ui
class Ui_Rooster_epd_sjablonen(object):
    def setupUi(self, Rooster_epd_afspraken):
        if not Rooster_epd_afspraken.objectName():
            Rooster_epd_afspraken.setObjectName(u"Rooster_epd_sjablonen")
        Rooster_epd_afspraken.resize(396, 281)
        Rooster_epd_afspraken.setMinimumSize(QSize(396, 171))
        Rooster_epd_afspraken.setMaximumSize(QSize(396, 16777215))
        self.buttonBox = QDialogButtonBox(Rooster_epd_afspraken)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(0, 240, 396, 41))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(True)
        self.scrollArea = QScrollArea(Rooster_epd_afspraken)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(-1, 0, 396, 241))
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 379, 241))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.nieuwButton = QPushButton(self.scrollAreaWidgetContents)
        self.nieuwButton.setObjectName(u"nieuwButton")

        self.verticalLayout.addWidget(self.nieuwButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Rooster_epd_afspraken)
        self.buttonBox.accepted.connect(Rooster_epd_afspraken.accept)
        self.buttonBox.rejected.connect(Rooster_epd_afspraken.reject)

        QMetaObject.connectSlotsByName(Rooster_epd_afspraken)
    # setupUi

    def retranslateUi(self, Rooster_epd_afspraken):
        Rooster_epd_afspraken.setWindowTitle(QCoreApplication.translate("Rooster_epd_afspraken", u"Sjablonen bewerken", None))
        self.nieuwButton.setText(QCoreApplication.translate("Rooster_epd_afspraken", u"Nieuw sjabloon", None))
    # retranslateUi

# The sjabloon frame
class Ui_Sjabloon(object):
    def setupUi(self, Sjabloon):
        if not Sjabloon.objectName():
            Sjabloon.setObjectName(u"Sjabloon")
        Sjabloon.resize(361, 71)
        Sjabloon.setMinimumSize(QSize(361, 71))
        Sjabloon.setMaximumSize(QSize(361, 71))
        Sjabloon.setFrameShape(QFrame.StyledPanel)
        self.lesuur = QLineEdit(Sjabloon)
        self.lesuur.setObjectName(u"lesuur")
        self.lesuur.setGeometry(QRect(210, 10, 41, 22))
        self.lesuur.setMaxLength(5)
        self.line = QFrame(Sjabloon)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(60, 10, 21, 51))
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setFrameShape(QFrame.VLine)
        self.onderwerpen = QLineEdit(Sjabloon)
        self.onderwerpen.setObjectName(u"onderwerpen")
        self.onderwerpen.setGeometry(QRect(80, 10, 121, 22))
        self.onderwerpen.setMaxLength(12)
        self.locaties = QLineEdit(Sjabloon)
        self.locaties.setObjectName(u"locaties")
        self.locaties.setGeometry(QRect(80, 40, 121, 22))
        self.locaties.setMaxLength(12)
        self.verwijderButton = QPushButton(Sjabloon)
        self.verwijderButton.setObjectName(u"verwijderButton")
        self.verwijderButton.setGeometry(QRect(271, 39, 81, 24))
        self.startTime = QTimeEdit(Sjabloon)
        self.startTime.setObjectName(u"startTime")
        self.startTime.setGeometry(QRect(10, 10, 51, 22))
        self.endTime = QTimeEdit(Sjabloon)
        self.endTime.setObjectName(u"endTime")
        self.endTime.setGeometry(QRect(10, 40, 51, 22))
        self.line_2 = QFrame(Sjabloon)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(250, 0, 21, 71))
        self.line_2.setFrameShadow(QFrame.Plain)
        self.line_2.setFrameShape(QFrame.VLine)
        self.naam = QLineEdit(Sjabloon)
        self.naam.setObjectName(u"naam")
        self.naam.setGeometry(QRect(272, 10, 81, 22))
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
        self.lesuur.setPlaceholderText(QCoreApplication.translate("Sjabloon", u"Lesuur", None))
        self.onderwerpen.setPlaceholderText(QCoreApplication.translate("Sjabloon", u"Onderwerp(en)", None))
        self.locaties.setPlaceholderText(QCoreApplication.translate("Sjabloon", u"Locatie(s)", None))
        self.verwijderButton.setText(QCoreApplication.translate("Sjabloon", u"Verwijder", None))
        self.naam.setPlaceholderText(QCoreApplication.translate("Sjabloon", u"Naam", None))
    # retranslateUi