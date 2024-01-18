import re
from abc import ABC,abstractmethod

from model.model import SQL_arg


class CommdReader(ABC):
    '''解析器基类'''
    def __init__(self):
        self.data = None

    def set(self,data):
        if type(data)!=SQL_arg:raise TypeError('类型不正确')
        self.data:SQL_arg  = data
        return self
    @abstractmethod
    def key(self):
        pass
    @abstractmethod
    def value(self):
        pass

    def decode_args(self,arg,is_strp = False):
        '''将context按行分割为一条一条记录'''
        #is_strp 是否过滤空行
        tmp = arg.split('\n')
        if is_strp:
            while tmp[0] == '':
                tmp = tmp[1:]
            while tmp[-1]=='':
                tmp = tmp[:-1]
        return tmp


class Reader_Factory(object):
    def __init__(self):
        pass

    @staticmethod
    def get_instance(data):
        if type(data)!=SQL_arg:raise TypeError('类型不正确')

        if data.arg_model == '字符串切割':
            tmp = Splits_Reader()
            return tmp.set(data)
        elif data.arg_model == '正则表达式':
            tmp = Regex_Reader()
            return tmp.set(data)
        elif data.arg_model == '轮询':
            tmp = Circle_Reader()
            return tmp.set(data)
        elif data.arg_model =='常规':
            tmp = Normal_Reader()
            print("@@@@@@@@@@@@@@@@@@@@@@@@"+tmp)

            return tmp.set(data)
        elif data.arg_model=='去除换行':
            tmp = RemoveN_Reader()
            print("@@@@@@@@@@@@@@@@@@@@@@@@"+tmp)
            return tmp.set(data)
        else:
            raise ValueError('未知的arg_model类型:{}'.format(data.arg_model))


class Splits_Reader(CommdReader):
    '''字符串分割解析器'''
    # data.json: SQL_arg = SQL_arg()
    def key(self):
        return self.data.arg_name
    @property
    def value(self):
        items = self.decode_args(self.data.arg_context)
        com = self.decode_com()
        ret = []
        for item in items:
            try:
                tmp = eval(com)
                if type(tmp)==str:
                    ret.append(eval(com))
                else:
                    raise ValueError('生成的结果只能是字符串')
            except Exception as e:
                raise ValueError('分割语句错误:{}'.format(e.__str__()))
        return ret

    def decode_com(self):
        return self.data.arg_contorl.replace('${arg}', 'item')

class Normal_Reader(CommdReader):
    '''常规解析器'''
    def key(self):
        return self.data.arg_name
    @property
    def value(self):
        items = self.decode_args(self.data.arg_context)
        ret = []
        for item in items:
            ret.append(item)
        return ret

class RemoveN_Reader(CommdReader):
    def key(self):
        return self.data.arg_name
    @property
    def value(self):
        items = self.decode_args(self.data.arg_context)
        ret = ''
        for item in items:
            ret+=item
        return [ret,]

class Regex_Reader(CommdReader):
    '''正则表达式解析器'''
    def key(self):
        return self.data.arg_name

    @property
    def value(self):

        ret = []
        reg,index = self.decode_com()
        try:
            reg_com = eval("re.compile('{}')".format(reg))
            for item in self.decode_args(self.data.arg_context):
                ret.append(re.search(reg_com,item).group(index))
            return ret
        except Exception as e:
            raise ValueError('正则表达不合法')

    def decode_com(self):
        contorl =  self.data.arg_contorl
        print(contorl)
        index_com = re.compile('index=([0-9]*)')
        reg_com = re.compile('reg=(.*?)(?=;|$)')
        try:
            reg = format(re.search(reg_com,contorl).group(1))
            index = re.search(index_com,contorl).group(1)
            return reg,int(index)
        except Exception as e:
            raise ValueError('传入参数错误')


class Circle_Reader(CommdReader):
    '''轮询'''

    def key(self):
        return self.data.arg_name
    @property
    def value(self):
        contorl = self.data.arg_contorl
        items = self.decode_args(self.data.arg_context)
        try:
            ret = []
            contorl = int(contorl)
            if contorl>0:
                for i in range(contorl):
                    for item in items:
                        ret.append(item)
            else:
                for item in items:
                    for i in range(-contorl):
                        ret.append(item)

            return ret
        except Exception as e:
            raise ValueError('轮询参数不合法，请输入一个整数')




class Genner_Com(object):
    def init_data(self,sql_args):
        '''装载'''
        ret = {}
        for item in sql_args:
            ret[item.arg_nike] = Reader_Factory.get_instance(item)
        return ret

    def __init__(self,com,project_name):
        self.com:str = com
        self.regex_com = re.compile('\$\{(.+?)\}')
        self.args = re.findall(self.regex_com,self.com)
        tmp = SQL_arg.select().where((SQL_arg.project_name ==project_name) , (SQL_arg.arg_nike.in_(self.args))).execute()
        self.data = self.init_data(tmp)

    @property
    def value(self):
        size = len(self.data[self.args[0]].value)
        re_tmp = ['${'+i+'}' for i in self.args]
        tmp = self.com
        for arg in re_tmp:
            tmp = tmp.replace(arg,'{}')
        ret = []
        for i in range(size):
            tmp_com = "tmp.format("
            for r in range(len(self.args)):
                _tmp =  "self.data.json[self.args[{}]].value[i]".format(str(r))
                tmp_com += "{},".format(_tmp)
            tmp_com = tmp_com[:-1] + ')'
            try:
                gener_str = eval(tmp_com)
            except Exception as e:
                gener_str = '********ERROR*********:{}'.format(e.__str__())
                # raise ValueError('生成语句错误:{}'.format(e.__str__()))
            ret.append(gener_str)
        return ret

# ${创表语句} comment '${字段描述信息}'
import pyperclip
if __name__ == '__main__':
    # s = ',SUM(IF (original_amount>${命名参数3}*${比较参数2},${赋值参数},0)) AS over_${比较参数2}${命名参数3}_${命名参数} --${注释}'
    # args = ['命名参数3','比较参数2','赋值参数','比较参数2','命名参数3','命名参数','注释']
    # re_tmp = re.compile('[{}$]'.format(''.join(args)))
    # tmp = re.sub(re_tmp, '', s)
    # print(tmp)
    pyperclip.copy('haha ')




