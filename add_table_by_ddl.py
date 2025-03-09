
from clinet.add_table_by_ddl_ui import Ui_add_table_by_ddl

from PySide6.QtGui import Qt, QIcon, QKeySequence, QStandardItemModel
from PySide6.QtWidgets import QTextEdit, QApplication, QMessageBox, QDateTimeEdit, QLineEdit, QPushButton, QTextBrowser, \
    QFormLayout, QHBoxLayout, QComboBox, QInputDialog, QMainWindow, QFileDialog, QTableWidget, QTableWidgetItem, \
    QHeaderView, QAbstractItemView, QWidget, QTableView, QDialog, QVBoxLayout, \
    QDialogButtonBox, QLabel, QToolTip, QColumnView
from PySide6.QtGui import QStandardItem

from model.model import Project_detail, SQL_arg, History, dp, create_tables, ARG_model, db, XQ_INFO, JB_INFO, YSJ_KJ, \
    XQ_TABLE_INFO, TABLE_COLUM_INFO, TABLE_INFO


from sql_helper.read_sql_file import Reader_SQL
from conf import DATA_PATH, GONGZUOQU_PATH, mhsheet
OUT_TABLE_HEADER = ['id','输出表名', '类型','表描述','备注','优先级']
OUT_TABLE_HEADER_ID=0
OUT_TABLE_HEADER_SRBM=1
OUT_TABLE_HEADER_LX=2
OUT_TABLE_HEADER_BMS=3
OUT_TABLE_HEADER_BZ=4
OUT_TABLE_HEADER_YXJ=5
class ADD_TABLE(QWidget):
    def __init__(self,pk):
        super().__init__()
        self.ui = Ui_add_table_by_ddl()
        self.pk =pk
        self.ui.setupUi(self)

        self.tx_ddl:QTextEdit = self.ui.tx_ddl
        self.tb_output:QTableView = self.ui.tb_output
        self.tx_sqldll:QTextEdit=self.ui.tx_sqldll

        self.tb_output.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_output.horizontalHeader().setStretchLastSection(True)
        self.tb_output.setStyleSheet(mhsheet)
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



    def f_yulan(self):
        if self.tb_output.selectionModel() is None:
            QMessageBox.warning(self,'提示','请先点击加载')
            return
        self.outputs = [index.model().data(index.sibling(index.row(), 0), Qt.DisplayRole) for index in
                        self.tb_output.selectionModel().selectedRows(OUT_TABLE_HEADER_ID)]
        self.save_output_names = [self.out_tables_model[int(i)] for i in self.outputs]
        self.save_output_zds = [self.out_tables_zds[int(i)] for i in self.outputs]

        out_text = "-----------------------------------------输出表列表:-----------------------------------------\n"
        out_text += '\n'.join([i.table_id for i in self.save_output_names])
        out_text += '\n'
        out_text += "-----------------------------------------表结构:-----------------------------------------"
        for x, y in zip(self.save_output_names, self.save_output_zds):
            out_text += f'\n表名：{x.table_id}::::${x.desc}\n'
            out_text += '\t'
            out_text += f'\n\t'.join([f'{i.col_name} {i.col_type} {i.col_desc}' for i in y])

        self.tx_sqldll.setText(out_text)

    def f_jiazai(self):
        sql_str = self.tx_ddl.toPlainText()
        self.init_tb_output(sql_str)
        self.tx_sqldll.clear()


    def init_tb_output(self,sql_str):
        # 抽取输入表，数据存储到 self.out_tables_model中

        out_datas,comment_dict =self.red_sql_eng.read_sql_str_to_out_table(sql_str)
        print('@@@@@@@@@@@@@@@@@@@@@')
        print(comment_dict)
        out_tables =out_datas.keys()
        t_id=0
        self.out_tables_model=[]
        self.out_tables_zds =[]
        qmodel = QStandardItemModel()
        for column, name in enumerate(OUT_TABLE_HEADER):
            header_item = QStandardItem(name)
            qmodel.setHorizontalHeaderItem(column, header_item)
        for i in out_datas:
            u,_=TABLE_INFO.get_or_create(table_id=i)
            u.desc=comment_dict[i]
            u.by2 = self.li_bz.text()

            i = i.upper()
            if 'TB_MID' in i:
                u.by1='3'
            elif 'PMID' in i:
                u.by1 ='2'
            elif 'PDATA' in i:
                u.by1='1'
            else:
                u.by1='0'

            u.save()
            self.out_tables_model.append(u)
            row_items = [QStandardItem(i) for i in [str(t_id), i, '输出',u.desc,u.by2,u.by1]]
            qmodel.appendRow(row_items)
            t_id+=1

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
            self.out_tables_zds.append(tmp_v)
        self.tb_output.setModel(qmodel)

    def f_bt_submit(self):
        # 保存所有数据
        # 输入表
        if self.tx_sqldll.toPlainText().strip()=='':
            QMessageBox.warning(self,'','请先预览')
            return
        with dp.transaction():
            try:
                for i in self.save_output_names:#输出表
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
                dp.commit()
                self.close()
            except Exception as e:
                QMessageBox.warning(self,'',e.__str__())
                dp.rollback()

