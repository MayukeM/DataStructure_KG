# # -*- coding: utf-8 -*-
# from pyltp import SentenceSplitter
# from pyltp import Segmentor
# from pyltp import Postagger
# from pyltp import NamedEntityRecognizer
#
# ldir = 'D:/app/ltp_data_v3.4.0/cws.model'  # 分词模型
# dicdir = 'D:/学习/毕设-知识图谱/12.我的项目/DataStructureKG_UIupdate/DataStructure_KG/test/ds_dict.txt'  # 外部字典
# text = "贵州财经大学要举办大数据比赛吗？那让欧几里得去问问看吧！其实是在贵阳花溪区吧。"
# with open(dicdir, encoding='utf-8') as f:
#     a = f.readline()
#     print(a)
# # 中文分词
# segmentor = Segmentor()  # 初始化实例
# segmentor.load_with_lexicon(ldir, 'word')  # 加载模型
# words = segmentor.segment(text)  # 分词
# print(' '.join(words))  # 分词拼接
# words = list(words)  # 转换list
# print(u"分词:", words)
# segmentor.release()


import os
from pyltp import Segmentor, Postagger
# 分词
LTP_DATA_DIR = 'D:/app/ltp_data_v3.4.0'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`
lexicon_path = os.path.join(LTP_DATA_DIR, 'D:/学习/毕设-知识图谱/12.我的项目/DataStructureKG_UIupdate/DataStructure_KG/test/ds_dict.txt')  # 参数lexicon是自定义词典的文件路径
segmentor = Segmentor()
segmentor.load_with_lexicon(cws_model_path, lexicon_path)
sent = '据韩联社12月28日反映，美国防部发言人杰夫·莫莱尔27日表示，美国防部长盖茨将于2011年1月14日访问韩国。2010年2月28日中国刘军报道'
words = segmentor.segment(sent)  # 分词

print(' '.join(words))  # 分词拼接
words = list(words)  # 转换list
print(u"分词:", words)
segmentor.release()