from flask import Flask, render_template, request, jsonify
from neo_db.query_graph import query, get_KGQA_answer, get_answer_profile, query_path, get_answer_all_profile
from KGQA.ltp import get_target_array
from neo_db.update import update_node

app = Flask(__name__)


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
    cate = request.args.get('cate')
    json_data = get_answer_all_profile(name, cate)
    return jsonify(json_data)


@app.route('/KGQA_answer', methods=['GET', 'POST'])
def KGQA_answer():
    question = request.args.get('name')
    json_data = get_KGQA_answer(get_target_array(str(question)))
    return jsonify(json_data)


# 知识点检索
@app.route('/search_name', methods=['GET', 'POST'])
def search_name():
    name = request.args.get('name')
    json_data = query(str(name))
    return jsonify(json_data)


# 查询最短路径
@app.route('/search_path', methods=['GET', 'POST'])
def search_path():
    a = request.args.get('a')
    b = request.args.get('b')
    json_data = query_path(str(a), str(b))
    return jsonify(json_data)


@app.route('/change_node', methods=['GET', 'POST'])
def change_node():
    node = request.args.get('node')
    cate = request.args.get('cate')
    json_data = update_node(str(node), str(cate))
    return jsonify(json_data)


@app.route('/all_relation.html', methods=['GET', 'POST'])
def get_all_relation():
    return render_template('all_relation.html')


# ------------------part------------------
@app.route('/graph.html', methods=['GET', 'POST'])
def graph():
    return render_template('part/graph.html')


# ------------------other------------------
@app.route('/search_path.html', methods=['GET', 'POST'])
def search_path1():
    return render_template('search_path.html')


@app.route('/welcome.html', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
