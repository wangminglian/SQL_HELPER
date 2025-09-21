import os
import re
import ast
from clinet.main_ui import Ui_MainWindow
from clinet.gy_ui import Ui_SQL_HELPER
import pyperclip
import pandas as pd

from PySide6.QtCore import QTime, QDateTime, QRect, QTimer, QCoreApplication
from PySide6.QtGui import Qt, QIcon, QKeySequence, QShortcut, QAction
from PySide6.QtWidgets import QTextEdit, QApplication, QMessageBox, QDateTimeEdit, QLineEdit, QPushButton, QTextBrowser, \
    QFormLayout, QHBoxLayout, QComboBox, QInputDialog, QMainWindow, QFileDialog, QTableWidget, QTableWidgetItem, \
    QHeaderView, QAbstractItemView,  QWidget, QToolBar, QMenu, QVBoxLayout, \
    QRadioButton, QLabel

from peewee import SqliteDatabase, fn
from collections import namedtuple
from model.model import Project_detail, SQL_arg, History, dp, create_tables, ARG_model,db
from sql_helper.helper_restruct import Reader_Factory, Genner_Com
from collections import deque
from xuqiu import XUQIU_UI
from yuanshuju import YSJGL_UI, RWXY_UI, ZDGL_UI, BGL_UI
from conf import MOBAN_PATH,DB_PATH,DB_NAME,TXHS,TXYD,TXSJ,XSQ_PATH,GEN_PATH


HELP_TEXT = """
                                    帮助文档
常规模式：不需要输入规则
字符串切割：${arg}.split('分割符号')[索引]
正则表达式：reg=\[(\d+):;index=1 注:reg为正则表达式，index为索引
轮询：一个数字，为轮询的次数(整数和负数是不一样的轮训策略，一言难尽，你试试就知道了)
字符串切割:if逻辑写法eg:"a" if (${arg}=="去除$符号") else "b"
GROUP BY:生产group by 后面的 1,2,3,4
行分隔: 写法 1:-1 或者 3
变量分发：将计算出的结果分发到别的变量中，并执行，最后展示出来
注:
序号越小执行优先级越高，序号为0忽略不计算
"""

Arg_Value = namedtuple('Arg_Value','name value')

com_model = ['常规','正则表达式','字符串切割','轮询','去除换行','GROUP BY','行分隔','变量分发','元数据','自定义函数','超级自定义函数']

ui_path = os.path.join(os.getcwd().split('SQL_Helper')[0],'SQL_Helper/clinet/ui/main.ui')
print(f'ui：${ui_path}')
MOBAN_PATH = MOBAN_PATH
DB_PATH = DB_PATH
DB_NAME = DB_NAME

TXSJ = int(TXSJ)*1000*60
TXHS = int(TXHS)
TXYD = int(TXYD)

class GY_UI(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_SQL_HELPER()
        self.ui.setupUi(self)


class DrinkWaterReminder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Drink Water Reminder')
        self.setGeometry(100, 100, 300, 200)

        self.label = QLabel('喝水&运动提醒器已开启', self)
        self.label.setStyleSheet('font-size: 20px; font-weight: bold; color: blue;')
        self.label.setAlignment(Qt.AlignCenter)
        flags = self.windowFlags()
        self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        self.setLayout(vbox)

        self.show()

        # 设置定时器，每隔30分钟提醒一次
        timer = QTimer(self)
        timer.timeout.connect(self.showReminder)
        timer.start(TXSJ)
        self.yd_cnt= 0
        self.hs_cnt=0

    def showReminder(self):
        self.yd_cnt +=1
        self.hs_cnt +=1
        my_str ='请：'
        if self.yd_cnt>= TXYD:
            my_str +='运动|'
            self.yd_cnt=0
        if self.hs_cnt>=TXHS:
            my_str += '喝水|'
            self.hs_cnt=0
        if self.yd_cnt*self.hs_cnt ==0:
            self.label.setText(my_str[:-1])
            self.show()






class MainWindow(QMainWindow):


    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)
        self.mycach = {}


        self.loading_qt()
        self.binding()
        self.stack = deque()





    def loading_qt(self):
        '''加载qt部件'''


        db_path =None
        db_path =  os.path.join(DB_PATH, DB_NAME)

        if not db_path: db_path,file_type = QFileDialog.getOpenFileName(self,'选取存储文件位置','/Users/','*.db')
        if db_path =="":exit()
        if not os.path.exists(db_path):
            QMessageBox.warning(self,'','数据库文件丢失,程序无法启动,请将${}拷贝至{}目录下'.format(DB_NAME,db_path))
            exit()
        else:
            db = SqliteDatabase(db_path)

            dp.initialize(db)

        self.bt_add_project:QPushButton = self.ui.bt_add_project
        self.bt_project_remove:QPushButton = self.ui.bt_project_remove
        self.bt_add_arg:QPushButton = self.ui.bt_add_arg
        self.bt_remove_arg:QPushButton = self.ui.bt_remove_arg
        self.bt_view:QPushButton = self.ui.bt_view
        self.bt_gener_sql:QPushButton = self.ui.bt_gener_sql
        self.bt_help:QPushButton = self.ui.bt_help
        self.bt_add_model:QPushButton = self.ui.bt_add_model
        self.bt_save_model:QPushButton = self.ui.bt_save_model
        self.bt_rm_model:QPushButton = self.ui.bt_rm_model
        self.bt_split_line:QPushButton=self.ui.bt_split_line
        self.bt_rm_line:QPushButton=self.ui.bt_rm_line
        self.bt_back:QPushButton=self.ui.bt_back
        self.bt_moban: QPushButton = self.ui.bt_moban
        self.li_search_moban:QLineEdit = self.ui.search_moban
        self.li_search_moban.textChanged.connect(self.init_com_moban)

        # self.search_line = QLineEdit(self.centralwidget)
        # self.search_line.setObjectName(u"search_line")

        self.search_line:QLineEdit = self.ui.search_line
        self.search_history:QLineEdit = self.ui.search_history




        self.bt_copy:QPushButton = self.ui.bt_copy
        self.li_project_name:QLineEdit = self.ui.li_project_name
        self.li_arg:QLineEdit = self.ui.li_arg
        self.li_complex:QLineEdit = self.ui.li_complex
        self.ta_model_list:QTableWidget = self.ui.ta_model_list
        self.bt_fenfa: QPushButton = self.ui.bt_fenfa
        self.com_moban: QComboBox = self.ui.com_moban

        self.com_history:QComboBox = self.ui.com_history
        # self.init_com_history()
        self.com_project_name:QComboBox = self.ui.com_project_name
        self.init_com_project_name()
        self.com_arg:QComboBox = self.ui.com_arg
        self.init_com_arg()
        self.init_com_moban()



        self.te_input:QTextEdit = self.ui.te_input
        self.te_input.setAcceptRichText(False)
        self.te_view:QTextBrowser = self.ui.te_view
        self.te_printer:QTextBrowser = self.ui.te_printer
        self.a_gy:QAction = self.ui.a_gy
        self.a_gy.triggered.connect(self.f_gy)
        self.a_xqgl:QAction = self.ui.a_xqgl
        self.a_xqgl.triggered.connect(self.f_xqgl)

        # 工具栏中添加菜单


        self.a_ysjgl:QAction=self.ui.a_kjgl
        self.a_ysjgl.triggered.connect(self.f_a_ysjgl)

        self.a_zdgl :QAction=self.ui.a_zdgl
        self.a_zdgl.triggered.connect(self.f_a_zdgl)

        self.a_bgl:QAction=self.ui.a_bgl
        self.a_bgl.triggered.connect(self.f_a_bgl)

        self.is_zd:QRadioButton = self.ui.is_zd
        self.is_zd.toggled.connect(self.f_is_zd)
        # self.is_zd.setChecked(True)



        self.a_rwxy:QAction = self.ui.a_rwxy
        self.a_rwxy.triggered.connect(self.f_a_rwxy)

        self.relaod_history()
        self.load_args()
        self.ta_model_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ta_model_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ta_model_list.setColumnHidden(3,True)
        self.init_ta_model_list()

        self.search_line.textChanged.connect(self.update_comArg)
        self.search_history.textChanged.connect(self.update_comHistory)

        # 修饰器需求名称
        self.li_xsq:QLineEdit = self.ui.li_xsq
        self.com_xsq:QComboBox = self.ui.com_xsq
        self.init_com_xsq()
        self.li_xsq_list:QLineEdit = self.ui.li_xsq_list
        self.li_xsq.textChanged.connect(self.init_com_xsq)
        # li_xsq 回车时提交
        self.li_xsq.returnPressed.connect(self.add_xsq_to_list)
        self.current_xsq_list = []

        # 打开项目根目录
        self.pb_home:QPushButton = self.ui.pb_home
        self.pb_home.clicked.connect(self.open_project_root)

        # 设置快捷键
        shortcut = QShortcut(QKeySequence("Ctrl+`"), self)
        shortcut.activated.connect(self.switch_focus)
        shortcut2 = QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Return), self)
        shortcut2.activated.connect(self.gener_sql)
        shortcut3 = QShortcut(QKeySequence(Qt.ALT | Qt.Key_Return), self)
        shortcut3.activated.connect(self.view_and_copy)


        self.txhs = DrinkWaterReminder()

    def open_project_root(self):
        # 获取当前项目根目录
        project_root = os.path.join(GEN_PATH,DB_PATH)
        if not os.path.exists(project_root):
            QMessageBox.warning(self, '警告', '项目根目录不存在')
            return
        # 打开项目根目录
        os.startfile(project_root)

    # 修饰器列表
    def init_xsq_list(self):
        tmp = self.li_xsq_list.text()
        tmp_list = tmp.split(';')
        # 判断修饰器文件是否存在，不存在，删除
        for xsq_name in tmp_list:
            if xsq_name == '':
                continue
            xsq_path = os.path.join(GEN_PATH, XSQ_PATH, xsq_name)
            if not os.path.exists(xsq_path):
                tmp_list.remove(xsq_name)
        return tmp_list

    # 添加修饰器
    def add_xsq_to_list(self):
        # 如果输入0，则情况修饰器列表
        if self.li_xsq.text() == '0':
            self.current_xsq_list = []
            self.li_xsq_list.setText('')
            self.li_xsq.setText('')
            self.repaint()
            return
        # 如果是负数，则删除负数对应的格式的修饰器
        # 首先判断输入时负数
        if self.li_xsq.text().startswith('-'):
            del_num = int(self.li_xsq.text())
            self.current_xsq_list = self.current_xsq_list[:del_num]
            self.li_xsq_list.setText(';'.join([i for i in self.current_xsq_list if i != '']))
            self.li_xsq.setText('')
            self.repaint()
            return

        # 获取当前修饰器
        xsq_name = self.com_xsq.currentText()
        self.current_xsq_list = self.init_xsq_list()
        self.current_xsq_list.append(xsq_name)
        # 初始化当前修饰器列表
        self.li_xsq_list.setText(';'.join([i for i in self.current_xsq_list if i != '']))
        self.li_xsq.setText('')
        self.repaint()

    # 初始化修饰器列表
    def init_com_xsq(self):
        self.com_xsq.clear()
        search_txt = self.li_xsq.text().upper()
        xsq_path = os.path.join(GEN_PATH, XSQ_PATH)
        files = self.get_files_in_directory(xsq_path)
        # files 排序
        files.sort()
        if search_txt =='':
            self.com_xsq.addItems(files)
        else:
            out_list = []
            out_list_2 = []
            for i in files:
                if i.upper().startswith(search_txt):
                    out_list.append(i)
                if search_txt in i.upper() and i not in out_list:
                    out_list_2.append(i)
            out_list.extend(out_list_2)
            self.com_xsq.addItems(out_list)
            
        self.repaint()




    def closeEvent(self, event):
        reply = QMessageBox.question(self, '确认', '确定要关闭窗口吗？',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        reply = QMessageBox.question(self, '确认', '签退了吗？        ',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def f_is_zd(self,checked):
        flags = self.windowFlags()
        if checked:
            self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
        self.show()

    def f_a_ysjgl(self):
        self.ysjgl_ui = YSJGL_UI()
        self.ysjgl_ui.show()

    def f_a_rwxy(self):
        self.rwxy_ui = RWXY_UI()
        self.rwxy_ui.show()

    def f_a_zdgl(self):
        self.zdgl_ui=ZDGL_UI()
        self.zdgl_ui.show()

    def f_a_bgl(self):
        self.bgl_ui=BGL_UI()
        self.bgl_ui.show()



    def f_gy(self):

        self.gy_ui = GY_UI()
        self.gy_ui.showNormal()

    def f_xqgl(self):
        self.xqgl=XUQIU_UI(self)
        self.xqgl.show()


    def switch_focus(self):
        # 切换焦点
        if self.search_line.hasFocus():
            self.search_history.setFocus()
        else:
            self.search_line.setFocus()


    def update_comArg(self,text):
        # 模糊查询变量
        self.com_arg.clear()
        project_name = self.com_project_name.currentText()
        items = [i.arg_nike for i in SQL_arg.select().where(SQL_arg.project_name==project_name )]
        ret= []
        for item in items:
            if text.upper() in item.upper():
                ret.append(item)
        self.com_arg.addItems(ret)
        self.repaint()
    def update_comHistory(self,text):
    # 模糊查询历史变量
        self.com_history.clear()
        project_name = self.com_project_name.currentText()

        my_gjz = text.strip().upper()
        my_gjz_list = my_gjz.split('&')
    #构造筛选条件语句
        gjz = ' and '.join(map(lambda x: f"genner_str like '%{x}%'",my_gjz_list))
        print(gjz)
        query = f"select genner_str AS genner_str from(select  genner_str,max(ctime) as ctime from history where  {gjz} group by genner_str ) ORDER BY ctime desc "

        print(query)
        result = db.execute_sql(query)
        tmp = []

        for i in result:
            tmp.append(i[0])
        self.com_history.addItems(tmp)
        self.repaint()

    def init_ta_model_list(self):
        _arg = self.get_current_arg()
        if _arg == None:return
        tmps = _arg.arg_model.order_by(ARG_model.rn)
        tmps = tmps.execute()
        self.ta_model_list.setRowCount(len(tmps))
        i = 0
        for item in tmps:
            self.ta_model_list.setItem(i,0,QTableWidgetItem(item.rn))
            com_tmp = QComboBox()
            com_tmp.addItems(com_model)
            com_tmp.setCurrentText(item.arg_model)
            self.ta_model_list.setCellWidget(i,1,com_tmp)
            self.ta_model_list.setItem(i,2,QTableWidgetItem(item.arg_contorl))
            print("*********???****"+str(item.id))
            self.ta_model_list.setItem(i,3,QTableWidgetItem(str(item.id)))
            i+=1
        self.repaint()

    def get_current_arg(self):
        name = self.com_arg.currentText()
        p_name = self.com_project_name.currentText()
        if (p_name.strip() == '' or p_name == None):
            return
        if (name.strip() == '' or name == None):
            return
        project_name = Project_detail.get_by_id(p_name)
        sql_arg = SQL_arg.get_or_none(SQL_arg.arg_nike == name, SQL_arg.project_name == project_name)
        return sql_arg

    def get_sql_arg_by_name(self,name):
        name = name
        p_name = self.com_project_name.currentText()
        if (p_name.strip() == '' or p_name == None):
            return
        if (name.strip() == '' or name == None):
            return
        project_name = Project_detail.get_by_id(p_name)
        sql_arg = SQL_arg.get_or_none(SQL_arg.arg_nike == name, SQL_arg.project_name == project_name)
        return sql_arg

    def save_arg_model(self):
        '''保存所有模式参数'''
        self.save_arg()
        row_cnt = self.ta_model_list.rowCount()
        for row in range(row_cnt):
            t_rn = self.ta_model_list.item(row, 0).text() if self.ta_model_list.item(row, 0) != None else ''
            t_model = self.ta_model_list.cellWidget(row, 1).currentText() if self.ta_model_list.cellWidget(row,1) != None else ''
            t_cotorl = self.ta_model_list.item(row, 2).text() if self.ta_model_list.item(row, 2) != None else ''
            t_id = self.ta_model_list.item(row, 3).text() if self.ta_model_list.item(row, 3) != None else ''
            tmp: ARG_model = ARG_model.get_or_create(id=t_id)[0]
            tmp.rn = t_rn
            tmp.arg_model = t_model
            tmp.arg_contorl = t_cotorl
            try:
                tmp.save()
            except Exception as e:
                QMessageBox.warning(self,'',e.__str__())
        self.init_ta_model_list()

    def add_ta_model_row(self):
        '''添加一行模式数据'''
        current_add_count = self.ta_model_list.rowCount() + 1
        arg_name = self.get_current_arg()
        tmp = ARG_model(arg_name=arg_name, rn=current_add_count, arg_model=com_model[0], arg_contorl='').save(force_insert=True)
        self.save_arg_model()
        self.init_ta_model_list()



    def init_com_project_name(self):
        self.com_project_name.clear()
        itmes =[i.project_name for i in  Project_detail.select()]
        self.com_project_name.addItems(itmes)

    def init_com_history(self):
        self.com_history.clear()
        itmes = History.select().order_by(-History.mtime).limit(50).execute()
        tmp = []
        for i in itmes:
            tmp.append(i.genner_str)
            # tmp.append(i.__str__())
            # self.mycach[i.__str__()] = i.ret
        self.com_history.addItems(tmp)
        self.repaint()



    def init_com_arg(self):
        self.com_arg.clear()
        project_name = self.com_project_name.currentText()
        items = [i.arg_nike for i in SQL_arg.select().where(SQL_arg.project_name==project_name)]
        self.com_arg.addItems(items)
        self.repaint()

    def get_files_in_directory(self,directory):
        files = []
        try:
            for filename in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, filename)):
                    files.append(filename)
            return files
        except Exception as e:
            raise Exception(f"模版路径不正确{MOBAN_PATH}")
    def init_com_moban(self):
        self.com_moban.clear()
        search_txt = self.li_search_moban.text().upper()
        files = self.get_files_in_directory(MOBAN_PATH)
        if search_txt =='':
            self.com_moban.addItems(files)
        else:
            for i in files:
                if search_txt in i.upper():
                    self.com_moban.addItem(i)
        self.repaint()


    def binding(self):
        '''绑定事件'''
        self.bt_add_project.clicked.connect(self.add_project)
        self.bt_project_remove.clicked.connect(self.remove_project)
        self.bt_add_arg.clicked.connect(self.add_arg)
        self.bt_gener_sql.clicked.connect(self.gener_sql)
        self.bt_help.clicked.connect(self.help)
        self.bt_copy.clicked.connect(self.copy)
        self.bt_fenfa.clicked.connect(self.fenfa)
        self.bt_add_model.clicked.connect(self.add_ta_model_row)
        self.bt_rm_model.clicked.connect(self.remove_arg_model)
        self.bt_moban.clicked.connect(self.moban_genersql)
        self.bt_split_line.clicked.connect(self.split_line)
        self.bt_rm_line.clicked.connect(self.rm_line)
        self.bt_back.clicked.connect(self.be_back)
        self.li_complex.textChanged.connect(self.li_complex_text_change)
        self.bt_remove_arg.clicked.connect(self.remove_arg)
        self.bt_view.clicked.connect(self.view)
        self.com_project_name.currentTextChanged.connect(self.init_com_arg)
        # self.com_arg.highlighted.connect(self.save_arg)
        self.com_history.currentTextChanged.connect(self.relaod_history)
        self.bt_save_model.clicked.connect(self.save_arg_model)
        self.com_arg.currentTextChanged.connect(self.load_args)

# 使用模版

    def moban_genersql(self):
        '''生成语句'''
        p_name = self.com_project_name.currentText()
        project_name = Project_detail.get_by_id(p_name)
        cur_moban = self.com_moban.currentText()
        mb_file_path = os.path.join(MOBAN_PATH,cur_moban)
        ret = []
        with open(mb_file_path,'r',encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                input_text = line.replace('\n','')
                try:
                    gc = Genner_Com(input_text, project_name)
                    values = gc.value
                    ret+=values
                except Exception as e:
                    QMessageBox.warning(self, '', e.__str__())
                    print(e.__str__())
            self.te_printer.clear()
            for item in ret:
                if item.strip()=='':
                    continue
                self.te_printer.append(item)

            self.repaint()



# 分发
    def fenfa(self):
        self.te_view.clear()
        self.save_arg_model()
        sql_arg = self.get_current_arg()
        fenfs = []
        fenfa_dats=[]
        try:
            viewer = Reader_Factory.get_instance(sql_arg)
            ct = '\n'.join(viewer.items)
            arg_models = sql_arg.arg_model.where(ARG_model.rn != 0).order_by(ARG_model.rn).execute()
            for item in arg_models:
                print(item.arg_model)
                if item.arg_model == '变量分发':
                    fenfs.append(item.arg_contorl)
            for fefitem in fenfs:
                self.save_arg_context_by_name(name=fefitem,context=ct)
                sql_arg1 = self.get_sql_arg_by_name(fefitem)
                viewer = Reader_Factory.get_instance(sql_arg1)
                fenfa_dats.append(viewer.items)
            for x,y in zip(fenfs,fenfa_dats):
                if type(x) == str:
                    self.te_view.append(f"********************{x}********************")
                else:
                    self.te_view.append(f"********************${str(x)}********************")
                for i in y:
                    if type(x) == str:
                        self.te_view.append(i)
                    else:
                        self.te_view.append(str(i))
            self.repaint()
        except Exception as e:
            QMessageBox.warning(self,'',e.__str__())


    def li_complex_text_change(self):
        pos = self.li_complex.cursorPosition()
        text = self.li_complex.text()
        # a = Ui_args()
        if text[pos-2:pos] == "${":
            print('查询')



    def remove_arg_model(self):
        result = QMessageBox.question(self, "提醒", "是否删除内容", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.No:
            return
        try:
            current_row = self.ta_model_list.currentRow()
            pk = int(self.ta_model_list.item(current_row,3).text())
            ARG_model.delete_by_id(pk)
            self.init_ta_model_list()
            self.repaint()
        except Exception:
            return


    def save_arg(self):
        '''保存arg'''
        name = self.com_arg.currentText()
        if (name == None or name.strip() == ''): return
        sql_arg = SQL_arg.get(SQL_arg.project_name == self.com_project_name.currentText()
                              , SQL_arg.arg_nike == name)
        data= self.te_input.toPlainText()
        sql_arg.arg_context = data.strip()
        sql_arg.save()

    def save_arg_context_by_name(self,name,context):
        '''保存arg'''
        name = name
        if (name == None or name.strip() == ''): return
        try:
            sql_arg = SQL_arg.get(SQL_arg.project_name == self.com_project_name.currentText()
                                  , SQL_arg.arg_nike == name)
            sql_arg.arg_context = context.strip()
            sql_arg.save()
        except Exception:
            raise ValueError(f'没有变量{name}')


    def relaod_history(self):
        '''加载历史数据'''
        key = self.com_history.currentText()
        # if key == '' :return
        # values = eval(self.mycach[key])
        # self.te_printer.clear()
        # for item in values:
        #     self.te_printer.append(item)
        self.li_complex.setText(key)
        self.repaint()

    def help(self):
        '''帮助按钮'''
        self.te_view.setText(HELP_TEXT)
        self.init_com_moban()
        self.repaint()

    def rm_line(self):
        '''去除特定行'''
        self.stack.append(self.te_input.toPlainText())
        text, okPressed = QInputDialog.getText(self, "请输入去除行的正则表达式", "正则表达式:", QLineEdit.Normal, "")
        if okPressed :
            ret = []
            tmp = self.te_input.toPlainText()
            tp_list = tmp.split('\n')
            if text!='':
                re_com = re.compile(text)
                for item in tp_list:
                    if re.search(re_com,item) != None :
                        ret.append(item)
            else:
                for item in tp_list:
                    if item.strip()!='' :
                        ret.append(item)

            self.te_input.setText('\n'.join(ret))
            self.save_arg()
            self.repaint()

    def be_back(self):
        try:
            self.te_input.setText(self.stack.pop())
            self.repaint()
        except:
            pass

    def split_line(self):
        '''分割换行'''
        self.stack.append(self.te_input.toPlainText())
        text, okPressed = QInputDialog.getText(self, "请输入换行符", "换行符:", QLineEdit.Normal, "")
        if okPressed and len(text)>0:
            ret = []
            tmp = self.te_input.toPlainText()
            tp_list = tmp.split('\n')
            for item in tp_list:
                tmp_items = item.split(text)
                ret += tmp_items
            self.te_input.setText('\n'.join(ret))
            self.save_arg()
            self.repaint()

    def copy(self):
        '''复制arg'''
        self.stack.append(self.te_input.toPlainText())
        text, okPressed = QInputDialog.getText(self, "请输入新的参数名称", "新参数名称:", QLineEdit.Normal, "")
        sql_arg = self.get_current_arg()
        arg_model = sql_arg.arg_model.execute()
        if okPressed and text!='':
            copy_itme = SQL_arg(
                project_name = sql_arg.project_name
                ,arg_context = sql_arg.arg_context
                ,arg_nike = text
            )
            copy_itme.save()

            for item in arg_model:
                tmp = ARG_model(
                    arg_name = copy_itme
                    ,rn = item.rn
                    ,arg_model = item.arg_model
                    ,arg_contorl = item.arg_contorl
                )
                tmp.save()
        self.init_com_arg()
        self.com_arg.setCurrentText(text)



    def remove_arg(self):
        result = QMessageBox.question(self, "提醒", "是否删除内容", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.No:
            return
        name = self.com_arg.currentText()
        p_name = self.com_project_name.currentText()
        if (p_name.strip()=='' or p_name == None):
            QMessageBox.warning(self,'','请先选择工程')
            return
        if (name.strip()=='' or name == None):
            QMessageBox.warning(self,'','参数名不能为空')
            return
        project_name =Project_detail.get_by_id(p_name)
        sql_arg = SQL_arg.get_or_none(SQL_arg.arg_nike ==name,SQL_arg.project_name ==project_name)
        if (sql_arg==None):return
        sql_arg.delete_instance()
        self.init_com_arg()

    def decode_args(self,arg):
        tmp = arg.split('\n')
        while True:
            try:
                tmp.remove('')
            except:
                return tmp

    def view_and_copy(self):
        self.view()
        tmp = self.te_view.toPlainText()
        pyperclip.copy(tmp)
    def view(self):
        '''预览保存'''
        self.save_arg_model()
        sql_arg = self.get_current_arg()
        try:
            viewer = Reader_Factory.get_instance(sql_arg)
            self.te_view.clear()
            for item in viewer.items:
                if type(item) == str:
                    self.te_view.append(item)
                else:
                    self.te_view.append(str(item))
            self.repaint()
        except ValueError as e:
            QMessageBox.warning(self,'',e.__str__())

    def decode_com(self,sql_args):
        com = None
        if sql_args.arg_model == '字符串切割':
            com = sql_args.arg_contorl.replace('${arg}', 'item')
        return com

    def decode_context(self,sql_arg):
        tmps = self.decode_args(sql_arg.arg_context)
        com = self.decode_com(sql_arg)
        ret = []
        for item in tmps:
            ret.append(eval(com))
        return Arg_Value(sql_arg.arg_name,ret)

    def init_arg(self,sql_args):
        '''装载'''
        ret = {}
        for item in sql_args:
            ret[item.arg_nike] = self.decode_context(item)
        return ret

    def str_to_func(self,func_str):
        # 将字符串转化为ast语法树
        try:
            func_ast = ast.parse(func_str.strip())
            # 获取函数定义节点
            func_def = func_ast.body[0]
            # 将ast语法树转化为函数对象
            func = compile(func_ast, "<string>", "exec")
            # 创建一个空的命名空间
            namespace = {}
            # 执行函数定义节点，将函数对象存储在命名空间中
            exec(func, namespace)
            # 获取函数对象
            func_obj = namespace[func_def.name]
            return func_obj
        except Exception as e:
            raise ValueError('自定义函数不正确')

    #${字段名称}[:1] comment '${临时表名}'
    def gener_sql(self):
        '''生成语句'''
        p_name =  self.com_project_name.currentText()
        input_text = self.li_complex.text()
        project_name =Project_detail.get_by_id(p_name)
        try:
            gc = Genner_Com(input_text,project_name)
            values = gc.value
            self.te_printer.clear()
            ret = ''
            for item in values:
                ret += item
                ret += '\n'

            

            # 开始执行修饰器
            for xsq_name in self.init_xsq_list():
                if xsq_name == '':
                    continue
                xsq_path = os.path.join(GEN_PATH, XSQ_PATH, xsq_name)
                print(f'修饰器地址:{xsq_path}')
                with open(xsq_path, 'r', encoding='utf-8') as f:
                    xsq_content = f.read()
                    func_obj = self.str_to_func(xsq_content)
                    ret = func_obj(ret)
            # 读取修饰器，并执行
            self.te_printer.setText(ret)    
            
            History(project_name=project_name
                    , genner_str=input_text
                    , ret=values
                    ).save()
            self.init_com_history()
            self.repaint()
        except Exception as e:
            QMessageBox.warning(self,'',e.__str__())
            print(e.__str__())



    def load_args(self):
        '''加载参数'''
        name = self.com_arg.currentText()
        if (name == None or name.strip() ==''):return
        sql_arg = SQL_arg.get(SQL_arg.project_name == self.com_project_name.currentText()
                              ,SQL_arg.arg_nike == name)
        print(f'{name}:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@加载参数:{sql_arg.arg_context}')

        self.te_input.setText(sql_arg.arg_context)
        self.te_view.setText(HELP_TEXT)
        # pyperclip.copy('${'+name+'}')
        self.init_ta_model_list()
        self.view()
        self.repaint()



    def add_arg(self):
        '''添加参数'''
        name = self.li_arg.text()
        p_name = self.com_project_name.currentText()
        if (p_name.strip()=='' or p_name == None):
            QMessageBox.warning(self,'','请先选择工程')
            return
        if (name.strip()=='' or name == None):
            QMessageBox.warning(self,'','参数名不能为空')
            return
        project_name =Project_detail.get_by_id(p_name)

        sql_arg = SQL_arg.get_or_none(SQL_arg.arg_nike ==name,SQL_arg.project_name ==project_name)
        if (sql_arg==None):
            tmp = SQL_arg(arg_nike =name,project_name =project_name)
            tmp.save(force_insert=True)
            self.init_com_arg()
            self.com_arg.setCurrentText(name)
        else:
            QMessageBox.warning(self, '', '参数已存在')
            return
        self.te_input.clear()
        self.repaint()


    def remove_project(self):
        '''删除工程'''
        result = QMessageBox.question(self, "提醒", "是否删除内容", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.No:
            return
        name = self.com_project_name.currentText()
        tmp = Project_detail.delete().where(Project_detail.project_name == name).execute()
        self.init_com_project_name()
        if tmp ==1:
            QMessageBox.information(self, '', '删除工程:{}成功'.format(name))
        else:
            QMessageBox.warning(self,'','没有要删除的工程')

    def add_project(self):
        '''添加工程'''
        name = self.li_project_name.text()
        tmp, created = Project_detail.get_or_create(project_name=name)

        try:            # tmp,created = Project_detail.get_or_create(project_name = name)
            if not created:
                self.com_project_name.setCurrentText(name)
                QMessageBox.information(self, '', '打开工程:{}成功'.format(name))
            else:
                self.init_com_project_name()
                self.com_project_name.setCurrentText(name)
                QMessageBox.information(self, '', '创建工程:{}成功'.format(name))
        except Exception as e:
            print(e.__str__())


from qt_material import apply_stylesheet


try:
    app = QApplication([])
    stats = MainWindow()
    # apply_stylesheet(app, theme='light_lightgreen.xml')

    stats.show()

    app.exec()
finally:
    pass

