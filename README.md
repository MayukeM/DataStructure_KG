# DataStructure_KG
数据结构知识图谱
项目来源https://github.com/chizhu/KGQA_HLM

## 文件树：
1)  app.py是整个系统的主入口
2)  templates文件夹是HTML的页面
     |-first.html 欢迎界面
     |-index.html 系统主界面
     |-search.html 搜索知识点
     |-all_relation.html 知识图谱全貌展示
     |-KGQA.html 智能问答页面
     |-part文件夹的html是小结图谱界面
3)  static文件夹存放css和js，是页面的样式和效果的文件
4)  raw_data文件夹是存在数据处理后的三元组文件
5)  neo_db文件夹是知识图谱构建模块
     |-config.py 配置参数
     |-create_graph.py 创建知识图谱，图数据库的建立
     |-query_graph.py 知识图谱的查询
6)  KGQA文件夹是问答系统模块
     |-ltp.py 分词、词性标注、命名实体识别
7)  spider文件夹是爬虫模块
     |- get_*.py 是之前爬取的代码，已经产生好images和json 可以不用再执行
     |-show_profile.py 是调用爬虫信息和图谱展示在前端的代码
8)  test文件夹为测试代码
     
## 部署步骤：
* 0.安装所需的库 执行pip install -r requirement.txt
* 1.先下载好neo4j图数据库，并配好环境（注意neo4j需要jdk8）。修改neo_db目录下的配置文件config.py,设置图数据库的账号和密码。
* 2.切换到neo_db目录下，执行python  create_graph.py 建立知识图谱
* 3.去 [这里](http://pyltp.readthedocs.io/zh_CN/latest/api.html#id2) 下载好ltp模型。[ltp简介](http://ltp.ai/)
* 4.在KGQA目录下，修改ltp.py里的ltp模型文件的存放目录

## 数据处理
1. kg_data/relation.csv与cate.csv为手工构建最原始数据
2. 执行data_processing.py进行数据处理
    - col_to_dic() 将cate.csv按列类别生成字典，返回data_dict
    - add_cate(data_dict) 添加概念级别,并保存到raw_data/relation.csv
    - get_json_data() 将raw_data/relation.csv的数据转换成data link的json格式保存到（static/data.json)以便前端展示
2. 执行creat_graph.py创建图数据库,数据来自raw_data/relation.csv
4. 执行get_ds.py爬虫得到百度百科词条和图片（spider/json/data.json)(spider/images)
5. 执行get_dict.py得到自定义词典，在进行分词的时候，自定义词典里的词不会被分开
6. creat_graph.py 新增 添加数据属性到图数据库
> 上面步骤只需运行一次

运行app.py或整个项目，注意清除浏览器缓存，图谱显示才能更新

## 一些点
- 路径问题
```python
import os
getpath = os.path.abspath(os.path.dirname(__file__)) # 获取本层目录
getpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) # 获取上层目录
getpath = ('/').join(getpath.split('\\'))
```
- python版本
python3.6或python3.7 版本太高容易出问题

- 本地项目更新到github
```
git add . 所有变动文件，工作区->待提交区
git cmmint -m "注释"
git pull origin master 从远程仓库拉去代码到本地仓库以防止产生冲突
git push origin master 从本地仓库推送代码到远程服务器
git push -f origin master 强推
```
