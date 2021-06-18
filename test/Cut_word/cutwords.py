# # -*- coding: utf-8 -*-
# import pyltp
# import os
# import base64
# import json
# from py2neo import Graph
#
# LTP_DATA_DIR = 'D:/app/ltp_data_v3.4.0'  # ltp模型目录的路径
# def cut_words(words):
#     user_dict = 'D:\学习\毕设-知识图谱/12.我的项目\DataStructureKG_UIupdate\DataStructure_KG/test\ds_dict.txt'
#     segmentor = pyltp.Segmentor()  # 初始化实例
#     seg_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
#     segmentor.load_with_lexicon(seg_model_path, user_dict)
#     # segmentor.load(seg_model_path)  # 加载模型
#     words = segmentor.segment(words)
#     print(words)
#     array_str = "|".join(words)
#     print(array_str)
#     array = array_str.split("|")
#     segmentor.release()
#     return array
#
#
# # array = cut_words("数据结构包括什么？")
# array = cut_words("可应用方法如中和沉淀法、硫化物沉淀法、上浮分离法、电解沉淀(或上浮)法、电解法、隔膜电解法等;二是将废水中的重金属在不改变其化学形态的条件下进行浓缩和分离，可应用方法有反渗透法、电渗析法、蒸发法和离子交换法等")
# print(array)



from pyltp import SentenceSplitter, Segmentor, Postagger, Parser, NamedEntityRecognizer, SementicRoleLabeller

# 分词
def cut(sent):
    segmentor = Segmentor()
    model_path = 'D:/app/ltp_data_v3.4.0/cws.model'
    user_dict = 'ds_dict.txt'
    segmentor.load_with_lexicon(model_path, user_dict)
    words = segmentor.segment(sent)
    print(words)
    array_str = "|".join(words)
    print(array_str)
    segmentor.release()  # 释放应用
    return
cut('数据结构')
sent = '可应用方法如中和沉淀法、硫化物沉淀法、上浮分离法、电解沉淀(或上浮)法、电解法、隔膜电解法等;二是将废水中的重金属在不改变其化学形态的条件下进行浓缩和分离，可应用方法有反渗透法、电渗析法、蒸发法和离子交换法等'
