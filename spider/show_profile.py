import codecs
import os
import json

getpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 获取上级目录
getpath = ('/').join(getpath.split('\\'))

with open(getpath + '/spider/json/data.json', encoding='utf-8')as f:
    data = json.load(f)


def get_profile(name):
    s = ''
    for i in data[name]:
        st = "<dt class = \"basicInfo-item name\" >" + str(i) + " \
        <dd class = \"basicInfo-item value\" >" + str(data[name][i]) + "</dd >"
        s += st
    return s
