from flask import Flask, render_template, request, jsonify, make_response, redirect, session
from neo_db.query_graph import query, get_KGQA_answer, get_answer_profile, query_path, get_answer_all_profile, \
    query_branch, all, fuzzy_search
from KGQA.ltp import get_target_array,get_fuzzy_array
from neo_db.update import update_node, add_node, delete_node
from kg_data.data_processing import get_data_num
from kg_data.data_show import get_train_data_list
from mysql_db.data_show import cate_rel_show, operation
from flask_session import Session
import numpy as np
import pandas as pd
import csv
import os
import datetime
import json

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.urandom(24)
app.secret_key = 'beifang changjian de keke ....'


# Session(app)

@app.route('/', methods=['GET', 'POST'])
# @app.route('/index', methods=['GET', 'POST'])
def first(name=None):
    return render_template('first.html', name=name)


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/search.html', methods=['GET', 'POST'])
def search():
    return render_template('search.html')


@app.route('/KGQA.html', methods=['GET', 'POST'])
def KGQA():
    return render_template('KGQA.html')


@app.route('/get_profile', methods=['GET', 'POST'])
def get_profile():
    name = request.args.get('character_name')
    json_data = get_answer_profile(name)
    return jsonify(json_data)


# all_relation.html所使用
@app.route('/get_all_profile', methods=['GET', 'POST'])
def get_all_profile():
    name = request.args.get('character_name')
    # cate = request.args.get('cate')
    json_data = get_answer_all_profile(name)
    return jsonify(json_data)


@app.route('/all_node', methods=['GET', 'POST'])
def all_node():
    json_data, name_dict = all()
    session['name_dict'] = name_dict
    return jsonify(json_data)


@app.route('/search_a_node', methods=['GET', 'POST'])
def search_a_node():
    name = request.args.get('name')
    id = session.get('name_dict')[name]
    json_data = {'id': id}
    return jsonify(json_data)


@app.route('/KGQA_answer', methods=['GET', 'POST'])
def KGQA_answer():
    question = request.args.get('name')
    target_array = get_target_array(str(question))
    if len(target_array) == 1:
        json_data = query(str(target_array[0]))
    elif len(target_array) == 0:
        json_data = query(question)
    else:
        json_data = get_KGQA_answer(target_array)
    return jsonify(json_data)


@app.route('/KGQA_fuzzy', methods=['GET', 'POST'])
def KGQA_fuzzy():
    question = request.args.get('name')
    target_array = get_fuzzy_array(question)
    # print(f"tar {target_array}")
    json_data = fuzzy_search(target_array)
    # print(f"js {json_data}")
    return jsonify(json_data)


# 知识点检索
@app.route('/search_name', methods=['GET', 'POST'])
def search_name():
    name = request.args.get('name')
    json_data = query(str(name))
    return jsonify(json_data)


# 多度查询，分支检索
@app.route('/search_branch', methods=['GET', 'POST'])
def search_branch():
    name = request.args.get('name')
    print(name)
    deep = request.args.get('deep')
    print(deep)
    json_data = query_branch(str(name), deep)
    return jsonify(json_data)


# 查询最短路径
@app.route('/search_path', methods=['GET', 'POST'])
def search_path():
    a = request.args.get('a')
    b = request.args.get('b')
    json_data = query_path(str(a), str(b))
    return jsonify(json_data)


## Neo4j数据库增删改查
# 改变节点概念级别
@app.route('/change_node', methods=['GET', 'POST'])
def change_node():
    node = request.args.get('node')
    cate = request.args.get('cate')
    update_node(node, cate)
    return render_template('all_relation.html')
    # json_data = update_node(str(node), str(cate))
    # return jsonify(json_data)


# 添加一条关系
@app.route('/add_Node', methods=['GET', 'POST'])
def add_Node():
    e1 = request.form.get('e1')
    e2 = request.form.get('e2')
    rel = request.form.get('rel')
    c1 = request.form.get('c1')
    c2 = request.form.get('c2')
    add_node(e1, e2, rel, c1, c2)
    # print(message)
    # print(e1)
    # response = make_response(jsonify({'status':'success'}))
    return redirect('/all_relation.html')


# 删除一个节点
@app.route('/delete_aNode', methods=['GET', 'POST'])
def delete_aNode():
    name = request.args.get('node')
    delete_node(name)
    return redirect('/all_relation.html')


@app.route('/all_relation.html', methods=['GET', 'POST'])
def get_all_relation():
    return render_template('all_relation.html')


# --------------------------part-------------------------------
# --------------------------part-------------------------------
@app.route('/graph.html', methods=['GET', 'POST'])
def graph():
    return render_template('part/graph.html')


@app.route('/linear.html', methods=['GET', 'POST'])
def linear():
    return render_template('part/linear.html')


@app.route('/stack.html', methods=['GET', 'POST'])
def stack():
    return render_template('part/stack.html')


@app.route('/queue.html', methods=['GET', 'POST'])
def queue():
    return render_template('part/queue.html')


@app.route('/string.html', methods=['GET', 'POST'])
def string():
    return render_template('part/string.html')


@app.route('/array.html', methods=['GET', 'POST'])
def array():
    return render_template('part/array.html')


@app.route('/lists.html', methods=['GET', 'POST'])
def lists():
    return render_template('part/lists.html')


@app.route('/tree.html', methods=['GET', 'POST'])
def tree():
    return render_template('part/tree.html')


@app.route('/searching.html', methods=['GET', 'POST'])
def searching():
    return render_template('part/searching.html')


@app.route('/sorting.html', methods=['GET', 'POST'])
def sorting():
    return render_template('part/sorting.html')


# -------------------------other------------------------------
# -------------------------other------------------------------
@app.route('/search_path.html', methods=['GET', 'POST'])
def search_path1():
    return render_template('search_path.html')


# -------------------------data_show------------------------------
# -------------------------data_show------------------------------
@app.route('/cate_rel', methods=['GET', 'POST'])
def cate_rel():
    """请求的数据源，该函数将数据库中存储的数据，返回以下这种数据的列表：
       {'name': '香蕉', 'id': 1, 'price': '10'}
       {'name': '苹果', 'id': 2, 'price': '10'}
    """
    # data = cate_rel_show()

    # if request.method == 'POST':
    #     print('post')
    # if request.method == 'GET':
    #     info = request.values
    #     limit = info.get('limit', 10)  # 每页显示的条数
    #     offset = info.get('offset', 0)  # 分片数，(页码-1)*limit，它表示一段数据的起点
    #     print('get', limit)
    # print('get  offset', offset)

    name = request.args.get('search_kw')
    if name:
        print(name)
        sql = "select * from cate_rel where e1 like '%{0}%' or e2 like '%{0}%' or rel like '%{0}%' or c1 like '%{0}%' or c2 like '%{0}%'".format(
            name)
    else:
        sql = 'SELECT * FROM cate_rel'
    data = cate_rel_show(sql)
    return jsonify(data)
    # return jsonify({'total': len(data), 'rows': data[int(offset):(int(offset) + int(limit))]})
    # 注意total与rows是必须的两个参数，名字不能写错，total是数据的总长度，rows是每页要显示的数据,它是一个列表
    # 前端根本不需要指定total和rows这俩参数，他们已经封装在了bootstrap table里了


# 添加一条记录
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    e1 = request.form.get('e1')
    e2 = request.form.get('e2')
    rel = request.form.get('rel')
    c1 = request.form.get('c1')
    c2 = request.form.get('c2')
    item = [e1, e2, rel, c1, c2]
    sql = 'insert cate_rel (e1, e2, rel, c1, c2)VALUES (%s, %s, %s, %s, %s)'
    operation(sql, item)
    print(e1)
    # response = make_response(jsonify({'status':'success'}))
    return redirect('/data_show.html')


# 更新一条记录
@app.route('/update_item', methods=['GET', 'POST'])
def update_item():
    cate_rel_id = request.form.get('cate_rel_id')
    e1 = request.form.get('update_e1')
    e2 = request.form.get('update_e2')
    rel = request.form.get('update_rel')
    c1 = request.form.get('update_c1')
    c2 = request.form.get('update_c2')
    item = [e1, e2, rel, c1, c2, cate_rel_id]
    # print(item)
    sql = 'update cate_rel set e1 = %s, e2 = %s, rel = %s, c1 = %s, c2 = %s where cate_rel_id = %s'

    operation(sql, item)
    print(e1)
    # response = make_response(jsonify({'status':'success'}))
    return redirect('/data_show.html')


# 删除一条记录
@app.route('/delete_item', methods=['GET', 'POST'])
def delete_item():
    cate_rel_id = request.args.get("id")
    cate_rel_id = int(cate_rel_id)
    print(cate_rel_id)
    item = [cate_rel_id]
    sql = 'delete from cate_rel where cate_rel_id = "%s"'
    operation(sql, item)
    return redirect('/data_show.html')


@app.route('/data_show.html', methods=['GET', 'POST'])
def data_show():
    # train_data_list = get_train_data_list('/kg_data/cate.csv')
    return render_template('data_show/data_show.html')


@app.route('/cate.html', methods=['GET', 'POST'])
def cate():
    train_data_list = get_train_data_list('/kg_data/cate.csv')
    return render_template('data_show/cate.html', train_data_list=train_data_list)


@app.route('/relation.html', methods=['GET', 'POST'])
def relation():
    train_data_list = get_train_data_list('/kg_data/relation.csv')
    return render_template('data_show/relation.html', train_data_list=train_data_list)


@app.route('/welcome.html', methods=['GET', 'POST'])
def welcome():
    relation, entity = get_data_num()
    return render_template('welcome.html', entity=entity, relation=relation)


if __name__ == '__main__':
    app.debug = True
    app.run()
