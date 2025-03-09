# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TBSQL_TAB.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QTabWidget, QTableView, QVBoxLayout, QWidget)

class Ui_TBSQL_TAB_UI(object):
    def setupUi(self, TBSQL_TAB_UI):
        if not TBSQL_TAB_UI.objectName():
            TBSQL_TAB_UI.setObjectName(u"TBSQL_TAB_UI")
        TBSQL_TAB_UI.resize(704, 322)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout = QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(self.tab)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.li_tab1_search_2 = QLineEdit(self.tab)
        self.li_tab1_search_2.setObjectName(u"li_tab1_search_2")

        self.horizontalLayout_4.addWidget(self.li_tab1_search_2)

        self.line_2 = QFrame(self.tab)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_4.addWidget(self.line_2)

        self.pb_tab1_data_in_2 = QPushButton(self.tab)
        self.pb_tab1_data_in_2.setObjectName(u"pb_tab1_data_in_2")

        self.horizontalLayout_4.addWidget(self.pb_tab1_data_in_2)

        self.pb_tab1_add_col_2 = QPushButton(self.tab)
        self.pb_tab1_add_col_2.setObjectName(u"pb_tab1_add_col_2")

        self.horizontalLayout_4.addWidget(self.pb_tab1_add_col_2)

        self.pb_tab1_add_row_2 = QPushButton(self.tab)
        self.pb_tab1_add_row_2.setObjectName(u"pb_tab1_add_row_2")

        self.horizontalLayout_4.addWidget(self.pb_tab1_add_row_2)

        self.pb_tab1_del_col_2 = QPushButton(self.tab)
        self.pb_tab1_del_col_2.setObjectName(u"pb_tab1_del_col_2")

        self.horizontalLayout_4.addWidget(self.pb_tab1_del_col_2)

        self.pb_tab1_del_row_2 = QPushButton(self.tab)
        self.pb_tab1_del_row_2.setObjectName(u"pb_tab1_del_row_2")

        self.horizontalLayout_4.addWidget(self.pb_tab1_del_row_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.tb_tab1_data_2 = QTableView(self.tab)
        self.tb_tab1_data_2.setObjectName(u"tb_tab1_data_2")

        self.verticalLayout_2.addWidget(self.tb_tab1_data_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.li_tab1_com_2 = QLineEdit(self.tab)
        self.li_tab1_com_2.setObjectName(u"li_tab1_com_2")

        self.horizontalLayout_5.addWidget(self.li_tab1_com_2)

        self.label_4 = QLabel(self.tab)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_5.addWidget(self.label_4)

        self.li_tab1_tb_2 = QLineEdit(self.tab)
        self.li_tab1_tb_2.setObjectName(u"li_tab1_tb_2")

        self.horizontalLayout_5.addWidget(self.li_tab1_tb_2)

        self.li_tab1_col_2 = QLineEdit(self.tab)
        self.li_tab1_col_2.setObjectName(u"li_tab1_col_2")

        self.horizontalLayout_5.addWidget(self.li_tab1_col_2)

        self.pb_tab1_run_2 = QPushButton(self.tab)
        self.pb_tab1_run_2.setObjectName(u"pb_tab1_run_2")

        self.horizontalLayout_5.addWidget(self.pb_tab1_run_2)

        self.horizontalLayout_5.setStretch(0, 9)
        self.horizontalLayout_5.setStretch(1, 1)
        self.horizontalLayout_5.setStretch(2, 3)
        self.horizontalLayout_5.setStretch(3, 4)
        self.horizontalLayout_5.setStretch(4, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        TBSQL_TAB_UI.addTab(self.tab, "")

        self.retranslateUi(TBSQL_TAB_UI)

        QMetaObject.connectSlotsByName(TBSQL_TAB_UI)
    # setupUi

    def retranslateUi(self, TBSQL_TAB_UI):
        TBSQL_TAB_UI.setWindowTitle(QCoreApplication.translate("TBSQL_TAB_UI", u"TabWidget", None))
        self.label_3.setText(QCoreApplication.translate("TBSQL_TAB_UI", u"\u641c\u7d22:", None))
        self.pb_tab1_data_in_2.setText(QCoreApplication.translate("TBSQL_TAB_UI", u"\u6570\u636e\u5bfc\u5165", None))
        self.pb_tab1_add_col_2.setText(QCoreApplication.translate("TBSQL_TAB_UI", u"\u65b0\u589e\u5217", None))
        self.pb_tab1_add_row_2.setText(QCoreApplication.translate("TBSQL_TAB_UI", u"\u65b0\u589e\u884c", None))
        self.pb_tab1_del_col_2.setText(QCoreApplication.translate("TBSQL_TAB_UI", u"\u5220\u9664\u5217", None))
        self.pb_tab1_del_row_2.setText(QCoreApplication.translate("TBSQL_TAB_UI", u"\u5220\u9664\u884c", None))
        self.label_4.setText(QCoreApplication.translate("TBSQL_TAB_UI", u"->\u5199\u5165\u5217:", None))
        self.pb_tab1_run_2.setText(QCoreApplication.translate("TBSQL_TAB_UI", u"\u6267\u884c", None))
        TBSQL_TAB_UI.setTabText(TBSQL_TAB_UI.indexOf(self.tab), QCoreApplication.translate("TBSQL_TAB_UI", u"\u9875", None))
    # retranslateUi

