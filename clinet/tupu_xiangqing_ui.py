# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tupu_xiangqing.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
class CustomTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFocusPolicy(Qt.StrongFocus)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab and self.currentRow() == self.rowCount() - 1:
            self.insertRow(self.rowCount())
            self.setCurrentCell(self.rowCount() - 1, 0)
        else:
            super().keyPressEvent(event)

class Ui_tupu_xiangqing(object):
    def setupUi(self, tupu_xiangqing):
        if not tupu_xiangqing.objectName():
            tupu_xiangqing.setObjectName(u"tupu_xiangqing")
        tupu_xiangqing.resize(736, 659)
        self.verticalLayout_2 = QVBoxLayout(tupu_xiangqing)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_7 = QLabel(tupu_xiangqing)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout.addWidget(self.label_7)

        self.line_2 = QFrame(tupu_xiangqing)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setRowWrapPolicy(QFormLayout.WrapLongRows)
        self.formLayout.setContentsMargins(1, 1, -1, -1)
        self.lb_id = QLabel(tupu_xiangqing)
        self.lb_id.setObjectName(u"lb_id")
        self.lb_id.setMinimumSize(QSize(80, 0))
        self.lb_id.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lb_id)

        self.li_id = QLineEdit(tupu_xiangqing)
        self.li_id.setObjectName(u"li_id")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.li_id)

        self.lb_lx = QLabel(tupu_xiangqing)
        self.lb_lx.setObjectName(u"lb_lx")
        self.lb_lx.setMinimumSize(QSize(80, 0))
        self.lb_lx.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.lb_lx)

        self.li_lx = QLineEdit(tupu_xiangqing)
        self.li_lx.setObjectName(u"li_lx")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.li_lx)

        self.lb_name = QLabel(tupu_xiangqing)
        self.lb_name.setObjectName(u"lb_name")
        self.lb_name.setMinimumSize(QSize(80, 0))
        self.lb_name.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.lb_name)

        self.li_name = QLineEdit(tupu_xiangqing)
        self.li_name.setObjectName(u"li_name")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.li_name)

        self.lb_start = QLabel(tupu_xiangqing)
        self.lb_start.setObjectName(u"lb_start")
        self.lb_start.setMinimumSize(QSize(80, 0))
        self.lb_start.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.lb_start)

        self.li_start = QLineEdit(tupu_xiangqing)
        self.li_start.setObjectName(u"li_start")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.li_start)

        self.lb_end = QLabel(tupu_xiangqing)
        self.lb_end.setObjectName(u"lb_end")
        self.lb_end.setMinimumSize(QSize(80, 0))
        self.lb_end.setAlignment(Qt.AlignCenter)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.lb_end)

        self.li_end = QLineEdit(tupu_xiangqing)
        self.li_end.setObjectName(u"li_end")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.li_end)


        self.verticalLayout.addLayout(self.formLayout)

        self.label_6 = QLabel(tupu_xiangqing)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout.addWidget(self.label_6)

        self.line_3 = QFrame(tupu_xiangqing)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.line_3)

        self.tb_zdy = CustomTableWidget(tupu_xiangqing)
        if (self.tb_zdy.columnCount() < 2):
            self.tb_zdy.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tb_zdy.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tb_zdy.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        if (self.tb_zdy.rowCount() < 10):
            self.tb_zdy.setRowCount(10)
        self.tb_zdy.setObjectName(u"tb_zdy")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_zdy.sizePolicy().hasHeightForWidth())
        self.tb_zdy.setSizePolicy(sizePolicy)
        self.tb_zdy.setAlternatingRowColors(True)
        self.tb_zdy.setRowCount(10)
        self.tb_zdy.horizontalHeader().setVisible(True)
        self.tb_zdy.horizontalHeader().setCascadingSectionResizes(False)
        self.tb_zdy.horizontalHeader().setHighlightSections(True)
        self.tb_zdy.horizontalHeader().setProperty("showSortIndicator", False)
        self.tb_zdy.horizontalHeader().setStretchLastSection(True)

        self.verticalLayout.addWidget(self.tb_zdy)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_2 = QPushButton(tupu_xiangqing)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(tupu_xiangqing)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout.setStretch(2, 3)
        self.verticalLayout.setStretch(5, 9)

        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(tupu_xiangqing)

        QMetaObject.connectSlotsByName(tupu_xiangqing)
    # setupUi

    def retranslateUi(self, tupu_xiangqing):
        tupu_xiangqing.setWindowTitle(QCoreApplication.translate("tupu_xiangqing", u"\u7f16\u8f91", None))
        self.label_7.setText(QCoreApplication.translate("tupu_xiangqing", u"\u56fa\u6709\u5c5e\u6027", None))
        self.lb_id.setText(QCoreApplication.translate("tupu_xiangqing", u" id", None))
        self.lb_lx.setText(QCoreApplication.translate("tupu_xiangqing", u"\u7c7b\u578b", None))
        self.lb_name.setText(QCoreApplication.translate("tupu_xiangqing", u"\u540d\u79f0", None))
        self.lb_start.setText(QCoreApplication.translate("tupu_xiangqing", u"\u5f00\u59cb\u8282\u70b9", None))
        self.lb_end.setText(QCoreApplication.translate("tupu_xiangqing", u"\u7ed3\u675f\u8282\u70b9", None))
        self.label_6.setText(QCoreApplication.translate("tupu_xiangqing", u"\u81ea\u5b9a\u4e49\u5c5e\u6027", None))
        ___qtablewidgetitem = self.tb_zdy.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("tupu_xiangqing", u"\u5c5e\u6027\u540d\u79f0", None));
        ___qtablewidgetitem1 = self.tb_zdy.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("tupu_xiangqing", u"\u5c5e\u6027\u503c", None));
        self.pushButton_2.setText(QCoreApplication.translate("tupu_xiangqing", u"\u9000\u51fa", None))
        self.pushButton.setText(QCoreApplication.translate("tupu_xiangqing", u"\u786e\u5b9a", None))
    # retranslateUi

