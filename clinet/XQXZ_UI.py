# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'XQXZ.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_XQXZ(object):
    def setupUi(self, XQXZ):
        if not XQXZ.objectName():
            XQXZ.setObjectName(u"XQXZ")
        XQXZ.resize(400, 146)
        self.verticalLayout_2 = QVBoxLayout(XQXZ)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(XQXZ)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.li_input = QLineEdit(XQXZ)
        self.li_input.setObjectName(u"li_input")

        self.horizontalLayout.addWidget(self.li_input)

        self.com_input = QComboBox(XQXZ)
        self.com_input.setObjectName(u"com_input")

        self.horizontalLayout.addWidget(self.com_input)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.pb_submit = QPushButton(XQXZ)
        self.pb_submit.setObjectName(u"pb_submit")

        self.verticalLayout.addWidget(self.pb_submit)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(XQXZ)

        QMetaObject.connectSlotsByName(XQXZ)
    # setupUi

    def retranslateUi(self, XQXZ):
        XQXZ.setWindowTitle(QCoreApplication.translate("XQXZ", u"\u9700\u6c42\u9009\u62e9", None))
        self.label.setText(QCoreApplication.translate("XQXZ", u"\u9009\u62e9\u9700\u6c42", None))
        self.pb_submit.setText(QCoreApplication.translate("XQXZ", u"\u786e\u5b9a", None))
    # retranslateUi

