# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'create_xq.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_create_xq(object):
    def setupUi(self, create_xq):
        if not create_xq.objectName():
            create_xq.setObjectName(u"create_xq")
        create_xq.resize(1004, 780)
        self.verticalLayoutWidget = QWidget(create_xq)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(9, 9, 981, 761))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(15)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.comboBox = QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName(u"comboBox")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboBox)

        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.lineEdit_2 = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.lineEdit_2)

        self.label_4 = QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.comboBox_2 = QComboBox(self.verticalLayoutWidget)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.comboBox_2)

        self.label_5 = QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.comboBox_3 = QComboBox(self.verticalLayoutWidget)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.comboBox_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout.setItem(5, QFormLayout.FieldRole, self.verticalSpacer)

        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.pushButton)

        self.lineEdit = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit)


        self.verticalLayout.addLayout(self.formLayout)


        self.retranslateUi(create_xq)

        QMetaObject.connectSlotsByName(create_xq)
    # setupUi

    def retranslateUi(self, create_xq):
        create_xq.setWindowTitle(QCoreApplication.translate("create_xq", u"\u521b\u5efa\u9700\u6c42", None))
        self.label.setText(QCoreApplication.translate("create_xq", u"\u9700\u6c42\u540d\u79f0", None))
        self.label_2.setText(QCoreApplication.translate("create_xq", u"\u9700\u6c42\u7c7b\u578b", None))
        self.label_3.setText(QCoreApplication.translate("create_xq", u"\u9700\u6c42\u63d0\u51fa\u4eba", None))
        self.label_4.setText(QCoreApplication.translate("create_xq", u"\u8f93\u5165\u6a21\u7248", None))
        self.label_5.setText(QCoreApplication.translate("create_xq", u"\u8f93\u51fa\u6a21\u7248", None))
        self.pushButton.setText(QCoreApplication.translate("create_xq", u"\u786e\u5b9a", None))
    # retranslateUi

