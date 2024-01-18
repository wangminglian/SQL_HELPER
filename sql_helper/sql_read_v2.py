import time
from sqlparse.keywords import KEYWORDS_COMMON
import sqlparse
from sqlparse.sql import Token
from collections import namedtuple
import re
import timeit




#添加Gbase关键字
KEYWORDS_COMMON ['DISTRIBUTED']= sqlparse.tokens.Keyword


SQL_SCHEMA = namedtuple('SQL_SCHEMA','idx sql_type sql_schema')
TABLE_INFO = namedtuple('TABLE_INFO','table_name cloums comment')
CLOUM_INFO = namedtuple('CLOUM_INFO','cloum_name cloum_type comment')

GBASE_KW = ('EXPRESS DISTRIBUTED','BY','UTF8')

EX_SQL_TYPE = (sqlparse.tokens.Text.Whitespace.Newline,sqlparse.tokens.Text.Whitespace)
#SQL解析工具
class SQL_DE_UTIL:
    def __init__(self):
        self.sql = None
        self.path = None
        self.sqlps_ = []
        self.sqlps = []
        self.sql_split_ps = []
        self.tokens = None
        self.create_tables =[]
        self.re_delte1 = re.compile('\s+DEFAULT\s+NULL\s*')
        self.re_delte2 = re.compile('\s+DEFAULT\s+\'.*\'\s*')
        self.re_delte3 = re.compile('\s+NOT\s+NULL\s*')




    @property
    def v_sqlps(self):
        return self.sqlps
    @property
    def v_sql_split_ps(self):
        return self.sql_split_ps
    # 设置SQL,返回规则后的SQL

    #去除左右两边引号
    def y_strip(self,tx:str):
        if (tx.startswith('"') and tx.endswith('"'))or(tx.startswith("'") and tx.endswith("'")):
            tx = tx[1:-1]
        return tx.upper()

    # 格式化字段类型
    def g_clty(self,tx:str):
        tx =re.sub(self.re_delte1,'',tx)
        tx =re.sub(self.re_delte2,'',tx)
        tx = re.sub(self.re_delte3, '', tx)
        tx = tx.upper()
        tx = tx.replace("'",'')
        tx = tx.replace('"','')
        return tx
    def set_sql(self,sql):
        self.sql = sqlparse.format(sql,reindent=True, keyword_case='upper',strip_comments=True)
        self.sqlps_ =sqlparse.parse(self.sql)

        tmp_split = []
        tmp = 0
        for  i in self.sqlps_:
            for it in i.tokens:
                if it.ttype in EX_SQL_TYPE:
                    continue
                self.sqlps.append(it)
                tmp_split.append(it)
                if it.ttype in (sqlparse.tokens.Punctuation):
                    tmp +=1
                    a = SQL_SCHEMA(idx=tmp,sql_type=f'{tmp_split[0].ttype}:{tmp_split[0]}',sql_schema=tmp_split)
                    self.sql_split_ps.append(a)
                    tmp_split=[]
        for i in self.sql_split_ps:
            if i.sql_type =='Token.Keyword.DDL:CREATE':
                self.create_tables.append(i)

    def get_cloums(self,sql):
        ret = []
        if sql is None:
            return ret
        sql = sql.value.strip()[1:-1]
        for line in sql.split('\n'):
            line = line.strip()
            if line.startswith(','):
                line = line[1:]
            if line.endswith(','):
                line = line[:-1]
            tp = line.split()
            if len(tp)<2:
                continue
            clname = tp[0]
            clname = self.y_strip(clname)

            if ' COMMENT ' in line:
                tp2 =line.split(' COMMENT ')
                clcomment = tp2[-1].strip()
                if clcomment.startswith("'") and clcomment.endswith("'"):
                    clcomment = clcomment[1:-1]
                elif clcomment.startswith('"') and clcomment.endswith('"'):
                    clcomment = clcomment[1:-1]
                tt = ' '.join(tp2[:-1])
                tt = tt.replace(clname,'')

                tt = self.g_clty(tt)
                cltype = tt
            else:
                tt = line.replace(clname,'')
                tt = self.g_clty(tt)
                cltype = tt
                clcomment =''
            cltype = cltype.replace(' ','')
            tp = CLOUM_INFO(cloum_name=clname,cloum_type=cltype,comment=clcomment)
            ret.append(tp)
        return ret



    def get_creat_tables(self):

        ret = []
        for its in self.create_tables:
            tb_name = None
            tb_cloums_str = None
            tb_tb_comment = None
            comment_flag = False
            for it in its.sql_schema:
                if it.ttype not in (sqlparse.tokens.Keyword) and tb_name is None:
                    tb_name = it.value
                    tb_name = self.y_strip(tb_name)
                    continue
                if it.ttype not in (sqlparse.tokens.Keyword) and tb_cloums_str is None:

                    tb_cloums_str = self.get_cloums(it)
                    continue
                if it.ttype in (sqlparse.tokens.Keyword) and it.value == 'COMMENT':
                    comment_flag = True
                    continue
                if it.ttype not in (sqlparse.tokens.Keyword,sqlparse.tokens.Operator.Comparison) and tb_tb_comment is None and comment_flag is True:
                    tb_tb_comment = it.value.strip()
                    if (tb_tb_comment.endswith('"') and tb_tb_comment.endswith('"'))or(tb_tb_comment.endswith("'") and tb_tb_comment.endswith("'")):
                        tb_tb_comment = tb_tb_comment[1:-1]

            # create .. like 写法过滤掉
            if ' LIKE '  in tb_name:
                continue
            else:
                ttinfo = TABLE_INFO(table_name=tb_name, cloums=tb_cloums_str, comment=tb_tb_comment)
                ret.append(ttinfo)
        return ret



    def set_sql_by_file(self,fp):

        with open(fp, 'r', encoding='utf8') as f:
            sql = '\n'.join(f.readlines())
        self.sql = self.set_sql(sql)






if __name__ == '__main__':
    a = SQL_DE_UTIL()
    start_time = time.time()

    a.set_sql_by_file('E:\\思特奇\\学习笔记\\数仓任务\\关于对政企经营沙盘系统中酒店清单摸排营销进行统计分析报表开发的需求.sql')
    end_time = time.time()



    u = a.get_creat_tables()

    for i in u:
        print(i)

    #
    # for i in u:
    #     print(f"--------------------{i.table_name}---------------------------")
    #     for y in i.cloums:
    #         print(y.cloum_name,y.cloum_type,y.comment)
    # for i in a.v_sql_split_ps:
    #     print(i.idx)



# # 解析 SQL 语句
# parsed = sqlparse.format(sql,reindent=True, keyword_case='upper',strip_comments=True)
#
# # a = sqlparse.split(parsed)
# # print(a)
# ps = sqlparse.parse(parsed)
#
# for i  in ps:
#     print(i.tokens)
#     for it in i.tokens:
#         # 去除空格、空行
#         if  it.ttype in (sqlparse.tokens.Text.Whitespace.Newline,sqlparse.tokens.Text.Whitespace):
#             continue
#         print(it.ttype,it)



# 获取解析后的语句
# 的各个部分
# for statement in parsed:
#     print('---------')
#     print(statement)