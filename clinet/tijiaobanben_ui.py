# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tijiaobanben.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_submit_banben(object):
    def setupUi(self, submit_banben):
        if not submit_banben.objectName():
            submit_banben.setObjectName(u"submit_banben")
        submit_banben.setWindowModality(Qt.NonModal)
        submit_banben.resize(1147, 999)
        self.verticalLayout_2 = QVBoxLayout(submit_banben)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_4 = QLabel(submit_banben)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.li_bz = QLineEdit(submit_banben)
        self.li_bz.setObjectName(u"li_bz")

        self.horizontalLayout.addWidget(self.li_bz)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label = QLabel(submit_banben)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.tb_input = QTableView(submit_banben)
        self.tb_input.setObjectName(u"tb_input")
        self.tb_input.setAlternatingRowColors(True)
        self.tb_input.setStyleSheet("gridline-color: #ccc;")
        self.tb_input.horizontalHeader().setStretchLastSection(True)
        self.tb_input.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tb_input.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.verticalLayout.addWidget(self.tb_input)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(submit_banben)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.tb_output = QTableView(submit_banben)
        self.tb_output.setObjectName(u"tb_output")
        self.tb_output.setAlternatingRowColors(True)
        self.tb_output.setStyleSheet("gridline-color: #ccc;")
        self.tb_output.horizontalHeader().setStretchLastSection(True)
        self.tb_output.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tb_output.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.verticalLayout_3.addWidget(self.tb_output)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.line_3 = QFrame(submit_banben)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_3.addWidget(self.line_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_5 = QLabel(submit_banben)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_4.addWidget(self.label_5)

        self.tb_koujing = QTableView(submit_banben)
        self.tb_koujing.setObjectName(u"tb_koujing")
        self.tb_koujing.setAlternatingRowColors(True)
        self.tb_koujing.setStyleSheet("gridline-color: #ccc;")
        self.tb_koujing.horizontalHeader().setStretchLastSection(True)
        self.tb_koujing.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tb_koujing.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.verticalLayout_4.addWidget(self.tb_koujing)


        self.horizontalLayout_3.addLayout(self.verticalLayout_4)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.line = QFrame(submit_banben)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.line_2 = QFrame(submit_banben)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.label_3 = QLabel(submit_banben)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.tx_sqldll = QTextEdit(submit_banben)
        self.tx_sqldll.setObjectName(u"tx_sqldll")

        self.verticalLayout.addWidget(self.tx_sqldll)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.bt_cxjz = QPushButton(submit_banben)
        self.bt_cxjz.setObjectName(u"bt_cxjz")

        self.horizontalLayout_2.addWidget(self.bt_cxjz)

        self.bt_yulan = QPushButton(submit_banben)
        self.bt_yulan.setObjectName(u"bt_yulan")

        self.horizontalLayout_2.addWidget(self.bt_yulan)

        self.bt_submit = QPushButton(submit_banben)
        self.bt_submit.setObjectName(u"bt_submit")

        self.horizontalLayout_2.addWidget(self.bt_submit)

        self.bt_close = QPushButton(submit_banben)
        self.bt_close.setObjectName(u"bt_close")

        self.horizontalLayout_2.addWidget(self.bt_close)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        submit_banben.setStyleSheet("""
            QWidget {
                background-color: #e0f7fa;
                color: #333;
            }
            QPushButton {
                background-color: #0288d1;
                color: white;
                border: none;
                padding: 5px 10px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
            }
            QPushButton:hover {
                background-color: white;
                color: black;
                border: 2px solid #0288d1;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QLineEdit, QComboBox {
                background-color: white;
                color: #333;
                border: 1px solid #ccc;
                padding: 5px;
            }
            QTextEdit, QTextBrowser {
                background-color: white;
                color: #333;
                border: 1px solid #ccc;
            }
        """)

        self.retranslateUi(submit_banben)

        QMetaObject.connectSlotsByName(submit_banben)
    # setupUi

    def retranslateUi(self, submit_banben):
        submit_banben.setWindowTitle(QCoreApplication.translate("submit_banben", u"\u63d0\u4ea4\u7248\u672c", None))
        self.label_4.setText(QCoreApplication.translate("submit_banben", u"\u5907\u6ce8\uff1a", None))
        self.label.setText(QCoreApplication.translate("submit_banben", u"\u8f93\u5165\u8868\u9009\u62e9", None))
        self.label_2.setText(QCoreApplication.translate("submit_banben", u"\u8f93\u51fa\u8868\u9009\u62e9", None))
        self.label_5.setText(QCoreApplication.translate("submit_banben", u"\u53e3\u5f84\u9009\u62e9", None))
        self.label_3.setText(QCoreApplication.translate("submit_banben", u"\u6548\u679c\u9884\u89c8:", None))
        self.bt_cxjz.setText(QCoreApplication.translate("submit_banben", u"\u91cd\u65b0\u52a0\u8f7d", None))
        self.bt_yulan.setText(QCoreApplication.translate("submit_banben", u"\u9884\u89c8", None))
        self.bt_submit.setText(QCoreApplication.translate("submit_banben", u"\u4fdd\u5b58", None))
        self.bt_close.setText(QCoreApplication.translate("submit_banben", u"\u5173\u95ed", None))
    # retranslateUi

