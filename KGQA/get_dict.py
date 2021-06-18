import os
getpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # 获取上级目录
getpath = ('/').join(getpath.split('\\'))
with open(getpath+"/kg_data/relation.csv") as f:
    enentiy = []
    for line in f.readlines():
        rela_array = line.strip("\n").split(",")
        enentiy.append(rela_array[0])
        enentiy.append(rela_array[1])
    set_eneity = set(enentiy)
with open(getpath+"/KGQA/my_dict.txt", mode="w", encoding="utf-8") as f:
    for item in set_eneity:
        f.write(item+"\n")

"""
冒泡排序的算法是?
折半查找的时间复杂度是？
快速排序的代码是？
如何实现BF算法？

快速排序是哪种排序？ --快速排序的父类关系
交换排序有哪些？  -- 交换排序的子类关系

"""