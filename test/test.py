import re
from py2neo import Graph
from neo_db.config import CA_LIST
from kg_data.data_processing import col_to_dic
graph = Graph(
    "http://localhost:11008",
    username="neo4j",
    password="123456"
)
data = graph.run("MATCH p =shortestPath((n { name: '串' })-[*..15]-(m {name:'索引存储'})) RETURN p")
print(data)
data = data.data()
print(data)
data = data[0]['p']
data = str(data)
print(data)
# pattern1 = re.compile("='(.*?)'")  # 正则表达式匹配
# pattern2 = re.compile("\), ([\u4e00-\u9fa5]*)\(")

pattern1 = re.compile("\(([\u4e00-\u9fa5]*)\)-\[:([\u4e00-\u9fa5]*) {}\]->\(([\u4e00-\u9fa5]*)\)")  # (串)-[:属于 {}]->(线性结构)
pattern11 = re.compile("\[:([\u4e00-\u9fa5]*) {}\]->\(([\u4e00-\u9fa5]*)\)")  # [:属于 {}]->(线性结构)
pattern2 = re.compile("\(([\u4e00-\u9fa5]*)\)<-\[:([\u4e00-\u9fa5]*) {}\]-\(([\u4e00-\u9fa5]*)\)")  # (线性结构)<-[:分类 {}]-(数据结构)
pattern22 = re.compile("\(([\u4e00-\u9fa5]*)\)<-\[:([\u4e00-\u9fa5]*) {}\]")  # (线性结构)<-[:分类 {}]
pattern3 = re.compile(":([\u4e00-\u9fa5]*)")  # :属于
pattern4 = re.compile("\(([\u4e00-\u9fa5]*)\)")  # (串)

right = pattern11.findall(data)  # [('属于', '线性结构'), ('研究对象', '存储结构'), ('包括', '索引存储')]
left = pattern22.findall(data)  # [('线性结构', '分类')]
relation = pattern3.findall(data)  # ['属于', '分类', '研究对象', '包括']
concept = pattern4.findall(data)  # ['串', '线性结构', '数据结构', '存储结构', '索引存储']
arr_list = []
for item in right:
    a = ""
    for j in range(len(concept)):
        if concept[j] == item[1]:
            a += concept[j-1]+","+item[1]+","+item[0]
    arr_list.append(a)
for item in left:
    a = ""
    for j in range(len(concept)):
        if concept[j] == item[0]:
            a += concept[j+1]+","+item[0]+","+item[1]
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
    link_item = {}
    link_item['source'] = name_dict[rela_array[0]]
    link_item['target'] = name_dict[rela_array[1]]
    link_item['value'] = rela_array[2]
    json_data['links'].append(link_item)
print(json_data)
    # print(rela_array)


# print(right)
# print(left)
# print(relation)
# print(concept)