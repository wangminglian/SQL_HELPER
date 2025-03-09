# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'NodeEditer.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_NodeEditer(object):
    def setupUi(self, NodeEditer):
        if not NodeEditer.objectName():
            NodeEditer.setObjectName(u"NodeEditer")
        NodeEditer.resize(1426, 951)
        self.verticalLayout = QVBoxLayout(NodeEditer)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.wi_p0 = QWidget(NodeEditer)
        self.wi_p0.setObjectName(u"wi_p0")
        self.horizontalLayout = QHBoxLayout(self.wi_p0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.wi_p1 = QWidget(self.wi_p0)
        self.wi_p1.setObjectName(u"wi_p1")
        self.verticalLayout_2 = QVBoxLayout(self.wi_p1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.wi_p1)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pb_add_node = QPushButton(self.wi_p1)
        self.pb_add_node.setObjectName(u"pb_add_node")

        self.horizontalLayout_2.addWidget(self.pb_add_node)

        self.pb_remove_node = QPushButton(self.wi_p1)
        self.pb_remove_node.setObjectName(u"pb_remove_node")

        self.horizontalLayout_2.addWidget(self.pb_remove_node)

        self.pb_modify_node = QPushButton(self.wi_p1)
        self.pb_modify_node.setObjectName(u"pb_modify_node")

        self.horizontalLayout_2.addWidget(self.pb_modify_node)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.li_search_node = QLineEdit(self.wi_p1)
        self.li_search_node.setObjectName(u"li_search_node")

        self.verticalLayout_2.addWidget(self.li_search_node)

        self.tb_n1 = QTableView(self.wi_p1)
        self.tb_n1.setObjectName(u"tb_n1")

        self.verticalLayout_2.addWidget(self.tb_n1)

        self.line = QFrame(self.wi_p1)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.label_3 = QLabel(self.wi_p1)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pb_add_port = QPushButton(self.wi_p1)
        self.pb_add_port.setObjectName(u"pb_add_port")

        self.horizontalLayout_3.addWidget(self.pb_add_port)

        self.pb_remove_port = QPushButton(self.wi_p1)
        self.pb_remove_port.setObjectName(u"pb_remove_port")

        self.horizontalLayout_3.addWidget(self.pb_remove_port)

        self.pb_modify_port = QPushButton(self.wi_p1)
        self.pb_modify_port.setObjectName(u"pb_modify_port")

        self.horizontalLayout_3.addWidget(self.pb_modify_port)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.li_search_func = QLineEdit(self.wi_p1)
        self.li_search_func.setObjectName(u"li_search_func")

        self.verticalLayout_2.addWidget(self.li_search_func)

        self.tb_n2 = QTableView(self.wi_p1)
        self.tb_n2.setObjectName(u"tb_n2")

        self.verticalLayout_2.addWidget(self.tb_n2)

        self.line_3 = QFrame(self.wi_p1)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_3)

        self.label_4 = QLabel(self.wi_p1)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.wi_func = QWidget(self.wi_p1)
        self.wi_func.setObjectName(u"wi_func")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wi_func.sizePolicy().hasHeightForWidth())
        self.wi_func.setSizePolicy(sizePolicy)
        self.wi_func.setMinimumSize(QSize(0, 90))

        self.verticalLayout_2.addWidget(self.wi_func)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pb_init_func = QPushButton(self.wi_p1)
        self.pb_init_func.setObjectName(u"pb_init_func")

        self.horizontalLayout_4.addWidget(self.pb_init_func)

        self.pb_run = QPushButton(self.wi_p1)
        self.pb_run.setObjectName(u"pb_run")

        self.horizontalLayout_4.addWidget(self.pb_run)

        self.pb_save = QPushButton(self.wi_p1)
        self.pb_save.setObjectName(u"pb_save")

        self.horizontalLayout_4.addWidget(self.pb_save)

        self.pb_release = QPushButton(self.wi_p1)
        self.pb_release.setObjectName(u"pb_release")

        self.horizontalLayout_4.addWidget(self.pb_release)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)


        self.horizontalLayout.addWidget(self.wi_p1)

        self.line_2 = QFrame(self.wi_p0)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.wi_p2 = QWidget(self.wi_p0)
        self.wi_p2.setObjectName(u"wi_p2")
        self.verticalLayout_4 = QVBoxLayout(self.wi_p2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_5 = QLabel(self.wi_p2)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_4.addWidget(self.label_5)

        self.li_search_gnode = QLineEdit(self.wi_p2)
        self.li_search_gnode.setObjectName(u"li_search_gnode")

        self.verticalLayout_4.addWidget(self.li_search_gnode)

        self.tr_nodes = QTreeWidget(self.wi_p2)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.tr_nodes.setHeaderItem(__qtreewidgetitem)
        self.tr_nodes.setObjectName(u"tr_nodes")

        self.verticalLayout_4.addWidget(self.tr_nodes)


        self.horizontalLayout.addWidget(self.wi_p2)

        self.line_4 = QFrame(self.wi_p0)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.VLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.wi_p3 = QWidget(self.wi_p0)
        self.wi_p3.setObjectName(u"wi_p3")
        self.verticalLayout_3 = QVBoxLayout(self.wi_p3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(self.wi_p3)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.wi_display = QWidget(self.wi_p3)
        self.wi_display.setObjectName(u"wi_display")

        self.verticalLayout_3.addWidget(self.wi_display)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 99)

        self.horizontalLayout.addWidget(self.wi_p3)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(4, 5)

        self.verticalLayout.addWidget(self.wi_p0)


        self.retranslateUi(NodeEditer)

        QMetaObject.connectSlotsByName(NodeEditer)
    # setupUi

    def retranslateUi(self, NodeEditer):
        NodeEditer.setWindowTitle(QCoreApplication.translate("NodeEditer", u"\u8282\u70b9\u7f16\u8f91\u5668", None))
        self.label_2.setText(QCoreApplication.translate("NodeEditer", u"\u8282\u70b9\u914d\u7f6e", None))
        self.pb_add_node.setText(QCoreApplication.translate("NodeEditer", u"\u65b0\u5efa", None))
        self.pb_remove_node.setText(QCoreApplication.translate("NodeEditer", u"\u5220\u9664", None))
        self.pb_modify_node.setText(QCoreApplication.translate("NodeEditer", u"\u53d8\u66f4", None))
        self.label_3.setText(QCoreApplication.translate("NodeEditer", u"\u5f15\u811a\u914d\u7f6e", None))
        self.pb_add_port.setText(QCoreApplication.translate("NodeEditer", u"\u65b0\u5efa", None))
        self.pb_remove_port.setText(QCoreApplication.translate("NodeEditer", u"\u5220\u9664", None))
        self.pb_modify_port.setText(QCoreApplication.translate("NodeEditer", u"\u53d8\u66f4", None))
        self.label_4.setText(QCoreApplication.translate("NodeEditer", u"\u6267\u884c\u51fd\u6570", None))
        self.pb_init_func.setText(QCoreApplication.translate("NodeEditer", u"\u751f\u6210\u51fd\u6570\u5934", None))
        self.pb_run.setText(QCoreApplication.translate("NodeEditer", u"\u8fd0\u884c", None))
        self.pb_save.setText(QCoreApplication.translate("NodeEditer", u"\u4fdd\u5b58", None))
        self.pb_release.setText(QCoreApplication.translate("NodeEditer", u"\u53d1\u5e03", None))
        self.label_5.setText(QCoreApplication.translate("NodeEditer", u"\u8282\u70b9\u9009\u62e9", None))
        self.label.setText(QCoreApplication.translate("NodeEditer", u"\u8282\u70b9\u7f16\u8f91\u5668", None))
    # retranslateUi

