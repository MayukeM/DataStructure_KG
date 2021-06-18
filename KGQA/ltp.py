# -*- coding: utf-8 -*-
import pyltp
import os
import jieba

LTP_DATA_DIR = 'D:/app/ltp_data_v3.4.0'  # ltp模型目录的路径
getpath = os.path.abspath(os.path.dirname(__file__))  # 获取本层目录
getpath = ('/').join(getpath.split('\\'))


# def cut_words(words):
#     segmentor = pyltp.Segmentor()
#     seg_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')
#     segmentor.load(seg_model_path)
#     words = segmentor.segment(words)
#     array_str = "|".join(words)
#     array = array_str.split("|")
#     segmentor.release()
#     return array

def cut_words(words):
    # list1 = jieba.lcut(words)
    jieba.load_userdict(getpath + "/my_dict.txt")
    array = jieba.lcut(words)
    # print(array)
    return array


# a = cut_words("数组的分类有哪些？")
# print(a)

def words_mark(array):
    # 词性标注模型路径，模型名称为`pos.model`
    pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')
    postagger = pyltp.Postagger()  # 初始化实例
    postagger.load(pos_model_path)  # 加载模型
    postags = postagger.postag(array)  # 词性标注
    pos_str = ' '.join(postags)
    pos_array = pos_str.split(" ")
    postagger.release()  # 释放模型
    return pos_array


def get_target_array(words):
    target_pos = ['n', 'v']
    target_array = []
    seg_array = cut_words(words)
    pos_array = words_mark(seg_array)
    for i in range(len(pos_array)):
        if pos_array[i] in target_pos:
            target_array.append(seg_array[i])
    return target_array


def get_fuzzy_array(words):
    seg_array = cut_words(words)
    return seg_array


# target_array = get_fuzzy_array("快排序")
# print(target_array)
