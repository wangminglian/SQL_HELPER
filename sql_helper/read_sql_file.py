import  re

from sql_helper.sql_read_v2 import SQL_DE_UTIL

# 从SQL文档中提取元数据

GBASE_SJLX=['TINYINT','SMALLINT','INT','BIGINT',' FLOAT','DOUBLE','DECIMAL','NUMERIC','CHAR','VARCHAR','TEXT','BLOB','LONGBLOB','DATE','TIME','DATETIME','TIMESTAMP']
class Reader_SQL:
    def __init__(self):
        self.re_rtl_table = re.compile(r"FROM\s+\b(\w+\.\w+)\b|JOIN\s+\b(\w+\.\w+)\b")
        # self.re_creat_tb = re.compile( r"CREATE TABLE IF NOT EXISTS[s\S]*?;")
        self.re_creat_tb =  r"CREATE TABLE IF NOT EXISTS [\w.]+[\s\S]*?;"
        self.re_out_tb = re.compile(r"CREATE TABLE IF NOT EXISTS ([^\s(]+)")
        self.re_out_comment=re.compile(r"COMMENT = \'(.+)\';")
        self.re_comment_ = re.compile(r"'(.*?)'")
        self.sql_eng = SQL_DE_UTIL()



    # 判断是否是关键字，是否需要保存
    def is_gjz(self,txt:str):
        if '-- >>' in txt:
            return True
        else:
            return False
    def read_sql_to_gjz(self,file_name):
        gjz_list=[]
        with open(file_name,'r',encoding='utf-8') as f:
            rn = 1
            line = f.readline()
            while line:
                if self.is_gjz(line):
                    gjz = line.split('-- >>')[-1].strip()
                    gjz_list.append((gjz,rn))
                rn +=1
                line = f.readline()
        return (file_name,gjz_list)

    def get_tbname(self,line):
        line = line.upper()
        matches = self.re_rtl_table.findall(line)
        if len(matches)>=1:
            tmp = matches[0]
            ret = ''.join(tmp)
            if ret.startswith('PTEMP'):
                return
            # if ret.endswith('_MANU'):
            #     return
            return ret
        else:
            return None
    def read_sql_to_rtl_table(self,file_name):
        _,out_tb = self.read_sql_to_out_table(file_name)
        out_tbs = out_tb.keys()
        # 获取输入表
        with open(file_name,'r', encoding='utf-8') as f:
            text = ''.join(f.readlines())
        text = self.get_real_sql(text)
        gjz_list = set()
        for line in text.split('\n'):
            tb_name = self.get_tbname(line)
            if tb_name and not tb_name in out_tbs:
                gjz_list.add((tb_name))
        return (file_name, list(gjz_list))




    def get_real_sql(self,text):
        ret = ''
        for i in text.split('\n'):
            if i.startswith('-- '):
                continue
            elif '-- ' in i:
                ret+=i.split('-- ')[0]
            else:
                ret+=i
            ret +='\n'
        return  ret

    #V2获取输出表元数据信息
    def read_sql_to_out_table(self, file_name):
    # 解析输出表
        ret_dict = {}
        comment_dict={}
        self.sql_eng.set_sql_by_file(file_name)
        tbs = self.sql_eng.get_creat_tables()
        for i in tbs:
            ret_dict[i.table_name] =i.cloums
            comment_dict[i.table_name] = i.comment

        return ret_dict, comment_dict



    #
    # # V1 获取输出表元数据信息
    # def read_sql_to_out_table(self,file_name):
    #     # 解析输出表
    #     ret_dict = {}
    #     comment_dict={}
    #     with open(file_name,'r', encoding='utf-8') as f:
    #         text = ''.join(f.readlines())
    #     text = self.get_real_sql(text)
    #     creat_sqls = self.get_creat_tb_sql(text)
    #
    #     for item in creat_sqls:
    #         try:
    #             if ' AS ' in item:
    #                 continue
    #             table_name = self.re_out_tb.findall(item)[0]
    #             comment = self.re_out_comment.findall(item)
    #             if len(comment)==1:
    #                 if comment[0]!='B域(Gbase)-域-PTEMP-描述':
    #                     comment_dict[table_name]=comment[0]
    #                 else:
    #                     comment_dict[table_name] = ''
    #             else:
    #                 comment_dict[table_name]=''
    #             items =item.split('\n')
    #             zdxxlist = []
    #
    #
    #             for _item in items:
    #                 _item=_item.strip()
    #                 if 'CREATE TABLE ' in _item:
    #                     continue
    #                 elif _item.strip()=='(' or _item.strip()==')' or _item.strip()==';':
    #                     continue
    #                 elif '=' in _item:
    #                     continue
    #                 elif 'DISTRIBUTED' in _item:
    #                     continue
    #                 if _item.startswith(','):
    #                     _item=_item[1:]
    #                 elif _item.endswith(','):
    #                     _item=_item[:-1]
    #                 zdxxs = _item.strip().split()
    #
    #
    #                 try:
    #                     name = zdxxs[0]
    #                     zdlx = zdxxs[1]
    #
    #                     ret = re.search(self.re_comment_,_item)
    #                     if ret:
    #                         zdms = ret.group(1)
    #                     else:
    #                         zdms='***'
    #
    #                     zdxxlist.append([name,zdlx,zdms])
    #                 except Exception as e:
    #                     print(f'解析表:{table_name}时出错::{zdxxs}::{e.__str__()}')
    #                     continue
    #             ret_dict[table_name]=zdxxlist
    #         except Exception as e:
    #             print(e.__str__())
    #             print(item)
    #             raise ValueError(f'解析表:{table_name}时出错')
    #     return ret_dict,comment_dict



    def get_creat_tb_sql(self,text):
        ret =[]
        # 获取建表语句
        mtches = re.finditer(self.re_creat_tb,text,re.DOTALL|re.MULTILINE|re.IGNORECASE)
        ret = [i.group() for i in mtches]
        return ret



if __name__ == '__main__':
    a = Reader_SQL()
    fn = 'E:\思特奇\学习笔记\数仓任务\逾期欠费集团新增专线欠费预警-数据源.sql'
    _,U =a.read_sql_to_out_table(fn)
    x = a.read_sql_to_rtl_table(fn)
    print(x)
    print(U.keys())

