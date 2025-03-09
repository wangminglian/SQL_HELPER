# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tupu_select_node.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_Tupu_select_node(object):
    def setupUi(self, Tupu_select_node):
        if not Tupu_select_node.objectName():
            Tupu_select_node.setObjectName(u"Tupu_select_node")
        Tupu_select_node.resize(775, 599)
        self.verticalLayout_2 = QVBoxLayout(Tupu_select_node)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(Tupu_select_node)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lb_lx = QLabel(self.widget)
        self.lb_lx.setObjectName(u"lb_lx")

        self.horizontalLayout.addWidget(self.lb_lx)

        self.li_lx = QLineEdit(self.widget)
        self.li_lx.setObjectName(u"li_lx")

        self.horizontalLayout.addWidget(self.li_lx)

        self.lb_gjz = QLabel(self.widget)
        self.lb_gjz.setObjectName(u"lb_gjz")

        self.horizontalLayout.addWidget(self.lb_gjz)

        self.li_gjz = QLineEdit(self.widget)
        self.li_gjz.setObjectName(u"li_gjz")

        self.horizontalLayout.addWidget(self.li_gjz)

        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(3, 5)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.widget)

        self.label = QLabel(Tupu_select_node)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.line = QFrame(Tupu_select_node)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.tb_nodes = QTableView(Tupu_select_node)
        self.tb_nodes.setObjectName(u"tb_nodes")

        self.verticalLayout.addWidget(self.tb_nodes)

        self.line_2 = QFrame(Tupu_select_node)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.widget_2 = QWidget(Tupu_select_node)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pb_quxiao = QPushButton(self.widget_2)
        self.pb_quxiao.setObjectName(u"pb_quxiao")

        self.horizontalLayout_4.addWidget(self.pb_quxiao)

        self.pb_queding = QPushButton(self.widget_2)
        self.pb_queding.setObjectName(u"pb_queding")

        self.horizontalLayout_4.addWidget(self.pb_queding)


        self.verticalLayout.addWidget(self.widget_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Tupu_select_node)

        QMetaObject.connectSlotsByName(Tupu_select_node)
    # setupUi

    def retranslateUi(self, Tupu_select_node):
        Tupu_select_node.setWindowTitle(QCoreApplication.translate("Tupu_select_node", u"选择节点", None))
        self.lb_lx.setText(QCoreApplication.translate("Tupu_select_node", u"\u7c7b\u578b:", None))
        self.lb_gjz.setText(QCoreApplication.translate("Tupu_select_node", u"\u5173\u952e\u5b57:", None))
        self.label.setText(QCoreApplication.translate("Tupu_select_node", u"\u8282\u70b9\u5217\u8868", None))
        self.pb_quxiao.setText(QCoreApplication.translate("Tupu_select_node", u"\u53d6\u6d88", None))
        self.pb_queding.setText(QCoreApplication.translate("Tupu_select_node", u"\u786e\u5b9a", None))
    # retranslateUi

