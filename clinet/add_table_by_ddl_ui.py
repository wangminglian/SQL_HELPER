# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_table_by_ddl.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_add_table_by_ddl(object):
    def setupUi(self, add_table_by_ddl):
        if not add_table_by_ddl.objectName():
            add_table_by_ddl.setObjectName(u"add_table_by_ddl")
        add_table_by_ddl.setWindowModality(Qt.NonModal)
        add_table_by_ddl.resize(1147, 1000)
        self.verticalLayout_2 = QVBoxLayout(add_table_by_ddl)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_4 = QLabel(add_table_by_ddl)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.li_bz = QLineEdit(add_table_by_ddl)
        self.li_bz.setObjectName(u"li_bz")

        self.horizontalLayout.addWidget(self.li_bz)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label = QLabel(add_table_by_ddl)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.line_4 = QFrame(add_table_by_ddl)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_4)

        self.tx_ddl = QTextEdit(add_table_by_ddl)
        self.tx_ddl.setObjectName(u"tx_ddl")

        self.verticalLayout.addWidget(self.tx_ddl)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(add_table_by_ddl)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.tb_output = QTableView(add_table_by_ddl)
        self.tb_output.setObjectName(u"tb_output")

        self.verticalLayout_3.addWidget(self.tb_output)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.line = QFrame(add_table_by_ddl)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.line_2 = QFrame(add_table_by_ddl)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.label_3 = QLabel(add_table_by_ddl)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout.addWidget(self.label_3)

        self.tx_sqldll = QTextEdit(add_table_by_ddl)
        self.tx_sqldll.setObjectName(u"tx_sqldll")

        self.verticalLayout.addWidget(self.tx_sqldll)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.bt_jiazai = QPushButton(add_table_by_ddl)
        self.bt_jiazai.setObjectName(u"bt_jiazai")

        self.horizontalLayout_2.addWidget(self.bt_jiazai)

        self.bt_yulan = QPushButton(add_table_by_ddl)
        self.bt_yulan.setObjectName(u"bt_yulan")

        self.horizontalLayout_2.addWidget(self.bt_yulan)

        self.bt_submit = QPushButton(add_table_by_ddl)
        self.bt_submit.setObjectName(u"bt_submit")

        self.horizontalLayout_2.addWidget(self.bt_submit)

        self.bt_close = QPushButton(add_table_by_ddl)
        self.bt_close.setObjectName(u"bt_close")

        self.horizontalLayout_2.addWidget(self.bt_close)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        add_table_by_ddl.setStyleSheet("""
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

        self.retranslateUi(add_table_by_ddl)

        QMetaObject.connectSlotsByName(add_table_by_ddl)
    # setupUi

    def retranslateUi(self, add_table_by_ddl):
        add_table_by_ddl.setWindowTitle(QCoreApplication.translate("add_table_by_ddl", u"\u65b0\u589e\u8868", None))
        self.label_4.setText(QCoreApplication.translate("add_table_by_ddl", u"\u5907\u6ce8\uff1a", None))
        self.label.setText(QCoreApplication.translate("add_table_by_ddl", u"\u8bf7\u8f93\u5165\u5efa\u8868\u8bed\u53e5", None))
        self.label_2.setText(QCoreApplication.translate("add_table_by_ddl", u"\u8f93\u51fa\u8868\u9009\u62e9", None))
        self.label_3.setText(QCoreApplication.translate("add_table_by_ddl", u"\u6548\u679c\u9884\u89c8:", None))
        self.bt_jiazai.setText(QCoreApplication.translate("add_table_by_ddl", u"\u52a0\u8f7d", None))
        self.bt_yulan.setText(QCoreApplication.translate("add_table_by_ddl", u"\u9884\u89c8", None))
        self.bt_submit.setText(QCoreApplication.translate("add_table_by_ddl", u"\u4fdd\u5b58", None))
        self.bt_close.setText(QCoreApplication.translate("add_table_by_ddl", u"\u5173\u95ed", None))
    # retranslateUi

