# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tupu.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from PySide6.QtWebEngineWidgets import QWebEngineView



class Ui_tupu(object):
    def setupUi(self, tupu):
        if not tupu.objectName():
            tupu.setObjectName(u"tupu")
        tupu.resize(918, 716)
        self.horizontalLayout_2 = QHBoxLayout(tupu)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.li_search = QLineEdit(tupu)
        self.li_search.setObjectName(u"li_search")

        self.verticalLayout_7.addWidget(self.li_search)

        self.line_4 = QFrame(tupu)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_7.addWidget(self.line_4)

        self.web = QWebEngineView(tupu)
        self.web.setObjectName(u"web")
        self.web.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_7.addWidget(self.web)

        self.tx_display = QTextBrowser(tupu)
        self.tx_display.setObjectName(u"tx_display")

        self.verticalLayout_7.addWidget(self.tx_display)

        self.verticalLayout_7.setStretch(0, 1)
        self.verticalLayout_7.setStretch(1, 1)
        self.verticalLayout_7.setStretch(2, 10)
        self.verticalLayout_7.setStretch(3, 1)

        self.horizontalLayout_2.addLayout(self.verticalLayout_7)

        self.line_6 = QFrame(tupu)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.VLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line_6)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(tupu)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.line_7 = QFrame(self.frame)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.HLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_7)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.frame_3)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.line_5 = QFrame(self.frame_3)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_5)

        self.lb_ctl = QLabel(self.frame_3)
        self.lb_ctl.setObjectName(u"lb_ctl")

        self.verticalLayout_2.addWidget(self.lb_ctl)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(2, 9)

        self.verticalLayout_6.addLayout(self.verticalLayout_2)


        self.verticalLayout_3.addWidget(self.frame_3)

        self.line_8 = QFrame(self.frame)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.HLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_8)

        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.line_2 = QFrame(self.frame_2)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_5.addWidget(self.line_2)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.pb_daoru = QPushButton(self.frame_2)
        self.pb_daoru.setObjectName(u"pb_daoru")

        self.verticalLayout_4.addWidget(self.pb_daoru)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)


        self.verticalLayout_3.addWidget(self.frame_2)

        self.verticalLayout_3.setStretch(1, 1)
        self.verticalLayout_3.setStretch(3, 1)

        self.verticalLayout.addWidget(self.frame)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.line_3 = QFrame(tupu)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line_3)

        self.horizontalLayout_2.setStretch(0, 9)
        self.horizontalLayout_2.setStretch(2, 2)

        self.retranslateUi(tupu)

        QMetaObject.connectSlotsByName(tupu)
    # setupUi

    def retranslateUi(self, tupu):
        tupu.setWindowTitle(QCoreApplication.translate("tupu", u"\u77e5\u8bc6\u56fe\u8c31", None))
        self.label.setText(QCoreApplication.translate("tupu", u"\u9009\u62e9\u8be6\u60c5\uff1a", None))
        self.lb_ctl.setText("")
        self.pb_daoru.setText(QCoreApplication.translate("tupu", u"\u6570\u636e\u5bfc\u5165", None))
    # retranslateUi

