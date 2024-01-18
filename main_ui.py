# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1549, 796)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QSize(15777215, 15777215))
        self.a_xqgl = QAction(MainWindow)
        self.a_xqgl.setObjectName(u"a_xqgl")
        self.a_ysjgl = QAction(MainWindow)
        self.a_ysjgl.setObjectName(u"a_ysjgl")
        self.a_gy = QAction(MainWindow)
        self.a_gy.setObjectName(u"a_gy")
        self.a_kjgl = QAction(MainWindow)
        self.a_kjgl.setObjectName(u"a_kjgl")
        self.a_bgl = QAction(MainWindow)
        self.a_bgl.setObjectName(u"a_bgl")
        self.a_zdgl = QAction(MainWindow)
        self.a_zdgl.setObjectName(u"a_zdgl")
        self.a_rwxy = QAction(MainWindow)
        self.a_rwxy.setObjectName(u"a_rwxy")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy1)
        self.centralwidget.setLayoutDirection(Qt.LeftToRight)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self._2 = QVBoxLayout()
        self._2.setObjectName(u"_2")
        self._2.setSizeConstraint(QLayout.SetNoConstraint)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.com_project_name = QComboBox(self.centralwidget)
        self.com_project_name.setObjectName(u"com_project_name")

        self.horizontalLayout_5.addWidget(self.com_project_name)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.com_xuqiu = QComboBox(self.centralwidget)
        self.com_xuqiu.setObjectName(u"com_xuqiu")

        self.horizontalLayout_5.addWidget(self.com_xuqiu)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.li_project_name = QLineEdit(self.centralwidget)
        self.li_project_name.setObjectName(u"li_project_name")

        self.horizontalLayout_5.addWidget(self.li_project_name)

        self.is_zd = QRadioButton(self.centralwidget)
        self.is_zd.setObjectName(u"is_zd")

        self.horizontalLayout_5.addWidget(self.is_zd)

        self.bt_add_project = QPushButton(self.centralwidget)
        self.bt_add_project.setObjectName(u"bt_add_project")

        self.horizontalLayout_5.addWidget(self.bt_add_project)

        self.bt_project_remove = QPushButton(self.centralwidget)
        self.bt_project_remove.setObjectName(u"bt_project_remove")

        self.horizontalLayout_5.addWidget(self.bt_project_remove)

        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 4)
        self.horizontalLayout_5.setStretch(3, 5)
        self.horizontalLayout_5.setStretch(4, 18)
        self.horizontalLayout_5.setStretch(5, 4)
        self.horizontalLayout_5.setStretch(7, 1)

        self._2.addLayout(self.horizontalLayout_5)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self._2.addWidget(self.line)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.te_input = QTextEdit(self.centralwidget)
        self.te_input.setObjectName(u"te_input")

        self.verticalLayout_5.addWidget(self.te_input)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_8.addWidget(self.label)

        self.search_line = QLineEdit(self.centralwidget)
        self.search_line.setObjectName(u"search_line")

        self.horizontalLayout_8.addWidget(self.search_line)

        self.com_arg = QComboBox(self.centralwidget)
        self.com_arg.setObjectName(u"com_arg")

        self.horizontalLayout_8.addWidget(self.com_arg)

        self.li_arg = QLineEdit(self.centralwidget)
        self.li_arg.setObjectName(u"li_arg")

        self.horizontalLayout_8.addWidget(self.li_arg)

        self.bt_add_arg = QPushButton(self.centralwidget)
        self.bt_add_arg.setObjectName(u"bt_add_arg")

        self.horizontalLayout_8.addWidget(self.bt_add_arg)

        self.bt_remove_arg = QPushButton(self.centralwidget)
        self.bt_remove_arg.setObjectName(u"bt_remove_arg")

        self.horizontalLayout_8.addWidget(self.bt_remove_arg)

        self.bt_copy = QPushButton(self.centralwidget)
        self.bt_copy.setObjectName(u"bt_copy")

        self.horizontalLayout_8.addWidget(self.bt_copy)

        self.bt_split_line = QPushButton(self.centralwidget)
        self.bt_split_line.setObjectName(u"bt_split_line")

        self.horizontalLayout_8.addWidget(self.bt_split_line)

        self.bt_rm_line = QPushButton(self.centralwidget)
        self.bt_rm_line.setObjectName(u"bt_rm_line")

        self.horizontalLayout_8.addWidget(self.bt_rm_line)

        self.bt_back = QPushButton(self.centralwidget)
        self.bt_back.setObjectName(u"bt_back")

        self.horizontalLayout_8.addWidget(self.bt_back)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)

        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(2, 3)
        self.horizontalLayout_8.setStretch(3, 3)
        self.horizontalLayout_8.setStretch(4, 2)
        self.horizontalLayout_8.setStretch(5, 2)
        self.horizontalLayout_8.setStretch(6, 2)
        self.horizontalLayout_8.setStretch(10, 6)

        self.verticalLayout_5.addLayout(self.horizontalLayout_8)


        self.horizontalLayout_7.addLayout(self.verticalLayout_5)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.VLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_7.addWidget(self.line_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.te_view = QTextBrowser(self.centralwidget)
        self.te_view.setObjectName(u"te_view")

        self.verticalLayout_2.addWidget(self.te_view)

        self.ta_model_list = QTableWidget(self.centralwidget)
        if (self.ta_model_list.columnCount() < 4):
            self.ta_model_list.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.ta_model_list.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.ta_model_list.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.ta_model_list.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.ta_model_list.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.ta_model_list.setObjectName(u"ta_model_list")

        self.verticalLayout_2.addWidget(self.ta_model_list)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.bt_add_model = QPushButton(self.centralwidget)
        self.bt_add_model.setObjectName(u"bt_add_model")

        self.horizontalLayout_4.addWidget(self.bt_add_model)

        self.bt_save_model = QPushButton(self.centralwidget)
        self.bt_save_model.setObjectName(u"bt_save_model")

        self.horizontalLayout_4.addWidget(self.bt_save_model)

        self.bt_view = QPushButton(self.centralwidget)
        self.bt_view.setObjectName(u"bt_view")

        self.horizontalLayout_4.addWidget(self.bt_view)

        self.bt_fenfa = QPushButton(self.centralwidget)
        self.bt_fenfa.setObjectName(u"bt_fenfa")

        self.horizontalLayout_4.addWidget(self.bt_fenfa)

        self.bt_help = QPushButton(self.centralwidget)
        self.bt_help.setObjectName(u"bt_help")

        self.horizontalLayout_4.addWidget(self.bt_help)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.bt_rm_model = QPushButton(self.centralwidget)
        self.bt_rm_model.setObjectName(u"bt_rm_model")

        self.horizontalLayout_4.addWidget(self.bt_rm_model)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.verticalLayout_2.setStretch(0, 5)
        self.verticalLayout_2.setStretch(1, 5)
        self.verticalLayout_2.setStretch(2, 1)

        self.horizontalLayout_7.addLayout(self.verticalLayout_2)

        self.line_6 = QFrame(self.centralwidget)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_7.addWidget(self.line_6)

        self.line_7 = QFrame(self.centralwidget)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.VLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_7.addWidget(self.line_7)

        self.verticalScrollBar = QScrollBar(self.centralwidget)
        self.verticalScrollBar.setObjectName(u"verticalScrollBar")
        self.verticalScrollBar.setOrientation(Qt.Vertical)

        self.horizontalLayout_7.addWidget(self.verticalScrollBar)


        self._2.addLayout(self.horizontalLayout_7)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self._2.addWidget(self.line_2)

        self.la_outputer = QHBoxLayout()
        self.la_outputer.setObjectName(u"la_outputer")
        self.li_complex = QLineEdit(self.centralwidget)
        self.li_complex.setObjectName(u"li_complex")

        self.la_outputer.addWidget(self.li_complex)

        self.bt_gener_sql = QPushButton(self.centralwidget)
        self.bt_gener_sql.setObjectName(u"bt_gener_sql")

        self.la_outputer.addWidget(self.bt_gener_sql)


        self._2.addLayout(self.la_outputer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)

        self.search_history = QLineEdit(self.centralwidget)
        self.search_history.setObjectName(u"search_history")

        self.horizontalLayout.addWidget(self.search_history)

        self.com_history = QComboBox(self.centralwidget)
        self.com_history.setObjectName(u"com_history")

        self.horizontalLayout.addWidget(self.com_history)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout.addWidget(self.label_6)

        self.search_moban = QLineEdit(self.centralwidget)
        self.search_moban.setObjectName(u"search_moban")

        self.horizontalLayout.addWidget(self.search_moban)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.com_moban = QComboBox(self.centralwidget)
        self.com_moban.setObjectName(u"com_moban")

        self.horizontalLayout.addWidget(self.com_moban)

        self.bt_moban = QPushButton(self.centralwidget)
        self.bt_moban.setObjectName(u"bt_moban")

        self.horizontalLayout.addWidget(self.bt_moban)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(2, 10)
        self.horizontalLayout.setStretch(4, 10)
        self.horizontalLayout.setStretch(6, 10)

        self._2.addLayout(self.horizontalLayout)

        self.te_printer = QTextBrowser(self.centralwidget)
        self.te_printer.setObjectName(u"te_printer")

        self._2.addWidget(self.te_printer)


        self.gridLayout.addLayout(self._2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1549, 26))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menu.addAction(self.a_xqgl)
        self.menu_2.addAction(self.a_gy)
        self.menu_3.addAction(self.a_kjgl)
        self.menu_3.addAction(self.a_bgl)
        self.menu_3.addAction(self.a_zdgl)
        self.menu_3.addAction(self.a_rwxy)
        self.toolBar.addAction(self.a_xqgl)
        self.toolBar.addAction(self.a_ysjgl)
        self.toolBar.addAction(self.a_kjgl)
        self.toolBar.addAction(self.a_bgl)
        self.toolBar.addAction(self.a_zdgl)
        self.toolBar.addAction(self.a_rwxy)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SQL\u52a9\u624b", None))
        self.a_xqgl.setText(QCoreApplication.translate("MainWindow", u"\u9700\u6c42\u7ba1\u7406", None))
#if QT_CONFIG(shortcut)
        self.a_xqgl.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+X", None))
#endif // QT_CONFIG(shortcut)
        self.a_ysjgl.setText(QCoreApplication.translate("MainWindow", u"\u5143\u6570\u636e\u7ba1\u7406", None))
#if QT_CONFIG(shortcut)
        self.a_ysjgl.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Y", None))
#endif // QT_CONFIG(shortcut)
        self.a_gy.setText(QCoreApplication.translate("MainWindow", u"SQL_HELPER", None))
        self.a_kjgl.setText(QCoreApplication.translate("MainWindow", u"\u53e3\u5f84\u7ba1\u7406", None))
#if QT_CONFIG(shortcut)
        self.a_kjgl.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+K", None))
#endif // QT_CONFIG(shortcut)
        self.a_bgl.setText(QCoreApplication.translate("MainWindow", u"\u8868\u7ba1\u7406", None))
#if QT_CONFIG(shortcut)
        self.a_bgl.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+B", None))
#endif // QT_CONFIG(shortcut)
        self.a_zdgl.setText(QCoreApplication.translate("MainWindow", u"\u5b57\u6bb5\u7ba1\u7406", None))
        self.a_rwxy.setText(QCoreApplication.translate("MainWindow", u"\u9700\u6c42\u8840\u7f18", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u5de5\u7a0b:", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u9700\u6c42:", None))
        self.is_zd.setText(QCoreApplication.translate("MainWindow", u"\u662f\u5426\u7f6e\u9876", None))
        self.bt_add_project.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u5de5\u7a0b", None))
        self.bt_project_remove.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u5de5\u7a0b", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u53c2\u6570:", None))
        self.bt_add_arg.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0", None))
        self.bt_remove_arg.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664", None))
        self.bt_copy.setText(QCoreApplication.translate("MainWindow", u"\u590d\u5236", None))
        self.bt_split_line.setText(QCoreApplication.translate("MainWindow", u"\u5206\u5272\u6362\u884c", None))
        self.bt_rm_line.setText(QCoreApplication.translate("MainWindow", u"\u53bb\u9664\u6307\u5b9a\u884c", None))
        self.bt_back.setText(QCoreApplication.translate("MainWindow", u"\u56de\u9000", None))
        ___qtablewidgetitem = self.ta_model_list.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u5e8f\u53f7", None));
        ___qtablewidgetitem1 = self.ta_model_list.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u5f0f", None));
        ___qtablewidgetitem2 = self.ta_model_list.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u89c4\u5219", None));
        ___qtablewidgetitem3 = self.ta_model_list.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"id", None));
        self.bt_add_model.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0", None))
        self.bt_save_model.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58", None))
        self.bt_view.setText(QCoreApplication.translate("MainWindow", u"\u9884\u89c8", None))
        self.bt_fenfa.setText(QCoreApplication.translate("MainWindow", u"\u5206\u53d1", None))
        self.bt_help.setText(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9\u6587\u6863", None))
        self.bt_rm_model.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664", None))
        self.bt_gener_sql.setText(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u8bed\u53e5", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"history\uff1a", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22\u6a21\u7248\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u9009\u62e9\u6a21\u7248", None))
        self.bt_moban.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u7248\u751f\u6210", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", u"\u5143\u6570\u636e\u7ba1\u7406", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

