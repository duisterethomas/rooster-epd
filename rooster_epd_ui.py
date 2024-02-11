from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt
from PySide6.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton, QSizePolicy, QStatusBar, QWidget, QDialogButtonBox, QTimeEdit, QMenu, QMenuBar
from PySide6.QtGui import QAction

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
        self.centralwidget = QWidget(Rooster_epd)
        self.centralwidget.setObjectName(u"centralwidget")
        self.morgen = QPushButton(self.centralwidget)
        self.morgen.setObjectName(u"morgen")
        self.morgen.setGeometry(QRect(160, 40, 81, 24))
        self.pico_port = QComboBox(self.centralwidget)
        self.pico_port.setObjectName(u"pico_port")
        self.pico_port.setGeometry(QRect(70, 10, 171, 22))
        self.label_pico_port = QLabel(self.centralwidget)
        self.label_pico_port.setObjectName(u"label_pico_port")
        self.label_pico_port.setGeometry(QRect(10, 10, 51, 21))
        self.label_pico_port.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.vandaag = QPushButton(self.centralwidget)
        self.vandaag.setObjectName(u"vandaag")
        self.vandaag.setGeometry(QRect(70, 40, 81, 24))
        self.label_pico_port_2 = QLabel(self.centralwidget)
        self.label_pico_port_2.setObjectName(u"label_pico_port_2")
        self.label_pico_port_2.setGeometry(QRect(10, 40, 51, 21))
        self.label_pico_port_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        Rooster_epd.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Rooster_epd)
        self.statusbar.setObjectName(u"statusbar")
        Rooster_epd.setStatusBar(self.statusbar)
        self.menuBar = QMenuBar(Rooster_epd)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 251, 22))
        self.menuSettings = QMenu(self.menuBar)
        self.menuSettings.setObjectName(u"menuSettings")
        Rooster_epd.setMenuBar(self.menuBar)

        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuSettings.addAction(self.actionZermelo_koppelen)
        self.menuSettings.addAction(self.actionTijden_instellen)

        self.retranslateUi(Rooster_epd)

        QMetaObject.connectSlotsByName(Rooster_epd)
    # setupUi

    def retranslateUi(self, Rooster_epd):
        Rooster_epd.setWindowTitle(QCoreApplication.translate("Rooster_epd", u"Rooster epd", None))
        self.actionTijden_instellen.setText(QCoreApplication.translate("Rooster_epd", u"Tijden instellen", None))
        self.actionZermelo_koppelen.setText(QCoreApplication.translate("Rooster_epd", u"Zermelo koppelen", None))
        self.morgen.setText(QCoreApplication.translate("Rooster_epd", u"Morgen", None))
        self.label_pico_port.setText(QCoreApplication.translate("Rooster_epd", u"Pico port:", None))
        self.vandaag.setText(QCoreApplication.translate("Rooster_epd", u"Vandaag", None))
        self.label_pico_port_2.setText(QCoreApplication.translate("Rooster_epd", u"Upload:", None))
        self.menuSettings.setTitle(QCoreApplication.translate("Rooster_epd", u"Instellingen", None))
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