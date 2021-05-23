import os
getpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) # 获取本层目录
getpath = ('/').join(getpath.split('\\'))
print(getpath)