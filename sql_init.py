import os
import sqlite3

from PySide2.QtWidgets import QMainWindow, QApplication
from peewee import SqliteDatabase

from clinet.sqlinit_ui import Ui_INIT_SQL
from PySide2.QtWidgets import QTextEdit, QApplication, QMessageBox, QDateTimeEdit, QLineEdit, QPushButton, QTextBrowser, \
    QFormLayout, QHBoxLayout, QComboBox, QInputDialog, QMainWindow, QFileDialog, QTableWidget, QTableWidgetItem, \
    QHeaderView, QAbstractItemView, QDesktopWidget, QAction, QShortcut, QWidget
import pandas as pd

#初始化级别
INIT_LEVEL = [
    'l3-保留全部数据（用于数据文件被锁恢复）'
    ,'l2-清空需求、元数据信息，保留其他数据'
    ,'l1-清空全部部数据，生成新的数据文件'
]

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_INIT_SQL()
        self.ui.setupUi(self)

        self.com_jb:QComboBox = self.ui.comboBox
        self.com_jb.addItems(INIT_LEVEL)
        self.li_fp:QLineEdit = self.ui.lineEdit
        self.bt_opf:QPushButton = self.ui.pushButton_2
        self.bt_init: QPushButton = self.ui.pushButton

        self.bt_opf.clicked.connect(self.f_opf)
        self.bt_init.clicked.connect(self.f_init)

    def f_opf(self):
        try:

            file_dialog = QFileDialog()

            file_dialog.setFileMode(QFileDialog.ExistingFiles)
            file_dialog.setNameFilter("数据文件 file (*.db)")
            if file_dialog.exec_():
                file_paths = file_dialog.selectedFiles()
                for file_path in file_paths:
                    self.li_fp.setText(file_path)
        except Exception as e:
            QMessageBox.warning(self, '', e.__str__())

    def f_init(self):
        s_path = self.li_fp.text().strip()
        d_path = s_path[:-3]+'_exp.db'
        if s_path =='':
            QMessageBox.warning(self, '', '请先选择源文件')
            return
        if not os.path.exists(s_path):
            QMessageBox.warning(self,'','源路径不存在')
            return
        if os.path.exists(d_path):
            os.remove(d_path)
        source_db =  sqlite3.connect(s_path)
        dict_db = sqlite3.connect(d_path)
        s_cursor = source_db.cursor()
        s_cursor.execute("SELECT * FROM sqlite_master WHERE type='table'")
        tables = s_cursor.fetchall()
        for table in tables:
            create_table_sql = table[4]
            print(create_table_sql)



app = QApplication([])
stats = MainWindow()
stats.show()
app.exec_()
