# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NodeDriver.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_NodeDriver(object):
    def setupUi(self, NodeDriver):
        if not NodeDriver.objectName():
            NodeDriver.setObjectName(u"NodeDriver")
        NodeDriver.resize(959, 811)
        self.verticalLayout_2 = QVBoxLayout(NodeDriver)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pb_create_func = QPushButton(NodeDriver)
        self.pb_create_func.setObjectName(u"pb_create_func")

        self.horizontalLayout.addWidget(self.pb_create_func)

        self.pb_create_node = QPushButton(NodeDriver)
        self.pb_create_node.setObjectName(u"pb_create_node")

        self.horizontalLayout.addWidget(self.pb_create_node)

        self.pb_open_file = QPushButton(NodeDriver)
        self.pb_open_file.setObjectName(u"pb_open_file")

        self.horizontalLayout.addWidget(self.pb_open_file)

        self.pb_save = QPushButton(NodeDriver)
        self.pb_save.setObjectName(u"pb_save")

        self.horizontalLayout.addWidget(self.pb_save)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.wi_node_display = QWidget(NodeDriver)
        self.wi_node_display.setObjectName(u"wi_node_display")

        self.verticalLayout.addWidget(self.wi_node_display)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 7)

        self.retranslateUi(NodeDriver)

        QMetaObject.connectSlotsByName(NodeDriver)
    # setupUi

    def retranslateUi(self, NodeDriver):
        NodeDriver.setWindowTitle(QCoreApplication.translate("NodeDriver", u"Form", None))
        self.pb_create_func.setText(QCoreApplication.translate("NodeDriver", u"\u521b\u5efa\u51fd\u6570", None))
        self.pb_create_node.setText(QCoreApplication.translate("NodeDriver", u"\u521b\u5efa\u8282\u70b9", None))
        self.pb_open_file.setText(QCoreApplication.translate("NodeDriver", u"\u6253\u5f00", None))
        self.pb_save.setText(QCoreApplication.translate("NodeDriver", u"\u4fdd\u5b58", None))
    # retranslateUi

