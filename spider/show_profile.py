import codecs
import os
import json
from neo_db.config import graph
getpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 获取上级目录
getpath = ('/').join(getpath.split('\\'))


def get_profile(name):
    with open(getpath + '/spider/json/data.json', encoding='utf-8')as f:
        data = json.load(f)
    s = ''
    for i in data[name]:
        st = "<dt class = \"basicInfo-item name\" >" + str(i) + " \
            <dd class = \"basicInfo-item value\" >" + str(data[name][i]) + "</dd >"
        s += st
    # 添加b站学习链接
    b_link = "https://search.bilibili.com/all?keyword=数据结构" + name
    st1 = "<dt class = \"basicInfo-item name\" >学习链接：<dd class = \"basicInfo-item value\" > <a href = ' "+ b_link + " '>"+name+"学习视频</a> </dd>"
    s += st1
    # 添加动态可视化链接
    v_link = ""
    v_link_dict = {
        "排序":"https://visualgo.net/zh/sorting"
        ,"链表":"https://visualgo.net/zh/list"
        ,"散列":"https://visualgo.net/zh/hashtable"
        ,"哈希":"https://visualgo.net/zh/hashtable"
        ,"图":"https://visualgo.net/zh/graphds"
        ,"最小生成树":"https://visualgo.net/zh/mst"
        ,"栈":"https://visualgo.net/zh/list"
        ,"队列":"https://visualgo.net/zh/list"
        # ,"拓扑排序":"https://www.cs.usfca.edu/~galles/visualization/TopoSortDFS.html"
        # ,"Prim":"https://www.cs.usfca.edu/~galles/visualization/Prim.html"
        # ,"Floyd":"https://www.cs.usfca.edu/~galles/visualization/Floyd.html"
        # ,"Dijkstra":"https://www.cs.usfca.edu/~galles/visualization/Dijkstra.html"
    }

    for key in v_link_dict.keys():
        if key in name:
            v_link = v_link_dict[key]
    if v_link != "":
        st2 = "<dt class = \"basicInfo-item name\" >可视化：<dd class = \"basicInfo-item value\" > <a href = ' "+ v_link + " '>"+name+"动态可视化</a> </dd>"
        s += st2
    return s

def get_all_profile(name):
    s = ''
    data = graph.run("MATCH (n) WHERE n.name = '%s' RETURN properties(n) as props" % name).data()
    # print(data)
    for i in data[0]['props']:
        # st = "<dt class = \"basicInfo-item name\" >" + str(i) + " \
        #         <dd class = \"basicInfo-item value\" >" + str(data[0]['props'][i]) + "</dd >"
        st = "<dt class = \"basicInfo-item name\" >" + str(i) + " \
        <input type=\"text\" value=\""+str(data[0]['props'][i])+"\" class=\"form-control\" class=\"prop\">"
                # <dd class = \"basicInfo-item value\" >" + str(data[0]['props'][i]) + "</dd >"
        s += st
    return s
# get_all_profile("数据结构")