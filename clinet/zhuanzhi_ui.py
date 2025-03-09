# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'zhuazhi.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


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
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout.addWidget(self.label_5)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

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

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_6.addWidget(self.label_7)

        self.li_daochu = QLineEdit(self.centralwidget)
        self.li_daochu.setObjectName(u"li_daochu")

        self.horizontalLayout_6.addWidget(self.li_daochu)

        self.pb_daochu = QPushButton(self.centralwidget)
        self.pb_daochu.setObjectName(u"pb_daochu")

        self.horizontalLayout_6.addWidget(self.pb_daochu)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

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

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_3)

        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_4)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_5.addWidget(self.label_6)

        self.li_index = QLineEdit(self.centralwidget)
        self.li_index.setObjectName(u"li_index")

        self.horizontalLayout_5.addWidget(self.li_index)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.ra_head = QRadioButton(self.centralwidget)
        self.ra_head.setObjectName(u"ra_head")

        self.horizontalLayout_5.addWidget(self.ra_head)


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.pb_split = QPushButton(self.centralwidget)
        self.pb_split.setObjectName(u"pb_split")

        self.horizontalLayout_3.addWidget(self.pb_split)

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
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u901a\u7528\u914d\u7f6e\u9879", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u540d", None))
        self.bt_xzwj.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6587\u4ef6", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u5bfc\u51fa\u76ee\u5f55", None))
        self.pb_daochu.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u76ee\u5f55", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u884c\u5206\u9694\u7b26", None))
        self.li_hfg.setText(QCoreApplication.translate("MainWindow", u"\\n", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5217\u5206\u9694\u7b26", None))
        self.li_lfg.setText(QCoreApplication.translate("MainWindow", u",", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u5206\u9694\u914d\u7f6e\u9879", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u5206\u9694\u5b57\u6bb5\u7d22\u5f15(0)\u5f00\u59cb", None))
        self.ra_head.setText(QCoreApplication.translate("MainWindow", u"\u662f\u5426\u5305\u542b\u8868\u5934", None))
        self.pb_split.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u5206\u9694\u6587\u4ef6", None))
        self.bt_kszh.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u8f6c\u7f6e", None))
    # retranslateUi

