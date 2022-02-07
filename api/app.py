from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request
from flask import jsonify
from flask import make_response
from wordle_helper import wordle

app = Flask(__name__)

CORS(app, resources={r'/*': {'origins': '*'}},CORS_SUPPORTS_CREDENTIALS = True)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/api", methods=['POST', 'GET'])
def api():
    if request.method == 'POST':
        data = request.get_json()
        greys = [g['text'] for g in data['misses'] if g['state'] == 'miss']
        yellows = [
            (g['text'].upper(), int(g['id']))
            for g in data['hits'] if g['state'] == 'yellow'
        ]
        greens = [
            (g['text'].upper(), int(g['id']))
            for g in data['hits'] if g['state'] == 'green'
        ]
        try:
            matches_list = wordle.main(greys, yellows, greens)
            return jsonify(matches=matches_list, success=True), 200
        except:
            return jsonify({'status': 500})
    # return jsonify({'status': 'ok'})

if __name__ == '__main__':
    api()
