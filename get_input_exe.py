

from clinet.add_table_by_ddl_ui import Ui_add_table_by_ddl

from PySide2.QtGui import Qt, QIcon, QKeySequence, QStandardItemModel
from PySide2.QtWidgets import QTextEdit, QApplication, QMessageBox, QDateTimeEdit, QLineEdit, QPushButton, QTextBrowser, \
    QFormLayout, QHBoxLayout, QComboBox, QInputDialog, QMainWindow, QFileDialog, QTableWidget, QTableWidgetItem, \
    QHeaderView, QAbstractItemView, QDesktopWidget, QAction, QShortcut, QWidget, QTableView, QDialog, QVBoxLayout, \
    QDialogButtonBox, QLabel, QToolTip, QColumnView



from sql_helper.read_sql_file import Reader_SQL
OUT_TABLE_HEADER = ['id','输出表名', '类型','表描述','备注','优先级']
OUT_TABLE_HEADER_ID=0
OUT_TABLE_HEADER_SRBM=1
OUT_TABLE_HEADER_LX=2
OUT_TABLE_HEADER_BMS=3
OUT_TABLE_HEADER_BZ=4
OUT_TABLE_HEADER_YXJ=5
class GET_INPUT_EXE(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_add_table_by_ddl()
        self.ui.setupUi(self)

        self.tx_ddl:QTextEdit = self.ui.tx_ddl
        self.tb_output:QTableView = self.ui.tb_output
        self.tx_sqldll:QTextEdit=self.ui.tx_sqldll

        self.tb_output.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_output.horizontalHeader().setStretchLastSection(True)
        self.tb_output.setSelectionBehavior(QTableView.SelectRows)
        self.red_sql_eng = Reader_SQL()
        self.bt_yulan:QPushButton = self.ui.bt_yulan
        self.bt_yulan.clicked.connect(self.f_yulan)

        self.bt_submit:QPushButton=self.ui.bt_submit
        self.bt_submit.clicked.connect(self.f_bt_submit)

        self.bt_jiazai: QPushButton = self.ui.bt_jiazai
        self.bt_jiazai.clicked.connect(self.f_jiazai)
        self.li_bz:QLineEdit=self.ui.li_bz

        self.bt_close:QPushButton=self.ui.bt_close
        self.bt_close.clicked.connect(self.close)

        # self.closeEvent=self.f_close

        self.outputs=[]

    def f_bt_submit(self):
        pass

    def f_yulan(self):
        pass

    def f_jiazai(self):
        sql_str = self.tx_ddl.toPlainText()
        self.tx_sqldll.clear()
        self.init_tb_output(sql_str)


    def init_tb_output(self,sql_str):
        # 抽取输入表，数据存储到 self.out_tables_model中
        inputs = self.red_sql_eng.read_sql_to_rtl_table_v2(sql_str)
        mystr = '\n'.join(inputs)
        self.tx_sqldll.setText(mystr)




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('主窗口')
        self.setGeometry(100, 100, 400, 300)

        self.button = QPushButton('提取输入表', self)
        self.button.clicked.connect(self.openNewWindow)
        self.button.move(150, 100)

        self.newWindow = GET_INPUT_EXE()

    def openNewWindow(self):
        self.newWindow.show()

try:
    app = QApplication([])
    stats = MainWindow()
    # apply_stylesheet(app, theme='light_lightgreen.xml')

    stats.show()

    app.exec_()
finally:

    pass

