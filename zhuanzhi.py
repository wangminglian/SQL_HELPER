from PySide2.QtWidgets import QMainWindow, QApplication

from clinet.zhuanzhi_ui import Ui_MainWindow
from PySide2.QtWidgets import QTextEdit, QApplication, QMessageBox, QDateTimeEdit, QLineEdit, QPushButton, QTextBrowser, \
    QFormLayout, QHBoxLayout, QComboBox, QInputDialog, QMainWindow, QFileDialog, QTableWidget, QTableWidgetItem, \
    QHeaderView, QAbstractItemView, QDesktopWidget, QAction, QShortcut, QWidget
import pandas as pd


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.li_hfg:QLineEdit = self.ui.li_hfg
        self.li_lfg:QLineEdit=self.ui.li_lfg
        self.li_wjm:QLineEdit=self.ui.li_wjm
        self.bt_xzwj:QPushButton=self.ui.bt_xzwj
        self.bt_kszh:QPushButton=self.ui.bt_kszh

        self.bt_xzwj.clicked.connect(self.f_xzwj)
        self.bt_kszh.clicked.connect(self.f_kszh)


    def f_xzwj(self):
        try:
            # 导入文件
            file_dialog = QFileDialog()
            file_dialog.setFileMode(QFileDialog.ExistingFile)
            file_dialog.setNameFilter("All files (*.*)")
            if file_dialog.exec_():
                file_paths = file_dialog.selectedFiles()
                self.li_wjm.setText(file_paths[0])
        except Exception as e:
            QMessageBox.warning(self,'',e.__str__())


    def f_kszh(self):
        hfg = self.li_hfg.text()
        lfg = self.li_lfg.text()
        wjm = self.li_wjm.text()
        if wjm.strip()=='':
            QMessageBox.warning(self,'','请先选择文件')

        try:
            if lfg=='\\t':
                df = pd.read_csv(wjm, delimiter='\t')
            else:
                df = pd.read_csv(wjm, delimiter=lfg)
            rdf = df.transpose()
            rdf.to_csv(f'{wjm}_out',header=False)
            QMessageBox.information(self,'',f'转化成功，存储位置:{wjm}_out')
        except Exception as e:
            QMessageBox.warning(self, '',e.__str__())



app = QApplication([])
stats = MainWindow()
stats.show()
app.exec_()
