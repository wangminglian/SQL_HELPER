import datetime
import sys
import os
import logging

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)
from peewee import *

import os,sys
from conf import MOBAN_PATH,DB_PATH,DB_NAME

DB_PATH = DB_PATH
DB_NAME = DB_NAME

db_path = os.path.join(DB_PATH, DB_NAME)



data_base = os.path.join(os.getcwd().split('SQL_Helper')[0],'SQL_Helper/clinet/data.json/SQL_Helper.db')
db = SqliteDatabase(db_path)

dp = DatabaseProxy()
dp.initialize(db)


class Base_Model(Model):
    ctime = DateTimeField(null=True)
    mtime = DateTimeField(null=True)

    def save(self, *args, **kwargs):
        tmp = datetime.datetime.now()
        if self.ctime == None:self.ctime = tmp
        self.mtime = tmp
        return super(Base_Model,self).save(*args, **kwargs)

class Project_detail(Base_Model):
    project_name = CharField(verbose_name='工程名称',primary_key=True)

    class Meta:
        database = dp


class SQL_arg(Base_Model):
    project_name = ForeignKeyField(Project_detail)
    arg_name = AutoField(verbose_name='参数名')
    arg_nike = CharField(verbose_name='参数别名')
    arg_context = TextField(verbose_name='参数内容',default='')


    class Meta:
        database = dp
        unique_together = ['arg_nike','project_name']
    @property
    def items(self):
        '''将context按行分割为一条一条记录'''
        #is_strp 是否过滤空行
        tmp = self.arg_context.split('\n')
        return tmp

class ARG_model(Base_Model):
    arg_name = ForeignKeyField(SQL_arg,related_name='arg_model')
    id = AutoField(primary_key=True)
    rn = CharField(verbose_name='执行顺序')
    arg_model = CharField(verbose_name='参数模式',choices=('正则表达式','字符串切割','轮询','常规','去除换行'),default='常规')
    arg_contorl = CharField(verbose_name='规则字段',default='')
    class Meta:
        database = dp
    def save(self, *args, **kwargs):

        if 'item' in self.arg_contorl:raise ValueError('item是特殊字符')
        return super(Base_Model,self).save(*args, **kwargs)


class History(Base_Model):
    project_name = ForeignKeyField(Project_detail)
    genner_str = CharField(verbose_name='生成语句')
    ret = TextField(verbose_name='运行结果')
    def __str__(self):
        return '{}->{}->{}'.format(self.id,self.project_name,self.genner_str)
    class Meta:
        database = dp

class XQ_INFO(Base_Model):
    id = AutoField(verbose_name='需求编号',primary_key=True)
    name = CharField(verbose_name='需求名称')
    path = CharField(verbose_name='需求存储位置')
    xuqiu_type = CharField(verbose_name='需求类型') # 任务/取数
    status = CharField(verbose_name='需求状态') # 开发中、完成、作废
    tcr = CharField(verbose_name='需求提出人')
    class Meta:
        database = dp


#脚本
class JB_INFO(Base_Model):
    id = AutoField(verbose_name='脚本编号', primary_key=True)
    xq_id = ForeignKeyField(XQ_INFO,on_delete='CASCADE')
    name = CharField(verbose_name='文件名称')
    desc = CharField(verbose_name='备注')
    type = CharField(verbose_name='类型') #开发/提交（版本）
    version = IntegerField(verbose_name='版本号')
    path = CharField(verbose_name='路径')
    gd_name = CharField(verbose_name='归档名称')
    class Meta:
        database = dp

# 引用脚本
class YY_JB_INFO(Base_Model):
    id = AutoField(verbose_name='引用脚本编号', primary_key=True)
    s_xq_id = ForeignKeyField(XQ_INFO,on_delete='CASCADE',verbose_name='源需求id')
    sjb_id = ForeignKeyField(JB_INFO,on_delete='CASCADE',verbose_name='源脚本id')
    t_xq_id = ForeignKeyField(XQ_INFO,on_delete='CASCADE',verbose_name='目标需求id')
    yy_desc = CharField(verbose_name='引用描述',null=True)
    class Meta:
        database = dp

class MD_INFO(Base_Model):
    '''
        markdown 文件信息
    '''
    file_id = AutoField(verbose_name='主键', primary_key=True)
    xq_id = ForeignKeyField(XQ_INFO,on_delete='CASCADE')
    xq_name = CharField(verbose_name='需求名称')
    name = CharField(verbose_name='名称')
    path = CharField(verbose_name='路径')
    bz = CharField(verbose_name='备注')
    tj_time = DateTimeField(verbose_name='提交时间')
    class Meta:
        database = dp


class TABLE_INFO(Base_Model):
    table_id = CharField(verbose_name='表名&主键',primary_key=True)
    desc = CharField(verbose_name='表描述',null=True)
    by1 = CharField(verbose_name='优先级',null=True)
    by2 = CharField(verbose_name='备注',null=True)
    by3 = CharField(null=True)
    class Meta:
        database = dp

# 需求输入输出表
class XQ_TABLE_INFO(Base_Model):
    id = AutoField(verbose_name='主键', primary_key=True)
    xq_id = ForeignKeyField(XQ_INFO,on_delete='CASCADE')
    jb_id =ForeignKeyField(JB_INFO,on_delete='CASCADE')
    table_id = ForeignKeyField(TABLE_INFO)
    table_type = CharField(verbose_name='类型:输入or输出')
    version = IntegerField(verbose_name='版本')
    class Meta:
        database = dp

# 表字段元数据信息
class TABLE_COLUM_INFO(Base_Model):
    id = CharField(verbose_name='字段主键：库.表.字段名称',primary_key=True)
    tb_id = ForeignKeyField(TABLE_INFO,on_delete='CASCADE')
    col_name = CharField(verbose_name='字段名称',null=True)
    col_type =CharField(verbose_name='字段类型',null=True)
    col_desc=CharField(verbose_name='字段描述',null=True)
    ex_text = CharField(verbose_name='特殊描述',null=True)
    class Meta:
        database = dp




# 元数据-口径
class YSJ_KJ(Base_Model):
    id = AutoField(verbose_name='脚本编号', primary_key=True)
    xq_id = ForeignKeyField(XQ_INFO,on_delete='CASCADE')
    jb_id = ForeignKeyField(JB_INFO,on_delete='CASCADE')
    name = CharField(verbose_name='口径名称')
    line = IntegerField(verbose_name='口径在文件中的行号')
    path = CharField(verbose_name='路径')
    class Meta:
        database = dp



class MY_CONFIG(Base_Model):
    id = AutoField(primary_key=True)
    key = CharField(verbose_name='key')
    value = CharField(verbose_name='值')
    tp = CharField(verbose_name='类型')
    class Meta:
        database = dp



create_tables = [YY_JB_INFO]
if __name__ == '__main__':
    print(os.path.join(os.getcwd().split('SQL_Helper')[0],'SQL_Helper/clinet/data.json/SQL_Helper.db'))
    db.connect()
    # # db.drop_tables([MY_CONFIG])
    db.create_tables([YY_JB_INFO])
    # print(db.get_tables())
    # db.create_tables([MD_INFO,])
    # com = db.get_tables()
    # print(com)
    # z = YSJ_KJ.select()
    # for i in z:
    #     print(i.name)

