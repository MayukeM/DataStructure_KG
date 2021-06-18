# -*- coding: utf-8 -*-
import pyltp
import os
import base64
import json
from py2neo import Graph


def words_mark(array):
    # 词性标注模型路径，模型名称为`pos.model`
    print(os.path)
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
    print(pos_model_path)
    postagger = pyltp.Postagger()  # 初始化实例
    postagger.load(pos_model_path)  # 加载模型
    postags = postagger.postag(array)  # 词性标注
    pos_str = ' '.join(postags)
    pos_array = pos_str.split(" ")
    postagger.release()  # 释放模型
    return pos_array


LTP_DATA_DIR = 'D:/app/ltp_data_v3.4.0'  # ltp模型目录的路径


def cut_words(words):
    user_dict = 'ds_dict.txt'
    segmentor = pyltp.Segmentor()  # 初始化实例
    seg_model_path = os.path.join(LTP_DATA_DIR, user_dict)
    segmentor.load(seg_model_path)  # 加载模型
    words = segmentor.segment(words)
    print(words)
    array_str = "|".join(words)
    print(array_str)
    array = array_str.split("|")
    segmentor.release()
    return array


array = cut_words("数据结构包括什么？")
print(array)


def get_target_array(words):
    target_pos = ['n', 'n']
    target_array = []
    seg_array = cut_words(words)
    pos_array = words_mark(seg_array)
    for i in range(len(pos_array)):
        if pos_array[i] in target_pos:
            target_array.append(seg_array[i])
    # target_array.append(seg_array[i])
    return target_array


graph = Graph(
    "http://localhost:11005",
    username="neo4j",
    password="123456"
)

similar_words = {
    "爸爸": "父亲",
    "妈妈": "母亲",
    "爸": "父亲",
    "妈": "母亲",
    "父亲": "父亲",
    "母亲": "母亲",
    "儿子": "儿子",
    "女儿": "女儿",
    "丫环": "丫环",
    "兄弟": "兄弟",
    "妻": "妻",
    "老婆": "妻",
    "哥哥": "哥哥",
    "表妹": "表兄妹",
    "弟弟": "弟弟",
    "妾": "妾",
    "养父": "养父",
    "姐姐": "姐姐",
    "娘": "母亲",
    "爹": "父亲",
    "father": "父亲",
    "mother": "母亲",
    "朋友": "朋友",
    "爷爷": "爷爷",
    "奶奶": "奶奶",
    "孙子": "孙子",
    "老公": "丈夫",
    '岳母': '岳母',
    "表兄妹": "表兄妹",
    "孙女": "孙女",
    "嫂子": "嫂子",
    "暧昧": "暧昧"

}

CA_LIST = {"贾家荣国府": 0, "贾家宁国府": 1, "王家": 2, "史家": 3, "薛家": 4, "其他": 5, "林家": 6}


def get_json_data(data):
    json_data = {'data': [], "links": []}
    d = []

    for i in data:
        # print(i["p.Name"], i["r.relation"], i["n.Name"], i["p.cate"], i["n.cate"])
        d.append(i['p.Name'] + "_" + i['p.cate'])
        d.append(i['n.Name'] + "_" + i['n.cate'])
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

        link_item['source'] = name_dict[i['p.Name']]

        link_item['target'] = name_dict[i['n.Name']]
        link_item['value'] = i['r.relation']
        json_data['links'].append(link_item)

    return json_data


def get_profile(name):
    with open('D:\学习\毕设-知识图谱/08.开源项目\HongLouMeng\KGQA_HLM\spider\json/data.json', encoding='utf-8')  as f:
        data = json.load(f)
    s = ''
    for i in data[name]:
        st = "<dt class = \"basicInfo-item name\" >" + str(i) + " \
        <dd class = \"basicInfo-item value\" >" + str(data[name][i]) + "</dd >"
        s += st
    return s


def get_KGQA_answer(array):
    data_array = []
    for i in range(len(array) - 1):
        if i == 0:
            name = array[0]
        else:
            name = data_array[-1]['p.Name']

        data = graph.run(
            "match(n:Person{Name:'%s'})-[r:%s{relation: '%s'}]->(p) return  p.Name,n.Name,r.relation,p.cate,n.cate" % (
                name, similar_words[array[i + 1]], similar_words[array[i + 1]])
        )

        data = list(data)
        print(data)
        data_array.extend(data)

        print("===" * 36)
    with open("D:\学习\毕设-知识图谱/08.开源项目\HongLouMeng\KGQA_HLM/spider/images/" + "%s.jpg" % (str(data_array[-1]['p.Name'])),
              "rb") as image:
        base64_data = base64.b64encode(image.read())
        b = str(base64_data)

    return [get_json_data(data_array), get_profile(str(data_array[-1]['p.Name'])), b.split("'")[1]]


# array = get_target_array("图的术语有什么？")
# json_data = get_KGQA_answer(array)
# jsonify(json_data)
