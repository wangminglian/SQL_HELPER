# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'create_xq.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QFormLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_create_xq(object):
    def setupUi(self, create_xq):
        if not create_xq.objectName():
            create_xq.setObjectName(u"create_xq")
        create_xq.resize(1004, 780)
        self.verticalLayoutWidget = QWidget(create_xq)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(9, 9, 981, 761))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(15)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label)

        self.lineEdit = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineEdit)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.comboBox = QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName(u"comboBox")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.comboBox)

        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.lineEdit_2 = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lineEdit_2)

        self.label_4 = QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.comboBox_2 = QComboBox(self.verticalLayoutWidget)
        self.comboBox_2.setObjectName(u"comboBox_2")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.comboBox_2)

        self.label_5 = QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.comboBox_3 = QComboBox(self.verticalLayoutWidget)
        self.comboBox_3.setObjectName(u"comboBox_3")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.comboBox_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.formLayout.setItem(8, QFormLayout.ItemRole.FieldRole, self.verticalSpacer)

        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.FieldRole, self.pushButton)

        self.da_start_date = QDateEdit(self.verticalLayoutWidget)
        self.da_start_date.setObjectName(u"da_start_date")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.da_start_date)

        self.label_6 = QLabel(self.verticalLayoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_6)

        self.label_7 = QLabel(self.verticalLayoutWidget)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.label_7)

        self.li_rentian = QLineEdit(self.verticalLayoutWidget)
        self.li_rentian.setObjectName(u"li_rentian")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.li_rentian)

        self.da_end_date = QDateEdit(self.verticalLayoutWidget)
        self.da_end_date.setObjectName(u"da_end_date")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.da_end_date)

        self.label_8 = QLabel(self.verticalLayoutWidget)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.label_8)


        self.verticalLayout.addLayout(self.formLayout)


        self.retranslateUi(create_xq)

        QMetaObject.connectSlotsByName(create_xq)
    # setupUi

    def retranslateUi(self, create_xq):
        create_xq.setWindowTitle(QCoreApplication.translate("create_xq", u"\u521b\u5efa\u9700\u6c42", None))
        self.label.setText(QCoreApplication.translate("create_xq", u"\u9700\u6c42\u540d\u79f0", None))
        self.label_2.setText(QCoreApplication.translate("create_xq", u"\u9700\u6c42\u7c7b\u578b", None))
        self.label_3.setText(QCoreApplication.translate("create_xq", u"\u9700\u6c42\u63d0\u51fa\u4eba", None))
        self.label_4.setText(QCoreApplication.translate("create_xq", u"\u8f93\u5165\u6a21\u7248", None))
        self.label_5.setText(QCoreApplication.translate("create_xq", u"\u8f93\u51fa\u6a21\u7248", None))
        self.pushButton.setText(QCoreApplication.translate("create_xq", u"\u786e\u5b9a", None))
        self.label_6.setText(QCoreApplication.translate("create_xq", u"\u5f00\u59cb\u65f6\u95f4", None))
        self.label_7.setText(QCoreApplication.translate("create_xq", u"\u4eba\u5929", None))
        self.label_8.setText(QCoreApplication.translate("create_xq", u"\u5b8c\u6210\u65f6\u95f4", None))
    # retranslateUi

