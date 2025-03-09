# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AI_UTL.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_COSMIC_UTL(object):
    def setupUi(self, COSMIC_UTL):
        if not COSMIC_UTL.objectName():
            COSMIC_UTL.setObjectName(u"COSMIC_UTL")
        COSMIC_UTL.resize(1091, 865)
        self.verticalLayout_2 = QVBoxLayout(COSMIC_UTL)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(COSMIC_UTL)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.line_2 = QFrame(COSMIC_UTL)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(COSMIC_UTL)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.li_key = QLineEdit(COSMIC_UTL)
        self.li_key.setObjectName(u"li_key")
        self.li_key.setEchoMode(QLineEdit.Password)

        self.horizontalLayout.addWidget(self.li_key)

        self.label_3 = QLabel(COSMIC_UTL)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.li_mode = QLineEdit(COSMIC_UTL)
        self.li_mode.setObjectName(u"li_mode")

        self.horizontalLayout.addWidget(self.li_mode)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.line_3 = QFrame(COSMIC_UTL)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_5 = QLabel(COSMIC_UTL)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_2.addWidget(self.label_5)

        self.tx_step1 = QTextEdit(COSMIC_UTL)
        self.tx_step1.setObjectName(u"tx_step1")

        self.horizontalLayout_2.addWidget(self.tx_step1)

        self.label_4 = QLabel(COSMIC_UTL)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_2.addWidget(self.label_4)

        self.tx_step2 = QTextEdit(COSMIC_UTL)
        self.tx_step2.setObjectName(u"tx_step2")

        self.horizontalLayout_2.addWidget(self.tx_step2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.line_4 = QFrame(COSMIC_UTL)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pb_input = QPushButton(COSMIC_UTL)
        self.pb_input.setObjectName(u"pb_input")

        self.horizontalLayout_3.addWidget(self.pb_input)

        self.pb_output = QPushButton(COSMIC_UTL)
        self.pb_output.setObjectName(u"pb_output")

        self.horizontalLayout_3.addWidget(self.pb_output)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.line = QFrame(COSMIC_UTL)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line)

        self.label_7 = QLabel(COSMIC_UTL)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_2.addWidget(self.label_7)

        self.pg_jd = QProgressBar(COSMIC_UTL)
        self.pg_jd.setObjectName(u"pg_jd")
        self.pg_jd.setValue(24)

        self.verticalLayout_2.addWidget(self.pg_jd)

        self.label_6 = QLabel(COSMIC_UTL)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_2.addWidget(self.label_6)

        self.tx_log = QTextEdit(COSMIC_UTL)
        self.tx_log.setObjectName(u"tx_log")

        self.verticalLayout_2.addWidget(self.tx_log)


        self.retranslateUi(COSMIC_UTL)

        QMetaObject.connectSlotsByName(COSMIC_UTL)
    # setupUi

    def retranslateUi(self, COSMIC_UTL):
        COSMIC_UTL.setWindowTitle(QCoreApplication.translate("COSMIC_UTL", u"COSMIC_UTL", None))
        self.label.setText(QCoreApplication.translate("COSMIC_UTL", u"\u914d\u7f6e\u4fe1\u606f", None))
        self.label_2.setText(QCoreApplication.translate("COSMIC_UTL", u"api_key", None))
        self.label_3.setText(QCoreApplication.translate("COSMIC_UTL", u"\u6a21\u578b\u540d", None))
        self.label_5.setText(QCoreApplication.translate("COSMIC_UTL", u"\u7b2c\u4e00\u6b65\u95ee\u9898\u6a21\u7248(\u63d0\u95ee)", None))
        self.tx_step1.setHtml(QCoreApplication.translate("COSMIC_UTL", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#ffffff;\"><span style=\" font-family:'Courier New'; font-size:9.8pt; color:#183691;\">\u4f60\u662f\u5199</span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#183691;\">COSMIC</span><span style=\" font-family:'Courier New'; font-size:9.8pt; color:#183691;\">\u7684\u4e13\u5bb6\uff0c\u5e2e\u6211\u5199</span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#183691;\">COSMIC,</span><span style=\" font-family:'Courier New'; font-size:9.8pt; color:#183691;\">\u529f\u80fd\u8fc7\u7a0b\u662f</"
                        "span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#183691;\">:&quot;{</span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#0086b3;\">gnd</span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#183691;\">}&quot;,</span><span style=\" font-family:'Courier New'; font-size:9.8pt; color:#183691;\">\u6839\u636e\u6211\u7ed9\u5b9a\u7684\u529f\u80fd\u8fc7\u7a0b\uff0c\u62c6\u5206\u51fa\u56db\u4e2a\u5b50\u8fc7\u7a0b\u63cf\u8ff0\uff0c\u5e76\u751f\u6210\u5bf9\u5e94\u7684\u6570\u636e\u7ec4\u548c\u6570\u636e\u5c5e\u6027\uff0c\u8981\u6c42\u6570\u636e\u5c5e\u6027\u6709</span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#183691;\">3</span><span style=\" font-family:'Courier New'; font-size:9.8pt; color:#183691;\">\u4e2a\uff0c\u4e14\u4e0d\u53ef\u91cd\u590d\uff0c\u6570\u636e\u7ec4\u6587\u5b57\u4e0d\u53ef\u91cd\u590d\u3002\u5e76\u4ee5\u5982\u4e0b\u683c\u5f0f\u8f93\u51fa</span><span style=\" font-fa"
                        "mily:'JetBrains Mono','monospace'; font-size:9.8pt; color:#183691;\">:</span><span style=\" font-family:'Courier New'; font-size:9.8pt; color:#183691;\">\u5b50\u8fc7\u7a0b\u63cf\u8ff0</span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#183691;\">|</span><span style=\" font-family:'Courier New'; font-size:9.8pt; color:#183691;\">\u6570\u636e\u7ec4</span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#183691;\">|</span><span style=\" font-family:'Courier New'; font-size:9.8pt; color:#183691;\">\u6570\u636e\u5c5e\u6027</span></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("COSMIC_UTL", u"\u7b2c\u4e8c\u6b65\u95ee\u9898\u6a21\u7248\uff08\u89c4\u6574\uff09", None))
        self.tx_step2.setHtml(QCoreApplication.translate("COSMIC_UTL", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#ffffff;\"><span style=\" font-family:'Courier New'; font-size:9.8pt; color:#183691;\">\u4ece\u6211\u7ed9\u5b9a\u7684\u6587\u672c\u4e2d\u63d0\u53d6</span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#183691;\">:</span><span style=\" font-family:'Courier New'; font-size:9.8pt; color:#183691;\">\u5b50\u8fc7\u7a0b\u3001\u6570\u636e\u7ec4\u3001\u6570\u636e\u5c5e\u6027</span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#183691;\">,</span><span style=\" font-family:'Courier New'; font-"
                        "size:9.8pt; color:#183691;\">\u5c06\u76f8\u540c\u5b57\u8fc7\u7a0b\u7684\u5185\u5bb9\u8f93\u51fa\u5230\u4e00\u884c\u8f93\u51fa\uff0c\u6587\u672c\u5185\u5bb9</span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#183691;\">{</span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#333333;\">a</span><span style=\" font-family:'JetBrains Mono','monospace'; font-size:9.8pt; color:#183691;\">}</span></p></body></html>", None))
        self.pb_input.setText(QCoreApplication.translate("COSMIC_UTL", u"\u5bfc\u5165\u6587\u4ef6", None))
        self.pb_output.setText(QCoreApplication.translate("COSMIC_UTL", u"\u4fdd\u5b58", None))
        self.label_7.setText(QCoreApplication.translate("COSMIC_UTL", u"\u67e5\u8be2\u8fdb\u5ea6", None))
        self.label_6.setText(QCoreApplication.translate("COSMIC_UTL", u"\u65e5\u5fd7\uff1a", None))
    # retranslateUi

