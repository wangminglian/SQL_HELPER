# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TBSQL.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QTableView, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_TBSQL_UI(object):
    def setupUi(self, TBSQL_UI):
        if not TBSQL_UI.objectName():
            TBSQL_UI.setObjectName(u"TBSQL_UI")
        TBSQL_UI.resize(917, 778)
        self.verticalLayout_5 = QVBoxLayout(TBSQL_UI)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pb_input_excel = QPushButton(TBSQL_UI)
        self.pb_input_excel.setObjectName(u"pb_input_excel")

        self.horizontalLayout.addWidget(self.pb_input_excel)

        self.pb_save = QPushButton(TBSQL_UI)
        self.pb_save.setObjectName(u"pb_save")

        self.horizontalLayout.addWidget(self.pb_save)

        self.pb_add_tab = QPushButton(TBSQL_UI)
        self.pb_add_tab.setObjectName(u"pb_add_tab")

        self.horizontalLayout.addWidget(self.pb_add_tab)

        self.pb_create_func = QPushButton(TBSQL_UI)
        self.pb_create_func.setObjectName(u"pb_create_func")

        self.horizontalLayout.addWidget(self.pb_create_func)

        self.pb_del_excel = QPushButton(TBSQL_UI)
        self.pb_del_excel.setObjectName(u"pb_del_excel")

        self.horizontalLayout.addWidget(self.pb_del_excel)

        self.pb_del_func = QPushButton(TBSQL_UI)
        self.pb_del_func.setObjectName(u"pb_del_func")

        self.horizontalLayout.addWidget(self.pb_del_func)

        self.ra_zhiding = QRadioButton(TBSQL_UI)
        self.ra_zhiding.setObjectName(u"ra_zhiding")

        self.horizontalLayout.addWidget(self.ra_zhiding)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout_2.setStretch(0, 1)

        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.line = QFrame(TBSQL_UI)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label = QLabel(TBSQL_UI)
        self.label.setObjectName(u"label")

        self.horizontalLayout_7.addWidget(self.label)

        self.li_tb_search = QLineEdit(TBSQL_UI)
        self.li_tb_search.setObjectName(u"li_tb_search")

        self.horizontalLayout_7.addWidget(self.li_tb_search)

        self.com_table = QComboBox(TBSQL_UI)
        self.com_table.setObjectName(u"com_table")

        self.horizontalLayout_7.addWidget(self.com_table)

        self.horizontalLayout_7.setStretch(0, 1)
        self.horizontalLayout_7.setStretch(1, 10)
        self.horizontalLayout_7.setStretch(2, 20)

        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_5 = QLabel(TBSQL_UI)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_2.addWidget(self.label_5)

        self.li_tab1_search = QLineEdit(TBSQL_UI)
        self.li_tab1_search.setObjectName(u"li_tab1_search")

        self.horizontalLayout_2.addWidget(self.li_tab1_search)

        self.pb_tab1_data_in = QPushButton(TBSQL_UI)
        self.pb_tab1_data_in.setObjectName(u"pb_tab1_data_in")

        self.horizontalLayout_2.addWidget(self.pb_tab1_data_in)

        self.pb_tab1_add_col = QPushButton(TBSQL_UI)
        self.pb_tab1_add_col.setObjectName(u"pb_tab1_add_col")

        self.horizontalLayout_2.addWidget(self.pb_tab1_add_col)

        self.pb_tab1_add_row = QPushButton(TBSQL_UI)
        self.pb_tab1_add_row.setObjectName(u"pb_tab1_add_row")

        self.horizontalLayout_2.addWidget(self.pb_tab1_add_row)

        self.pb_tab1_del_col = QPushButton(TBSQL_UI)
        self.pb_tab1_del_col.setObjectName(u"pb_tab1_del_col")

        self.horizontalLayout_2.addWidget(self.pb_tab1_del_col)

        self.pb_tab1_del_row = QPushButton(TBSQL_UI)
        self.pb_tab1_del_row.setObjectName(u"pb_tab1_del_row")

        self.horizontalLayout_2.addWidget(self.pb_tab1_del_row)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.tb_data = QTableView(TBSQL_UI)
        self.tb_data.setObjectName(u"tb_data")

        self.horizontalLayout_3.addWidget(self.tb_data)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.li_com = QLineEdit(TBSQL_UI)
        self.li_com.setObjectName(u"li_com")

        self.horizontalLayout_8.addWidget(self.li_com)

        self.label_6 = QLabel(TBSQL_UI)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_8.addWidget(self.label_6)

        self.li_tb = QLineEdit(TBSQL_UI)
        self.li_tb.setObjectName(u"li_tb")

        self.horizontalLayout_8.addWidget(self.li_tb)

        self.li_col = QLineEdit(TBSQL_UI)
        self.li_col.setObjectName(u"li_col")

        self.horizontalLayout_8.addWidget(self.li_col)

        self.pb_run_arg = QPushButton(TBSQL_UI)
        self.pb_run_arg.setObjectName(u"pb_run_arg")

        self.horizontalLayout_8.addWidget(self.pb_run_arg)

        self.horizontalLayout_8.setStretch(0, 9)
        self.horizontalLayout_8.setStretch(1, 1)
        self.horizontalLayout_8.setStretch(2, 2)
        self.horizontalLayout_8.setStretch(3, 2)
        self.horizontalLayout_8.setStretch(4, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_8)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.line_2 = QFrame(TBSQL_UI)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.tx_all_com = QTextEdit(TBSQL_UI)
        self.tx_all_com.setObjectName(u"tx_all_com")

        self.horizontalLayout_5.addWidget(self.tx_all_com)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_4 = QLabel(TBSQL_UI)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_6.addWidget(self.label_4)

        self.li_search_arg = QLineEdit(TBSQL_UI)
        self.li_search_arg.setObjectName(u"li_search_arg")

        self.horizontalLayout_6.addWidget(self.li_search_arg)


        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.tb_arg_list = QTableView(TBSQL_UI)
        self.tb_arg_list.setObjectName(u"tb_arg_list")

        self.verticalLayout_4.addWidget(self.tb_arg_list)


        self.horizontalLayout_5.addLayout(self.verticalLayout_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.line_3 = QFrame(TBSQL_UI)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_3 = QLabel(TBSQL_UI)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_4.addWidget(self.label_3)

        self.li_mb_search = QLineEdit(TBSQL_UI)
        self.li_mb_search.setObjectName(u"li_mb_search")

        self.horizontalLayout_4.addWidget(self.li_mb_search)

        self.line_4 = QFrame(TBSQL_UI)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_4.addWidget(self.line_4)

        self.pb_save_mb = QPushButton(TBSQL_UI)
        self.pb_save_mb.setObjectName(u"pb_save_mb")

        self.horizontalLayout_4.addWidget(self.pb_save_mb)

        self.pb_history = QPushButton(TBSQL_UI)
        self.pb_history.setObjectName(u"pb_history")

        self.horizontalLayout_4.addWidget(self.pb_history)

        self.pb_run = QPushButton(TBSQL_UI)
        self.pb_run.setObjectName(u"pb_run")

        self.horizontalLayout_4.addWidget(self.pb_run)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.tx_out = QTextEdit(TBSQL_UI)
        self.tx_out.setObjectName(u"tx_out")

        self.verticalLayout_3.addWidget(self.tx_out)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(3, 5)
        self.verticalLayout_3.setStretch(4, 5)
        self.verticalLayout_3.setStretch(5, 5)
        self.verticalLayout_3.setStretch(6, 1)
        self.verticalLayout_3.setStretch(7, 5)

        self.verticalLayout_5.addLayout(self.verticalLayout_3)


        self.retranslateUi(TBSQL_UI)

        # 设置整体背景样式
        TBSQL_UI.setStyleSheet("""
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
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: white;
                color: black;
                border: 2px solid #0288d1;
            }
            QLabel {
                font-size: 14px;
                color: #01579B;
            }
            QLineEdit, QComboBox {
                background-color: white;
                color: #01579B;
                border: 1px solid #ccc;
                padding: 5px;
            }
            QTextEdit {
                background-color: white;
                color: #333;
                border: 1px solid #ccc;
            }
            QTableView {
                gridline-color: #B3E5FC;
                selection-background-color: #0288D1;
                alternate-background-color: #E1F5FE;
            }
            QTableView QHeaderView::section {
                background-color: #0288D1;
                color: white;
                padding: 5px;
            }
            QRadioButton {
                color: #01579B;
            }
        """)

        # 设置表格样式
        self.tb_data.setAlternatingRowColors(True)
        self.tb_data.horizontalHeader().setStyleSheet("background-color: #0288D1; color: white;")
        self.tb_data.verticalHeader().setStyleSheet("background-color: #0288D1; color: white;")
        
        self.tb_arg_list.setAlternatingRowColors(True)
        self.tb_arg_list.horizontalHeader().setStyleSheet("background-color: #0288D1; color: white;")
        self.tb_arg_list.verticalHeader().setStyleSheet("background-color: #0288D1; color: white;")

        # 设置文本框样式
        self.tx_all_com.setStyleSheet("background-color: white; color: #333; border: 1px solid #ccc;")
        self.tx_out.setStyleSheet("background-color: white; color: #333; border: 1px solid #ccc;")

        # 设置分割线样式
        line_style = "background-color: #B3E5FC;"
        self.line.setStyleSheet(line_style)
        self.line_2.setStyleSheet(line_style)
        self.line_3.setStyleSheet(line_style)
        self.line_4.setStyleSheet(line_style)

        QMetaObject.connectSlotsByName(TBSQL_UI)
    # setupUi

    def retranslateUi(self, TBSQL_UI):
        TBSQL_UI.setWindowTitle(QCoreApplication.translate("TBSQL_UI", u"SQL_TABLE_TOOL", None))
        self.pb_input_excel.setText(QCoreApplication.translate("TBSQL_UI", u"\u5bfc\u5165\u6587\u6863", None))
        self.pb_save.setText(QCoreApplication.translate("TBSQL_UI", u"\u4fdd\u5b58\u6570\u636e", None))
        self.pb_add_tab.setText(QCoreApplication.translate("TBSQL_UI", u"\u65b0\u5efa\u8868\u683c", None))
        self.pb_create_func.setText(QCoreApplication.translate("TBSQL_UI", u"\u521b\u5efa\u51fd\u6570", None))
        self.pb_del_excel.setText(QCoreApplication.translate("TBSQL_UI", u"\u5220\u9664\u8868\u683c", None))
        self.pb_del_func.setText(QCoreApplication.translate("TBSQL_UI", u"\u5220\u9664\u51fd\u6570", None))
        self.ra_zhiding.setText(QCoreApplication.translate("TBSQL_UI", u"\u662f\u5426\u7f6e\u9876", None))
        self.label.setText(QCoreApplication.translate("TBSQL_UI", u"\u8868\u683c\u641c\u7d22:", None))
        self.label_5.setText(QCoreApplication.translate("TBSQL_UI", u"\u5b57\u6bb5\u7b5b\u9009:", None))
        self.pb_tab1_data_in.setText(QCoreApplication.translate("TBSQL_UI", u"\u6570\u636e\u5bfc\u5165", None))
        self.pb_tab1_add_col.setText(QCoreApplication.translate("TBSQL_UI", u"\u65b0\u589e\u5217", None))
        self.pb_tab1_add_row.setText(QCoreApplication.translate("TBSQL_UI", u"\u65b0\u589e\u884c", None))
        self.pb_tab1_del_col.setText(QCoreApplication.translate("TBSQL_UI", u"\u5220\u9664\u5217", None))
        self.pb_tab1_del_row.setText(QCoreApplication.translate("TBSQL_UI", u"\u5220\u9664\u884c", None))
        self.label_6.setText(QCoreApplication.translate("TBSQL_UI", u"->\u5199\u5165\u5217:", None))
        self.pb_run_arg.setText(QCoreApplication.translate("TBSQL_UI", u"\u6267\u884c", None))
        self.label_4.setText(QCoreApplication.translate("TBSQL_UI", u"\u53d8\u91cf\u641c\u7d22", None))
        self.label_3.setText(QCoreApplication.translate("TBSQL_UI", u"\u9009\u62e9\u6a21\u677f:", None))
        self.pb_save_mb.setText(QCoreApplication.translate("TBSQL_UI", u"\u5b58\u4e3a\u6a21\u677f", None))
        self.pb_history.setText(QCoreApplication.translate("TBSQL_UI", u"\u5386\u53f2\u8bb0\u5f55", None))
        self.pb_run.setText(QCoreApplication.translate("TBSQL_UI", u"\u751f\u6210", None))
    # retranslateUi

