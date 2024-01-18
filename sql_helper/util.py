import yaml
from collections import OrderedDict
#
# class MyConf:
#     def __init__(self):
#         pass
#
#     def get_value(self,key,tp):
#         tmp = MY_CONFIG.select().where((MY_CONFIG.key==key)&(MY_CONFIG.tp==tp)).order_by(MY_CONFIG.mtime.desc()).limit(1)
#         if len(tmp)==0:
#             return None
#         else:
#             return tmp[0].value
#     def set_value(self,key,value,tp):
#         tmp = MY_CONFIG(key=key,value=value,tp=tp)
#         tmp.save()
#         return 1
#     def delete(self,id):
#         MY_CONFIG.delete_by_id(id)


class MyConf2:
    def __init__(self,ps):
        self.ps = ps
        with open(self.ps,'rb') as f:
            self.value = yaml.safe_load(f)

    def get_path(self,name):
        datas = self.value.get('conf_path')
        ret = datas.get(name,None)
        if ret == None:
            raise KeyError(f"配置文件配置不正确，请配置，文件路径：{self.ps}")
        return datas.get(name,None)


class FIFOdict(OrderedDict):
    def __init__(self, capacity):
        super().__init__()
        self._capacity = capacity

    def __setitem__(self, key, value):
        containsKey = 1 if key in self else 0
        if len(self) - containsKey >= self._capacity:
            last = self.popitem(last=False)
            print('remove:', last)
        if containsKey:
            del self[key]
            print('set:', (key, value))
        else:
            print('add:', (key, value))
        OrderedDict.__setitem__(self, key, value)





if __name__ == '__main__':
    # 创建一个容量为3的先进先出字典
    fifo_dict = FIFOdict(3)

    # 添加元素
    fifo_dict['a'] = 1
    fifo_dict['b'] = 2
    fifo_dict['c'] = 3
    fifo_dict['d'] = 4
    # 输出字典
    print(fifo_dict)
