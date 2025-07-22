import ast
import re
from abc import ABC,abstractmethod

from model.model import SQL_arg, ARG_model, TABLE_COLUM_INFO, TABLE_INFO


class CommdReader(ABC):
    '''解析器基类'''
    def __init__(self,data,arg_contorl='',sp=None):
        try:
            if type(data) ==SQL_arg:
                self.data = data
            else:
                self.data = data.data
            if sp is None:
                self.items = data.items
            else:
                self.items=eval(f'data.items[{sp}]')
                print('type::::::::')
                print(type(self.items))
                if type(self.items) != list:
                    self.items = [self.items]
            self.arg_contorl = arg_contorl
        except:
            raise ValueError('输入参数类型错误:{}'.format(type(data)))

    def bulid(self):
        tmp = self.value
        return self

    @property
    def key(self):
        return self.data.arg_name

    @property
    def value(self):
        return self.items


class Reader_Factory(object):
    def __init__(self):
        pass

    @staticmethod
    def get_instance(data,sp=None):
        arg_models = data.arg_model.where(ARG_model.rn!=0).order_by(ARG_model.rn).execute()
            # order_by(ARG_model.rn)
            # .execute()
        
        data = Normal_Reader(data,sp=sp).bulid()
        
        for item in arg_models:
            if item.arg_model == '字符串切割':
                data= Splits_Reader(data,item.arg_contorl).bulid()
            elif item.arg_model == '正则表达式':
                data= Regex_Reader(data,item.arg_contorl).bulid()
            elif item.arg_model == '轮询':
                data= Circle_Reader(data,item.arg_contorl).bulid()
            elif item.arg_model =='常规':
                data= Normal_Reader(data,item.arg_contorl).bulid()
            elif item.arg_model =='去除换行':
                data=RemoveN_Reader(data, item.arg_contorl).bulid()
            elif item.arg_model == 'GROUP BY':
                data = GroupBy_Reader(data, item.arg_contorl).bulid()
            elif item.arg_model == '行分隔':
                data = LineSplit_Reader(data, item.arg_contorl).bulid()
            elif item.arg_model == '变量分发':
                data = Normal_Reader(data, item.arg_contorl).bulid()
            elif item.arg_model=='元数据':
                data=Sql_Reader(data,item.arg_contorl).bulid()
            elif item.arg_model=='自定义函数':
                data=ZDY_FUN_Reader(data,item.arg_contorl).bulid()
            elif item.arg_model=='超级自定义函数':
                data=CJ_ZDY_FUN_Reader(data,item.arg_contorl).bulid()
            else:
                raise ValueError('未知的arg_model类型:{}'.format(item.arg_model))
        return data
class LineSplit_Reader(CommdReader):
    @property
    def value(self):
        ret =[]
        print(self.arg_contorl)
        if ':' in self.arg_contorl:
            try:
                # contl = self.arg_contorl.strip().split(':')
                # start = int(contl[0])
                #
                # size = len(self.items)
                # print(contl)
                # if  len(contl)>1:
                #     end = int(contl[1])
                # else:
                #     end =size-1
                # if end >size-1:
                #     xc = end-(size)
                #     end = size
                #     ret = self.items[start:end]
                #     for i in range(xc):
                #         ret.append('******')
                # else:
                ret = eval(f'self.items[{self.arg_contorl}]')
                # ret = eval(f"self.items[{self.arg_contorl}]")
            except Exception:
                raise ValueError(f"{self.data.arg_nike}::参数：{self.arg_contorl}不合法")
        else:
            try:
                end = int(self.arg_contorl)
                size = len(self.items)
                if end >size-1:
                    ret = ['******',]
                else:
                    ret = [self.items[end],]

                # ret = [eval(f"self.items[{self.arg_contorl}]"),]
            except Exception:
                raise ValueError(f"{self.data.arg_nike}::参数：{self.arg_contorl}不合法")
        self.items = ret
        return ret
class RemoveN_Reader(CommdReader):
    @property
    def value(self):
        ret = self.arg_contorl.join(self.items)
        self.items = [ret,]
        return [ret,]
class GroupBy_Reader(CommdReader):
    @property
    def value(self):
        tmp = 1
        ret = []
        for i in self.items:
            ret.append(str(tmp))
            tmp += 1
        self.items =[','.join(ret),]
        return [','.join(ret),]

class ZDY_FUN_Reader(CommdReader):

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
    @property
    def value(self):
        com = self.arg_contorl
        my_fun = self.str_to_func(com)
        ret = []
        for i in self.items:
            i_tmp = my_fun(i)
            if type(i_tmp)!=str:
                raise ValueError('自定义函数输出格式必须为字符串')
            ret.append(i_tmp)
        self.items = ret


class CJ_ZDY_FUN_Reader(CommdReader):

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
    @property
    def value(self):
        com = self.arg_contorl
        my_fun = self.str_to_func(com)
        tmp_ret = my_fun(self.items)
        if type(tmp_ret)!=list:
            raise ValueError('超级自定义函数输出格式必须为列表')
        ret = []
        for i in tmp_ret:
            i_tmp = i
            if type(i_tmp)!=str:
                raise ValueError('超级自定义函数输出列表内内容必须是字符串')
            ret.append(i_tmp)
        self.items = ret


class Sql_Reader(CommdReader):

    # TB: PTEMP.TMP_RPT_GRP_OWE_USER_XZZXYJ_M2 T1
    def decode_tb(self,line):
        # 解析表控制语句
        tmp_alis='T999'
        tmp = line.split(':')[1:]
        tb = tmp[0].split()
        tb_name=tb[0].strip()
        if len(tb)>1:
            tmp_alis=tb[1].strip()
        return (tb_name,tmp_alis)

    def decode_cl(self,line):
        # 解析列语句
        tp = line.split('.')
        tba = 'T999'
        cname = tp[-1].strip()
        if len(tp)>1:
            tba=tp[0]
        return tba,cname

    def get_date_from_db(self):
        pass
    def decode_text(self,text):
        text = text.strip()
        tb_dict={}
        res_list=[]
        for line in text.split('\n'):
            line = line.strip()
            if line=='':
                continue
            if ':' in line:
                tb_name,tb_alis=self.decode_tb(line)
                tbs = tb_dict.get(tb_alis,[])
                tbs.append(tb_name)
                tb_dict[tb_alis]=tbs
            else:
                cba,cname =self.decode_cl(line)
                res_list.append((cba,cname))

        return res_list,tb_dict

    @property
    def value(self):
        com = self.arg_contorl.strip()
        res_list, tb_dict = self.decode_text('\n'.join(self.items))
        ret = []
        for tba,cln in res_list:
            tbs = tb_dict.get(tba,[])
            if tbs==[]:
                items = TABLE_COLUM_INFO.select().where((TABLE_COLUM_INFO.col_name == cln)).join(TABLE_INFO).order_by(TABLE_INFO.by1.desc()).limit(1)
            else:
                items = TABLE_COLUM_INFO.select().where((TABLE_COLUM_INFO.col_name==cln) &(TABLE_COLUM_INFO.tb_id.in_(tbs))).join(TABLE_INFO).order_by(TABLE_INFO.by1.desc()).limit(1)
            col_name = cln
            col_type = '***'
            col_desc='***'
            for i in items:
                col_name = i.col_name
                col_type = i.col_type
                col_desc = i.col_desc
            tmp = f"{tba}|{col_name}|{col_type}|{col_desc}"
            ret.append(tmp)
        self.items=ret
        return ret

class Splits_Reader(CommdReader):
    '''字符串分割解析器'''
    @property
    def value(self):
        com = self.decode_com()
        ret = []
        for item in self.items:
            try:

                print(item,com)
                tmp = eval(com)
                if type(tmp)==str:
                    ret.append(eval(com))
                else:
                    raise ValueError(f'{self.data.arg_nike}::生成的结果只能是字符串')
            except Exception as e:
                raise ValueError('{}::分割语句错误:{}'.format(self.data.arg_nike,e.__str__()))
        self.items = ret
        return ret

    def decode_com(self):
        return self.arg_contorl.replace('${arg}', 'item')

class Normal_Reader(CommdReader):
    '''常规解析器'''
    pass

class Regex_Reader(CommdReader):
    '''正则表达式解析器'''
    @property
    def value(self):
        ret = []
        reg,index = self.decode_com()
        try:
            reg_com = eval("re.compile('{}')".format(reg))
            for item in self.items:
                try:
                    tmp = re.search(reg_com, item).group(index)
                except Exception as e:
                    tmp = '*******ERROR********:{}'.format(e.__str__())
                ret.append(tmp)
            self.items = ret
            return ret
        except Exception as e:
            raise ValueError(f'{self.data.arg_nike}::正则表达不合法')

    def decode_com(self):
        contorl =  self.arg_contorl
        print(contorl)
        index_com = re.compile('index=([0-9]*)')
        reg_com = re.compile('reg=(.*?)(?=;index=|$)')
        try:
            reg = format(re.search(reg_com,contorl).group(1))
            index = re.search(index_com,contorl).group(1)
            return reg,int(index)
        except Exception as e:
            raise ValueError(f'{self.data.arg_nike}::传入参数错误')


class Circle_Reader(CommdReader):
    '''轮询'''

    def key(self):
        return self.data.arg_name
    @property
    def value(self):
        contorl = self.arg_contorl
        try:
            ret = []
            contorl = int(contorl)
            if contorl>0:
                for i in range(contorl):
                    for item in self.items:
                        ret.append(item)
            else:
                for item in self.items:
                    for i in range(-contorl):
                        ret.append(item)
            self.items = ret
            return ret
        except Exception as e:
            raise ValueError(f'{self.data.arg_nike}::轮询参数不合法，请输入一个整数')




class Genner_Com(object):
    def init_data(self,sql_args):
        '''装载'''
        ret = {}
        for item,sp in zip(sql_args,self.args_list_dict):
            ret[item.arg_nike] = Reader_Factory.get_instance(item,sp)
        return ret
    def get_szys(self,item):
        rc = re.compile('\[(.+?)\]')
        args = re.search(rc, item)
        if args:
            return (item.replace(f'[{args.group(1)}]', '')),args.group(1)
        else:
            return item,None

    def __init__(self,com,project_name):
        self.com:str = com
        self.regex_com = re.compile('\$\{(.+?)\}')
        self.args1 = re.findall(self.regex_com,self.com)
        self.args=[]
        self.args_list_dict=[]
        for i in self.args1:
            x,y = self.get_szys(i)
            self.args.append(x)
            self.args_list_dict.append(y)
        print(self.args,self.args_list_dict)
        tmp = SQL_arg.select().where((SQL_arg.project_name ==project_name) , (SQL_arg.arg_nike.in_(self.args))).execute()
        self.data = self.init_data(tmp)

    @property
    def value(self):
        if len(self.args)==0:
            return [self.com,]
        size = max([len(self.data[i].items) for i in self.args])
        # re_tmp = ['${'+i+'}' for i in zip(self.args,self.args_list_dict)]
        re_tmp = []
        for x,y in zip(self.args,self.args_list_dict):
            if y:
                re_tmp_i = '${'+x+f'[{y}]'+'}'
            else:
                re_tmp_i = '${'+x+'}'
            re_tmp.append(re_tmp_i)
            print(re_tmp_i)
        tmp = self.com
        for arg in re_tmp:
            tmp = tmp.replace(arg,'{}')
        ret = []
        for i in range(size):
            tmp_com = "tmp.format("
            for r in range(len(self.args)):
                if len(self.data[self.args[r]].items)==1:
                    _tmp = "self.data[self.args[{}]].items[0]".format(str(r))
                else:
                    _tmp =  "self.data[self.args[{}]].items[i]".format(str(r))
                tmp_com += "{},".format(_tmp)
            tmp_com = tmp_com[:-1] + ')'
            try:
                print(f"self.data[self.args[0]].items[0]:{self.data[self.args[0]].items}")
                print(f'tmp_com:{tmp_com}')
                print(f"tmp:{tmp}")
                gener_str = eval(tmp_com)
            except Exception as e:
                gener_str = '********ERROR*********:{}'.format(e.__str__())
                # raise ValueError('生成语句错误:{}'.format(e.__str__()))
            ret.append(gener_str)
        return ret




# ${创表语句} comment '${字段描述信息}'
import pyperclip
if __name__ == '__main__':
    test = """
    TB:PTEMP.TMP_RPT_GRP_OWE_USER_XZZXYJ_M2 
    TB:PTEMP.TMP_RPT_GRP_OWE_USER_XZZXYJ_M1 T2
    TB:PTEMP.TMP_RPT_GRP_OWE_USER_XZZXYJ_M3
    
    T1.CUST_ID
    T2.CITY_DESC
    CITY_CODE
    """
    a = Sql_Reader(111)
    u=a.decode_text(test)
    print(u)




