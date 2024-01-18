from sql_helper.util import MyConf2
import  os

ps = './conf.yml'
my_conf = MyConf2(ps)

print(f'当前目录{os.getcwd()}')

GEN_PATH = my_conf.get_path('GEN_PATH')
XUQIU_MOBAN_PATH = os.path.join(GEN_PATH,my_conf.get_path('XUQIU_MOBAN_PATH'))
GONGZUOQU_PATH= os.path.join(GEN_PATH,my_conf.get_path('GONGZUOQU_PATH'))
DATA_PATH =  os.path.join(GEN_PATH,my_conf.get_path('DATA_PATH'))
HSZ_PATH =  os.path.join(GEN_PATH,my_conf.get_path('HSZ_PATH'))
VS_PATH= my_conf.get_path('VS_PATH')
WPS_PATH= my_conf.get_path('WPS_PATH')
EDGE_PATH= my_conf.get_path('EDGE_PATH')
MOBAN_PATH = os.path.join(GEN_PATH,my_conf.get_path('MOBAN_PATH'))
SJTC_MOBAN_PATH = os.path.join(GEN_PATH,my_conf.get_path('SJTC_MOBAN_PATH'))
DB_PATH = os.path.join(GEN_PATH,my_conf.get_path('DB_PATH'))
DB_NAME = my_conf.get_path('DB_NAME')
LSJS_PATH=my_conf.get_path('LSJS_PATH')
XQLX =my_conf.get_path('XQLX')
ZDGL_MAX_CNT = my_conf.get_path('ZDGL_MAX_CNT')
TXT_PATH  = my_conf.get_path('TXT_PATH')
VSDX_PATH = my_conf.get_path('VSDX_PATH')
TXHS = my_conf.get_path('TXHS')
TXYD = my_conf.get_path('TXYD')
TXSJ = my_conf.get_path('TXSJ')
ZDXQ = my_conf.get_path('ZDXQ')

for i in [XUQIU_MOBAN_PATH,GONGZUOQU_PATH,DATA_PATH,HSZ_PATH,MOBAN_PATH,DB_PATH,SJTC_MOBAN_PATH,LSJS_PATH]:
    if os.path.exists(i):
        print(f'{i}》》文件路径存在，不新建')
    else:
        print(f'{i}》》不存在，新建文件夹!!!!!!!!!!!!!!!!')
        os.makedirs(i)

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