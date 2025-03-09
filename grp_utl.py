from collections import defaultdict

import py2neo
import pyvis
from networkx import NetworkXError
from py2neo import Graph, Node, Relationship, NodeMatcher
import networkx as ntx
from pyvis.edge import Edge
from pyvis.network import Network
import matplotlib.pyplot as plt

NEO4J_PATH = 'D:\\code\\neo4j-community-4.4.25\\bin\\neo4j'
NEO4J_IP = '127.0.0.1'
NEO4J_POST ='7474'
NEO4J_USER = 'neo4j'
NEO4J_PASSWORD = '123456'
import uuid




# uuid生成器
class GenUid:
    def __init__(self,id2uid_map=None,uid2id_map=None,if_uniq=False,pk=None):
        self.if_uniq = if_uniq
        self.pk = pk
        if id2uid_map:
            self.id2uid_map=id2uid_map
            self.uid2id_map=uid2id_map
        else:
            self.id2uid_map={}
            self.uid2id_map={}

    def is_in(self,uid):
        if uid in  self.uid2id_map:
            return True
        else:
            return False

    def is_in_pk(self,uid):
        if self.pk:
            ret = self.pk.is_in(uid)
            return ret
        return False

    # 更新uid2id和id2uid
    def add_uid(self,uid,id):
        self.uid2id_map[uid]=id
        if self.if_uniq:
            tmp = self.id2uid_map.get(id)
            if tmp:
                if id !=tmp:
                    raise ValueError('id唯一生成器，一个id对应了多个uid')
            else:
                self.id2uid_map[id]=uid
        else:
            tmp = self.id2uid_map.get(id,[])
            if uid not in tmp:
                tmp.append(uid)
                self.id2uid_map[id]=tmp
        if self.pk:
            self.pk.add_uid(uid,id)

    #　输出全局uid 和id 对应关系
    def uid2id(self,uid,default_dict=None):
        if default_dict:
            ret = default_dict.get(uid)
            if ret:
                return ret
        if self.pk:
            id = self.pk.uid2id(uid)
            return id
        else:
            id = self.uid2id_map.get(uid)
            return id
    # 删除uid
    def delete_uid(self,uid):
        id = self.uid2id_map.pop(uid)
        tmp = self.id2uid_map.get(id)
        tmp.pop(uid)
        if self.pk:
            self.pk.delete_uid(uid)
        return id

    # 获取自己的id对应的uid列表
    def get_uids_byid(self,id):
        return self.id2uid_map.get(id)

    # 获取全部的id 对应的uid列表
    def get_all_uids_byid(self,id):
        if self.pk:
            return self.pk.get_uids_byid(id)
        else:
            return self.get_uids_byid(id)
    def id2uid(self,id,default_dict=None):
        if default_dict:
            ret = default_dict.get(id)
            if ret:
                return ret
        if self.if_uniq:
            uni_id = self.id2uid_map.get(id)
        else:
            uni_id = None
        # uid不重复（包括没出现在父节点）

        if uni_id is None:
            uni_id = uuid.uuid4().__str__()
            while self.is_in(uni_id) or self.is_in_pk(uni_id):
                uni_id = uuid.uuid4().__str__()
            self.add_uid(uid=uni_id,id=id)
            return uni_id
        else:
            return uni_id

    # 生成一个唯一uid生成器 ，id->uid 一对一
    def gen_uni_uid_genner(self):
        return GenUid(pk=self,if_uniq=True)

    # 生成一个不唯一Uid生成器 id -> uid 一对多
    def gen_in_uni_uid_genner(self):
        return GenUid(pk=self,if_uniq=False)





GENNER_UID = GenUid()

VIS_SHAPE_CONF={
    '主体': {'shape':'circle','size':30,'color':'rgba(255, 0, 0, 0.5)'}
    ,'业务过程':{'shape':'ellipse','size':30,'color':'rgba(0, 255, 0, 0.5)'}
    ,'属性':{'shape':'box','size':30}
    ,'表':{'shape':'box','size':30,'color':'rgba(0, 0, 255, 0.5)'}
    ,'字段':{'shape':'box','size':30,'color':'rgba(0, 255, 255, 0.5)'}
    ,'域':{'shape':'circle','size':30,'color':'rgba(255, 0, 0, 0.9)'}
}
VIS_HIDE_LABELS =['字段']
# 默认值
VIS_DEFAULT_CONF={'shape':'box','size':30}
class EX_NetWork(Network):
    def __init__(self):
        super().__init__()
        self.directed = True
        self.edge_ids =[]

    # 重写add_edge 方法，增加必传参数id
    def add_edge(self, source, to, **options):
        edge_exists = False
        # verify nodes exists
        assert source in self.get_nodes(), \
            "non existent node '" + str(source) + "'"
        assert to in self.get_nodes(), \
            "non existent node '" + str(to) + "'"
        # we only check existing edge for undirected graphs
        if not self.directed:
            for e in self.edges:
                frm = e['from']
                dest = e['to']
                if (
                        (source == dest and to == frm) or
                        (source == frm and to == dest)
                ):
                    # edge already exists
                    edge_exists = True
        if not edge_exists:
            id = options.get('id')
            e = Edge(source, to, self.directed, **options)
            self.edges.append(e.options)
            # print(f"**options:{options}")
            self.edge_ids.append(id)
    def get_node_by_id(self,id):
        index = self.node_ids.index(id)
        node = self.nodes[index]
        return node

    def get_relation_by_id(self,id):
        index = self.edge_ids.index(id)
        relation = self.edges[index]
        return relation

    def delete_node_by_id(self,id):
        index = self.node_ids.index(id)
        if index:
            self.node_ids.pop(index)
            print(index)
            node = self.nodes.pop(index)
            return  node
    def delete_relation_by_id(self,id):
        index = self.edge_ids.index(id)
        if index:
            self.edge_ids.pop(index)
            relation = self.edges.pop(index)
            return  relation

    def add_node_by_dict(self,data,x=None,y=None):
        data = dict(data)
        lable = data.get('labels')
        # 默认隐藏节点设置
        shape = VIS_SHAPE_CONF.get(lable,VIS_DEFAULT_CONF).get('shape')
        size = VIS_SHAPE_CONF.get(lable,VIS_DEFAULT_CONF).get('size')
        color = VIS_SHAPE_CONF.get(lable,VIS_DEFAULT_CONF).get('color')
        hidden = False
        if lable in VIS_HIDE_LABELS:
            hidden = True
        self.add_node(data.get('id')
                      , label=data.get('name')
                      , shape=shape
                      , size=size
                      , x=x, y=y
                      , pro=data
                      , color=color
                      # ,hidden = hidden
                      )
        ret = self.get_node_by_id(data.get('id'))
        return ret

    def add_relation_by_dict(self,data):
        data = dict(data)

        self.add_edge(data.get('start')
                    , data.get('end')
                    , id=data.get('id')
                    , label=data.get('type')
                    , pro=data)
        return self.edges[-1]
    def update_node_by_id(self,id,data):
        pass

class vis_Node:
    pass

class Ntx_Graph(ntx.Graph):
    def add_nodes_from_NtxNode(self, nodes_for_adding, **attr):
        for n in nodes_for_adding:
            try:
                newnode = n not in self._node
                newdict = nodes_for_adding[n]
            except TypeError:
                n, ndict = n
                newnode = n not in self._node
                newdict = attr.copy()
                newdict.update(ndict)
            if newnode:
                if n is None:
                    raise ValueError("None cannot be a node")
                self._adj[n] = self.adjlist_inner_dict_factory()
                self._node[n] = self.node_attr_dict_factory()
            self._node[n].update(newdict)
    def add_edgs_from_NtxNode(self, ebunch_to_add, **attr):
        for e in ebunch_to_add:
            ne = len(e)
            if ne == 3:
                u, v, dd = e
            elif ne == 2:
                u, v = e
                dd = {}  # doesn't need edge_attr_dict_factory
            else:
                raise NetworkXError(f"Edge tuple {e} must be a 2-tuple or 3-tuple.")
            if u not in self._node:
                if u is None:
                    raise ValueError("None cannot be a node")
                self._adj[u] = self.adjlist_inner_dict_factory()
                self._node[u] = self.node_attr_dict_factory()
            if v not in self._node:
                if v is None:
                    raise ValueError("None cannot be a node")
                self._adj[v] = self.adjlist_inner_dict_factory()
                self._node[v] = self.node_attr_dict_factory()
            datadict = self._adj[u].get(v, self.edge_attr_dict_factory())
            newattr = ebunch_to_add[e]
            datadict.update(attr)
            datadict.update(newattr)
            datadict.update(dd)
            self._adj[u][v] = datadict
            self._adj[v][u] = datadict


class Vis_Graph(pyvis.network.Network):
    def add_nodes_from_VisDatas(self, nodes, **kwargs):
        for node in nodes:
            node_datas = dict(node)
            # node_datas.update(kwargs)
            id = node_datas.pop('id')
            self.add_node(id, **node_datas)

    def add_edgs_from_VisDatas(self,edges):
        for edge in edges:
            edg_data = dict(edge)
            pro = edg_data.get('pro')
            start = edg_data.pop('from')
            end = edg_data.pop('to')
            id = None
            if '_id' in pro:
                id = pro.get('_id')
            self.add_edge(start,end,id=id,pro=pro)



# ntx data 传入neo4j 查到的data,转化为network可以接受的data
class Ntx_Datas(ntx.Graph):
    def __init__(self,if_uniq=False):
        super().__init__()

        if if_uniq:
            self.G_uid = GENNER_UID.gen_uni_uid_genner()
        else:
            self.G_uid =GENNER_UID.gen_in_uni_uid_genner()

        self.nodes_dict = {}
        self.relations_dict= {}

    def add_neo4j_datas(self,neo4j_datas):
        nodes =[]
        relations =[]
        for items in neo4j_datas:
            for item in items:
                if isinstance(item,py2neo.Node):
                    nodes.append(item)
                if isinstance(item,py2neo.Relationship):
                    relations.append(item)

        self.add_neo4j2ntx_nodes(nodes)
        self.add_neo4j2ntx_relations(relations)
        return nodes,relations

    def add_neo4j2ntx_nodes(self,nodes):
        ret = []
        for node in nodes:
            tmp = self.add_neo4j2ntx_node(node)
            ret.append(tmp)
        return ret

    def add_neo4j2ntx_node(self,node:Node):
        id = node.identity
        uid = self.G_uid.id2uid(id)
        labels = str(node.labels).replace(':', '')
        pro = {
            'id':id
            ,'_id':uid
            ,'labels':labels
        }
        pro.update(dict(node.items()))
        self.add_node(uid,pro=pro)
        self.nodes_dict[uid]=pro
        return self.nodes.get(uid)

    def add_neo4j2ntx_relations(self, relations):
        ret = []
        for relation in relations:
            tmp = self.add_neo4j2ntx_relation(relation)
            ret.append(tmp)
        return ret
    def add_neo4j2ntx_relation(self,relation:Relationship):
        pro = dict(relation.items())
        id =relation.identity
        start = relation.start_node.identity
        start_id = self.G_uid.id2uid(start)
        end = relation.end_node.identity
        end_id = self.G_uid.id2uid(end)
        type = ''.join(relation.types())
        _id = f'{start_id}~{end_id}'
        pro['_id'] = _id
        pro['id'] = id
        pro['start'] = start
        pro['end'] = end
        pro['_start'] = start_id
        pro['_end'] = end_id
        pro['type']=type
        self.add_edge(start_id,end_id,id=_id,attr=pro)

# 将ntx data 转化为pyvis可以接受的data
class Vis_Datas(pyvis.network.Network):
    def __init__(self):
        super().__init__()
    def add_ntx_datas(self,ntx_datas:Ntx_Datas):
        nodes = []
        edgs = []
        for node in ntx_datas.nodes:
            nodes.append(ntx_datas.nodes[node])
        for edg in ntx_datas.edges:
            edgs.append(ntx_datas.edges[edg])
        self.add_ntx2vis_nodes(nodes)
        self.add_ntx2vis_edgs(edgs)

    def add_ntx2vis_nodes(self,nodes):
        for node in nodes:
            self.add_ntx2vis_node(node)
        return self.nodes
    def add_ntx2vis_node(self,node:dict):
        node_data = dict(node)
        pro = node_data.get('pro')
        pos = node_data.get('pos')
        id = pro.get('_id')
        lable = pro.get('labels')
        if pos is None:
            x = None
            y = None
        else:
            x = pos[0]
            y = pos[1]
        # # 默认隐藏节点设置
        shape = VIS_SHAPE_CONF.get(lable, VIS_DEFAULT_CONF).get('shape')
        size = VIS_SHAPE_CONF.get(lable, VIS_DEFAULT_CONF).get('size')
        color = VIS_SHAPE_CONF.get(lable, VIS_DEFAULT_CONF).get('color')
        name = pro.get('name')
        self.add_node(id
                      , label=name
                      , shape=shape
                      , size=size
                      , x=x, y=y
                      , pro=pro
                      , color=color
                      )
    def add_ntx2vis_edgs(self,edgs):
        for edg in edgs:
            self.add_ntx2vis_edg(edg)
        return self.edges
    def add_ntx2vis_edg(self,edg:dict):
        edg_data = dict(edg.get('attr'))
        id = edg_data.get('id')
        start = edg_data.get('_start')
        end = edg_data.get('_end')
        label = edg_data.get('type')
        self.add_edge(start,end,id=id,label=label,pro=edg_data)


class GRP_UTL:
    def __init__(self,neo4j_url,NEO4J_USER,NEO4J_PASSWORD):

        if neo4j_url:
            neo4j_url = neo4j_url
        if NEO4J_USER:
            NEO4J_USER=NEO4J_USER
        if NEO4J_PASSWORD:
            NEO4J_PASSWORD = NEO4J_PASSWORD
        self.neo_Grp = Graph(neo4j_url, auth=(NEO4J_USER, NEO4J_PASSWORD))
        self.ntx_Grp= Ntx_Graph()
        self.vis_Grp = Vis_Graph()
        self.pos =None


    def NeoGet_Nodes(self)->list:
        # Node 返回Node类型的list
        str = ' MATCH (n) RETURN n LIMIT 20;'
        ret = self.neo_Grp.run(str)
        ret_list = []
        for item in ret.data():
            ret_list.append(item['n'])
        return ret_list

    def Neo4jGet_All(self):
        str = ' MATCH (n)-[r]-(m) WHERE id(n)=20 RETURN n,r,m LIMIT 20;'
        ret = self.neo_Grp.run(str)
        my_g = Ntx_Datas(if_uniq=True)
        my_g.add_neo4j_datas(ret)
        return my_g

    def NtxAdd_GRP(self,ntx_data:Ntx_Datas):
        # ntx添加节点
        self.ntx_Grp.add_nodes_from_NtxNode(ntx_data.nodes)
        self.ntx_Grp.add_edgs_from_NtxNode(ntx_data.edges)
        self.init_node_pos()
        return self.ntx_Grp

    def init_node_pos(self):
        fixed_key = None
        if self.pos:
            fixed_key = self.pos.keys()
        self.pos = ntx.spring_layout(self.ntx_Grp, pos=self.pos, fixed=fixed_key,scale=100)
        for key,vaule in self.pos.items():
            self.ntx_Grp.nodes.get(key)['pos']=vaule

    def VisAdd_GRP(self,ntx_datas):
        u = Vis_Datas()
        u.add_ntx_datas(ntx_datas)
        self.vis_Grp.add_nodes_from_VisDatas(u.nodes)
        self.vis_Grp.add_edgs_from_VisDatas(u.edges)
        return self.vis_Grp

    def Ntxid2Neoid(self,id):
        if '~' in id:
            data = self.ntx_Grp.edges.get(id)
            if data:
                attr_dict = data.get('attr')
                id = attr_dict.get('id')
                return id
            else:
                raise ValueError('错误的uuid')
        else:
            data = self.ntx_Grp.nodes.get(id)
            if data:
                attr_dict = data.get('pro')
                id = attr_dict.get('id')
                return id
            else:
                raise ValueError('错误的uuid')

    def getNtx_Date_by_uuid(self,id):
        return self.ntx_Grp.nodes.get(id).get('pro')

    def test(self):
        my_g = self.Neo4jGet_All()
        self.NtxAdd_GRP(my_g)
        self.VisAdd_GRP(self.ntx_Grp)

        # self.ntx_Grp.nodes.get()



        # f = self.ntx_Grp.edges.get(start,end)
        #
        #     .get_edge_data(start,end)
        # print(start)

        # for i in self.ntx_Grp.edges:
        #     print(i)

        node_dict = dict(self.ntx_Grp.nodes)
        for i in self.ntx_Grp.nodes:
            print(self.ntx_Grp.nodes.get(i))








if __name__ == '__main__':


    neo4j_url = f"http://{NEO4J_IP}:{NEO4J_POST}"
    grp_utl = GRP_UTL(neo4j_url=neo4j_url,NEO4J_USER=NEO4J_USER,NEO4J_PASSWORD=NEO4J_PASSWORD)
    grp_utl.test()


