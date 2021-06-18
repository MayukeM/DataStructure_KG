import json
import os
from neo_db.config import CA_LIST, graph
import os

getpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 获取本层目录
getpath = ('/').join(getpath.split('\\'))
path = getpath + "/static/data.json"


def update_node(node, cate):
    print(node, cate)
    graph.run("MATCH (n) WHERE n.name = '%s' SET n.cate = '%s'" % (node, cate))
    return
    # with open(path, "r", encoding='utf-8') as json_f:
    #     json_dict = json.load(json_f)
    #     for item in json_dict['data']:
    #         if item['name'] == node:
    #             item['category'] = CA_LIST[cate]
    # with open(path, "w", encoding='utf-8') as dump_f:
    #     json.dump(json_dict, dump_f, ensure_ascii=False)
    # with open(path, "r", encoding='utf-8') as json_f:
    #     json_data = json.load(json_f)
    # return json_data


# update_node("数据结构", "一级概念")

def add_node(e1, e2, rel, c1, c2):
    message = "添加成功"
    a = [e1, e2, rel, c1, c2]
    num1 = graph.run("MATCH (m:Concept {name:'%s' })return count(m)" % e1).data()[0]['count(m)']
    num2 = graph.run("MATCH (m:Concept {name:'%s' })return count(m)" % e2).data()[0]['count(m)']
    if num1 == 0 and num2 == 0 :
        graph.run("CREATE(n:Concept {name:'%s', cate:'%s'})-[r:%s{relation: '%s'}]->(m:Concept {name:'%s', cate:'%s'})" % (e1, c1, rel, rel, e2, c2))
    if num1 != 0 and num2 == 0:
        graph.run("MATCH(m: Concept {name: '%s', cate:'%s'}) CREATE(m) - [r:%s{relation: '%s'}]->(n:Concept {name:'%s', cate:'%s'})"  % (e1, c1, rel,rel, e2, c2))
    if num1 == 0 and num2 != 0:
        graph.run("MATCH(m: Concept {name: '%s', cate:'%s'}) CREATE(n:Concept {name:'%s', cate:'%s'})-[r:%s{relation: '%s'}]->(m)"  % (e2, c2, e1, c1, rel, rel))
    # num = data
    if num1 != 0 and num2 != 0:
        graph.run("MATCH(m: Concept {name: '%s'}),(n:Concept {name:'%s'}) CREATE (m)-[r:%s{relation: '%s'}]->(n)"  % (e2, e1, rel, rel))
        # message = "此条关系已存在！"
    print(num1, num2, message)

    # MATCH(m: Concept {name: 'C语言'}) CREATE(m) - [: 包括]->(n:Concept {name:'函数'}) return m
    # graph.run("CREATE(n:Concept {name:'%s', cate:'%s'}) return n") %(e1,e2)
    print(a)
    return message

def delete_node(name):
    graph.run("match (n {name:'%s'} ) detach delete n" % name)
    return

# add_node('Java', 'C语言', '相关', '一级概念', '一级概念')
