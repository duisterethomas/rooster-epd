from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt
from PySide6.QtWidgets import QComboBox, QLabel, QLineEdit, QPushButton, QSizePolicy, QStatusBar, QWidget

# The main UI
class Ui_Rooster_epd(object):
    def setupUi(self, Rooster_epd):
        if not Rooster_epd.objectName():
            Rooster_epd.setObjectName(u"Rooster_epd")
        Rooster_epd.resize(251, 91)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Rooster_epd.sizePolicy().hasHeightForWidth())
        Rooster_epd.setSizePolicy(sizePolicy)
        Rooster_epd.setMinimumSize(QSize(251, 91))
        Rooster_epd.setMaximumSize(QSize(251, 91))
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

        self.retranslateUi(Rooster_epd)

        QMetaObject.connectSlotsByName(Rooster_epd)
    # setupUi

    def retranslateUi(self, Rooster_epd):
        Rooster_epd.setWindowTitle(QCoreApplication.translate("Rooster_epd", u"Rooster epd", None))
        self.morgen.setText(QCoreApplication.translate("Rooster_epd", u"Morgen", None))
        self.label_pico_port.setText(QCoreApplication.translate("Rooster_epd", u"Pico port:", None))
        self.vandaag.setText(QCoreApplication.translate("Rooster_epd", u"Vandaag", None))
        self.label_pico_port_2.setText(QCoreApplication.translate("Rooster_epd", u"Upload:", None))
    # retranslateUi

# The setup UI
class Ui_Rooster_epd_setup(object):
    def setupUi(self, Rooster_epd_setup):
        if not Rooster_epd_setup.objectName():
            Rooster_epd_setup.setObjectName(u"Rooster_epd_setup")
        Rooster_epd_setup.resize(271, 101)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Rooster_epd_setup.sizePolicy().hasHeightForWidth())
        Rooster_epd_setup.setSizePolicy(sizePolicy)
        Rooster_epd_setup.setMinimumSize(QSize(271, 101))
        Rooster_epd_setup.setMaximumSize(QSize(271, 101))
        self.centralwidget = QWidget(Rooster_epd_setup)
        self.centralwidget.setObjectName(u"centralwidget")
        self.save = QPushButton(self.centralwidget)
        self.save.setObjectName(u"save")
        self.save.setGeometry(QRect(180, 70, 81, 24))
        self.koppelcode = QLineEdit(self.centralwidget)
        self.koppelcode.setObjectName(u"koppelcode")
        self.koppelcode.setGeometry(QRect(90, 40, 171, 22))
        self.schoolnaam = QLineEdit(self.centralwidget)
        self.schoolnaam.setObjectName(u"schoolnaam")
        self.schoolnaam.setGeometry(QRect(90, 10, 171, 22))
        self.label_koppelcode = QLabel(self.centralwidget)
        self.label_koppelcode.setObjectName(u"label_koppelcode")
        self.label_koppelcode.setGeometry(QRect(10, 40, 71, 21))
        self.label_koppelcode.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_schoolnaam = QLabel(self.centralwidget)
        self.label_schoolnaam.setObjectName(u"label_schoolnaam")
        self.label_schoolnaam.setGeometry(QRect(10, 10, 71, 21))
        self.label_schoolnaam.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        Rooster_epd_setup.setCentralWidget(self.centralwidget)

        self.retranslateUi(Rooster_epd_setup)

        QMetaObject.connectSlotsByName(Rooster_epd_setup)
    # setupUi

    def retranslateUi(self, Rooster_epd_setup):
        Rooster_epd_setup.setWindowTitle(QCoreApplication.translate("Rooster_epd_setup", u"Rooster epd", None))
        self.save.setText(QCoreApplication.translate("Rooster_epd_setup", u"Save", None))
        self.label_koppelcode.setText(QCoreApplication.translate("Rooster_epd_setup", u"Koppelcode:", None))
        self.label_schoolnaam.setText(QCoreApplication.translate("Rooster_epd_setup", u"Schoolnaam:", None))
    # retranslateUi