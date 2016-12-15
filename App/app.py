from flask import Flask, render_template, jsonify, request, session
from utils.prepare_sigma import PrepareSigma

app = Flask(__name__)

app.config['SECRET_KEY'] = ',\xe0\xdc`\xd60\x91}IL\x0e\xa8\x84\xdd\\\x03\xa6\xe8\x07Z\xf7\x04?\xa1'
app.config['DATABASE'] = 'sqlite:///./data/graph.db'
# some kind of cacheing system for JSON objects here?


@app.route('/', methods=['GET'])
def index():
    # render main page
    return render_template('/index.html.j2')


@app.route('/make_graph', methods=['POST'])
def make_graph():
    db_path = app.config['DATABASE']
    # AJAX request form query

    query = request.form['query']
    gtype = request.form['gtype']

    graph_name = query + '_' + gtype   #<--- need to write assemble from the forms

    # <---process query here... hit sqlite for tables-->
    try:
        if graph_name not in session:
            graph = PrepareSigma(graph_name, db_path)
            session[graph_name] = graph.sigma_obj
        # <---make tables sigma ready and return json--->

        return jsonify(session[graph_name])

    except ValueError as e:
        return jsonify({'error': 'Value Error on server'})

if __name__ == '__main__':
    app.run(debug=True)
