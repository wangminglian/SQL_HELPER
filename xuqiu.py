import ctypes
import logging
import os
import stat
import time
import re
from asyncio import sleep
from concurrent.futures import ThreadPoolExecutor
from clinet.xuqiu_ui import Ui_Form
from clinet.create_xq_ui import Ui_create_xq
import pyperclip
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import QTime, QDateTime, QDir, QAbstractTableModel, QModelIndex
from PySide2.QtGui import Qt, QIcon, QKeySequence, QStandardItemModel, QColor
from PySide2.QtWidgets import QTextEdit, QApplication, QMessageBox, QDateTimeEdit, QLineEdit, QPushButton, QTextBrowser, \
    QFormLayout, QHBoxLayout, QComboBox, QInputDialog, QMainWindow, QFileDialog, QTableWidget, QTableWidgetItem, \
    QHeaderView, QAbstractItemView, QDesktopWidget, QAction, QShortcut, QWidget, QTableView, QDialog, QVBoxLayout, \
    QDialogButtonBox, QLabel, QToolTip, QRadioButton, QMenu
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QStandardItem
from peewee import SqliteDatabase, fn
from playhouse.shortcuts import model_to_dict
from collections import namedtuple
from model.model import Project_detail, SQL_arg, History, dp, create_tables, ARG_model, db, XQ_INFO, JB_INFO, YSJ_KJ, \
    XQ_TABLE_INFO, TABLE_INFO, TABLE_COLUM_INFO
from sql_helper.helper_restruct import Reader_Factory, Genner_Com
from collections import deque
import shutil
import subprocess
from conf import XUQIU_MOBAN_PATH,VSDX_PATH, GONGZUOQU_PATH, DATA_PATH, HSZ_PATH, VS_PATH, WPS_PATH, EDGE_PATH, LSJS_PATH, XQLX, \
    TXT_PATH,ZDXQ
from sql_helper.read_sql_file import Reader_SQL
from tijiaobanben import Submit_banben_UI
from yuanshuju import CJJS_UI

XUQIU_MOBAN_PATH = XUQIU_MOBAN_PATH
GONGZUOQU_PATH=GONGZUOQU_PATH
DATA_PATH = DATA_PATH
HSZ_PATH = HSZ_PATH
VS_PATH=VS_PATH
VSDX_PATH=VSDX_PATH
WPS_PATH=WPS_PATH
EDGE_PATH=EDGE_PATH
ZDXQ = ZDXQ
print(GONGZUOQU_PATH)
# XUQIU_TTYPE= ['任务','取数']
XUQIU_TTYPE = XQLX.split(',')

def get_files_in_directory(directory):
    files = []
    dirs = [] #文件夹
    try:
        for filename in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, filename)):
                files.append(filename)
            else:
                if filename=='代码':
                    continue
                dirs.append(filename)
        return files,dirs
    except Exception as e:
        raise Exception("Failed to execute script 'main' due to unhandled exception!")
class Create_XUQIU_UI(QWidget):
    def __init__(self,wb):
        super().__init__()
        self.ui = Ui_create_xq()
        self.ui.setupUi(self)
        self.tl_xqmc:QLineEdit = self.ui.lineEdit
        self.com_xqlx:QComboBox = self.ui.comboBox
        self.tl_tcr:QLineEdit = self.ui.lineEdit_2
        self.com_srmm:QComboBox=self.ui.comboBox_2
        self.com_scmm:QComboBox = self.ui.comboBox_3
        self.bt_qd :QPushButton =self.ui.pushButton
        self.bt_qd.clicked.connect(self.bcxq)
        self.wb = wb

        self.inint_xqlx()
        self.init_com_srmm()

    def init_com_srmm(self):
        #输入模版 输出模版初始化
        files,_ = get_files_in_directory(XUQIU_MOBAN_PATH)
        for i in files:
            if i.startswith('输入'):
                self.com_srmm.addItem(i)
            elif i.startswith('输出'):
                self.com_scmm.addItem(i)
            else:
                continue


    def inint_xqlx(self):
        #需求类型
        self.com_xqlx.clear()
        for i in XUQIU_TTYPE:
            self.com_xqlx.addItem(i)



    def init_xuqiu(self,name,srmb,scmb):
        #创建数据目录，如果目录已存在，则报错
        pt = os.path.join(DATA_PATH,name)
        srpt = os.path.join(XUQIU_MOBAN_PATH,srmb)
        srhz = srmb.split('.')[-1]
        scpt=os.path.join(XUQIU_MOBAN_PATH,scmb)
        schz = scmb.split('.')[-1]
        if os.path.exists(pt):
            raise ValueError('需求已存在，请勿重复创建')
        else:
            os.mkdir(pt)
            os.mkdir(os.path.join(pt,'代码'))
            shutil.copy(srpt,os.path.join(pt,f'输入-{name}.{srhz}'))
            shutil.copy(scpt,os.path.join(pt, f'输出-{name}.{schz}'))
        return pt


    def bcxq(self):
        # 确定，保存需求
        try:
            name = self.tl_xqmc.text()
            srmb = self.com_srmm.currentText()
            scmb = self.com_scmm.currentText()
            path = self.init_xuqiu(name,srmb,scmb)
            xuqiu_type = self.com_xqlx.currentText()
            status='开发中'
            tcr = self.tl_tcr.text()
            ret_dic = {'name':name,'path':path,'xuqiu_type':xuqiu_type,'status':status,'tcr':tcr}
            xq_info = XQ_INFO(**ret_dic)
            xq_info.save()
            self.wb.init_tb_xuqiu()
            self.close()
        except Exception as e:
            QMessageBox.warning(self, '', e.__str__())



xuqiu_header = ['id','需求名称','需求类型','需求状态','需求提出人','需求存储位置']
xuqiu_header_id =0
xuqiu_header_xqmc =1
xuqiu_header_xqlx =2
xuqiu_header_xqzt =3
xuqiu_header_xqtcr =4
xuqiu_header_xqccwz =5


xuqiu_dtl_header = ['id','类型','文件名','版本','备注','创建日期','更新日期','路径']
xuqiu_dtl_header_id=0
xuqiu_dtl_header_lx=1
xuqiu_dtl_header_wjm=2
xuqiu_dtl_header_bb=3
xuqiu_dtl_header_bz=4
xuqiu_dtl_ctime = 5
xuqiu_dtl_mtime = 6
xuqiu_dtl_header_lj=7
mhsheet="""
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


class MyTableView(QTableView):
    def __init__(self, parent=None,vv=None):
        super().__init__(vv)
        self.setMouseTracking(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def mouseMoveEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid():
            item = self.model().itemFromIndex(index)
            if item:
                QToolTip.showText(event.globalPos(), item.text())


class XUQIU_UI(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.tb_xuqiu:QTableView=self.ui.tb_xuqiu

        self.tb_xuqiu.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.bt_rename:QPushButton = self.ui.bt_rename
        self.bt_rename.clicked.connect(self.f_bt_rename)

        self.bt_create:QPushButton = self.ui.bt_create
        self.bt_create.clicked.connect(self.create_xuqiu)
        self.bt_remove:QPushButton=self.ui.bt_remove
        self.bt_remove.clicked.connect(self.remove_xuqiu)
        self.li_search:QLineEdit=self.ui.lineEdit
        model = QStandardItemModel()
        self.li_search.textChanged.connect(self.search_xuqiu)
        self.com_type:QComboBox = self.ui.com_type
        self.com_type.addItems(['','文档','脚本','文件夹'])
        self.com_type.currentTextChanged.connect(self.f_com_type)
        self.tb_xuqiudtl:QTableView =self.ui.tb_xuqiudtl



        self.com_sear_type:QComboBox=self.ui.com_sear_type
        self.com_sear_type.currentTextChanged.connect(self.init_tb_xuqiu)

        self.tb_xuqiudtl.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tb_xuqiudtl.setWordWrap(True)


        self.bt_new_jiaoben:QPushButton =self.ui.new_jiaoben
        self.bt_new_jiaoben.clicked.connect(self.new_jiaoben)
        self.bt_submit_jiaoben:QPushButton=self.ui.submit_jiaoben
        self.bt_submit_jiaoben.clicked.connect(self.submit_jiaoben)
        self.tb_xuqiudtl.doubleClicked.connect(self.op_wenjian)
        self.bt_rm_jb:QPushButton=self.ui.bt_rm_jb
        self.bt_rm_jb.clicked.connect(self.rm_jb)
        self.tb_xuqiu.setStyleSheet(mhsheet)

        for column, name in enumerate(xuqiu_header):
            header_item = QStandardItem(name)
            model.setHorizontalHeaderItem(column, header_item)
        self.tb_xuqiu.setModel(model)
        self.bt_daoru:QPushButton =self.ui.bt_daoru
        self.bt_daoru.clicked.connect(self.f_bt_daoru)

        self.bt_xqzt:QPushButton = self.ui.bt_xqzt
        self.bt_xqzt.clicked.connect(self.f_bt_xqzt)
        self.ra_banben:QRadioButton = self.ui.ra_banben

        self.tb_xuqiu.clicked.connect(self.dj_xuqiu)
        self.tb_xuqiu.doubleClicked.connect(self.ddj_xuqiu)
        self.li_search_wd:QLineEdit=self.ui.li_search_wd
        self.li_search_wd.textChanged.connect(self.f_com_type)
        self.init_tb_xuqiu()
        self.tb_xuqiu.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_xuqiu.horizontalHeader().setStretchLastSection(True)
        self.tb_xuqiudtl.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_xuqiudtl.horizontalHeader().setStretchLastSection(True)
        self.ra_banben.clicked.connect(self.f_com_type)

        self.bt_cjjs:QPushButton = self.ui.bt_cjjs
        self.bt_cjjs.clicked.connect(self.f_cjjs)

        self.read_sql_eng = Reader_SQL()
        self.com_sear_type.addItems(['开发中','','完成'])

        self.is_zd: QRadioButton = self.ui.is_zd
        self.is_zd.toggled.connect(self.f_is_zd)
        # self.is_zd.setChecked(True)
        
    def f_cjjs(self):
        select_idxs = self.tb_xuqiu.selectedIndexes()
        xqids = []
        for idx in select_idxs:
            datas = self.get_row_content(idx)
            item = datas[xuqiu_header_id]
            xqids.append(item)
        self.ysjgl_ui = CJJS_UI(xqids)
        self.ysjgl_ui.show()

    def contextMenuEvent(self, event):
        # 创建右键菜单
        menu = QMenu(self)
        # 创建QAction
        action = QAction("修改备注", self)
        action.triggered.connect(self.xgbz)

        action2 = QAction("复制文件", self)
        action2.triggered.connect(self.fzwj)
        # 将QAction添加到菜单中
        menu.addAction(action)
        menu.addAction(action2)
        #
        # action2 = QAction("备注", self)
        # action2.triggered.connect(self.f_bzb)
        # # 将QAction添加到菜单中
        # menu.addAction(action2)
        # 显示菜单
        menu.exec_(event.globalPos())

    #修改备注
    def xgbz(self):
        idx = self.tb_xuqiudtl.currentIndex()
        datas = self.get_row_content(idx)

        id = datas[xuqiu_dtl_header_id]
        bz = datas[xuqiu_dtl_header_bz]


        ret = self.show_rename_dialog2(bz)
        item = JB_INFO.get_by_id(id)
        if ret.get('bz'):
            item.desc = ret.get('bz')
        item.save()
        self.inint_tb_xuqiudtl(item.xq_id)


    # 复制文件到剪切版
    def fzwj(self):
        select_idxs = self.tb_xuqiudtl.selectedIndexes()
        path = []
        for idx in select_idxs:
            datas =self.get_row_content(idx)
            item = datas[xuqiu_dtl_header_lj]
            path.append(item)
        tmp = ','.join(path)
        str = f'Get-Item {tmp} | Set-Clipboard'
        args = ['powershell', str]
        subprocess.Popen(args =args)



    def show_rename_dialog2(self,bz):
        # 创建一个修改需求的对话框
        dialog = QDialog()
        dialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        dialog.setWindowTitle('修改备注')
        dialog.setFixedSize(600, 200)
        layout = QVBoxLayout()

        #备注信息
        lb1 = QLabel()
        lb1.setText('备注信息')
        in_bmss = QLineEdit()
        in_bmss.setText(bz)

        layout.addWidget(lb1)
        layout.addWidget(in_bmss)

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
            return { 'bz':in_bmss.text()}
        else:
            return {}



    def f_is_zd(self,checked):
        flags = self.windowFlags()
        if checked:
            self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
        self.show()


    def show_rename_dialog(self,xqlx,tcr,xqmc):
        # 创建一个修改需求的对话框
        dialog = QDialog()
        dialog.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        dialog.setWindowTitle('修改需求')
        dialog.setFixedSize(600,200)
        layout = QVBoxLayout()

        #需求名称
        lb2 = QLabel()
        lb2.setText('需求名称')
        in_xqmc = QLineEdit()
        in_xqmc.setText(xqmc)

        lb0 = QLabel()
        lb0.setText('需求类型')
        in_xqlx = QComboBox()
        in_xqlx.clear()
        in_xqlx.addItems(XUQIU_TTYPE)
        in_xqlx.setCurrentText(xqlx)
        # 创建一个输入框
        lb1 = QLabel()
        lb1.setText('提出人姓名')
        in_tcr = QLineEdit()
        in_tcr.setText(tcr)

        layout.addWidget(lb2)
        layout.addWidget(in_xqmc)
        layout.addWidget(lb0)
        layout.addWidget(in_xqlx)
        layout.addWidget(lb1)
        layout.addWidget(in_tcr)

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
            return {'xqlx':in_xqlx.currentText(),'tcr':in_tcr.text(),'xqmc':in_xqmc.text()}
        else:
            return {}
    def f_bt_rename(self):
        idx = self.tb_xuqiu.currentIndex()
        if idx.isValid():
            datas = self.get_row_content(idx)
            id = datas[0]
            itme = XQ_INFO.get_by_id(id)
            ret = self.show_rename_dialog(itme.xuqiu_type,itme.tcr,itme.name)
            itme.xuqiu_type = ret.get('xqlx')
            itme.tcr = ret.get('tcr')
            print(f"*******************{ ret.get('xqmc')}")
            itme.name = ret.get('xqmc')
            itme.save()
            self.init_tb_xuqiu()

    def f_bt_xqzt(self):
        idx = self.tb_xuqiu.currentIndex()
        if idx.isValid():
            datas = self.get_row_content(idx)
            id = datas[0]
            xq_info = XQ_INFO.get_by_id(id)
            if xq_info.status =='开发中':
                xq_info.status='完成'
            else:
                xq_info.status ='开发中'
            xq_info.save()
        self.init_tb_xuqiu()



    def f_bt_daoru(self):
        try:
            idx = self.tb_xuqiu.currentIndex()
            d_datas = self.get_row_content(idx)
            dpth = d_datas[-1]
            # 导入文件
            initial_dir = QDir(LSJS_PATH)
            file_dialog = QFileDialog()
            file_dialog.setDirectory(initial_dir)

            file_dialog.setFileMode(QFileDialog.ExistingFiles)
            file_dialog.setNameFilter("All files (*.*);;doc files (*.docx);;xls file (*.xlsx)")
            if file_dialog.exec_():
                file_paths = file_dialog.selectedFiles()
                for file_path in file_paths:
                    s_pth = file_path
                    shutil.copy(s_pth,dpth)
            self.f_com_type()
        except Exception as e:
            QMessageBox.warning(self,'',e.__str__())

# datas = self.get_row_content(index)
# path = datas[-1]
# os.startfile(path)
    def op_wenjian(self):
        idx = self.tb_xuqiudtl.currentIndex()
        datas = self.get_row_content(idx)
        print(datas[4])
        if datas[1]=='文档':
            if datas[-1].endswith('.pdf'):
                subprocess.Popen(F'{EDGE_PATH} "{datas[-1]}"')
            elif datas[-1].endswith('.txt') or datas[-1].endswith('.sql'):
                subprocess.Popen(f'{TXT_PATH} "{datas[-1]}"')
            elif datas[-1].endswith('.txt') or datas[-1].endswith('.vsdx'):
                subprocess.Popen(f'{VSDX_PATH} "{datas[-1]}"')
                # VSDX_PATH
            else:
                subprocess.Popen(F'{WPS_PATH} "{datas[-1]}"')
        elif datas[1]=='文件夹':
            path = datas[-1]
            os.startfile(path)
        else:
            subprocess.Popen(F'{VS_PATH}  "{datas[-1]}"')

    def set_file_permissions(self,file_path): #设置为可读可写
        try:
            # 获取文件属性
            file_attributes = ctypes.windll.kernel32.GetFileAttributesW(file_path)

            # 移除只读属性
            new_attributes = file_attributes & ~stat.FILE_ATTRIBUTE_READONLY

            # 设置新的文件属性
            ctypes.windll.kernel32.SetFileAttributesW(file_path, new_attributes)
            print(f"成功设置文件 {file_path} 为可读可写")
        except Exception as e:
            print(f"设置文件权限失败：{e}")
    def rm_jb(self):
        #删除脚本
        idx = self.tb_xuqiudtl.currentIndex()
        dts = self.get_row_content(idx)
        id = int(dts[0])
        if id>=0:
            data = JB_INFO.get_by_id(id)
            path = data.path
            if os.path.exists(path):
                self.set_file_permissions(path)
                os.remove(path)
            tmp = JB_INFO.get_by_id(id)
            kjs = YSJ_KJ.select().where(YSJ_KJ.jb_id == tmp)
            for i in kjs:
                YSJ_KJ.delete_by_id(i.id)
            JB_INFO.delete_by_id(id)
            xqis = XQ_TABLE_INFO.select().where(XQ_TABLE_INFO.jb_id==tmp)
            for i in xqis:
                XQ_TABLE_INFO.delete_by_id(i.id)
            self.f_com_type()
        else:
            QMessageBox.warning(self,'','文档请去对应目录自行删除')


    def show_input_dialog_submit(self):
        # 创建一个对话框
        dialog = QDialog()
        dialog.setWindowTitle('提交脚本')
        dialog.setFixedSize(600,200)
        layout = QVBoxLayout()
        lb1 = QLabel()
        lb1.setText('备注')
        in_bz = QLineEdit()
        layout.addWidget(lb1)
        layout.addWidget(in_bz)
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
            return {'bz':in_bz.text()}
        else:
            return {'bz':''}

    def submit_jiaoben(self):
        #提交版本
        try:
            index = self.tb_xuqiudtl.currentIndex()
            if index.isValid():
                index_datas = self.get_row_content(index)
                idx = int(index_datas[xuqiu_dtl_header_id])
                version = index_datas[xuqiu_dtl_header_bb]
                print(idx,version)
                if idx < 0 or version!='0':
                    raise ValueError('只可提交工作区代码（版本为0）')
                self.tijiaobanben_ui = Submit_banben_UI(idx)
                self.tijiaobanben_ui.show()

        except Exception as e:
            print(e.__str__())
            QMessageBox.warning(self,'',e.__str__())


    def new_jiaoben(self):
        # 新建脚本
        try:
            index = self.tb_xuqiu.currentIndex()
            if not index.isValid():
                return
            data = self.get_row_content(index)
            id = int(data[0])
            xq_id = XQ_INFO.get_by_id(id)
            diago = self.show_input_dialog(xq_id.name)
            if  diago.get('name') and diago.get('name').endswith('.sql'):
                pt =os.path.join(xq_id.path,diago.get('name'))
                if os.path.exists(pt):
                    QMessageBox.warning(self, '', '文件已存在，导入文件')
                else:
                    with open(pt,'w',encoding='utf-8') as f:
                        f.write(f"-- {diago.get('name')}::{diago.get('bz')}")
                name = diago.get('name')
                desc = diago.get('bz')
                type='脚本'
                version=0
                jb_info = JB_INFO()
                jb_info.xq_id = xq_id
                jb_info.name=name
                jb_info.desc=desc
                jb_info.type=type
                jb_info.version=0
                jb_info.path= pt
                jb_info.save()
                self.f_com_type()
            else:
                QMessageBox.warning(self,'','文件名为空或文件不合法')
                return
        except Exception as e:
            QMessageBox.warning(self,'',e.__str__())

    def show_input_dialog(self,name):
        # 创建一个对话框
        dialog = QDialog()
        dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)
        dialog.setWindowTitle('新建脚本')
        dialog.setFixedSize(600,200)
        layout = QVBoxLayout()

        lb0 = QLabel()
        lb0.setText('文件名称')
        in_name = QLineEdit()
        in_name.setText(f"{name}.sql")
        # 创建一个输入框
        lb1 = QLabel()
        lb1.setText('备注')
        in_bz = QLineEdit()
        layout.addWidget(lb0)
        layout.addWidget(in_name)
        layout.addWidget(lb1)
        layout.addWidget(in_bz)

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
            return {'name':in_name.text(),'bz':in_bz.text()}
        else:
            return {}


    def search_xuqiu(self):
        search_str = self.li_search.text()
        self.init_tb_xuqiu(search_str)


    def remove_xuqiu(self):
        #删除需求
        try:
            cur_index = self.tb_xuqiu.currentIndex()
            data = self.get_row_content(cur_index)
            id = int(data[0])
            pt = data[-1]
            shutil.move(pt,HSZ_PATH)
            XQ_INFO.delete_by_id(id)
            self.init_tb_xuqiu()
            
        except Exception as e:
            QMessageBox.warning(self,'',e.__str__())

    # xuqiu_dtl_header = ['id','类型', '文件名', '版本', '备注','创建日期','更新日期', '路径']
    def inint_tb_xuqiudtl(self,xq_item):
        files,dirs = get_files_in_directory(xq_item.path)
        if self.ra_banben.isChecked():
            items = JB_INFO.select().where(JB_INFO.xq_id==xq_item).order_by(JB_INFO.name)
        else:
            items = JB_INFO.select().where((JB_INFO.xq_id == xq_item) & (JB_INFO.version==0)).order_by(JB_INFO.name)
        model = QStandardItemModel()
        for column, name in enumerate(xuqiu_dtl_header):
            header_item = QStandardItem(name)
            model.setHorizontalHeaderItem(column, header_item)
        ct = self.com_type.currentText()
        datas = []
        search_str = self.li_search_wd.text()

        ex_file = [item.name for item in items]

        if ct == '' or ct == '文件夹':
            for file in dirs :
                id = '-999'
                name = file
                desc = ''
                type = '文件夹'
                version='0'
                path = os.path.join(xq_item.path,file)
                ctime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime( os.path.getctime(path)))
                mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime( os.path.getmtime(path)))
                datas.append([id,type, name, version, desc,ctime,mtime, path])

        for ln_file in files:
            if ln_file.endswith('.ln'):
                path = os.path.join(xq_item.path, ln_file)
                with open(path,'r',encoding='utf-8') as f:
                    lines = f.readlines()
                    print(lines)
                for line in lines:
                    line = line.strip()
                    if os.path.exists(line):
                        files.append(line)
        files.reverse()
        if ct == '' or ct == '文档':
            for file in files :
                if file in ex_file:
                    continue
                if file.endswith('.ln'):
                    continue
                id = '-999'
                name = file
                desc = ''
                type = '文档'
                version='0'
                if os.path.exists(file):
                    tmp = file.split("\\")
                    name = f'@@@@-{tmp[-1]}'
                    path = file
                else:
                    path = os.path.join(xq_item.path,file)
                ctime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime( os.path.getctime(path)))
                mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime( os.path.getmtime(path)))

                datas.append([id,type, name, version, desc,ctime,mtime, path])



        if ct == '' or ct == '脚本':
            for item in items:
                id =str(item.id)
                name = item.name
                desc = item.desc
                type = item.type
                ctime = item.ctime.strftime("%Y-%m-%d %H:%M:%S")
                path = item.path
                mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime( os.path.getmtime(path)))
                version = str(item.version)
                datas.append([id, type, name, version, desc,ctime, mtime,path])

        for item in datas:
            if item[2].startswith('~$'):
                continue
            if search_str.upper() in item[2].upper() or search_str.strip()=='' or search_str.upper() in item[4].upper():
                row_items = [QStandardItem(i) for i in item]
                model.appendRow(row_items)


        self.tb_xuqiudtl.setModel(model)
        self.tb_xuqiudtl.setStyleSheet(mhsheet)


        # self.tb_xuqiudtl.resizeRowsToContents()
        self.repaint()
    def init_tb_xuqiu(self,search=None):
        # 显示需求表格
        rwlx =''
        com_status = self.com_sear_type.currentText()
        gjz_str_ss = self.li_search.text()
        model = QStandardItemModel()
        gjz_str_l =[]
        zd_list = ZDXQ.split('|')
        gjz_str_l += zd_list
        gjz_str_l += gjz_str_ss.split('|')
        xs_ids = []
        for gjz_str in gjz_str_l:
            gjz_list = gjz_str.split('&')
            items = XQ_INFO.select().order_by(XQ_INFO.mtime.desc())
            if com_status!='':
                items = items.where(XQ_INFO.status==com_status)
            for gjz in gjz_list:
                items = items.where((XQ_INFO.name ** f'%{gjz}%')|(XQ_INFO.xuqiu_type == gjz)|(XQ_INFO.tcr  ** f'%{gjz}%'))
            for column, name in enumerate(xuqiu_header):
                header_item = QStandardItem(name)
                model.setHorizontalHeaderItem(column, header_item)
            for item in items[:500]:
                id = str(item.id)
                if id in xs_ids:
                    continue
                xs_ids.append(id)
                name = item.name
                path = item.path
                xuqiu_type = item.xuqiu_type
                status = item.status
                tcr = item.tcr
                row_items = [QStandardItem(i) for i in [id,name,xuqiu_type,status,tcr,path]]
                model.appendRow(row_items)
        self.tb_xuqiu.setModel(model)

        #列宽行高
        self.tb_xuqiu.setEditTriggers(QTableView.NoEditTriggers)
        self.repaint()

    def get_row_content(self,index):
        try:
        # 获取行内容
            row = [index.model().data(index.sibling(index.row(), column), Qt.DisplayRole) for column in
                   range(index.model().columnCount())]
            return row
        except Exception as e:
            raise ValueError('未正确选择行')


    def ddj_xuqiu(self,index):
        datas = self.get_row_content(index)
        path = datas[-1]
        os.startfile(path)
    def dj_xuqiu(self,index):
        #刷新需求内容
        datas = self.get_row_content(index)
        id = int(datas[0])
        xq_item = XQ_INFO.get_by_id(id)
        self.inint_tb_xuqiudtl(xq_item)

    def f_com_type(self):
        row = self.tb_xuqiu.currentIndex()
        self.tb_xuqiu.setFocus()
        self.dj_xuqiu(row)
        self.li_search_wd.setFocus()

    # id = AutoField(verbose_name='脚本编号', primary_key=True)
    # xq_id = ForeignKeyField(XQ_INFO,on_delete='CASCADE')
    # name = CharField(verbose_name='文件名称')
    # desc = CharField(verbose_name='备注')
    # type = CharField(verbose_name='类型') #开发/提交（版本）
    # version = IntegerField(verbose_name='版本号')
    # path = CharField(verbose_name='路径')
    def create_xuqiu(self):
        # 创建需求
        if self.li_search.text() == '#*#*脚本迁移*#*#':
            print('开始迁移')
            qylist = JB_INFO.select(JB_INFO,XQ_INFO).join(XQ_INFO).where(JB_INFO.version==0)
            for i in qylist:
                try:
                    xq_id = i.xq_id
                    name = i.name
                    desc = i.desc
                    type = i.type
                    version = 0
                    path = os.path.join(xq_id.path,name)
                    old_jb = JB_INFO.get_by_id(i.id)
                    new_jb = JB_INFO(name=name,desc = desc,type=type,version=version,path = path,xq_id=xq_id)
                    print(old_jb.name,old_jb.path,new_jb.path,new_jb.name)

                    shutil.copy(old_jb.path,new_jb.path)
                    old_jb.version = '-1'
                    new_jb.save()
                    old_jb.save()
                except Exception as e:
                    print(e.__str__())
        #*#*导入表*#*#$$E:\思特奇\SQL_HELPER目录\数据\图书馆\元数据\YSJ (1)\表元数据.xlsx
        if '#*#*导入表*#*#$$' in self.li_search.text() :
            my_path = self.li_search.text()
            my_path = my_path.replace('#*#*导入表*#*#$$','')
            from openpyxl import load_workbook
            wb = load_workbook(filename=my_path)
            ws = wb['Sheet1']
            for  row in ws.iter_rows():
                db = row[0].value.upper().strip()
                tb_name = row[1].value.upper().strip()
                table_comment = f'{row[2].value}-批量导入'
                i = f'{db}.{tb_name}'
                print(i,db, tb_name, table_comment)
                u, is_create = TABLE_INFO.get_or_create(table_id=i)
                if not is_create:
                    continue
                else:
                    if 'TB_MID' in i:
                        u.by1 = '3'
                    elif 'PMID' in i:
                        u.by1 = '2'
                    elif 'PDATA' in i:
                        u.by1 = '1'
                    else:
                        u.by1 = '0'
                    u.desc = table_comment
                    u.save()
        #*#*导入字段*#*#$$E:\思特奇\SQL_HELPER目录\数据\图书馆\元数据\YSJ (1)\字段元数据.xlsx
        if '#*#*导入字段*#*#$$' in self.li_search.text():
            my_path = self.li_search.text()
            my_path = my_path.replace('#*#*导入字段*#*#$$', '')
            from openpyxl import load_workbook
            wb = load_workbook(filename=my_path)
            ws = wb['Sheet1']
            for row in ws.iter_rows():
                db = row[0].value.upper().strip()
                tb_name = row[1].value.upper().strip()
                cl_name = row[2].value.upper().strip()
                cl_type = row[3].value.upper().strip()
                cl_comment = f'{row[4].value}'
                i = f'${db}.{tb_name}.${cl_name}'
                tb_id = f'{db}.{tb_name}'
                print(i, db, tb_name, cl_name,cl_type,cl_comment,tb_id)
                u, is_create = TABLE_COLUM_INFO.get_or_create(id=i,tb_id=tb_id)
                if not is_create:
                    continue
                else:
                    u.col_name = cl_name
                    u.col_type = cl_type
                    u.col_desc = cl_comment
                    u.ex_text ='批量导入'
                    u.save()


        else:
            self.creat_xq = Create_XUQIU_UI(self)
            self.creat_xq.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
            self.creat_xq.show()
            self.init_tb_xuqiu()
            self.repaint()
