# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'yuanshuju.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1119, 911)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.is_zd = QRadioButton(Form)
        self.is_zd.setObjectName(u"is_zd")

        self.horizontalLayout.addWidget(self.is_zd)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.tb_ysj = QTableView(Form)
        self.tb_ysj.setObjectName(u"tb_ysj")

        self.verticalLayout.addWidget(self.tb_ysj)

        self.tx_yl = QTextBrowser(Form)
        self.tx_yl.setObjectName(u"tx_yl")

        self.verticalLayout.addWidget(self.tx_yl)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u5143\u6570\u636e\u7ba1\u7406", None))
        self.is_zd.setText(QCoreApplication.translate("Form", u"\u662f\u5426\u7f6e\u9876", None))
    # retranslateUi

