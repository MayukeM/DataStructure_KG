from neo_db.config import CA_LIST
import json
import codecs
def get_json_data():
    with open("relation.txt", encoding='utf-8') as f:
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
    with open("relation.txt", encoding='utf-8') as f:
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
# with open("../static/data.json",encoding='utf-8') as f:
#     f.write(json.dumps(json_data))
# print(json_data)