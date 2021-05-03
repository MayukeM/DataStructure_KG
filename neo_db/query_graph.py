from neo_db.config import graph, CA_LIST
from spider.show_profile import get_profile
import codecs
import os
import json
import base64


def query(name):
    data = graph.run(
        "match(p)-[r]->(n:Concept {name:'%s'}) return  p.name,r.relation,n.name,p.cate,n.cate\
            Union all\
        match(p:Concept {name:'%s'}) -[r]->(n) return p.name, r.relation, n.name, p.cate, n.cate" % (name, name)
    )
    data = list(data)
    return get_json_data(data)


def get_json_data(data):
    json_data = {'data': [], "links": []}
    d = []
    for i in data:
        # print(i["p.Name"], i["r.relation"], i["n.Name"], i["p.cate"], i["n.cate"])
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

    return json_data


# f = codecs.open('./static/test_data.json','w','utf-8')
# f.write(json.dumps(json_data,  ensure_ascii=False))
getpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 获取上级目录
getpath = ('/').join(getpath.split('\\'))
print(getpath)


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
        print(data)
        data_array.extend(data)

        print("===" * 36)

    with open(getpath + "/spider/images/%s.jpg" % (
            str(data_array[-1]['n.name'])), "rb") as image:  # n
        base64_data = base64.b64encode(image.read())
        b = str(base64_data)

    return [get_json_data(data_array), get_profile(str(data_array[-1]['n.name'])), b.split("'")[1]]  # n


def get_answer_profile(name):
    with open(getpath + "/spider/images/%s.jpg" % (str(name)),
              "rb") as image:
        base64_data = base64.b64encode(image.read())
        b = str(base64_data)
    return [get_profile(str(name)), b.split("'")[1]]
