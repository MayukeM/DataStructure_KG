from neo_db.config import graph, CA_LIST, GraphService
from neo4j import GraphDatabase
from spider.show_profile import get_profile, get_all_profile
import codecs
import os
import json
import base64
import re
from py2neo import Graph
from neo_db.config import CA_LIST
from kg_data.data_processing import col_to_dic
import pandas as pd

# 知识点查询
def query(name):
    data = graph.run(
        "match(p)-[r]->(n:Concept {name:'%s'}) return  p.name,r.relation,n.name,p.cate,n.cate\
            Union all\
        match(p:Concept {name:'%s'}) -[r]->(n) return p.name, r.relation, n.name, p.cate, n.cate" % (name, name)
    )
    data = list(data)
    return get_json_data(data)

# 模糊搜索
def fuzzy_search(array):
    ss = ''
    for name in array:
        if name == "?" or name == "的":
            continue
        name_lst = name[::1]
        sql_str = '.*'.join(name_lst)
        data = graph.run("match (n:Concept) where n.name =~ '.*%s.*' return n.name" % sql_str).data()
        s = ''
        if str(data) != "[]":
            for i in data:
                st = '<button class="btn btn-default" data='+i["n.name"]+'>'+i["n.name"]+'</button>&nbsp;&nbsp;'
                s += st
        ss += s
    return ss
# fuzzy_search("快速排序")

# 多度查询
def query_branch(name, deep):
    if deep == '二度查询':
        graph.run(
            'CALL apoc.export.json.query("match data=(n1{name:\'%s\'})-[r1]->(n2) return n1 {.*}, r1 {.*}, n2 {.*}", '
            '"knows-with-node-properties.json", {writeNodeProperties:true})' % (name))
    elif deep == '三度查询':
        graph.run(
            'CALL apoc.export.json.query("match data=(n1{name:\'%s\'})-[r1]->(n2)-[r2]->(n3) return n1 {.*}, r1 {.*}, n2 {.*}, r2 {.*}, n3 {.*}", '
            '"knows-with-node-properties.json", {writeNodeProperties:true})' % (name))
    elif deep == '四度查询':
        graph.run(
            'CALL apoc.export.json.query("match data=(n1{name:\'%s\'})-[r1]->(n2)-[r2]->(n3)-[r3]->(n4) return n1 {.*}, r1 {.*}, n2 {.*}, r2 {.*}, n3 {.*}, r3 {.*}, n4 {.*}", '
            '"knows-with-node-properties.json", {writeNodeProperties:true})' % (name))
    else:
        graph.run(
            'CALL apoc.export.json.query("match data=(n1{name:\'%s\'})-[r1]->(n2)-[r2]->(n3) return n1 {.*}, r1 {.*}, n2 {.*}, r2 {.*}, n3 {.*}", '
            '"knows-with-node-properties.json", {writeNodeProperties:true})' % (name))
    # print(data)
    json_data = {'data': [], "links": []}  # echarts关系图所需要的数据格式
    d = []
    with open(
            "D:\\Program Files (x86)\\.Neo4jDesktop\\neo4jDatabases\\database-3c0c8037-2a1b-4d51-baf0-9de130846239\\installation-3.5.12\\import\\knows-with-node-properties.json",
            encoding='utf-8') as f:
        for item in f:
            item = json.loads(item)
            for i in ['n1', 'n2', 'n3', 'n4', 'n5']:
                if i in item:
                    d.append(item[i]['name'] + "_" + item[i]['cate'])
            d = list(set(d))
        name_dict = {}
        count = 0
        for j in d:
            j_array = j.split("_")
            data_item = {}
            name_dict[j_array[0]] = count
            count += 1
            data_item['name'] = j_array[0]
            data_item['category'] = CA_LIST[j_array[1]]
            json_data['data'].append(data_item)
        # print(name_dict)
    with open(
            "D:\\Program Files (x86)\\.Neo4jDesktop\\neo4jDatabases\\database-3c0c8037-2a1b-4d51-baf0-9de130846239\\installation-3.5.12\\import\\knows-with-node-properties.json",
            encoding='utf-8') as f:
        for item in f:
            item = json.loads(item)
            for i, key in enumerate(['r1', 'r2', 'r3', 'r4']):
                if key in item:
                    link_item = {}
                    link_item['source'] = name_dict[item["n" + str(i + 1)]['name']]
                    link_item['target'] = name_dict[item["n" + str(i + 2)]['name']]
                    link_item['value'] = item[key]['relation']
                    json_data['links'].append(link_item)
        # print(json_data)
    return json_data


getpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 获取上级目录
getpath = ('/').join(getpath.split('\\'))
# print(getpath)  # D:/学习/毕设-知识图谱/12.我的项目/DataStructureKG_UIupdate/DataStructure_KG


def all():
    data = graph.run("match (p)-[r]->(n) return p.name, r.relation, n.name, p.cate, n.cate")
    data = list(data)

    d = []
    for i in data:
        d.append(i['p.name'] + "_" + i['p.cate'])
        d.append(i['n.name'] + "_" + i['n.cate'])
        d = list(set(d))
    name_dict = {}
    count = 0
    for j in d:
        j_array = j.split("_")
        name_dict[j_array[0]] = count
        count += 1
    name_dict_f = open(getpath + '/neo_db/name_dict.txt', 'w+')
    name_dict_f.write(str(name_dict))
    name_dict_f.close()

    json_data = get_json_data(data)
    return json_data, name_dict


# query_branch("串")

# 路径查询
def query_path(a, b):
    data = graph.run("MATCH p =shortestPath((n { name: '%s' })-[*..15]-(m {name:'%s'})) RETURN p" % (a, b))
    data = data.data()
    # print(data)
    data = data[0]['p']
    data = str(data)
    # print(data)
    pattern11 = re.compile("\[:([\u4e00-\u9fa5]*) {}\]->\(([\u4e00-\u9fa5]*)\)")  # [:属于 {}]->(线性结构)
    pattern22 = re.compile("\(([\u4e00-\u9fa5]*)\)<-\[:([\u4e00-\u9fa5]*) {}\]")  # (线性结构)<-[:分类 {}]
    pattern3 = re.compile(":([\u4e00-\u9fa5]*)")  # :属于
    pattern4 = re.compile("\(([\u4e00-\u9fa5]*)\)")  # (串)

    right = pattern11.findall(data)  # [('属于', '线性结构'), ('研究对象', '存储结构'), ('包括', '索引存储')]
    left = pattern22.findall(data)  # [('线性结构', '分类')]
    # relation = pattern3.findall(data)  # ['属于', '分类', '研究对象', '包括']
    concept = pattern4.findall(data)  # ['串', '线性结构', '数据结构', '存储结构', '索引存储']
    arr_list = []
    for item in right:
        a = ""
        for j in range(len(concept)):
            if concept[j] == item[1]:
                a += concept[j - 1] + "," + item[1] + "," + item[0]
        arr_list.append(a)
    for item in left:
        a = ""
        for j in range(len(concept)):
            if concept[j] == item[0]:
                a += concept[j + 1] + "," + item[0] + "," + item[1]
        arr_list.append(a)
    print(f"list:{arr_list}")  # list:['串,线性结构,属于', '数据结构,存储结构,研究对象', '存储结构,索引存储,包括', '数据结构,线性结构,分类']
    data_dict = col_to_dic()

    json_data = {'data': [], "links": []}
    d = []
    for line in arr_list:
        rela_array = line.split(",")
        for item in data_dict:
            if rela_array[0] in data_dict[item]:
                rela_array.append(item)
            if rela_array[1] in data_dict[item]:
                rela_array.append(item)
        d.append(rela_array[0] + "_" + rela_array[3])
        d.append(rela_array[1] + "_" + rela_array[4])
        d = list(set(d))
    name_dict = {}
    count = 0
    for j in d:
        j_array = j.split("_")
        data_item = {}
        name_dict[j_array[0]] = count
        count += 1
        data_item['name'] = j_array[0]
        data_item['category'] = CA_LIST[j_array[1]]
        json_data['data'].append(data_item)
    for line in arr_list:
        rela_array = line.split(",")
        link_item = {}
        link_item['source'] = name_dict[rela_array[0]]
        link_item['target'] = name_dict[rela_array[1]]
        link_item['value'] = rela_array[2]
        json_data['links'].append(link_item)

    return json_data


# 转换成echarts关系图所需要的数据格式
def get_json_data(data):
    json_data = {'data': [], "links": []}  # echarts关系图所需要的数据格式
    d = []
    for i in data:
        d.append(i['p.name'] + "_" + i['p.cate'])
        d.append(i['n.name'] + "_" + i['n.cate'])
        d = list(set(d))
    name_dict = {}
    count = 0
    for j in d:
        j_array = j.split("_")
        data_item = {}
        name_dict[j_array[0]] = count
        count += 1
        data_item['name'] = j_array[0]
        data_item['category'] = CA_LIST[j_array[1]]
        json_data['data'].append(data_item)
    for i in data:
        link_item = {}
        link_item['source'] = name_dict[i['p.name']]
        link_item['target'] = name_dict[i['n.name']]
        link_item['value'] = i['r.relation']
        json_data['links'].append(link_item)
    # print(f"namedict:{name_dict}")
    return json_data


# f = codecs.open('./static/test_data.json','w','utf-8')
# f.write(json.dumps(json_data,  ensure_ascii=False))


def get_KGQA_answer(array):
    data_array = []
    for i in range(len(array) - 1):
        if i == 0:
            name = array[0]
        else:
            name = data_array[-1]['n.name']  # n

        data = graph.run(
            # "match(p)-[r:%s{relation: '%s'}]->(n:Person{Name:'%s'}) return  p.Name,n.Name,r.relation,p.cate,n.cate" % (
            #     similar_words[array[i+1]], similar_words[array[i+1]], name)
            "match(p:Concept {name:'%s'})-[r:%s{relation: '%s'}]->(n) return  p.name,n.name,r.relation,p.cate,n.cate" % (
                name, array[i + 1], array[i + 1])
        )  # n, p

        data = list(data)
        # print(data)
        data_array.extend(data)
        # print(data_array)
    # b = ''
    # if len(array) >= 1:
    #     last_name = str(data_array[-1]['n.name'])

    # image_path = getpath + "/spider/images/%s.jpg" % (str(data_array[-1]['n.name']))
    # if not os.path.exists(image_path):
    #     image_path = getpath + "/spider/images/数据结构.jpg"
    #     with open(image_path, "rb") as image:  # n
    #         base64_data = base64.b64encode(image.read())
    #         b = str(base64_data)

    # else:
    #     last_name = '数据结构'
    #     image_path = getpath + "/spider/images/数据结构.jpg"
    #     with open(image_path, "rb") as image:  # n
    #         base64_data = base64.b64encode(image.read())
    #         b = str(base64_data)

    # with open(getpath + "/spider/images/%s.jpg" % (str(data_array[-1]['n.name'])), "rb") as image:  # n
    #     base64_data = base64.b64encode(image.read())
    #     b = str(base64_data)

    # return [get_json_data(data_array), get_profile(str(data_array[-1]['n.name'])), b.split("'")[1]]  # n
    return [get_json_data(data_array)]  # n
# get_KGQA_answer(['数据结构'])

def get_answer_profile(name):
    # 判断图片是否存在
    image_path = getpath + "/spider/images/%s.jpg" % (str(name))
    if not os.path.exists(image_path):
        image_path = getpath + "/spider/images/数据结构.jpg"

    with open(image_path, "rb") as image:
        base64_data = base64.b64encode(image.read())
        b = str(base64_data)
    return [get_profile(str(name)), b.split("'")[1]]


def get_answer_all_profile(name):
    # 判断图片是否存在
    image_path = getpath + "/spider/images/%s.jpg" % (str(name))
    if not os.path.exists(image_path):
        image_path = getpath + "/spider/images/数据结构.jpg"

    with open(image_path, "rb") as image:
        base64_data = base64.b64encode(image.read())
        b = str(base64_data)
    return [get_all_profile(str(name)), b.split("'")[1]]

# if __name__ == '__main__':
#     data = all()
#     print(data)
