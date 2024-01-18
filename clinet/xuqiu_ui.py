# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'xuqiu.ui'
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
        Form.setEnabled(True)
        Form.resize(1282, 936)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.com_sear_type = QComboBox(Form)
        self.com_sear_type.setObjectName(u"com_sear_type")

        self.horizontalLayout.addWidget(self.com_sear_type)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.is_zd = QCheckBox(Form)
        self.is_zd.setObjectName(u"is_zd")

        self.horizontalLayout.addWidget(self.is_zd)

        self.bt_cjjs = QPushButton(Form)
        self.bt_cjjs.setObjectName(u"bt_cjjs")
        self.bt_cjjs.setText('超级检索')

        self.horizontalLayout.addWidget(self.bt_cjjs)

        self.bt_rename = QPushButton(Form)
        self.bt_rename.setObjectName(u"bt_rename")

        self.horizontalLayout.addWidget(self.bt_rename)

        self.bt_create = QPushButton(Form)
        self.bt_create.setObjectName(u"bt_create")

        self.horizontalLayout.addWidget(self.bt_create)

        self.bt_remove = QPushButton(Form)
        self.bt_remove.setObjectName(u"bt_remove")

        self.horizontalLayout.addWidget(self.bt_remove)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line_2 = QFrame(Form)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.tb_xuqiu = QTableView(Form)
        self.tb_xuqiu.setObjectName(u"tb_xuqiu")

        self.verticalLayout.addWidget(self.tb_xuqiu)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.ra_banben = QRadioButton(Form)
        self.ra_banben.setObjectName(u"ra_banben")

        self.horizontalLayout_2.addWidget(self.ra_banben)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.li_search_wd = QLineEdit(Form)
        self.li_search_wd.setObjectName(u"li_search_wd")

        self.horizontalLayout_2.addWidget(self.li_search_wd)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_2.addWidget(self.label_3)

        self.com_type = QComboBox(Form)
        self.com_type.setObjectName(u"com_type")

        self.horizontalLayout_2.addWidget(self.com_type)

        self.bt_daoru = QPushButton(Form)
        self.bt_daoru.setObjectName(u"bt_daoru")

        self.horizontalLayout_2.addWidget(self.bt_daoru)

        self.bt_xqzt = QPushButton(Form)
        self.bt_xqzt.setObjectName(u"bt_xqzt")

        self.horizontalLayout_2.addWidget(self.bt_xqzt)

        self.submit_jiaoben = QPushButton(Form)
        self.submit_jiaoben.setObjectName(u"submit_jiaoben")

        self.horizontalLayout_2.addWidget(self.submit_jiaoben)

        self.new_jiaoben = QPushButton(Form)
        self.new_jiaoben.setObjectName(u"new_jiaoben")

        self.horizontalLayout_2.addWidget(self.new_jiaoben)

        self.bt_rm_jb = QPushButton(Form)
        self.bt_rm_jb.setObjectName(u"bt_rm_jb")

        self.horizontalLayout_2.addWidget(self.bt_rm_jb)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.line = QFrame(Form)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.tb_xuqiudtl = QTableView(Form)
        self.tb_xuqiudtl.setObjectName(u"tb_xuqiudtl")

        self.verticalLayout.addWidget(self.tb_xuqiudtl)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u9700\u6c42\u7ba1\u7406", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u72b6\u6001", None))
        self.is_zd.setText(QCoreApplication.translate("Form", u"\u7f6e\u9876", None))
        self.bt_rename.setText(QCoreApplication.translate("Form", u"\u4fee\u6539", None))
        self.bt_create.setText(QCoreApplication.translate("Form", u"\u521b\u5efa", None))
        self.bt_remove.setText(QCoreApplication.translate("Form", u"\u5220\u9664", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u9700\u6c42\u5217\u8868", None))
        self.ra_banben.setText(QCoreApplication.translate("Form", u"\u663e\u793a\u5386\u53f2\u7248\u672c", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u6587\u4ef6\u7c7b\u578b", None))
        self.bt_daoru.setText(QCoreApplication.translate("Form", u"\u5bfc\u5165\u6587\u6863", None))
        self.bt_xqzt.setText(QCoreApplication.translate("Form", u"\u4efb\u52a1\u72b6\u6001\u53d8\u66f4", None))
        self.submit_jiaoben.setText(QCoreApplication.translate("Form", u"\u63d0\u4ea4\u7248\u672c", None))
        self.new_jiaoben.setText(QCoreApplication.translate("Form", u"\u65b0\u5efa\u811a\u672c", None))
        self.bt_rm_jb.setText(QCoreApplication.translate("Form", u"\u5220\u9664", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u9700\u6c42\u8be6\u60c5", None))
    # retranslateUi

