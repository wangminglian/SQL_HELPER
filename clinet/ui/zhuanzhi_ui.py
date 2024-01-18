# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'zhuazhi.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(651, 551)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.li_wjm = QLineEdit(self.centralwidget)
        self.li_wjm.setObjectName(u"li_wjm")

        self.horizontalLayout.addWidget(self.li_wjm)

        self.bt_xzwj = QPushButton(self.centralwidget)
        self.bt_xzwj.setObjectName(u"bt_xzwj")

        self.horizontalLayout.addWidget(self.bt_xzwj)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.li_hfg = QLineEdit(self.centralwidget)
        self.li_hfg.setObjectName(u"li_hfg")

        self.horizontalLayout_2.addWidget(self.li_hfg)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.li_lfg = QLineEdit(self.centralwidget)
        self.li_lfg.setObjectName(u"li_lfg")

        self.horizontalLayout_2.addWidget(self.li_lfg)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.bt_kszh = QPushButton(self.centralwidget)
        self.bt_kszh.setObjectName(u"bt_kszh")

        self.horizontalLayout_3.addWidget(self.bt_kszh)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 651, 26))
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"csv\u8f6c\u7f6e\u5de5\u5177", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u540d", None))
        self.bt_xzwj.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u884c\u5206\u9694\u7b26", None))
        self.li_hfg.setText(QCoreApplication.translate("MainWindow", u"\\t", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5217\u5206\u9694\u7b26", None))
        self.li_lfg.setText(QCoreApplication.translate("MainWindow", u"\\n", None))
        self.bt_kszh.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u8f6c\u6362", None))
    # retranslateUi

