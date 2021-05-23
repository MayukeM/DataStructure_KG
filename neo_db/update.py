import json
import os
from neo_db.config import CA_LIST
import os
getpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) # 获取本层目录
getpath = ('/').join(getpath.split('\\'))
path = getpath+"/static/data.json"
def update_node(node, cate):
    print(node, cate)
    with open(path, "r", encoding='utf-8') as json_f:
        json_dict = json.load(json_f)
        for item in json_dict['data']:
            if item['name'] == node:
                item['category'] = CA_LIST[cate]
    with open(path, "w", encoding='utf-8') as dump_f:
        json.dump(json_dict, dump_f, ensure_ascii=False)
    with open(path, "r", encoding='utf-8') as json_f:
        json_data = json.load(json_f)
    return json_data


# update_node("数据结构", "一级概念")
