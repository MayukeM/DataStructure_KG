"""
数据处理模块
"""
from neo_db.config import CA_LIST, graph
import json
import codecs
import pandas as pd
import csv
import os

getpath = os.path.abspath(os.path.dirname(__file__))  # 获取本层目录
getpath = ('/').join(getpath.split('\\'))


def col_to_dic():
    # 将cate.csv按列类别生成字典

    data = pd.read_csv(getpath + "/cate.csv", encoding='gbk')
    data_dict = {}
    for col in data.columns:
        data_dict[col] = []
        for item in list(data[col]):
            if not isinstance(item, str):
                break
            data_dict[col].append(item)
    print(data_dict)
    # print(data_dict)  # {'一级概念': ['数据结构', 'C语言'], '二级概念': ['逻辑结构', '物理结构', '存储结构'
    return data_dict


def add_cate(data_dict):
    # 添加概念级别,并保存到raw_data/relation.csv
    with open("relation.csv", encoding='gbk') as f:
        with open('../raw_data/relation.csv', "w", newline='') as csv_file:
            writer = csv.writer(csv_file)
            for line in f.readlines():
                rela_array = line.strip("\n").split(",")
                for item in data_dict:
                    if rela_array[0] in data_dict[item]:
                        rela_array.append(item)
                for item in data_dict:
                    if rela_array[1] in data_dict[item]:
                        rela_array.append(item)
                # print(rela_array)
                writer.writerow(rela_array)
    return


def get_json_data():
    # 将raw_data/relation.csv的数据转换成data link的json格式以便前端展示
    with open("../raw_data/relation.csv", encoding='gbk') as f:
        json_data = {'data': [], "links": []}
        d = []
        for line in f.readlines():
            rela_array = line.strip("\n").split(",")
            d.append(rela_array[0] + "_" + rela_array[3])
            d.append(rela_array[1] + "_" + rela_array[4])
            d = list(set(d))
        print(d)
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
    with open("../raw_data/relation.csv", encoding='gbk') as f:
        for line in f.readlines():
            rela_array = line.strip("\n").split(",")
            link_item = {}
            link_item['source'] = name_dict[rela_array[0]]
            link_item['target'] = name_dict[rela_array[1]]
            link_item['value'] = rela_array[2]
            json_data['links'].append(link_item)
    f = codecs.open('../static/data.json', 'w', 'utf-8')
    f.write(json.dumps(json_data, ensure_ascii=False))
    return

# 得到数据量
def get_data_num():
    data1 = graph.run("match (n) return count(*)").data()
    entity = data1[0]['count(*)']
    data2 = graph.run("MATCH (n)-[r]->() RETURN COUNT(r)").data()
    relation = data2[0]['COUNT(r)']
    # getpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # getpath = ('/').join(getpath.split('\\'))
    #
    # with open(getpath + '/raw_data/relation.csv', 'r') as f:
    #     relation = len(f.readlines())
    # with open(getpath + '/KGQA/my_dict.txt', 'r', encoding='utf-8') as f:
    #     entity = len(f.readlines())
    print(relation,entity)
    return relation, entity


if __name__ == '__main__':
    data_dict = col_to_dic()
    add_cate(data_dict)
    get_json_data()
    get_data_num()
