from http import HTTPStatus
import dashscope
from PySide2.QtWidgets import QWidget, QApplication, QProgressBar
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import QTime, QDateTime, QRegExp, QDir, QThread, Signal, Slot
from PySide2.QtGui import Qt, QIcon, QKeySequence, QStandardItemModel, QTextCursor, QSyntaxHighlighter, QTextCharFormat, \
    QFont
from PySide2.QtWidgets import QTextEdit, QApplication, QMessageBox, QDateTimeEdit, QLineEdit, QPushButton, QTextBrowser, \
    QFormLayout, QHBoxLayout, QComboBox, QInputDialog, QMainWindow, QFileDialog, QTableWidget, QTableWidgetItem, \
    QHeaderView, QAbstractItemView, QDesktopWidget, QAction, QShortcut, QWidget, QTableView, QDialog, QVBoxLayout, \
    QDialogButtonBox, QLabel, QToolTip, QMenu, QRadioButton, QStackedWidget
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QStandardItem
from clinet.AI_UTL_ui import Ui_COSMIC_UTL
# https://help.aliyun.com/zh/dashscope/developer-reference/tongyi-qianwen-7b-14b-72b-metering-and-billing?spm=a2c4g.11186623.0.0.79ad3a4770nDqv
dashscope.api_key="sk-b35850d77da944b09705a74ede63d81b"
import time

S1_STR= """
你是写COSMIC的专家，帮我写COSMIC,功能过程是:"{gnd}",根据我给定的功能过程，拆分出四个子过程描述，子过程需要包含谓语，并生成对应的数据组和数据属性，要求数据属性有3个，且不可重复，数据组文字不可重复。并以如下格式输出:子过程描述|数据组|数据属性
"""

MGZD_DICT={
    '运维':'操作'
    ,'运营':'操作'
    ,'扩容':'操作'
    ,'迁移':'操作'
    ,'国产化':'适配'
    ,'重构':'构建'
    ,'脚本':'代码语句'
    ,'开发':'设计语言'
    ,'环境搭建':'配置基础环境'
    ,'巡检':'代码检查'
    ,'监控':'输出运行状态'
    ,'收入保障':'读取'
    ,'工单':'任务清单'
    ,'新集群功能':'系统功能'
    ,'告警':'异常信息通知'
    ,'数据迁移':'读取数据，并输出到指定环境'
    ,'数据维护':'SQL代码生成'
    ,'分析':'检测'
    ,'验证':'鉴定'
    ,'调度':'鉴权'
    ,'采集':'提取'
    ,'整理':'转化'
    ,'处理':'响应'
    ,'配置':'设置基础属性'
    ,'测试':'鉴定'
}

def str_replace(str,dict_in):
    for k,v in dict_in.items():
        str = str.replace(k,v)
    return str


import queue
q = queue.Queue()
# 自定义线程类
class AI_WorkerThread(QThread):
    # 定义信号，用于传递线程执行结果
    result_signal = Signal(str)
    result_cnt = Signal(float)
    ok_flag = Signal(str)

    def __init__(self, gnds,mode_name,step1,step2):
        super().__init__()
        self.gnds = gnds
        self.mode_name = mode_name
        self.step1 = step1
        self.step2 = step2
        self.stop = False

    def get_cosmic(self,gnd,mode_name,step1,step2):
        try:
            messages = step1.replace('{gnd}',gnd)
            print(messages)
            a = self.call_with_messages2(messages,mode_name)
            msg2=step2.replace('{a}',a)[:250]
            print(msg2)
            b = self.call_with_messages2(msg2,mode_name)
            ret = [gnd+'@'+i for i in b.split('\n') if i.strip()!='']
            return '\n'.join(ret)
        except Exception as e:
            print(e.__str__())
            return ''
    def call_with_messages2(self,msg,mode_name):
        messages = [
                    {'role': 'user', 'content':msg}
        ]

        response = dashscope.Generation.call(
            mode_name,
            messages=messages,
            result_format='message',  # set the result is message format.
        )
        if response.status_code == HTTPStatus.OK:
            response = response.get('output').get('choices')[0].get('message').get('content')
            return response

        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
            raise ValueError('返回失败')

    @Slot()
    def run(self):
        total = len(self.gnds)
        jd = 0
        for gnd in self.gnds:
            if not q.empty():
                msg = q.get(block=False)
            else:
                msg = 'Run'
            print(msg, '@@@@@@@@@@@@@@@@@')
            if msg=='Stop':
                self.ok_flag.emit('终止成功')
                break
            ret = self.get_cosmic(gnd,self.mode_name,self.step1,self.step2)
            n = 3
            while ret =='' and n>0:
                time.sleep(1)
                ret = self.get_cosmic(gnd,self.mode_name,self.step1,self.step2)
                n-=1
            if ret!='':
                self.result_signal.emit(ret)
            else:
                self.result_signal.emit(f'{gnd}@ERROR')
            jd+=1
            self.result_cnt.emit(jd/total)
        self.ok_flag.emit('获取完成')



class COSMIC(QWidget):
    ## 超级检索
    def __init__(self):
        super().__init__()
        self.ui = Ui_COSMIC_UTL()
        self.ui.setupUi(self)

        self.li_key:QLineEdit =self.ui.li_key
        self.li_mode:QLineEdit = self.ui.li_mode
        self.tx_step1 :QTextEdit= self.ui.tx_step1
        self.tx_step2 :QTextEdit= self.ui.tx_step2
        self.tx_log :QTextEdit= self.ui.tx_log
        self.pg_jd:QProgressBar=self.ui.pg_jd
        self.pg_jd.setValue(0)
        self.tx_step1.setText(S1_STR)

        self.pb_input :QPushButton= self.ui.pb_input
        self.pb_output :QPushButton=self.ui.pb_output
        self.pb_output.setText('输出文件')

        self.li_mode.setText('qwen-1.8b-chat')
        # self.li_mode.setEnabled(False)

        # self.li_key.setText('sk-dd4b044f7967499aa3d7f9bfdceaabf9')

        self.api_key =''
        self.mode_name =''
        self.step1 =''
        self.step2 =''

        self.fun_save_conf()
        self.li_key.textChanged.connect(self.fun_save_conf)
        self.li_mode.textChanged.connect(self.fun_save_conf)
        self.tx_step1.textChanged.connect(self.fun_save_conf)
        self.tx_step2.textChanged.connect(self.fun_save_conf)
        self.pb_input.clicked.connect(self.f_bt_daoru)

        self.worker = None
    def fun_save_conf(self):
        self.api_key =self.li_key.text().strip()
        self.mode_name=self.li_mode.text().strip()
        self.step1=self.tx_step1.toPlainText().strip()
        self.step2 =self.tx_step2.toPlainText().strip()





    def f_bt_daoru(self):
        try:
            if self.pb_input.text()=='导入文件':
                # 导入文件
                initial_dir = QDir("C://")
                file_dialog = QFileDialog()
                file_dialog.setDirectory(initial_dir)

                file_dialog.setFileMode(QFileDialog.ExistingFile)
                file_dialog.setNameFilter("txt (*.txt)")
                if file_dialog.exec_():
                    file_paths = file_dialog.selectedFiles()
                    for file_path in file_paths:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            in_ls = [i.strip() for i in f.readlines() if i.strip() != '']
                            self.pg_jd.setValue(0)
                            a = AI_WorkerThread(in_ls,self.mode_name,self.step1,self.step2)
                            a.result_signal.connect(self.disply_tx_log)
                            a.result_cnt.connect(self.disply_jd)
                            a.ok_flag.connect(self.fun_finshed)
                            a.start()
                            self.worker=a
                            self.pb_input.setText('终止')
                else:
                    q.put('Stop')
                    print(q)
        except Exception as e:
            print(e.__str__())
            QMessageBox.warning(self,'',e.__str__())

    def fun_out(self):
        pass

    @Slot(object)
    def fun_finshed(self,msg):
        print('完成@@@@@@@@@@@@@@@@@@@@@@')
        self.worker=None
        self.pb_input.setText('导入文件')
        QMessageBox.warning(self,'',msg)
        self.showNormal()

    @Slot(object)
    def disply_tx_log(self,msg):
        msg = str_replace(msg,MGZD_DICT)
        self.tx_log.append(msg)
        self.repaint()

    @Slot(object)
    def disply_jd(self,jd):
        self.pg_jd.setValue(jd*100)
        print(jd*100)

    def fun_input(self):
        pass
    def cosmic_utl(self,input_path,mode_name,step1,step2):
        print(self.api_key)
        dashscope.api_key = self.api_key
        with open(input_path,'r',encoding='utf-8') as f:
            in_ls = [i.strip() for i in f.readlines() if i.strip()!='']
        print(f'输入:{in_ls}')
        out = self.contorl(in_ls,mode_name,step1,step2)
        return out
        # with open(output_path,'w',encoding='utf-8') as f:
        #     f.write(out)
        # print(f'输出：{output_path}')



if __name__ == '__main__':
    app = QApplication([])
    stats = COSMIC()
    stats.show()
    app.exec_()

