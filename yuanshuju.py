import logging
from datetime import datetime, timedelta
import pyperclip
from collections import deque
import os
import re
from asyncio import sleep
from concurrent.futures import ThreadPoolExecutor

from add_table_by_ddl import ADD_TABLE
from clinet.yuanshuju_ui import Ui_Form
from clinet.create_xq_ui import Ui_create_xq
import pyperclip
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import QRegularExpression

from PySide6.QtCore import QTime, QDateTime
from PySide6.QtGui import Qt, QIcon, QKeySequence, QStandardItemModel, QTextCursor, QSyntaxHighlighter, QTextCharFormat, \
    QFont, QShortcut, QAction
from PySide6.QtWidgets import QTextEdit, QApplication, QMessageBox, QDateTimeEdit, QLineEdit, QPushButton, QTextBrowser, \
    QFormLayout, QHBoxLayout, QComboBox, QInputDialog, QMainWindow, QFileDialog, QTableWidget, QTableWidgetItem, \
    QHeaderView, QAbstractItemView, QWidget, QTableView, QDialog, QVBoxLayout, \
    QDialogButtonBox, QLabel, QToolTip, QMenu, QRadioButton, QStackedWidget
from PySide6.QtGui import QStandardItem


from model.model import Project_detail, SQL_arg, History, dp, create_tables, ARG_model, db, XQ_INFO, JB_INFO, YSJ_KJ, \
    XQ_TABLE_INFO, TABLE_COLUM_INFO, TABLE_INFO
from collections import deque
import subprocess
from conf import VS_PATH, SJTC_MOBAN_PATH,ZDGL_MAX_CNT
from sql_helper.util import FIFOdict
from pygments import highlight
from pygments.lexers import SqlLexer
from pygments.formatters import HtmlFormatter

VS_PATH=VS_PATH
ZDGL_MAX_CNT = ZDGL_MAX_CNT

mhsheet = """
        QTableView {
            background-color: #f2f2f2;
            border: 1px solid #ccc;
            font-family: Arial;
            font-size: 16px;
        }

        QTableView::item {
            padding: 5px;
            border: none;
        }

        QTableView::item:selected {
            background-color: #b3d9ff;
        }
"""
kj_header =['编号','需求名称','口径名称','版本','口径行号','文件位置']
KJ_HEADER_BH=0
KJ_HEADER_XQMC=1
KJ_HEADER_KJMC=2
KJ_HEADER_BB=3
KJ_HEADER_KJHH=4
KJ_HEADER_WJWZ=5


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)

        self.highlightingRules = []

        # 定义需要高亮显示的规则
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(Qt.blue)
        keywords = ["@das"]
        for word in keywords:
            pattern = QRegularExpression("\\b" + word + "\\b")
            rule = (pattern, keywordFormat)
            self.highlightingRules.append(rule)

        # 定义注释的高亮显示规则
        commentFormat = QTextCharFormat()
        commentFormat.setForeground(Qt.red)
        commentFormat.setFontWeight(QFont.Bold)
        commentPattern = QRegularExpression("-- >>")
        self.highlightingRules.append((commentPattern, commentFormat))

    def highlightBlock(self, text):
        for rule in self.highlightingRules:
            pattern = rule[0]
            format = rule[1]
            expression = QRegularExpression(pattern)
            match = expression.match(text)
            index = match.capturedStart()
            while index >= 0:
                length = match.capturedLength()
                self.setFormat(index, length, format)
                match = expression.match(text, index + length)
                index = match.capturedStart()


jb_header =['脚本编号','需求名称','文件名称','备注','版本号','路径','行数']
jb_header_id=0
jb_header_xqmc=1
jb_header_wjmc=2
jb_header_bz=3
jb_header_bbh=4
jb_header_lj=5
jb_header_line=6


class SqlHighlighter:
    def __init__(self, sql_code):
        self.sql_code = sql_code

    def get_highlighted_html(self):
        # 使用 pygments 生成带有语法高亮的 HTML 代码
        formatter = HtmlFormatter(style='colorful', full=True)
        highlighted_code = highlight(self.sql_code, SqlLexer(), formatter)

        style = """
        <style>
            .highlight {
                background: #f8f8f8;
                font-family: monospace;
                font-size: 18px;
                line-height: 1.5;
                padding: 10px;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            .k { color: #005cc5 !important; } /* 关键字 */
            .n { color: #24292e !important; } /* 普通文本 */
            .o { color: #d73a4a !important; } /* 运算符 */
            .s { color: #032f62 !important; } /* 字符串 */
            .c { color: #6a737d !important; } /* 注释 */
            .err { color: #d73a4a !important; } /* 错误 */
            .p { color: #d73a4a !important; } /* 标点符号 */
            .cm { color: #6a737d !important; } /* 单行注释 */
            .cp { color: #005cc5 !important; } /* 预处理器指令 */
            .c1 { color: #6a737d !important; } /* 注释 */
            .cs { color: #6a737d !important; } /* 块注释 */
            .ge { color: #24292e !important; } /* 泛型 */
            .gs { font-weight: bold !important; } /* 强调 */
            .kc { color: #005cc5 !important; } /* 关键字常量 */
            .kd { color: #005cc5 !important; } /* 关键字声明 */
            .kn { color: #005cc5 !important; } /* 关键字命名空间 */
            .kp { color: #005cc5 !important; } /* 关键字参数 */
            .kr { color: #005cc5 !important; } /* 关键字保留 */
            .kt { color: #d73a4a !important; } /* 关键字类型 */
            .ld { color: #032f62 !important; } /* 字面量 */
            .m { color: #24292e !important; } /* 数字 */
            .s1 { color: #032f62 !important; } /* 单引号字符串 */
            .s2 { color: #032f62 !important; } /* 双引号字符串 */
            .sb { color: #032f62 !important; } /* 块字符串 */
            .sc { color: #032f62 !important; } /* 字符 */
            .sd { color: #032f62 !important; } /* 文档字符串 */
            .se { color: #032f62 !important; } /* 特殊转义字符 */
            .sh { color: #032f62 !important; } /* shell 命令 */
            .si { color: #032f62 !important; } /* 插入变量 */
            .sx { color: #032f62 !important; } /* shell 命令 */
            .sr { color: #032f62 !important; } /* 正则表达式 */
            .ss { color: #032f62 !important; } /* 符号 */
            .vc { color: #005cc5 !important; } /* 变量常量 */
            .vg { color: #005cc5 !important; } /* 变量全局 */
            .vi { color: #005cc5 !important; } /* 变量实例 */
            .vm { color: #005cc5 !important; } /* 变量成员 */
            .il { color: #24292e !important; } /* 整数 */
        </style>
        """

        return style + highlighted_code
        # return highlighted_code
class CJJS_UI(QWidget):
    ## 超级检索
    def __init__(self,xqids):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self,'超级检索')
        self.tb_ysj:QTableView=self.ui.tb_ysj
        self.li_search:QLineEdit = self.ui.lineEdit
        self.li_search.setPlaceholderText('--.*{输入查询的注释行的关键字}&{关键字}&!{过滤的关键字}')
        # self.bt_kj:QPushButton=self.ui.bt_kj
        # self.bt_kj.clicked.connect(self.f_bt_kj)
        self.tb_ysj.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_ysj.horizontalHeader().setStretchLastSection(True)

        self.tb_ysj.setSortingEnabled(True)
        self.tb_ysj.resizeColumnsToContents()

        self.is_zd: QRadioButton = self.ui.is_zd
        self.tx_yl: QTextBrowser = self.ui.tx_yl
        # highlighter = SyntaxHighlighter(self.tx_yl.document())
        self.xqids = xqids # 查询的需求范围
        shortcut2 = QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Return), self)
        shortcut2.activated.connect(self.cjjs)
        self.tb_ysj.clicked.connect(self.show_ysj)
        self.tb_ysj.doubleClicked.connect(self.dbc_ysj)
    def get_row_content(self,index):
        try:
        # 获取行内容
            row = [index.model().data(index.sibling(index.row(), column), Qt.DisplayRole) for column in
                   range(index.model().columnCount())]
            return row
        except Exception as e:
            raise ValueError('未正确选择行')

    #判断内容是否在文件中
    def check_regex_in_file(self,regex, file_path,xgstr):
        ret = False
        # 是否取反标记
        flag = False
        if regex.startswith('!'):
            flag = True
            regex = regex[1:]
        if not os.path.exists(file_path):
            return ret
        if re.search(regex, xgstr,re.IGNORECASE):
            ret = True
        else:
            with open(file_path, 'r',encoding='utf8') as file:
                for line_number, line in enumerate(file, start=1):

                    if re.search(regex, line,re.IGNORECASE):
                        ret = True
                        break
        if flag:
            ret = not ret
        if ret:
            return 1
        else:
            return 0
    def cjjs(self):
        model = QStandardItemModel()
        self.tb_ysj.setStyleSheet(mhsheet)
        self.tb_ysj.setEditTriggers(QTableView.NoEditTriggers)
        for column, name in enumerate(jb_header):
            header_item = QStandardItem(name)
            model.setHorizontalHeaderItem(column, header_item)
        self.tb_ysj.setModel(model)
        if len(self.xqids)==0:
            items = JB_INFO.select()
        else:
            items = JB_INFO.select().where(JB_INFO.xq_id.in_(self.xqids))
        gjz = self.li_search.text()
        # 支持与查询
        gjz_list = gjz.split('&')

        for item in items:
            id = str(item.id)
            xq_name = item.xq_id.name
            name = item.name
            bz = item.desc
            version = str(item.version)
            path = item.path
            line =1
            xgstr = f'{xq_name},{name},{bz}'
            for v in gjz_list:
                tmp =self.check_regex_in_file(v,path,xgstr)
                line = line * tmp
                if tmp ==0:
                    break

            if line>0:
                row_items = [QStandardItem(i) for i in [id, xq_name, name,bz, version, path,'#']]
                model.appendRow(row_items)
                self.tb_ysj.setModel(model)
                self.repaint()

    def show_ysj(self):
        idx = self.tb_ysj.currentIndex()
        if idx.isValid():
            datas = self.get_row_content(idx)
            pth = datas[jb_header_lj]
            line = datas[jb_header_line]
            with open(pth, 'r', encoding='utf8') as f:
                lines = f.readlines()
            str = ''
            for l_str in lines:
                str += f'{l_str}'

            # 创建 SQL 高亮器
            highlighter = SqlHighlighter(str)
            # 获取带有语法高亮的 HTML 代码
            highlighted_html = highlighter.get_highlighted_html()

            # 设置 QTextBrowser 的内容为带有语法高亮的 HTML 代码
            self.tx_yl.setHtml(highlighted_html)

            self.tb_ysj.show()
    def dbc_ysj(self):
        idx = self.tb_ysj.currentIndex()
        if idx.isValid():
            datas = self.get_row_content(idx)
            pth = datas[jb_header_lj]
            line = datas[jb_header_line]
            subprocess.Popen(F'{VS_PATH} -g "{pth}"')


class YSJGL_UI(QWidget):
    ## 口径管理
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self,'口径管理')
        self.tb_ysj:QTableView=self.ui.tb_ysj
        self.li_search:QLineEdit = self.ui.lineEdit
        # self.bt_kj:QPushButton=self.ui.bt_kj
        # self.bt_kj.clicked.connect(self.f_bt_kj)
        self.li_search.textChanged.connect(self.init_tb_ysj)
        self.tb_ysj.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_ysj.horizontalHeader().setStretchLastSection(True)
        self.tb_ysj.doubleClicked.connect(self.dbc_ysj)
        self.tb_ysj.clicked.connect(self.show_ysj)
        self.init_tb_ysj()
        self.is_zd: QRadioButton = self.ui.is_zd
        self.is_zd.toggled.connect(self.f_is_zd)
        self.tx_yl: QTextBrowser = self.ui.tx_yl
        highlighter = SyntaxHighlighter(self.tx_yl.document())



    def f_is_zd(self, checked):
        flags = self.windowFlags()
        if checked:
            self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
        self.show()

    def get_row_content(self,index):
        try:
        # 获取行内容
            row = [index.model().data(index.sibling(index.row(), column), Qt.DisplayRole) for column in
                   range(index.model().columnCount())]
            return row
        except Exception as e:
            raise ValueError('未正确选择行')
    def dbc_ysj(self):
        idx = self.tb_ysj.currentIndex()
        if idx.isValid():
            datas = self.get_row_content(idx)
            pth = datas[KJ_HEADER_WJWZ]
            line = datas[KJ_HEADER_KJHH]
            subprocess.Popen(F'{VS_PATH} -g "{pth}":{line}')


    def show_ysj(self):
        idx = self.tb_ysj.currentIndex()
        if idx.isValid():
            datas = self.get_row_content(idx)
            pth = datas[KJ_HEADER_WJWZ]
            line = int(datas[KJ_HEADER_KJHH])
            try:
                with open(pth, 'r', encoding='utf8') as f:
                    lines = f.readlines()
                content = ''.join(lines)

                highlighter = SqlHighlighter(content)
                highlighted_html = highlighter.get_highlighted_html()

                self.tx_yl.setHtml(highlighted_html)

                cursor = self.tx_yl.textCursor()
                cursor.movePosition(QTextCursor.Start)

                # 把光标移动到中间
                for _ in range(line+9):
                    cursor.movePosition(QTextCursor.Down)




                self.tx_yl.setTextCursor(cursor)
                self.tx_yl.ensureCursorVisible()

                self.tb_ysj.show()
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "错误", f"无法读取文件: {e}")


    def init_tb_ysj(self):
        # 显示界面
        model = QStandardItemModel()
        for column, name in enumerate(kj_header):
            header_item = QStandardItem(name)
            model.setHorizontalHeaderItem(column, header_item)
        self.tb_ysj.setModel(model)
        items = YSJ_KJ.select().order_by(YSJ_KJ.mtime.desc())
        gjz_str = self.li_search.text().strip()
        gjz_list = gjz_str.strip('&')
        for gjz in gjz_list:
            gjz = gjz.upper()
            items = items.select().where(YSJ_KJ.name ** f'%{gjz}%')

        for item in items[:500]:
            id = str(item.id)
            xq_id = item.xq_id.name
            name = item.name
            version = str(item.jb_id.version)
            line = str(item.line)
            path = item.path
            row_items = [QStandardItem(i) for i in [id, xq_id, name, version,line, path]]
            model.appendRow(row_items)

        self.tb_ysj.setModel(model)
        self.tb_ysj.setStyleSheet(mhsheet)
        #列宽行高

        self.tb_ysj.setEditTriggers(QTableView.NoEditTriggers)
        self.repaint()


RWXY=['脚本编号','需求名称','需求类型','需求提出人','脚本名称','脚本版本','脚本地址']
RWXY_XQ_JBBH=0
RWXY_XQ_XQMC=1
RWXY_XQ_XQLX=2
RWXY_XQ_XQTCR=3
RWXY_XQ_JBMC=4
RWXY_XQ_JBBB=5
RWXY_XQ_JBDZ=6


class RWXY_UI(QWidget):
    # 任务血缘
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self,'任务血缘')
        self.tb_ysj:QTableView=self.ui.tb_ysj
        self.li_search:QLineEdit = self.ui.lineEdit

        self.li_search.textChanged.connect(self.init_tb_ysj)
        self.tb_ysj.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_ysj.horizontalHeader().setStretchLastSection(True)
        self.tb_ysj.doubleClicked.connect(self.dbc_ysj)
        self.tb_ysj.clicked.connect(self.f_tb_ysj)
        self.init_tb_ysj()
        self.tx_yl:QTextBrowser = self.ui.tx_yl

        self.is_zd: QRadioButton = self.ui.is_zd
        self.is_zd.toggled.connect(self.f_is_zd)
        # self.is_zd.setChecked(True)


    def f_is_zd(self, checked):
        flags = self.windowFlags()
        if checked:
            self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
        self.show()
    def get_row_content(self,index):
        try:
        # 获取行内容
            row = [index.model().data(index.sibling(index.row(), column), Qt.DisplayRole) for column in
                   range(index.model().columnCount())]
            return row
        except Exception as e:
            raise ValueError('未正确选择行')
    def dbc_ysj(self):
        idx = self.tb_ysj.currentIndex()
        if idx.isValid():
            datas = self.get_row_content(idx)
            pth = datas[RWXY_XQ_JBDZ]
            subprocess.Popen(F'{VS_PATH} -g "{pth}"')

    def f_tb_ysj(self):
        self.tx_yl.clear()
        idx = self.tb_ysj.currentIndex()
        if idx.isValid():
            datas = self.get_row_content(idx)
            id = datas[RWXY_XQ_JBBH]
            jb_info = JB_INFO.get_by_id(id)
            items  = XQ_TABLE_INFO.select().where(XQ_TABLE_INFO.jb_id==jb_info)
            shuru = []
            shuchu=[]
            for i in items:
                if i.table_type=='输入':
                    shuru.append(i.table_id.table_id)
                elif i.table_type=='输出':
                    shuchu.append(i.table_id.table_id)
            text_str = '-------------------------------输入表-------------------------------\n\t'
            if len(shuru)>0:
                text_str+='\n\t'.join(shuru)
            text_str+='\n'
            text_str += '-------------------------------输出表-------------------------------\n\t'
            if len(shuchu):
                text_str += '\n\t'.join(shuchu)
            self.tx_yl.setText(text_str)

    # RWXY = ['脚本编号', '需求名称', '需求类型', '需求提出人', '脚本名称', '脚本版本', '脚本地址']
    def init_tb_ysj(self):
        # 显示界面
        model = QStandardItemModel()
        for column, name in enumerate(RWXY):
            header_item = QStandardItem(name)
            model.setHorizontalHeaderItem(column, header_item)
        self.tb_ysj.setModel(model)
        gjz = self.li_search.text().strip()
        items = XQ_INFO.select().where(XQ_INFO.name ** f'%{gjz}%').order_by(XQ_INFO.mtime.desc())

        for uu in items:
            jbs = JB_INFO.select().where((JB_INFO.xq_id==uu)&(JB_INFO.version>0))
            for item in jbs:
                id = str(item.id)
                xqmc = uu.name
                xqlx = uu.xuqiu_type
                xqtcr=uu.tcr
                jbmc=item.name
                jbbb=str(item.version)
                jbdz = item.path
                row_items = [QStandardItem(i) for i in [id, xqmc,xqlx,xqtcr,jbmc,jbbb,jbdz]]
                model.appendRow(row_items)
        self.tb_ysj.setModel(model)
        self.tb_ysj.setStyleSheet(mhsheet)
        #列宽行高
        self.tb_ysj.setEditTriggers(QTableView.NoEditTriggers)
        self.repaint()


ZDXX=['字段名', '字段描述', '备注信息','字段类型', '表名', '表描述']
ZDXX_ZDMC=0
ZDXX_ZDMS=1
ZDXX_BZXX = 2
ZDXX_ZDLX=3
ZDXX_BM=4
ZDXX_BMS=5

class ZDGL_UI(QWidget):
    ## 字段管理
    def __init__(self,table_name =None,p_ck=None,is_zd = False,tupu_p=None):
        super().__init__()
        self.ui = Ui_Form()
        if not table_name:
            self.ui.setupUi(self,'字段管理')
        else:
            self.ui.setupUi(self, f'表-{table_name}')

        self.horizontalLayout:QHBoxLayout = self.ui.horizontalLayout

        self.bt_tz_parent = QPushButton(self)
        self.bt_tz_parent.setObjectName(u"bt_add_item")
        self.bt_tz_parent.setText('跳转上一级(CTRL+Z)')
        self.horizontalLayout.addWidget(self.bt_tz_parent)

        self.bt_tz_parent.clicked.connect(self.f_tz_parent)


        self.bt_add_item = QPushButton(self)
        self.bt_add_item.setObjectName(u"bt_add_item")
        self.bt_add_item.setText('添加字段')
        self.horizontalLayout.addWidget(self.bt_add_item)

        self.bt_add_item.clicked.connect(self.f_add_item)


        self.bt_rm_item = QPushButton(self)
        self.bt_rm_item.setObjectName(u"bt_add_item")
        self.bt_rm_item.setText('删除字段')
        self.horizontalLayout.addWidget(self.bt_rm_item)
        self.bt_rm_item.clicked.connect(self.f_rm_item)

        self.tupi_p = tupu_p
        if tupu_p:
            self.tupu_daoru = QPushButton(self)
            self.tupu_daoru.setObjectName(u"tupu_daoru")
            self.tupu_daoru.setText('导入知识图谱')
            self.horizontalLayout.addWidget(self.tupu_daoru)
            self.tupu_daoru.clicked.connect(self.f_tupu_daoru)

        self.tb_ysj:QTableView=self.ui.tb_ysj
        self.li_search:QLineEdit = self.ui.lineEdit

        # self.li_search.textChanged.connect(self.init_tb_ysj)
        self.tb_ysj.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tb_ysj.horizontalHeader().setStretchLastSection(True)
        self.tb_ysj.doubleClicked.connect(self.dbc_ysj)
        self.tb_ysj.clicked.connect(self.print_ysj)

        self.sjtc_dict = {}
        self.tx_yl: QTextBrowser = self.ui.tx_yl
        self.re_tn = re.compile(r'\S+\${SELECT_ZDMC_MS}')

        shortcut2 = QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Return), self)
        shortcut2.activated.connect(self.init_tb_ysj)
        self.table_name = table_name
        # if table_name:
        #     self.li_search.setText(table_name)
        self.init_tb_ysj()
        self.is_zd: QRadioButton = self.ui.is_zd
        self.is_zd.toggled.connect(self.f_is_zd)
        self.is_zd.setChecked(is_zd)
        self.p_ck = p_ck
        self.tb_name_k = table_name

        if self.p_ck:
            rect_pck = self.p_ck.geometry()
            rect = self.p_ck.geometry()
            if rect == rect_pck:
                self.move(rect.x() + 100, rect.y() + 100)

        shortcut3 = QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Z), self)
        shortcut3.activated.connect(self.f_tz_parent)


    def f_tupu_daoru(self):
        select_idxs = self.tb_ysj.selectedIndexes()

        _clist = []
        _ret = {}

        for i in select_idxs:
            tmp = self.get_row_content(i)
            col_name = tmp[ZDXX_ZDMC]
            col_desc = tmp[ZDXX_ZDMS]
            col_type = tmp[ZDXX_ZDLX]
            table_name = tmp[ZDXX_BM]
            table_desc = tmp[ZDXX_BMS]
            _tmp = {
                'name':f'{col_desc}|{col_name}'
                ,'col_name': col_name
                ,'col_type': col_type
                ,'col_desc': col_desc
                ,'labels':'字段'
                ,'table_name':table_name
                ,'table_desc': table_desc
                ,'uni_id':f'{table_name}.{col_name}'
            }
            _clist.append(_tmp)
            _ret = {
                'name':table_name
                ,'labels':'表'
                ,'_daoru_type':'父对子' # 父对子
                , 'table_name': table_name
                ,'table_desc':table_desc
                ,'uni_id':table_name
            }
        _ret['_clist']=_clist
        self.tupi_p.daoru_table(data=_ret)
        self.close()




    def f_tz_parent(self):
        if self.p_ck is None:
            QMessageBox.warning(self,'提醒','没有上一级')
        else:
            self.p_ck.is_zd.setChecked(True)
            self.p_ck.is_zd.setChecked(self.is_zd.isChecked())
            self.p_ck.showNormal()

            rect = self.geometry()
            rect_pck = self.p_ck.geometry()
            if rect== rect_pck:
                self.p_ck.move(rect.x()-100,rect.y()-100)

    def f_is_zd(self, checked):
        flags = self.windowFlags()
        if checked:
            self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
        self.show()
    def closeEvent(self, event):
        if self.p_ck is not  None and self.tb_name_k is not None:
            del self.p_ck.table_dict [self.tb_name_k]
            self.p_ck.init_tb_ysj_ydk()
        super().closeEvent(event)


    def f_rm_item(self):
        result = QMessageBox.question(self, "提醒", "是否删除内容", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.No:
            return
        idx = self.tb_ysj.currentIndex()
        datas = self.get_row_content(idx)
        col_name = datas[ZDXX_ZDMC]
        tb_name = datas[ZDXX_BM]
        id = f'${tb_name}.${col_name}'

        u = TABLE_COLUM_INFO.delete_by_id(id)
        self.init_tb_ysj()
    def f_add_item(self):
        table_id = self.table_name
        tzxx = self.show_rename_dialog('','', '','')
        if tzxx:
            id =  tzxx.get('zdm')
            if id.strip() =='':
                return
            zdmc = tzxx.get('zdmc')
            zdex = tzxx.get('tzxx')
            zdlx = tzxx.get('zdlx')
            clo_id = f'${table_id}.${id}'
            tb_id = TABLE_INFO.get_by_id(table_id)

            try:
                TABLE_COLUM_INFO.insert(
                    id =clo_id
                    ,tb_id = tb_id
                    ,col_name = id
                    ,col_type = zdlx
                    ,col_desc = zdmc
                    ,ex_text=zdex
                ).execute()
            except Exception as e:
                QMessageBox.warning(self,'异常提醒',f'添加字段异常{e.__str__()}')

            self.init_tb_ysj()

        # id = CharField(verbose_name='字段主键：库.表.字段名称', primary_key=True)
        # tb_id = ForeignKeyField(TABLE_INFO, on_delete='CASCADE')
        # col_name = CharField(verbose_name='字段名称', null=True)
        # col_type = CharField(verbose_name='字段类型', null=True)
        # col_desc = CharField(verbose_name='字段描述', null=True)
        # ex_text = CharField(verbose_name='特殊描述', null=True)

        # idx = self.tb_ysj.currentIndex()
        # datas = self.get_row_content(idx)
        # col_name = datas[ZDXX_ZDMC]
        # tb_name = datas[ZDXX_BM]
        # id = f'${tb_name}.${col_name}'
        # u = TABLE_COLUM_INFO.get_by_id(id)
        # tzxx = self.show_rename_dialog(u.ex_text, u.col_desc, u.col_type)
        # if tzxx:
        #     u.ex_text = tzxx.get('tzxx')
        #     u.col_desc = tzxx.get('zdmc')
        #     u.col_type = tzxx.get('zdlx')
        #     u.save()
        #     self.init_tb_ysj()



    # 元数据探查界面
    def contextMenuEvent(self, event):
        files = self.get_files_in_directory(SJTC_MOBAN_PATH)
        context_menu = QMenu(self)
        for file in files:
            if file.endswith('.txt'):
                tp_action = QAction(file, self)
                context_menu.addAction(tp_action)
                self.sjtc_dict[file] = tp_action
        action = context_menu.exec_(self.mapToGlobal(event.pos()))
        if action:
            idx = self.tb_ysj.currentIndex()
            datas = self.get_row_content(idx)
            ZDMC = datas[ZDXX_ZDMC]
            BM = datas[ZDXX_BM]
            TX_DATE = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
            TX_DATE_FORMAT = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            TX_MONTH = (datetime.today().replace(day=1) - timedelta(days=1)).strftime("%Y%m")
            select_idxs = self.tb_ysj.selectedIndexes()
            select_list = []
            select_ZDMC_list =[]
            select_ZDMS_list=[]
            select_ZDMC_MS_list = []
            select_RANGE_LIST = []
            select_ZDMC_MS_LS_list =[]
            ALTER_LIST = []
            SELECT_BT_LIST =[]
            SELECT_TO_EXCEL=[]
            tmp_range = 0
            for i in select_idxs:
                tmp = self.get_row_content(i)
                select_list.append(tmp)
                T_MC = tmp[ZDXX_ZDMC]
                T_MS = tmp[ZDXX_ZDMS]
                T_LX = tmp[ZDXX_ZDLX]
                select_ZDMC_list.append(T_MC)
                select_ZDMS_list.append(T_MS)
                select_ZDMC_MS_list .append(f"{T_MC} AS {T_MC} -- {T_MS}")
                select_ZDMC_MS_LS_list.append(f",{T_MC} {T_LX} COMMENT '{T_MS}'")
                ALTER_LIST.append(f"ALTER TABLE {BM} MODIFY {T_MC} {T_LX} COMMENT '{T_MS}';")
                SELECT_BT_LIST.append((f"{T_MC} AS '{T_MS}'"))
                SELECT_TO_EXCEL.append(f"{T_MC}\t{T_MS}\t{T_LX}")
                tmp_range +=1
                select_RANGE_LIST.append(tmp_range.__str__())
            # str = f'\n-- {action.text()} \n'
            str = ''
            fname = os.path.join(SJTC_MOBAN_PATH,action.text())
            with open(fname,'r',encoding='utf8') as f:
                lines = f.readlines()
            fs = ' '.join(lines)
            matches = self.re_tn.findall(fs)
            if len(matches) >= 1:
                TN = matches[0]
                TN = TN.replace('.${SELECT_ZDMC_MS}','')
                # print(TN)
            else:
                TN =''

            GJZ_DICT = {
                "ZDMC":ZDMC
                ,"BM":BM+f' {TN}'
                ,"TX_DATE":TX_DATE
                ,"TX_DATE_FORMAT":TX_DATE_FORMAT
                ,"TX_MONTH":TX_MONTH
                ,'SELECT_ZDMC':','.join(select_ZDMC_list)
                ,'SELECT_ZDMC_MS':f'\n,{TN}.'.join(select_ZDMC_MS_list)
                ,'SELECT_ZDMC_RANGE':','.join(select_RANGE_LIST)
                ,'SELECT_ZDMC_MS_LS':'\n'.join(select_ZDMC_MS_LS_list)
                ,'ALTER_LIST':'\n'.join(ALTER_LIST)
                ,'SELECT_BT_LIST':'\n\t,'.join(SELECT_BT_LIST)
                ,'SELECT_TO_EXCEL':'\n'.join(SELECT_TO_EXCEL)
            }
            for line in lines:
                if line.startswith('-- '):
                    continue
                tmp = line
                for gjz in GJZ_DICT.keys():
                    tmp = tmp.replace('${'+gjz+'}',GJZ_DICT.get(gjz))
                str+= tmp
            pyperclip.copy(str)
            self.tx_yl.append(str)


    def get_files_in_directory(self,directory):
        files = []
        try:
            for filename in os.listdir(directory):
                if os.path.isfile(os.path.join(directory, filename)):
                    files.append(filename)
            return files
        except Exception as e:
            raise Exception(f"模版路径不正确{SJTC_MOBAN_PATH}")
    def get_row_content(self,index):
        try:
        # 获取行内容
            row = [index.model().data(index.sibling(index.row(), column), Qt.DisplayRole) for column in
                   range(index.model().columnCount())]
            return row
        except Exception as e:
            raise ValueError('未正确选择行')

    def show_rename_dialog(self, tzxx,zdmc,zdlx,zdm=None):
        # 创建一个修改需求的对话框
        dialog = QDialog()
        dialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        dialog.setWindowTitle('编辑信息')
        dialog.setFixedSize(600, 300)
        layout = QVBoxLayout()


        lb0 = QLabel()
        lb0.setText('字段名称')
        in_zdm = QLineEdit()
        in_zdm.setText(zdm)
        layout.addWidget(lb0)
        layout.addWidget(in_zdm)

        if zdmc != '':
            in_zdm.setEnabled(False)

        lb1 = QLabel()
        lb1.setText('字段描述')
        in_zdmc = QLineEdit()
        in_zdmc.setText(zdmc)
        layout.addWidget(lb1)
        layout.addWidget(in_zdmc)

        # 需求名称
        lb2 = QLabel()
        lb2.setText('备注')
        in_tzxx = QLineEdit()
        in_tzxx.setText(tzxx)

        layout.addWidget(lb2)
        layout.addWidget(in_tzxx)

        # 需求名称
        lb3 = QLabel()
        lb3.setText('字段类型')
        in_zdlx = QLineEdit()
        in_zdlx.setText(zdlx)

        layout.addWidget(lb3)
        layout.addWidget(in_zdlx)

        # 创建一个按钮框
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(button_box)
        # 设置按钮的点击事件
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        # 将布局设置给对话框
        dialog.setLayout(layout)
        # 显示对话框并等待用户点击按钮
        result = dialog.exec_()
        # 获取用户输入的文本
        if result == QDialog.Accepted:
            if zdm is None:
                return { 'tzxx': in_tzxx.text(),'zdmc':in_zdmc.text(),'zdlx':in_zdlx.text()}
            else:
                return {'tzxx': in_tzxx.text(), 'zdmc': in_zdmc.text(), 'zdlx': in_zdlx.text(),'zdm':in_zdm.text()}
        else:
            return {}
    def dbc_ysj(self):
        idx = self.tb_ysj.currentIndex()
        datas = self.get_row_content(idx)
        col_name = datas[ZDXX_ZDMC]
        tb_name = datas[ZDXX_BM]
        id = f'${tb_name}.${col_name}'
        u = TABLE_COLUM_INFO.get_by_id(id)
        tzxx = self.show_rename_dialog(u.ex_text,u.col_desc,u.col_type,u.col_name)
        if tzxx:
            u.ex_text = tzxx.get('tzxx')
            u.col_desc = tzxx.get('zdmc')
            u.col_type = tzxx.get('zdlx')
            u.save()
            self.init_tb_ysj()

    def print_ysj(self):
        idx = self.tb_ysj.currentIndex()
        datas = self.get_row_content(idx)
        col_name = datas[ZDXX_ZDMC]
        tb_name = datas[ZDXX_BM]
        bz = datas[ZDXX_BZXX]
        ms = datas[ZDXX_ZDMS]
        tb_ms = datas[ZDXX_BMS]
        str = f'表信息:{tb_name}-{tb_ms}\n' \
              f'字段信息:{col_name}-{ms}\n' \
              f'备注信息:{bz}\n'
        self.tx_yl.append(str)







    ZDXX = ['字段名', '字段描述', '备注信息', '字段类型', '表名', '表描述']

    def init_tb_ysj(self):
        # 显示界面
        model = QStandardItemModel()
        for column, name in enumerate(ZDXX):
            header_item = QStandardItem(name)
            model.setHorizontalHeaderItem(column, header_item)
        self.tb_ysj.setModel(model)

        gjz_str = self.li_search.text().strip()
        ret = []
        or_list = gjz_str.split('|')
        for and_list in or_list:
            if self.table_name is None:
                items = TABLE_COLUM_INFO.select().limit(500).join(TABLE_INFO).order_by(TABLE_INFO.by1.desc())
            else:
                items = TABLE_COLUM_INFO.select().where(TABLE_COLUM_INFO.tb_id == self.table_name).join(
                    TABLE_INFO).order_by(TABLE_INFO.by1.desc())

            gjz_list = and_list.split('&')
            for gjz in  gjz_list:
                gjz = gjz.upper()
                if self.table_name is None:
                    items = items.select().where(
                            ((TABLE_COLUM_INFO.col_name ** f'%{gjz}%')|(TABLE_COLUM_INFO.col_desc ** f'%{gjz}%')|(TABLE_COLUM_INFO.tb_id ** f'%{gjz}%'))
                        )
                else:
                    items = items.select().where(
                            ((TABLE_COLUM_INFO.col_name ** f'%{gjz}%')|(TABLE_COLUM_INFO.col_desc ** f'%{gjz}%'))
                        )
            for item in items:
                if item in ret:
                    continue
                else:
                    ret.append(item)

        # if '&' in gjz:
        #     gjzs = gjz.split('&')
        #     gjz = gjzs[0]
        #     a_str = gjzs[-1]
        #     t_items = TABLE_COLUM_INFO.select().where(
        #         ((TABLE_COLUM_INFO.col_name ** f'%{gjz}%')|(TABLE_COLUM_INFO.col_desc ** f'%{gjz}%')|(TABLE_COLUM_INFO.tb_id ** f'%{gjz}%'))
        #         &((TABLE_COLUM_INFO.col_name ** f'%{a_str}%')|(TABLE_COLUM_INFO.col_desc ** f'%{a_str}%'))
        #     ).join(TABLE_INFO).order_by(TABLE_INFO.by1.desc()).limit(500)
        # else:
        #     t_items = TABLE_COLUM_INFO.select().where(
        #         ((TABLE_COLUM_INFO.col_name ** f'%{gjz}%')|(TABLE_COLUM_INFO.col_desc ** f'%{gjz}%')|(TABLE_COLUM_INFO.tb_id ** f'%{gjz}%'))
        #     ).join(TABLE_INFO).order_by(TABLE_INFO.by1.desc()).limit(500)

        for item in ret[:500]:
            zdmc=item.col_name
            zdms=item.col_desc
            zdlx=item.col_type
            zdbzxx = item.ex_text
            bmc=item.tb_id.table_id
            bms=item.tb_id.desc
            row_items = [QStandardItem(i) for i in [zdmc,zdms,zdbzxx,zdlx,bmc,bms]]
            model.appendRow(row_items)

        self.tb_ysj.setModel(model)
        self.tb_ysj.setStyleSheet(mhsheet)
        #列宽行高

        self.tb_ysj.setEditTriggers(QTableView.NoEditTriggers)
        self.repaint()


BGL=['表名','备注', '描述']
BGL_BM=0
BGL_BZ=1
BGL_MS=2
class BGL_UI(QWidget):
    # 表管理，表维度分析输入输出的任务
    def __init__(self,tupu_p=None):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self,'表管理')
        self.tb_ysj:QTableView=self.ui.tb_ysj
        self.li_search:QLineEdit = self.ui.lineEdit

        self.horizontalLayout: QHBoxLayout = self.ui.horizontalLayout

        self.bt_add_ddl = QPushButton(self)
        self.bt_add_ddl.setObjectName(u"bt_add_ddl")
        self.bt_add_ddl.setText('创表语句导入表')
        self.horizontalLayout.addWidget(self.bt_add_ddl)
        self.bt_add_ddl.clicked.connect(self.f_add_ddl)

        self.tupu_p = tupu_p
        if tupu_p:
            self.tupu_daoru = QPushButton(self)
            self.tupu_daoru.setObjectName(u"tupu_daoru")
            self.tupu_daoru.setText('导入知识图谱')
            self.horizontalLayout.addWidget(self.tupu_daoru)
            self.tupu_daoru.clicked.connect(self.f_tupu_daoru)


        # self.li_search.textChanged.connect(self.init_tb_ysj)
        self.tb_ysj.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_ysj.horizontalHeader().setStretchLastSection(True)
        self.tb_ysj.doubleClicked.connect(self.dbc_ysj)
        self.tb_ysj.clicked.connect(self.f_tb_ysj)
        self.init_tb_ysj()
        self.tx_yl:QTextBrowser = self.ui.tx_yl
        self.tb_ysj.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.zdui_dq = deque(maxlen=int(ZDGL_MAX_CNT))
        self.is_zd: QRadioButton = self.ui.is_zd
        self.is_zd.toggled.connect(self.f_is_zd)
        self.table_dict =FIFOdict(int(ZDGL_MAX_CNT))
        self.stacked_widget = QStackedWidget(self)





        self.tb_ysj_ydk:QTableView = QTableView(self)
        self.tb_ysj_ydk.setObjectName(u"tb_ysj_ydk")
        self.ui.verticalLayout.addWidget(self.tb_ysj_ydk)
        self.tb_ysj_ydk.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_ysj_ydk.horizontalHeader().setStretchLastSection(True)

        self.tb_ysj_ydk.doubleClicked.connect(self.dbc_ysj_ydk)

        shortcut2 = QShortcut(QKeySequence(Qt.CTRL | Qt.Key_Return), self)
        shortcut2.activated.connect(self.init_tb_ysj)

    # 图谱导入
    def f_tupu_daoru(self):
        self.dbc_ysj()

    def f_add_ddl(self):
        self.add_ui = ADD_TABLE(self)
        self.add_ui.showNormal()


    def f_is_zd(self, checked):
        flags = self.windowFlags()
        if checked:
            self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
        self.show()

    def contextMenuEvent(self, event):
        # 创建右键菜单
        menu = QMenu(self)
        # 创建QAction
        action = QAction("删除", self)
        action.triggered.connect(self.scb)
        # 将QAction添加到菜单中
        menu.addAction(action)

        action2 = QAction("备注", self)
        action2.triggered.connect(self.f_bzb)
        # 将QAction添加到菜单中
        menu.addAction(action2)
        # 显示菜单
        menu.exec_(event.globalPos())

    def show_rename_dialog(self,bms,tzxx):
        # 创建一个修改需求的对话框
        dialog = QDialog()
        dialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        dialog.setWindowTitle('编辑拓展信息')
        dialog.setFixedSize(600, 200)
        layout = QVBoxLayout()

        #表描述
        lb1 = QLabel()
        lb1.setText('表描述')
        in_bmss = QLineEdit()
        in_bmss.setText(bms)

        layout.addWidget(lb1)
        layout.addWidget(in_bmss)

        # 备注信息
        lb2 = QLabel()
        lb2.setText('备注信息')
        in_tzxx = QLineEdit()
        in_tzxx.setText(tzxx)

        layout.addWidget(lb2)
        layout.addWidget(in_tzxx)

        # 创建一个按钮框
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(button_box)
        # 设置按钮的点击事件
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        # 将布局设置给对话框
        dialog.setLayout(layout)
        # 显示对话框并等待用户点击按钮
        result = dialog.exec_()
        # 获取用户输入的文本
        if result == QDialog.Accepted:
            return { 'tzxx': in_tzxx.text(),'bmss':in_bmss.text()}
        else:
            return {}

    def f_bzb(self):
        idx = self.tb_ysj.currentIndex()
        datas = self.get_row_content(idx)
        bz = datas[BGL_BZ]
        id = datas[BGL_BM]
        ms = datas[BGL_MS]
        ret = self.show_rename_dialog(ms,bz)
        if ret =={}:
            return
        item = TABLE_INFO.get_by_id(id)
        item.by2 = ret.get('tzxx')
        item.desc = ret.get('bmss')
        item.save()
        self.init_tb_ysj()



    def scb(self):
        idx= self.tb_ysj.selectionModel().selectedRows(0)
        rms = [index.model().data(index.sibling(index.row(), 0), Qt.DisplayRole) for index in idx]
        for tb_name in rms:
            TABLE_INFO.delete_by_id(tb_name)
            TABLE_COLUM_INFO.delete().where(TABLE_COLUM_INFO.tb_id==tb_name).execute()

        self.init_tb_ysj()

    def get_row_content(self,index):
        try:
        # 获取行内容
            row = [index.model().data(index.sibling(index.row(), column), Qt.DisplayRole) for column in
                   range(index.model().columnCount())]
            return row
        except Exception as e:
            raise ValueError('未正确选择行')
    def open_zdui(self,tb_name):
        my_ui = self.table_dict.get(tb_name,None)
        if my_ui is None:
            my_ui = ZDGL_UI(tb_name,self, self.is_zd.isChecked(),tupu_p=self.tupu_p)
            self.table_dict[tb_name] = my_ui

        my_ui.hide()
        my_ui.showNormal()

        self.init_tb_ysj_ydk()



    def closeEvent(self, event):
        self.table_dict.clear()
        super().closeEvent(event)


    def dbc_ysj(self):
        idx = self.tb_ysj.currentIndex()
        datas = self.get_row_content(idx)
        table_name = datas[BGL_BM]
        self.open_zdui(table_name)

    def dbc_ysj_ydk(self):
        idx = self.tb_ysj_ydk.currentIndex()
        datas = self.get_row_content(idx)
        table_name = datas[BGL_BM]
        self.open_zdui(table_name)

    def f_tb_ysj(self):
        self.tx_yl.clear()
        idx = self.tb_ysj.currentIndex()
        if idx.isValid():
            datas = self.get_row_content(idx)
            id = datas[BGL_BM]
            items = XQ_TABLE_INFO.select().where(XQ_TABLE_INFO.table_id==id)
            shuru = []
            shuchu=[]
            for i in items:
                if i.table_type=='输入':
                    shuru.append(f"需求名称:{i.xq_id.name}\n脚本名称:{i.jb_id.name}\n脚本地址:{i.jb_id.path}\n")
                elif i.table_type=='输出':
                    shuchu.append(f"需求名称:{i.xq_id.name}\n脚本名称:{i.jb_id.name}\n脚本地址:{i.jb_id.path}\n")

            text_str = '-------------------------------使用-------------------------------\n'
            if len(shuru)>0:
                text_str+='\n'.join(shuru)
            text_str+='\n'
            text_str += '-------------------------------生成-------------------------------\n'
            if len(shuchu):
                text_str += '\n'.join(shuchu)
            self.tx_yl.setText(text_str)

    # BGL = ['表名', '描述']
    def init_tb_ysj(self):
        # 显示界面
        model = QStandardItemModel()
        for column, name in enumerate(BGL):
            header_item = QStandardItem(name)
            model.setHorizontalHeaderItem(column, header_item)
        self.tb_ysj.setModel(model)
        gjz_str = self.li_search.text().strip()
        gjz_list = gjz_str.split('&')

        items = TABLE_INFO.select().where(TABLE_INFO.desc.is_null(False)&(TABLE_INFO.desc!=''))
        for gjz in gjz_list:
            gjz = gjz.strip().upper()
            items = items.select().where((TABLE_INFO.table_id ** f'%{gjz}%')|(TABLE_INFO.desc ** f'%{gjz}%')|(TABLE_INFO.by2 ** f'%{gjz}%'))

        for item in items[:100]:
            table_id = item.table_id
            desc = item.desc
            bzxx =  item.by2
            row_items = [QStandardItem(i) for i in [table_id,bzxx,desc]]
            model.appendRow(row_items)
        self.tb_ysj.setModel(model)
        self.tb_ysj.setStyleSheet(mhsheet)
        #列宽行高
        self.tb_ysj.setEditTriggers(QTableView.NoEditTriggers)
        self.repaint()

    def init_tb_ysj_ydk(self):
        t_items = [i for i in self.table_dict.keys()]


        model = QStandardItemModel()
        for column, name in enumerate(BGL):
            header_item = QStandardItem(name)
            model.setHorizontalHeaderItem(column, header_item)
        self.tb_ysj_ydk.setModel(model)
        items = TABLE_INFO.select().where(TABLE_INFO.desc.is_null(False) & (TABLE_INFO.desc != ''))
        items = items.select().where(TABLE_INFO.table_id << t_items)
        for item in items:
            table_id = item.table_id
            desc = item.desc
            bzxx =  item.by2
            row_items = [QStandardItem(i) for i in [table_id,bzxx,desc]]
            model.appendRow(row_items)
        self.tb_ysj_ydk.setModel(model)
        self.tb_ysj_ydk.setStyleSheet(mhsheet)
        #列宽行高
        self.tb_ysj_ydk.setEditTriggers(QTableView.NoEditTriggers)
        self.repaint()
