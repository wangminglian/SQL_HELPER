# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sqlinit.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_INIT_SQL(object):
    def setupUi(self, INIT_SQL):
        if not INIT_SQL.objectName():
            INIT_SQL.setObjectName(u"INIT_SQL")
        INIT_SQL.resize(621, 297)
        self.gridLayout_2 = QGridLayout(INIT_SQL)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_2 = QPushButton(INIT_SQL)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(INIT_SQL)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.lineEdit = QLineEdit(INIT_SQL)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 1, 1, 1, 1)

        self.label = QLabel(INIT_SQL)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QLabel(INIT_SQL)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.comboBox = QComboBox(INIT_SQL)
        self.comboBox.setObjectName(u"comboBox")

        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_2.addItem(self.verticalSpacer, 1, 0, 1, 1)


        self.retranslateUi(INIT_SQL)

        QMetaObject.connectSlotsByName(INIT_SQL)
    # setupUi

    def retranslateUi(self, INIT_SQL):
        INIT_SQL.setWindowTitle(QCoreApplication.translate("INIT_SQL", u"SQL\u52a9\u624b\u521d\u59cb\u5316\u5de5\u5177", None))
        self.pushButton_2.setText(QCoreApplication.translate("INIT_SQL", u"\u9009\u62e9\u5e93\u6587\u4ef6", None))
        self.pushButton.setText(QCoreApplication.translate("INIT_SQL", u"\u521d\u59cb\u5316", None))
        self.label.setText(QCoreApplication.translate("INIT_SQL", u"\u521d\u59cb\u5316\u7ea7\u522b", None))
        self.label_2.setText(QCoreApplication.translate("INIT_SQL", u"\u6570\u636e\u6587\u4ef6\u8def\u5f84", None))
    # retranslateUi

