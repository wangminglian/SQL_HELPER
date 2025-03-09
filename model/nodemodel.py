import datetime

from peewee import *

# 节点库

import os,sys

nd_db_path = 'D:\\code\\SQL_Helper\\Node_db.db'

nd_db = SqliteDatabase(nd_db_path)

nd_dp = DatabaseProxy()
nd_dp.initialize(nd_db)


class Base_Model(Model):
    ctime = DateTimeField(null=True)
    mtime = DateTimeField(null=True)

    def save(self, *args, **kwargs):
        tmp = datetime.datetime.now()
        if self.ctime == None:self.ctime = tmp
        self.mtime = tmp
        return super(Base_Model,self).save(*args, **kwargs)

#　函数信息
class Func_Info(Base_Model):
    func_id = CharField(verbose_name='函数ID',primary_key=True)
    func_name = CharField(verbose_name='函数名称')
    func_type = CharField(verbose_name='函数类型')
    func_desc = CharField(verbose_name='函数描述')
    func = CharField(verbose_name='函数内容')
    is_public = BooleanField(verbose_name='是否发布')
    class Meta:
        database = nd_dp

# 基础节点Port信息
class Func_Port(Base_Model):
    func_port_id = CharField(verbose_name='函数端口Id',primary_key=True)
    func_id = ForeignKeyField(Func_Info,on_delete='CASCADE',backref='func_port')
    func_port_name = CharField(verbose_name='函数端口名称')
    func_port_type = CharField(verbose_name='函数端口类型:输入、输出')
    func_port_data_type = CharField(verbose_name='函数端口数据类型')
    func_port_desc = CharField(verbose_name='函数端口描述')
    func_port_default = CharField(verbose_name='函数端口默认值')
    func_row_number = IntegerField(verbose_name='函数节点排序')
    class Meta:
        database = nd_dp

# # 节点实例化信息
# class Node_Instance(Base_Model):
#     node_instance_id = CharField(verbose_name='实例ID',primary_key=True)
#     node_id = ForeignKeyField(Func_Info,on_delete='SET NULL')
#     node_instance_name = CharField(verbose_name='实例名称')
#     node_instance_desc = CharField(verbose_name='实例描述')
#     class Meta:
#         database = nd_dp
#
#
# # 节点Port实例化信息
# class Node_Port_Instance(Base_Model):
#     port_instance_id = CharField(verbose_name='实例ID',primary_key=True)
#     node_instance_id = ForeignKeyField(Node_Instance,on_delete='CASCADE',backref='node_port_instance')
#     port_id = ForeignKeyField(Node_Port,on_delete='SET NULL')
#     port_instance_name = CharField(verbose_name='实例名称')
#     port_instance_desc = CharField(verbose_name='实例描述')
#     port_instance_default = CharField(verbose_name='实例默认值')
#     class Meta:
#         database = nd_dp





create_tables = [Func_Info,Func_Port]
if __name__ == '__main__':
    nd_db.connect()
    # db.drop_tables([MY_CONFIG])
    nd_db.create_tables(create_tables)
    print(nd_db.get_tables())