import json
from flask import Flask, request


app = Flask(__name__)

f = open('././dataset.json',)
dataset = json.load(f)

def get_id_by_game(game):
    try:
        return int(game['id'])
    except:
        return -1

@app.route('/', methods=['GET'])
def index():
    return "Welcome to BridgeBuff!"

@app.route('/api/game/<id>', methods=['GET'])
def get_id(id):
    try:
        for game in dataset:
            if 'id' in game.keys() and game['id'] == int(id):
                jsonReturned = {
                'game_id': game['id'],
                'game_stats': game
                }
                return json.dumps(jsonReturned)
    except:
        return json.dumps({'msg':'Game not found'})

@app.route('/api/rank/sunk', methods=['GET'])
def get_sunk_ships():
    start_index = int(request.args.get('start'))
    end_index = int(request.args.get('end'))
    dataset.sort(key=sunk_ships_number)
    ranking = dataset[start_index-1:end_index]
    idRank = map(get_id_by_game, ranking)
    jsonReturn = { "ranking": "sunk",
    "start": start_index,
    "end": end_index,
    "game_ids": list(idRank)
    }

    return json.dumps(jsonReturn)

def sunk_ships_number(k):
    try:
        return k['score']['sunk_ships'] * -1
    except:
        return -1

@app.route('/api/rank/escaped', methods=['GET'])
def get_escaped_ships():
    start_index = int(request.args.get('start'))
    end_index = int(request.args.get('end'))
    dataset.sort(key=escaped_ships_number)
    ranking = dataset[start_index-1:end_index]
    idRank = map(get_id_by_game, ranking)
    jsonReturn = { "ranking": "escaped",
    "start": start_index,
    "end": end_index,
    "game_ids": list(idRank)
    }

    return json.dumps(jsonReturn)

def escaped_ships_number(k):
    try:
        return k['score']['escaped_ships']
    except:
        return -1

app.run(debug=True)





