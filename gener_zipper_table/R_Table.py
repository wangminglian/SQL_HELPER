from collections import namedtuple

# with open('./select.txt','rb') as f:

class R_Select():
    def __init__(self,filename):
        with open(filename, 'r') as f:
            self.sql = f.readlines()
    @property
    def keys(self):
        ret = []
        for i in self.sql[1:-3]:
            #过滤非key字段
            i = i.replace('\n','')
            i = i.replace(',','')
            if i in ('z_start','z_end'):continue
            ret.append(i)
        return ret

    @property
    def str_keys(self):
        ret = ''
        tmp = 0
        for i in self.keys:
            ret +='\t'+ ','+i.strip()+'\n'
            if tmp ==0:ret = ret.replace(',','')
            tmp +=1
        return ret.strip()

    @property
    def table_name(self):
        name = self.sql[-2].split('.')[1].strip()
        return name
    @property
    def prject_name(self):
        name = self.sql[-2].split(' ')[2].split('.')[0]
        return name


table_meta = namedtuple('table_meta','type comment')

class R_DLL():
    def __init__(self,filename):
        with open(filename, 'r') as f:
            self.sql = f.readlines()
    @property
    def di_dll(self):
        self.sql[0] = self.sql[0].strip()+'_di'
        sql = ''
        for i in self.sql:
            sql+=i
        return sql

    def metadata(self):
        tmp_s = False
        for item in self.sql:
            if item == '(\n':
                tmp_s = True
                continue
            if item == ')\n':
                tmp_s = False
                continue
            if not tmp_s :
                continue
            print(item.strip().split())




if __name__ == '__main__':
    a = R_Select('./select.txt')
    b = R_DLL('./dll.txt')
    b.metadata()
