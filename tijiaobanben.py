import logging
import os
import re
from asyncio import sleep
from concurrent.futures import ThreadPoolExecutor
from clinet.tijiaobanben_ui import Ui_submit_banben
from clinet.create_xq_ui import Ui_create_xq
import pyperclip
from PySide2 import QtWidgets
from PySide2.QtCore import QTime, QDateTime
from PySide2.QtGui import Qt, QIcon, QKeySequence, QStandardItemModel
from PySide2.QtWidgets import QTextEdit, QApplication, QMessageBox, QDateTimeEdit, QLineEdit, QPushButton, QTextBrowser, \
    QFormLayout, QHBoxLayout, QComboBox, QInputDialog, QMainWindow, QFileDialog, QTableWidget, QTableWidgetItem, \
    QHeaderView, QAbstractItemView, QDesktopWidget, QAction, QShortcut, QWidget, QTableView, QDialog, QVBoxLayout, \
    QDialogButtonBox, QLabel, QToolTip, QColumnView
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QStandardItem
from peewee import SqliteDatabase, fn
from playhouse.shortcuts import model_to_dict
from collections import namedtuple
from model.model import Project_detail, SQL_arg, History, dp, create_tables, ARG_model, db, XQ_INFO, JB_INFO, YSJ_KJ, \
    XQ_TABLE_INFO, TABLE_COLUM_INFO, TABLE_INFO
from sql_helper.helper_restruct import Reader_Factory, Genner_Com
from collections import deque
import shutil
import subprocess

from sql_helper.read_sql_file import Reader_SQL
from conf import DATA_PATH, GONGZUOQU_PATH, mhsheet

# id = AutoField(verbose_name='主键', primary_key=True)
# xq_id = ForeignKeyField(XQ_INFO)
# jb_id =ForeignKeyField(JB_INFO)
# table_name = CharField(verbose_name='表名称')
# table_type = CharField(verbose_name='类型:输入or输出')
# version = IntegerField(verbose_name='版本')

INPUT_TABLE_HEADER = ['id','输入表名', '类型']
INPUT_TABLE_HEADER_ID=0
INPUT_TABLE_HEADER_SRBM=1
INPUT_TABLE_HEADER_LX=2

OUT_TABLE_HEADER = ['id','输出表名', '类型']
OUT_TABLE_HEADER_ID=0
OUT_TABLE_HEADER_SRBM=1
OUT_TABLE_HEADER_LX=2

OUT_KOUJING = ['id','口径名称', '类型']
OUT_KOUJING_ID=0
OUT_KOUJING_KJMC=1
OUT_KOUJING_LX=2
class Submit_banben_UI(QWidget):
    def __init__(self,idx):
        super().__init__()
        self.ui = Ui_submit_banben()

        self.ui.setupUi(self)

        self.idx = idx
        self.tb_input:QTableView = self.ui.tb_input
        self.tb_output:QTableView = self.ui.tb_output
        self.tx_sqldll:QTextEdit=self.ui.tx_sqldll
        self.tb_koujing: QTableView = self.ui.tb_koujing

        self.tb_input.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_input.horizontalHeader().setStretchLastSection(True)
        self.tb_input.setStyleSheet(mhsheet)
        self.tb_output.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_output.horizontalHeader().setStretchLastSection(True)
        self.tb_output.setStyleSheet(mhsheet)
        self.tb_koujing.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_koujing.horizontalHeader().setStretchLastSection(True)
        self.tb_koujing.setStyleSheet(mhsheet)
        self.bt_submit:QPushButton=self.ui.bt_submit
        self.bt_submit.clicked.connect(self.f_bt_submit)


        self.tb_input.setSelectionBehavior(QTableView.SelectRows)
        self.tb_output.setSelectionBehavior(QTableView.SelectRows)
        self.tb_koujing.setSelectionBehavior(QTableView.SelectRows)

        self.bt_yulan:QPushButton=self.ui.bt_yulan
        self.bt_yulan.clicked.connect(self.init_tx_sqldll)
        self.bt_close:QPushButton=self.ui.bt_close
        self.bt_close.clicked.connect(self.f_bt_close)
        self.li_bz:QLineEdit=self.ui.li_bz
        self.closeEvent=self.f_close



        self.red_sql_eng = Reader_SQL()

        self.input_tables_model = []
        self.out_tables_model = []
        self.out_put_koujing=[]
        self.out_tables_zds = []
        self.save_input_names = []
        self.save_output_names = []
        self.save_koujing_names = []
        self.save_output_zds=[]

        self.tj_jiapben_info()
        self.init_tb_input()
        self.init_tb_output()
        self.init_tb_koujing()

    def f_close(self,event):
        if os.path.exists(self.new_jb_info.path):
            return
        else:
            JB_INFO.delete_by_id(self.new_jb_info.id)
        event.accept()


    def f_bt_submit(self):
        # 保存所有数据
        # 输入表
        if self.tx_sqldll.toPlainText().strip()=='':
            QMessageBox.warning(self,'','请先预览')
            return
        with dp.transaction():
            try:
                self.new_jb_info.desc = self.li_bz.text()
                for i in self.save_input_names:#输入表
                    i.save()
                for i in self.save_output_names:#输出表
                    i.save()
                for i in self.save_koujing_names:#口径
                    i.save()
                flat_list = [num for sublist in self.save_output_zds for num in sublist]
                for i in flat_list:#字段
                    my_dict = {'id':i.id,'tb_id':i.tb_id,'col_name':i.col_name,'col_type':i.col_type,'col_desc':i.col_desc}
                    print(my_dict)
                    query=TABLE_COLUM_INFO.insert(my_dict).on_conflict(
                        conflict_target=[TABLE_COLUM_INFO.id]
                        ,preserve=[TABLE_COLUM_INFO.tb_id,TABLE_COLUM_INFO.col_name,TABLE_COLUM_INFO.col_type,TABLE_COLUM_INFO.col_desc]
                    )
                    query.execute()

                shutil.copy(self.spth,self.new_jb_info.path)
                os.chmod(self.new_jb_info.path,0o400) ## 设置版本文件为只读
                dp.commit()
                self.new_jb_info.save()
                self.close()
            except Exception as e:
                QMessageBox.warning(self,'',e.__str__())
                dp.rollback()


    def f_bt_close(self,event):
        self.close()

    def init_tx_sqldll(self):
        self.tx_sqldll.clear()
        inputs = [index.model().data(index.sibling(index.row(), 0), Qt.DisplayRole) for  index in self.tb_input.selectionModel().selectedRows(INPUT_TABLE_HEADER_ID)]
        outputs = [index.model().data(index.sibling(index.row(), 0), Qt.DisplayRole) for index in self.tb_output.selectionModel().selectedRows(OUT_TABLE_HEADER_ID)]
        koujings = [index.model().data(index.sibling(index.row(), 0), Qt.DisplayRole) for index in self.tb_koujing.selectionModel().selectedRows(OUT_KOUJING_ID)]
        self.save_input_names = [self.input_tables_model[int(i)] for  i in inputs]
        self.save_output_names = [self.out_tables_model[int(i)] for i in outputs]
        self.save_koujing_names = [self.out_put_koujing[int(i)] for i in koujings]
        self.save_output_zds=[self.out_tables_zds[int(i)] for i in outputs]

        out_text = "-----------------------------------------输入表列表:-----------------------------------------\n"
        out_text+= '\n'.join([i.table_id.table_id for i in self.save_input_names])
        out_text+='\n'
        out_text+="-----------------------------------------输出表列表:-----------------------------------------\n"
        out_text += '\n'.join([i.table_id.table_id for i in self.save_output_names])
        out_text += '\n'
        out_text+="-----------------------------------------输出口径:-----------------------------------------\n"
        out_text += '\n'.join([i.name for i in self.save_koujing_names])
        out_text += '\n'
        out_text += "-----------------------------------------表结构:-----------------------------------------"
        for x,y in zip(self.save_output_names,self.save_output_zds):
            out_text += f'\n表名：{x.table_id.table_id}::::${x.table_id.desc}\n'
            out_text+='\t'
            out_text+=f'\n\t'.join([f'{i.col_name} {i.col_type} {i.col_desc}' for i in y])


        self.tx_sqldll.setText(out_text)


    def tj_jiapben_info(self):
        idx = self.idx
        jb_info = JB_INFO.get_by_id(idx)
        xq_id = jb_info.xq_id
        name = jb_info.name
        sql = JB_INFO.select(fn.Max(JB_INFO.version)).where(JB_INFO.xq_id==xq_id and JB_INFO.name==name).group_by(JB_INFO.xq_id,JB_INFO.name)
        max_version=sql.scalar()
        type ='脚本'
        version = int(max_version)+1
        pt = os.path.join(DATA_PATH, f"{xq_id.path}\\代码\\")
        path=os.path.join(pt,f"{name[:-4]}-V{version}.sql")
        ret = JB_INFO()
        ret.xq_id = xq_id
        ret.name = name
        ret.type = type
        ret.version=version
        ret.path=path
        ret.desc=''
        spth = os.path.join(xq_id.path,name)
        ret.save()
        self.new_jb_info = ret
        self.spth = spth

    def init_tb_input(self):
        # 抽取输入表，数据存储到 self.input_tables_model中
        pth = self.spth
        _,input_tables = self.red_sql_eng.read_sql_to_rtl_table(pth)
        self.input_tables_model = []
        t_id = 0
        qmodel = QStandardItemModel()
        for column, name in enumerate(INPUT_TABLE_HEADER):
            header_item = QStandardItem(name)
            qmodel.setHorizontalHeaderItem(column, header_item)
        for i in input_tables:
            tmp = XQ_TABLE_INFO()
            tmp.xq_id = self.new_jb_info.xq_id
            tmp.jb_id = self.new_jb_info.id
            i = i.upper()
            u,_ = TABLE_INFO.get_or_create(table_id=i)
            if 'TB_MID' in i:
                u.by1='3'
            elif 'PMID' in i:
                u.by1 ='2'
            elif 'PDATA' in i:
                u.by1='1'
            else:
                u.by1='0'
            u.save()
            tmp.table_id =u
            tmp.table_type='输入'
            tmp.version=self.new_jb_info.version
            tmp.___id = t_id
            self.input_tables_model.append(tmp)
            row_items = [QStandardItem(i) for i in [str(t_id), i, tmp.table_type]]
            qmodel.appendRow(row_items)
            t_id+=1
        self.tb_input.setModel(qmodel)


    def init_tb_koujing(self):
        # 抽取输入表，数据存储到 self.input_tables_model中
        pth = self.spth
        _,koujings = self.red_sql_eng.read_sql_to_gjz(pth)
        self.out_put_koujing = []
        t_id = 0
        qmodel = QStandardItemModel()
        for column, name in enumerate(INPUT_TABLE_HEADER):
            header_item = QStandardItem(name)
            qmodel.setHorizontalHeaderItem(column, header_item)
        for i in koujings:
            tmp = YSJ_KJ()
            tmp.xq_id = self.new_jb_info.xq_id
            tmp.jb_id = self.new_jb_info.id
            tmp.name =i[0].split('-- >>')[-1]
            tmp.line = i[1]
            tmp.table_type='口径'
            tmp.version=self.new_jb_info.version
            tmp.___id = t_id
            tmp.path = self.new_jb_info.path
            self.out_put_koujing.append(tmp)
            row_items = [QStandardItem(i) for i in [str(t_id), tmp.name, tmp.table_type,str(tmp.line)]]
            qmodel.appendRow(row_items)
            t_id+=1
        self.tb_koujing.setModel(qmodel)
    def init_tb_output(self):
        # 抽取输入表，数据存储到 self.out_tables_model中
        pth = self.spth
        out_datas,comment_dict =self.red_sql_eng.read_sql_to_out_table(pth)
        out_tables =out_datas.keys()
        t_id=0
        self.out_tables_model=[]
        self.out_tables_zds =[]
        qmodel = QStandardItemModel()
        for column, name in enumerate(OUT_TABLE_HEADER):
            header_item = QStandardItem(name)
            qmodel.setHorizontalHeaderItem(column, header_item)
        for i in out_tables:
            tmp = XQ_TABLE_INFO()
            tmp.xq_id = self.new_jb_info.xq_id
            tmp.jb_id = self.new_jb_info.id
            u,_=TABLE_INFO.get_or_create(table_id=i)
            u.desc=comment_dict[i]
            u.save()
            tmp.table_id =u
            tmp.table_type='输出'
            tmp.version=self.new_jb_info.version
            tmp.___id = t_id
            self.out_tables_model.append(tmp)
            row_items = [QStandardItem(i) for i in [str(t_id), i, tmp.table_type]]
            qmodel.appendRow(row_items)

            #表字段信息
            tb_values = out_datas.get(i)
            tmp_v = []
            for vlu in tb_values:
                tmp_col = TABLE_COLUM_INFO()
                tmp_col.id = f'${i}.${vlu[0]}'
                tmp_col.tb_id = u
                tmp_col.col_name=vlu[0]
                tmp_col.col_type=vlu[1]
                tmp_col.col_desc=vlu[2]
                tmp_v.append(tmp_col)
            t_id+=1
            self.out_tables_zds.append(tmp_v)
        self.tb_output.setModel(qmodel)









