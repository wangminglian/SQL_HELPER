import ctypes
import logging
import os
import signal
import stat
import time
import re
from asyncio import sleep
from concurrent.futures import ThreadPoolExecutor
import sys
import json
from PySide2.QtWidgets import QApplication, QMenu, QAction, QCompleter
from PySide2.QtCore import QObject, Slot, QEvent, QStringListModel
from PySide2.QtWebChannel import QWebChannel
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtCore import QTimer
from pyvis.edge import Edge
from pyvis.network import Network

from PySide2.QtWebEngineWidgets import QWebEngineView

from clinet.tupu_select_node_ui import Ui_Tupu_select_node
from clinet.tupu_ui import Ui_tupu
from clinet.tupu_xiangqing_ui import Ui_tupu_xiangqing
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
from yuanshuju import CJJS_UI, BGL_UI
import copy
from collections import defaultdict

XUQIU_MOBAN_PATH = XUQIU_MOBAN_PATH
GONGZUOQU_PATH=GONGZUOQU_PATH
DATA_PATH = DATA_PATH
HSZ_PATH = HSZ_PATH
VS_PATH=VS_PATH
VSDX_PATH=VSDX_PATH
WPS_PATH=WPS_PATH
EDGE_PATH=EDGE_PATH
ZDXQ = ZDXQ

NEO4J_PATH = 'D:\\code\\neo4j-community-4.4.25\\bin\\neo4j'
NEO4J_IP = '127.0.0.1'
NEO4J_POST ='7474'
NEO4J_USER = 'neo4j'
NEO4J_PASSWORD = '123456'

from py2neo import Graph,Node,Relationship

# 圆形（“circle”）：节点以圆形的形式显示。
# 椭圆形（“ellipse”）：节点以椭圆形的形式显示。
# 正方形（“box”）：节点以正方形的形式显示。
# 菱形（“diamond”）：节点以菱形的形式显示。
# 三角形（“triangle”）：节点以三角形的形式显示。
# 图标（“icon”）：节点可以使用自定义的图标进行显示。
# vis 形状配置
VIS_SHAPE_CONF={
    '主体': {'shape':'circle','size':30,'color':'rgba(255, 0, 0, 0.5)'}
    ,'业务过程':{'shape':'ellipse','size':30,'color':'rgba(0, 255, 0, 0.5)'}
    ,'属性':{'shape':'box','size':30}
    ,'表':{'shape':'box','size':30,'color':'rgba(0, 0, 255, 0.5)'}
    ,'字段':{'shape':'box','size':30,'color':'rgba(0, 255, 255, 0.5)'}
}
# 默认值
VIS_DEFAULT_CONF={'shape':'box','size':30}

# 0 为完全相等；负数为含有不同的keys；正数为keys相同，但是对应的值不完全相同
def compare_dict(dict1,dict2):
    cnt = 0
    dif_keys = []
    if (dict1.keys() ^ dict2.keys()):
        print('Two dictionaries have different keys!')
        dif_keys = list(dict1.keys() ^ dict2.keys())
        cnt = cnt - len(dif_keys)
        return cnt, dif_keys
    else:
        for (k1,v1),(k2,v2) in zip(dict1.items(), dict2.items()):
            if type(v1) == list or type(v2) == list:
                if bool(set(v1).difference(set(v2))):
                    cnt = cnt + 1
                    dif_keys.append(k1)
            else:
                if v1 != v2:
                    cnt = cnt + 1
                    dif_keys.append(k1)
        return cnt, dif_keys

class EX_NetWork(Network):
    def __init__(self):
        super().__init__()
        self.directed = True
        self.edge_ids =[]


    # 重写add_edge 方法，增加必传参数id
    def add_edge(self, source, to, **options):
        edge_exists = False

        # verify nodes exists
        assert source in self.get_nodes(), \
            "non existent node '" + str(source) + "'"

        assert to in self.get_nodes(), \
            "non existent node '" + str(to) + "'"

        # we only check existing edge for undirected graphs
        if not self.directed:
            for e in self.edges:
                frm = e['from']
                dest = e['to']
                if (
                        (source == dest and to == frm) or
                        (source == frm and to == dest)
                ):
                    # edge already exists
                    edge_exists = True
        if not edge_exists:
            id = options.get('id')
            e = Edge(source, to, self.directed, **options)
            self.edges.append(e.options)
            # print(f"**options:{options}")
            self.edge_ids.append(id)
    def get_node_by_id(self,id):
        index = self.node_ids.index(id)
        node = self.nodes[index]
        return node

    def get_relation_by_id(self,id):
        index = self.edge_ids.index(id)
        relation = self.edges[index]
        return relation

    def delete_node_by_id(self,id):
        index = self.node_ids.index(id)
        if index:
            self.node_ids.pop(index)
            print(index)
            node = self.nodes.pop(index)
            return  node
    def delete_relation_by_id(self,id):
        print(self.edge_ids)
        index = self.edge_ids.index(id)
        if index:
            self.edge_ids.pop(index)
            print(index)
            relation = self.edges.pop(index)
            return  relation

    def add_node_by_dict(self,data,x=None,y=None):
        data = dict(data)
        lable = data.get('labels')
        shape = VIS_SHAPE_CONF.get(lable,VIS_DEFAULT_CONF).get('shape')
        size = VIS_SHAPE_CONF.get(lable,VIS_DEFAULT_CONF).get('size')
        color = VIS_SHAPE_CONF.get(lable,VIS_DEFAULT_CONF).get('color')
        if x and y:
            self.add_node(data.get('id'), label=data.get('name'),shape = shape,size=size,x=x,y=y,pro=data,color=color)
        else:
            self.add_node(data.get('id'), label=data.get('name'),shape = shape,size=size ,pro=data,color=color)
        ret = self.get_node_by_id(data.get('id'))
        return ret

    def add_relation_by_dict(self,data):
        data = dict(data)

        self.add_edge(data.get('start')
                    , data.get('end')
                    , id=data.get('id')
                    , label=data.get('type')
                    , pro=data)
        return self.edges[-1]
    def update_node_by_id(self,id,data):
        pass


TUPU_SELECT_TB=['ID','类型','名称','详细信息']
TUPU_SELECT_TB_ID = 0
TUPU_SELECT_TB_LX = 1
TUPU_SELECT_TB_MC = 2
TUPU_SELECT_TB_XXXX = 3
TUPU_SELECT_TB_CONF = {
    'ID':'id'
    ,'类型':'labels'
    ,'名称':'name'
    ,'详细信息':'all'
}

class Tupu_select_node_UI(QWidget):
    def __init__(self,flag,main_pk=None):
        super().__init__()
        self.ui = Ui_Tupu_select_node()
        self.ui.setupUi(self)
        self.pk: TUPU_XIANGQING_UI = main_pk
        self.li_lx:QLineEdit = self.ui.li_lx
        self.li_gjz: QLineEdit = self.ui.li_gjz
        self.tb_nodes:QTableView =  self.ui.tb_nodes
        self.pb_quxiao:QPushButton = self.ui.pb_quxiao
        self.pb_queding:QPushButton = self.ui.pb_queding
        neo4j_url = f"http://{NEO4J_IP}:{NEO4J_POST}"
        self.graph = Graph(neo4j_url, auth=(NEO4J_USER, NEO4J_PASSWORD))
        self.li_lx.setClearButtonEnabled(True)
        self.flag = flag
        completer = QCompleter()
        completer.setFilterMode(Qt.MatchContains)
        self.li_lx.setCompleter(completer)
        lbs = self.Neo4j_get_all_lables()
        model = QStringListModel()
        model.setStringList(lbs)
        completer.setModel(model)
        self.li_lx.returnPressed.connect(self.init_tb_nodes)
        self.li_gjz.returnPressed.connect(self.init_tb_nodes)
        self.tb_nodes.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_nodes.horizontalHeader().setStretchLastSection(True)
        self.init_tb_nodes()
        self.tb_nodes.doubleClicked.connect(self.f_xuanze)


    def f_xuanze(self):
        idx = self.tb_nodes.currentIndex()
        if idx.isValid():
            data = self.get_row_content(idx)
            ret = data[TUPU_SELECT_TB_XXXX]
            tmp :QLineEdit= self.pk.flag_conf[self.flag]
            tmp.setText(ret)
            self.pk.repaint()
            self.close()


    def get_row_content(self,index):
        try:
        # 获取行内容
            row = [index.model().data(index.sibling(index.row(), column), Qt.DisplayRole) for column in
                   range(index.model().columnCount())]
            return row
        except Exception as e:
            raise ValueError('未正确选择行')

    def Node2dict(self,node:Node):
        id = node.identity
        labels = str(node.labels).replace(':','')
        property = dict(node.items())
        property['id'] = id
        property['labels']=labels
        return property

    def init_tb_nodes(self):
        datas:list = self.Neo4j_get_nodes_by_gjz()
        model = QStandardItemModel()
        for column, name in enumerate(TUPU_SELECT_TB):
            header_item = QStandardItem(name)
            model.setHorizontalHeaderItem(column, header_item)
        self.tb_nodes.setModel(model)
        for data in datas:
            ret_ = []
            for key_ in TUPU_SELECT_TB:
                key = TUPU_SELECT_TB_CONF[key_]
                if key == 'all':
                    ret_.append(json.dumps(data,ensure_ascii=False))
                else:
                    ret_.append(str(data.get(key)))
            row_items = [QStandardItem(i) for i in ret_]
            model.appendRow(row_items)
        self.tb_nodes.setModel(model)
        self.tb_nodes.setEditTriggers(QTableView.NoEditTriggers)


    # 解析关键字 支持 | & = =~
    def jx_gjz(self,gjz_str):
        alis = 'n'
        if gjz_str.strip()=='':
            return ''
        cons =  gjz_str.split('|')
        or_c_sql =[]
        for con in cons:
            and_str = con.split('&')
            and_c_sql = []
            for itme_ in and_str:
                if '=~' in itme_:
                    tmp = itme_.split('=')
                    pro = tmp[0].strip()
                    pro_vaule = tmp[1].strip()[1:]
                    gs = '=~'
                elif '=' in itme_:
                    tmp = itme_.split('=')
                    pro = tmp[0].strip()
                    pro_vaule = tmp[1].strip()
                    gs = '='
                else:
                    pro = 'name'
                    pro_vaule = f".*{itme_}.*"
                    gs = '=~'
                _str = f" toLower({alis}.{pro}) {gs} '{pro_vaule}' "
                and_c_sql.append(_str)
            and_str = f" ({' AND '.join(and_c_sql)}) "
            or_c_sql.append(and_str)
        ret = f"WHERE {' OR '.join(or_c_sql)}"
        return ret


   #　根据关键字。ｌａｂｌｅ获取neo4j节点
    def Neo4j_get_nodes_by_gjz(self):
        labels = self.li_lx.text().strip()
        gjz = self.jx_gjz(self.li_gjz.text())
        if labels !='':
            labels = ':'+labels
        str = f"MATCH (n{labels}) " \
              f"{gjz}" \
              f"RETURN id(n) as id,n " \
              f" LIMIT 1000"
        print(str)
        datas = self.graph.run(str)

        ret = []
        for item in datas.data():
            # n 是起始节点，m是终止节点,r是关系
            node:Node = item['n']
            ret_ = self.Node2dict(node)
            ret.append(ret_)
        return ret


    # 获取Neo4j全部lable
    def Neo4j_get_all_lables(self):
        str = "MATCH (n) RETURN DISTINCT labels(n) AS labels"
        labels = self.graph.run(str)
        ret = []
        for i in labels.to_table():
            ret.append(' '+i[0][0])
        return ret






class TUPU_XIANGQING_UI(QWidget):

    def __init__(self,data=None,main_pk=None,flag=None,mou_x=None,mou_y=None):
        super().__init__()
        self.ui = Ui_tupu_xiangqing()
        self.ui.setupUi(self)
        self.pk:ZHISHITUPU_UI = main_pk
        self.csh_flag = 2

        self.mou_y = mou_y
        self.mou_x = mou_x

        self.lb_id:QLabel = self.ui.lb_id
        self.lb_lx:QLabel = self.ui.lb_lx
        self.lb_end:QLabel = self.ui.lb_end
        self.lb_start:QLabel = self.ui.lb_start
        self.lb_name:QLabel = self.ui.lb_name

        self.li_id:QLineEdit = self.ui.li_id
        self.li_lx:QLineEdit = self.ui.li_lx
        self.li_end:QLineEdit = self.ui.li_end
        self.li_start:QLineEdit = self.ui.li_start
        self.li_name:QLineEdit = self.ui.li_name

        self.tb_zdy:QTableWidget =self.ui.tb_zdy

        self.pb_queding:QPushButton = self.ui.pushButton
        self.pb_quxiao:QPushButton = self.ui.pushButton_2

        self.pb_quxiao.clicked.connect(self.close)

        self.pb_queding.clicked.connect(self.f_queding)
        self.flag = flag

        self.tb_zdy.setFocus()

        # 配置更新项
        self.flag_conf = {
            'start':self.li_start
            ,'end':self.li_end
        }

        self.li_start.cursorPositionChanged.connect(self.f_select_start_node)
        self.li_end.cursorPositionChanged.connect(self.f_select_end_node)
        self.ui_list =[]


        # 配置节点、对接的页面袁术
        self.my_conf = {
            'node':
                {
                     'id': self.li_id
                    , 'labels': self.li_lx
                    , 'name': self.li_name
                }
            ,'relation':{
                    'id':self.li_id
                    ,'type':self.li_lx
                    ,'start':self.li_start
                    ,'end':self.li_end
            }
        }

        genner_key_ = list(self.my_conf.get('node').keys())+list(self.my_conf.get('relation').keys())
        self.genner_key=set(genner_key_)


        if data is None:
            self.data = {}
        else:
            self.data = data
        self.init_ls(self.data)


        jiedian_hide_list=[self.lb_end,self.lb_start,self.li_end,self.li_start]
        bian_hide_list =[self.lb_name,self.li_name]

        self.li_id.setDisabled(True)
        if 'node' in  self.flag :
            for i in jiedian_hide_list:
                i.hide()
        elif 'relation' in self.flag:
            for i in bian_hide_list:
                i.hide()

    #node 和str 转换
    def id_2_node_str(self,id):
        if id.isdigit():
            node = self.pk.cache_nodes.get(int(id))
            ret = json.dumps(node,ensure_ascii=False)
        else:
            ret =id
        return ret


    def f_select_start_node(self):
        if self.li_start.cursorPosition()==len(self.li_start.text()):
            return
        self.f_select_node('start')
    def f_select_end_node(self):
        if self.li_end.cursorPosition() == len(self.li_end.text()):
            return
        self.f_select_node('end')

    def f_select_node(self,form_str):
        my_ui = Tupu_select_node_UI(main_pk=self,flag=form_str)
        self.ui_list.append(my_ui)
        my_ui.show()

    def node_str_2_id(self,m_str):
        tmp = json.loads(m_str)
        ret = tmp.get('id')
        if ret is None:
            QMessageBox.warning(self,'错误','未指定节点id')
            raise ValueError('未指定节点id')
        if self.pk.cache_nodes.get(ret) is None:
            QMessageBox.warning(self, '错误', '节点id不存在')
            raise ValueError('节点id不存在')
        return tmp.get('id')
    # 如果传入数据，则根据类型显示数据
    def init_ls(self,data):
        print(self.flag)
        if self.flag =='edt_node':
            self.li_lx.setReadOnly(True)
        elif self.flag =='edt_relation':
            self.li_start.setEnabled(False)
            self.li_end.setEnabled(False)
        flag = self.flag.split('_')[-1]
        items = self.my_conf[flag]
        for key,imte_li in items.items():
            vaule = str(data.pop(key))
            if key in ['start','end'] :
                vaule = self.id_2_node_str(vaule)
            imte_li.setText(vaule)
        row_count = len(data)+1
        self.tb_zdy.setRowCount(row_count)
        n = 0
        for key,vaule in data.items():
            item_key = QTableWidgetItem(key)
            item_value = QTableWidgetItem(vaule)
            self.tb_zdy.setItem(n,0,item_key)
            self.tb_zdy.setItem(n,1,item_value)
            n+=1
        self.repaint()

    # 获取table 表单的数据，并把他转化为dict键值对
    def get_table_date(self):
        row_cnt = self.tb_zdy.rowCount()
        keys,values = [],[]
        for  x in range(row_cnt):
            key,value = '',''
            key_,value_ = self.tb_zdy.item(x,0),self.tb_zdy.item(x,1)
            if key_ :
                key = key_.text().strip()
            if value_:
                value = value_.text().strip()
            if key in self.genner_key:
                QMessageBox.warning(self,'错误','自定义属性key是内部关键字')
                raise ValueError('自定义属性key是内部关键字')
            if key == '':
                continue
            keys.append(key)
            values.append(value)
        if len(set(keys))!=len(keys):
            QMessageBox.warning(self,'错误','自定义属性key重复')
            raise ValueError('自定义属性key重复')
        else:
            ret = dict(zip(keys,values))
        return ret

    # 判断边数据是否合法
    def isVisible_Relation(self,data):
        ret = dict(data)
        if ret['start'] == ret['end']:
            QMessageBox.warning(self, '错误', '起始节点和节数节点不能相同')
            raise ValueError('数据提交失败')
        if ret['type'] == '':
            QMessageBox.warning(self, '错误', '类型必填')
            raise ValueError('数据提交失败')

    def isVisible_Node(self,data):
        ret = dict(data)
        if ret['labels'] == '' :
            QMessageBox.warning(self, '错误', '类型必填')
            raise ValueError('数据提交失败')
        if ret['name'] == '' :
            QMessageBox.warning(self, '错误', '名称必填')
            raise ValueError('数据提交失败')

    def f_queding(self):
        ret = {}
        _flag = self.flag.split('_')[-1]
        items = self.my_conf[_flag]
        for key,imte_li in items.items():
            tmp_v = imte_li.text()
            if key in ['id']:
                if tmp_v == '':
                    tmp_v='-999' # 新建的时候设置为-999，由系统分配id
                tmp_v = int(tmp_v)
            if key in ['start', 'end']:
                tmp_v = self.node_str_2_id(tmp_v)
            ret[key] = tmp_v
        zdy_dict = self.get_table_date()
        ret.update(zdy_dict)
        print(f'提交修改数据:{ret}')
        if self.flag =='edt_node':
            # 更新节点
           self.pk.update_Node(ret,if_noe4j=True,if_vis=True)
        elif self.flag=='edt_relation':
            self.isVisible_Relation(ret)
            self.pk.delete_Relation(ret,if_noe4j=True,if_cache=True,if_vis=True)
            self.pk.create_Relation(ret,if_noe4j=True,if_vis=True)
        elif self.flag =='add_relation':
            self.isVisible_Relation(ret)
            self.pk.create_Relation(ret,if_noe4j=True,if_vis=True)
        elif self.flag=='add_node':
            self.isVisible_Node(ret)
            ret_ = self.pk.create_Node(ret)




            # 更新Neo4j
            # r_ret_new,r_ret_old = self.pk.update_Neo4j_Relation_by_id(data=ret)
            # print(f'Neo4j数据{r_ret_new}')
            # # 更新 vis
            # self.pk.vis_relation_add_by_dict(r_ret_new,self.pk.network)
            # print(self.pk.network.edges)
            # # 删除
            # tmp_ret = self.pk.to_vis_delete_relation(r_ret_old)
            # self.pk.send_msg(self.pk.network.nodes,self.pk.network.edges)



            
        self.close()


def beautify_json(json_str):
    try:
        parsed = json.loads(json_str)
        beautified = json.dumps(parsed, indent=4, sort_keys=True,ensure_ascii=False)
        return beautified
    except json.JSONDecodeError:
        return "Invalid JSON format"
class ZHISHITUPU_UI(QWidget):
    def __init__(self,main_pk=None):
        super().__init__()
        self.ui = Ui_tupu()
        self.ui.setupUi(self)
        self.pk = main_pk
        #定义页面元素
        self.li_search:QLineEdit = self.ui.li_search
        self.web:QWebEngineView = self.ui.web
        self.tx_display:QTextBrowser = self.ui.tx_display
        self.pb_daoru:QPushButton=self.ui.pb_daoru
        self.page = self.web.page()

        self.url = os.getcwd().replace('\\', '/') + '/web/my_vis.html'
        self.web.load(self.url)
        self.web.showMaximized()
        self.pb_daoru.clicked.connect(self.init_grap)

        neo4j_url = f"http://{NEO4J_IP}:{NEO4J_POST}"
        self.graph = Graph(neo4j_url,auth=(NEO4J_USER,NEO4J_PASSWORD))

        # 初始化边缓存和节点缓存
        self.cache_nodes ={}
        self.cache_relation={}
        self.ui_list =[]
        self.network:EX_NetWork = None
        self.init_grap()



    def if_list_get_0(self,data):
        if type(data)==list:
            return data[0]
        else:
            return data

    @Slot(str, result=str)
    def getmsg(self, message):
        """接收Js回传的信息"""

        print(f'收到信息{message}')

        self.tx_display.clear()
        self.tx_display.setText(beautify_json(message))

        message = json.loads(message)

        method = message.get('method')


        if method =='双击节点':
            xq_ui = TUPU_XIANGQING_UI(data=message.get('selectNode').get('pro'),main_pk=self,flag='edt_node')
            self.ui_list.append(xq_ui)
            xq_ui.showNormal()
        if method == '新建节点':
            # 鼠标的x,y坐标
            mou_x = message.get('mou_x')
            mou_y = message.get('mou_y')
            ret = {
               "id":''
                ,"labels":''
                ,"name":''
            }
            xq_ui = TUPU_XIANGQING_UI(data=ret, main_pk=self, flag='add_node',mou_x=mou_x,mou_y=mou_y)
            self.ui_list.append(xq_ui)
            xq_ui.showNormal()
        elif method =='双击边':
            xq_ui = TUPU_XIANGQING_UI(data=message.get('selectEdg').get('pro'), main_pk=self,flag='edt_relation')
            self.ui_list.append(xq_ui)
            xq_ui.showNormal()
        elif method == '删除关系':
            select_edgs = message.get('selectEdgs')
            ret = [item.get('pro') for item in select_edgs ]
            self.delete_Relations(ret,if_cache=True,if_vis=True,if_noe4j=True)
        elif method == '新建关系':
            tmp_dict = {}
            start_id = "点击请选择"
            end_id = "点击请选择"
            end_node = self.if_list_get_0(message.get('lastSelect'))
            start_node = self.if_list_get_0(message.get('last_select2'))
            select_edgs = message.get('selectNodes')
            select_edgs_ = [item.get('pro') for item in select_edgs]
            for item in select_edgs_:
                tmp_dict[item.get('id')]=item
            if end_node:
                _end_id = end_node.get('pro').get('id')
                if _end_id in tmp_dict:
                    end_id = _end_id
            if start_node:
                _start_id = start_node.get('pro').get('id')
                if _start_id in tmp_dict:
                    start_id = _start_id
            if start_id =='点击请选择':
                start_id = end_id
                end_id ='点击请选择'

            ret = {
                "start":start_id
                ,"end":end_id
                ,"id":''
                ,"type":''
            }
            xq_ui = TUPU_XIANGQING_UI(ret, main_pk=self, flag='add_relation')
            self.ui_list.append(xq_ui)
            xq_ui.showNormal()
        elif method =='删除节点':
            nodes = message.get('selectNodes')
            for node in nodes:
                if node:
                    node_info = node.get('pro')
                    print(f'删除节点{node_info}')
                    self.delete_Node(data=node_info)
                else:
                    QMessageBox.warning(self,'错误','请选择要删除的节点')
        return f'{message}'



    def get_Neo4j_by_id(self,id):
        node = self.graph.nodes.get(id)
        return node

    def delete_Neo4j_Relation_by_id(self,data):
        data = dict(data)
        id = data.pop('id')
        str = f"MATCH ()-[r]->() WHERE id(r) = {id} DELETE r"
        self.graph.run(str)
        return True

    def delete_Neo4j_Node_by_id(self,data):
        data = dict(data)
        id = data.pop('id')
        str = f"MATCH (n) WHERE id(n) = {id} DELETE n"
        try:
            self.graph.run(str)
        except Exception as e:
            if 'because it still has relationships' in  e.__str__():
                QMessageBox.warning(self,'失败','删除边失败！需要先删除关系')
                raise ValueError('删除边失败！需要先删除关系')
        return True





    def create_Neo4j_Node(self,data):
        print(f'创建Neo4j节点:{data}')
        data = dict(data)
        labels = data.pop('labels')
        id = data.pop('id')
        new_Node = Node(labels, **data)
        self.graph.create(new_Node)
        return new_Node



    def create_Neo4j_Relation_by_id(self,data):
        # 创建关系
        print(f'创建Neo4j关系:{data}')
        data = dict(data)
        type_str = data.pop('type')
        start_id = data.pop('start')
        end_id = data.pop('end')
        start_node =self.get_Neo4j_by_id(start_id)
        end_node = self.get_Neo4j_by_id(end_id)
        new_relation = Relationship(start_node,type_str,end_node,**data)
        self.graph.create(new_relation)
        # ret_new = self.Relationship2dict(new_relation)
        return new_relation

    def create_Node(self,data,if_noe4j=True,if_vis=True,x=None,y=None):
        if if_noe4j:
            ret = self.create_Neo4j_Node(data)
        if if_vis:
            ret = self.vis_node_add_by_dict(ret,x=x,y=y)



    # 更新Node
    def update_Node(self,data,if_noe4j=True,if_vis=True):
        """

        :param data: 要修改数据的信息
        :param if_noe4j: 是否更新neo4j
        :param if_vis: 是否更新vis.js
        """
        data = dict(data)
        if if_noe4j:
            r_ret = self.update_Neo4j_Node_by_id(data)
            if r_ret==data:
                pass
            else:
                QMessageBox.warning(self, '错误', '数据提交Neo4j失败，请重试')
                raise ValueError('数据提交失败')

        if if_vis:
            nodestr = self.vis_node_update_by_dict(data, self.network)
            self.to_vis_update_node(nodestr)

    def delete_Node(self,data,if_noe4j=True,if_vis=True,if_cache=True):
        """
        :param data:
        :param if_noe4j: 是否更新neo4j
        :param if_vis: 是否更新vis.js
        :param if_cache: 是否更新cache
        """
        data = dict(data)
        id = data.get('id')
        if if_noe4j:
            ret = self.delete_Neo4j_Node_by_id(data)
            if ret:
                print(f'Noe4j删除节点id={id},{data}成功')
        if  if_cache:
            self.cache_nodes.pop(id)
            print(f'缓存删除节点id={id},{data}成功')
        if if_vis:
            ret = self.to_vis_delete_node(data)
            print('vis.js缓存删除节点id={id}，{data}成功')


    def  delete_Relations(self,data,if_noe4j=True,if_vis=True,if_cache=True):
        for item in data:
            self.delete_Relation(item,if_noe4j=if_noe4j,if_vis=if_vis,if_cache=if_cache)

    def delete_Relation(self,data,if_noe4j=True,if_vis=True,if_cache=True):
        """

        :param data: 要删除的边的数据
        :param if_noe4j: 是否更新neo4j
        :param if_vis: 是否更新vis.js
        :param if_cache: 是否更新cache
        """
        data = dict(data)
        id = data.get('id')
        if if_noe4j:
            ret = self.delete_Neo4j_Relation_by_id(data)
            if ret:
                print(f'Noe4j删除节点id={id},{data}成功')
        if  if_cache:
            self.cache_relation.pop(id)
            print(f'缓存删除节点id={id},{data}成功')
        if if_vis:
            ret = self.to_vis_delete_relation(data)
            print('vis.js缓存删除节点id={id}，{data}成功')

    def create_Relation(self,data,if_noe4j=True,if_vis=True):
        """
        :param data:  数据
        :param if_noe4j:  是否更新neo4j
        :param if_vis:  是否更新vis
        :param if_cache:  是否更新缓存
        """
        data = dict(data)
        id = data.pop('id')
        if if_noe4j:
            ret= self.create_Neo4j_Relation_by_id(data)
            print(f"新创建的边是:{ret}")
        if if_vis:
            self.to_vis_add_relation(ret)



    #通过id更新neo4j数据
    def update_Neo4j_Node_by_id(self,data):
        data = dict(data)
        id = data.pop('id')
        labels = data.pop('labels')
        node = self.get_Neo4j_by_id(id)
        node.clear()
        for key,vaule in data.items():
            node[key]=vaule
        self.graph.push(node)
        r_node = self.get_Neo4j_by_id(id)
        ret = dict(self.Node2dict(r_node))
        return ret

    #删除节点
    def to_vis_delete_node(self,data):
        id = data.get('id')
        self.network.delete_node_by_id(id)
        str = f"delete_node({json.dumps(data)});"
        print(str)
        self.page.runJavaScript(str)

    #　创建节点
    def to_vis_add_node(self,node_str):
        str = f"add_node({json.dumps(node_str)});"
        print(f"vis.js新建节点:{str}")
        self.page.runJavaScript(str)
    #删除边
    def to_vis_delete_relation(self,relation_str):
        #　删除　netowrk中的边
        id = relation_str.get('id')
        ret = self.network.delete_relation_by_id(id)
        str = f"delete_relation({json.dumps(relation_str)});"
        print(str)
        self.page.runJavaScript(str)



    # 新增边
    def to_vis_add_relation(self,relation_str:Relationship):
        """
        :param relation_str: 输入Neo4j关系，输出vis.js关系
        """
        data = self.Relationship2dict(relation_str)
        ret = self.network.add_relation_by_dict(data)
        # add_relation
        str = f"add_relation({json.dumps(ret)});"
        print(f"vis.js新建数据{str}")
        self.page.runJavaScript(str)


  # node_str 更新vis
    def to_vis_update_node(self,node_str):
        str = f"update_node({json.dumps(node_str)});"
        self.page.runJavaScript(str)
    def send_msg(self,nodes,edges):
        """传输数据，刷新参数"""
        str = f"drawGraph({json.dumps(nodes)},{json.dumps(edges)});"
        self.page.runJavaScript(str)


    # neo4j Node对象转dict
    def Node2dict(self,node:Node):
        id = node.identity
        labels = str(node.labels).replace(':','')
        property = dict(node.items())
        property['id'] = id
        property['labels']=labels
        self.cache_nodes[property.get('id')] = property
        return property

    # Neo4jdict转vis.js dict
    def Relationship2dict(self,relation:Relationship):
        if relation is None:
            return None
        property = dict(relation.items())
        id =relation.identity
        start = relation.start_node.identity
        end = relation.end_node.identity
        type = ''.join(relation.types())
        property['id'] = id
        property['start'] = start
        property['end'] = end
        property['type']=type
        self.cache_relation[property.get('id')] = property
        return property


    def vis_relation_add_by_dict(self,my_dict,nt:EX_NetWork):
        id = my_dict.get('id')
        start = my_dict.get('start')
        end = my_dict.get('end')
        pro = my_dict
        nt.add_edge(start,end,pro=pro)
        return nt

    def vis_node_add_by_dict(self,data,x=None,y=None):
        vis_dict = self.Node2dict(data)
        ret = self.network.add_node_by_dict(vis_dict,x=x,y=y)
        self.to_vis_add_node(ret)
        print(f"vis_str:{ret}")



    def vis_node_update_by_dict(self,my_dict,nt:EX_NetWork):
        id = my_dict.get('id')
        ret = self.cache_nodes[id]
        lable = ret.get('labels')
        shape = VIS_SHAPE_CONF.get(lable, VIS_DEFAULT_CONF).get('shape')
        size = VIS_SHAPE_CONF.get(lable, VIS_DEFAULT_CONF).get('size')
        color = VIS_SHAPE_CONF.get(lable, VIS_DEFAULT_CONF).get('color')
        node = nt.get_node_by_id(id)
        node['shape']=shape
        node['size']=size
        node['pro']=ret
        node['color']=color
        node['label']=ret.get('name')
        return node
        # self.send_msg(self.network.nodes,self.network.edges)


            # nt.add_node(ret.get('id'), label=ret.get('name'), shape=shape, size=size, pro=ret)
    # dict转vis nt node
    # def dict2vis(self,my_dict:dict,nt:EX_NetWork):
    #     ret = copy.deepcopy(my_dict)
    #     if ret.get('lx')=='node':
    #         lable = my_dict.get('labels')
    #         shape = VIS_SHAPE_CONF.get(lable,VIS_DEFAULT_CONF).get('shape')
    #         size = VIS_SHAPE_CONF.get(lable,VIS_DEFAULT_CONF).get('size')
    #         nt.add_node(ret.get('id'), label=ret.get('name'),shape = shape,size=size ,pro=ret)
    #     elif ret.get('lx')=='relation':
    #         nt.add_edge(ret.get('start')
    #                     ,ret.get('end')
    #                     ,id= ret.get('id')
    #                     ,label= ret.get('type')
    #                     ,pro = ret
    #                     )
    #     else:
    #         return nt
    #     return nt



    #neo4jNode数据转vis.jsshju
    def neo4j2vis_node(self,ret,nt=None):
        if nt is None:
            nt = EX_NetWork()
        for item in ret.data():
            # n 是起始节点，m是终止节点,r是关系
            from_tmp_Node = self.Node2dict(item['n'])
            nt.add_node_by_dict(from_tmp_Node)
            tmp_Relation = self.Relationship2dict(item.get('r'))
            if tmp_Relation is not None:
                to_tmp_Node= self.Node2dict(item['m'])
                nt.add_node_by_dict(to_tmp_Node)
                nt.add_relation_by_dict(tmp_Relation)
        return nt

    def init_grap(self):
        # 查询节点
        self.network = EX_NetWork()
        sql = 'MATCH(n) RETURN n LIMIT 1000'
        ret = self.graph.run(sql)
        self.network = self.neo4j2vis_node(ret,self.network)
        #查询边
        sql = 'MATCH(n)-[r]->(m) RETURN n,r,m LIMIT 1000'
        ret = self.graph.run(sql)
        self.network = self.neo4j2vis_node(ret,self.network)

        self.web.loadFinished.connect(lambda: self.send_msg(self.network.nodes, self.network.edges))
        self.web.reload()
        print(self.network.edges)


    def test(self):
        nt = EX_NetWork()

        nt.add_node(1, label='Node 1', shape='image', image='image/img.png')

        nt.add_node(2, label='Node 2')
        nt.add_node(3, label='Node 3')
        nt.add_node(4, label='Node 4')
        nt.add_node(5, label='Node 5')
        nt.add_edge(1, 2, label='测试', id="1-2")
        nt.add_edge(3, 2, id="3-2")
        nt.add_edge(4, 2, id="4-2")
        nt.add_edge(5, 2, id="5-2")
        self.web.loadFinished.connect(lambda: self.send_msg(nt.nodes, nt.edges))
        self.web.reload()

#注册接口

import psutil

def find_pid_by_port(port):
    for conn in psutil.net_connections():
        if  conn.laddr.port == int(port):
            return conn.pid
    return None

def start_neo4j():
    pid = find_pid_by_port(NEO4J_POST)
    if pid :
        print(f'neo4j已启动,端口号{pid}')
    else:
        command = f"neo4j console"
        subprocess.Popen(command,shell=True)

if __name__ == '__main__':
    try:
        # subprocess.Popen([NEO4J_PATH,'console'])
        start_neo4j()
        app = QApplication([])
        stats = ZHISHITUPU_UI(None)
        stats.showMaximized()
        # 注册
        channel = QWebChannel()
        channel.registerObject('py', stats)
        stats.page.setWebChannel(channel)
        app.exec_()
    finally:
        # subprocess.Popen([NEO4J_PATH, 'stop'])
        pass

