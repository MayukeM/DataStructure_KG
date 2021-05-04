from flask import Flask, render_template, request, jsonify
from neo_db.query_graph import query, get_KGQA_answer, get_answer_profile
from KGQA.ltp import get_target_array

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


@app.route('/KGQA_answer', methods=['GET', 'POST'])
def KGQA_answer():
    question = request.args.get('name')
    json_data = get_KGQA_answer(get_target_array(str(question)))
    return jsonify(json_data)


@app.route('/search_name', methods=['GET', 'POST'])
def search_name():
    name = request.args.get('name')
    json_data = query(str(name))
    return jsonify(json_data)


@app.route('/all_relation.html', methods=['GET', 'POST'])
def get_all_relation():
    return render_template('all_relation.html')


@app.route('/graph.html', methods=['GET', 'POST'])
def graph():
    return render_template('part/graph.html')


if __name__ == '__main__':
    app.debug = True
    app.run()
