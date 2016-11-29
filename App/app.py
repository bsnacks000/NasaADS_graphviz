from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
# some kind of cacheing system for JSON objects here?

@app.route('/', methods=['GET'])
def index():
    # render main page
    return render_template('/index.j2')


@app.route('/make_graph', methods=['POST'])
def make_graph():
    # AJAX request form query
    query = request.form['query']

    # <---process query here... hit sqlite for tables-->
    # <---make tables sigma ready and return json--->

    # ..placeholder code.. for json object
    new_graph = {
        'nodes': [
            {'id':1,'label':'Node A','x':0,'y':0,'color':'#4286f4','size':10},
            {'id':2,'label':'Node B','x':3,'y':1,'color':'#55d67c','size':5},
            {'id':3,'label':'Node C','x':1,'y':3,'color':'#c43e88','size':3}
        ], 'edges':[
            {'id':1,'source':1, 'target':2},
            {'id':2,'source':2, 'target':3},
            {'id':3,'source':1, 'target':3}
        ]
    }

    return jsonify(new_graph)

if __name__ == '__main__':
    app.run(debug=True)
