from R_Table import R_Select, R_DLL


class G_sql():
    def __init__(self,file_name,dll_name=None):
        self.table = R_Select(file_name)
        self.table_dll = R_DLL(dll_name)

    @property
    def init_his_sql(self):
        #将全量历史数据 去重复 生成增量表
        sql = f"""
INSERT OVERWRITE TABLE {self.table.table_name}_di PARTITION (pt )
SELECT
  --原{self.table.table_name}中字段，除z_start,z_end 开始
    {self.table.str_keys}
  --原{self.table.table_name}中字段，除z_start,z_end 结束
    ,min(pt) AS pt
FROM {self.table.prject_name}.{self.table.table_name}
WHERE pt >0
AND pt <= ${{bdp.system.bizdate}}
GROUP BY {self.table.str_keys}   
;        
        """
        return sql
    @property
    def update_sql(self):
        ##比较两日数据差异，返回变化的数据
        sql = f"""
WITH t1 AS(
    SELECT
      --原{self.table.table_name}中字段，除z_start,z_end 开始
        {self.table.str_keys}
      --原{self.table.table_name}中字段，除z_start,z_end 结束
        ,min(pt) AS pt
    FROM {self.table.prject_name}.{self.table.table_name}
    WHERE pt > TO_CHAR(DATEADD(TO_DATE(${{bdp.system.bizdate}},'yyyymmdd'),-2,'dd'),'yyyymmdd')
    AND pt <= ${{bdp.system.bizdate}}
    GROUP BY {self.table.str_keys}   
    HAVING pt = ${{bdp.system.bizdate}}
)
INSERT OVERWRITE TABLE {self.table.table_name}_di PARTITION (pt )
SELECT * FROM t1
;        
                """
        return sql
    @property
    def di_dll(self):
        ##返回增量表创表语句
        return self.table_dll.di_dll




if __name__ == '__main__':
    g = G_sql('./select.txt','./dll.txt')
    # print(g.init_his_sql())
    # print(g.di_dll)
    print(g.update_sql)

    """
    gz-> (20 + 5.4 +5.4+ 1 ) *20 =636 
    zm-> 80 * 4 =320
    mm-> 100+50 =150
    636 + 320 + 150 + 3600 +100 +300
    """


# 8000 -> 3000*1.025 + 3000*1.038+750*1.4+500*1.2+1.6*350+1.8*350
#(8789+7789)*0.5
# 61200+43200
#34560

# 1/4 ->1/3 -> 1/2 ->1