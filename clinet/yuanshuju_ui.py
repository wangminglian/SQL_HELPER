# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'yuanshuju.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form,name):
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

        # 设置与main_ui.py一致的样式表
        Form.setStyleSheet("""
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

        # 调整布局间距
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setSpacing(10)
        self.horizontalLayout.setSpacing(10)

        # 优化QTableView显示效果
        self.tb_ysj.setAlternatingRowColors(True)
        self.tb_ysj.setStyleSheet(u""
            "QTableView {"
            "    gridline-color: #d3d3d3;"
            "    selection-background-color: #b0e0e6;"
            "    alternate-background-color: #f0f8ff;"
            "}"
            "QHeaderView::section {"
            "    background-color: #e0f7fa;"
            "    padding: 4px;"
            "    border: 1px solid #ccc;"
            "    font-size: 14px;"
            "    font-weight: bold;"
            "}"
        )
        self.tb_ysj.horizontalHeader().setStretchLastSection(True)
        self.tb_ysj.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tb_ysj.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_ysj.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tb_ysj.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # 进一步优化QTableView横向显示效果
        self.tb_ysj.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.tb_ysj.horizontalHeader().setStretchLastSection(False)
        self.tb_ysj.setShowGrid(True)
        self.tb_ysj.setWordWrap(False)
        self.tb_ysj.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tb_ysj.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tb_ysj.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tb_ysj.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.tb_ysj.setCornerButtonEnabled(False)

        self.retranslateUi(Form,name)

        QMetaObject.connectSlotsByName(Form)


    # setupUi

    def retranslateUi(self, Form,name):
        Form.setWindowTitle(QCoreApplication.translate("Form", name, None))
        self.is_zd.setText(QCoreApplication.translate("Form", u"\u662f\u5426\u7f6e\u9876", None))
    # retranslateUi

