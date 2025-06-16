# SQL代码解释器，传入参数，输入文件、输出文件、输入表元数据信息（可选）
import logging
import dataclasses
import sqlglot
import re
from sqlglot import exp

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# 数据解析基础数据类

@dataclasses.dataclass
# 存储一个sql文件读入的sql代码
class SQL_CODE:
    sql_code: str # 原始sql代码
    sql_code_base: str # 标准化后的sql代码
    sql_list: list # 标准化后的sql语句列表
    file_name: str # 文件名

@dataclasses.dataclass
# 存储一条单一的sql语句
class SQL_ITEM:
    sql_str: str



class SQL_ANA:
    def __init__(self, sql_file, output_file, input_meta_info=None):
        self.sql_file = sql_file
        self.output_file = output_file
        self.input_meta_info = input_meta_info
        self.sql_code = self.read_sql_file()


    def read_sql_file(self):
        # 读取sql文件
        with open(self.sql_file, "r", encoding="utf-8") as f:
            sql_code = f.read()
        out = SQL_CODE(sql_code=sql_code
                       , sql_code_base=self.sql_parse(sql_code)
                       , sql_list=self.sql_split(sql_code)
                       , file_name=self.sql_file)
        logging.info(f"读取sql文件成功: {self.sql_file}")
        
        return out
    
    def sql_parse(self, sql_code: str):
        pass



    def sql_split(self,sql_code):
        # 将sql代码分割成多个sql语句
        pass

        
        
        
    
    def read_meta_info(self):
        # 读取表元数据信息
        pass
    
    def analyze_sql(self):
        # 分析sql代码
        pass
    
    def write_output(self):
        # 输出结果
        pass




if __name__ == "__main__":
    sa = SQL_ANA(sql_file="./test/代付划拨明细.sql", output_file="./test/代付划拨明细_out.txt")
