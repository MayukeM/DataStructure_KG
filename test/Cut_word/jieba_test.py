import jieba
str = "李小福是创新办主也是云计算方面的专家"
list1 = jieba.lcut(str)
print(list1)

jieba.load_userdict("my_jieba_dict.txt")
list1 = jieba.lcut(str)
print(list1)