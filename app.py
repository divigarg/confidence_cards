from flask import Flask, render_template, request
from jinja2 import Environment

def int_filter(value):
    return int(value)

def len_filter(value):
    return len(value)

env = Environment()
env.filters['int'] = int_filter
env.filters['length'] = len_filter

app = Flask(__name__)
app.jinja_env.globals.update(sum=sum)
players = []
sorted_players = []
total_players = 0
num_players = 0
num_rounds = 0
total_rounds = 0
current_status = -1

def sortPlayers():
    global sorted_players
    score_sort = {}
    correct_sort = {}
    for player in players:
        score_sort[player['name']] = player['sum_score']
        if player['correct_count'] not in correct_sort.keys():
            correct_sort[player['correct_count']] = []
        correct_sort[player['correct_count']].append(player['name'])
    score_sort = {k:score_sort[k] for k in sorted(score_sort, key = lambda x: -score_sort[x])}
    correct_sort = {k:correct_sort[k] for k in sorted(correct_sort, key = lambda x: -x)}
    print(score_sort)
    print()
    print(correct_sort)
    for name in score_sort:
        if(len(correct_sort) == 0):
            break
        first_value = []
        first_key = 0
        for key in correct_sort:
            first_value = correct_sort[key]
            first_key = key
            break
        for pname in first_value:
            pelement = {}
            for dictelem in players:
                if(dictelem['name']==pname):
                    pelement = dictelem                  
            # pelement = next((item for item in players if item['name'] == pname), None)
            pelement['total_score'] = pelement['sum_score'] + score_sort[name]
        correct_sort.pop(first_key)
    sorted_players = sorted(players, key = lambda x: -x['total_score'])

@app.route('/')
def index():
    return render_template('index.html', num_players = num_players, num_rounds = num_rounds, current_status = current_status)

@app.route('/new_game', methods=['POST'])
def new_game():
    global players, sorted_players, total_players, num_players, num_rounds, total_rounds, current_status
    players = []
    sorted_players = []
    total_players = 0
    num_players = 0
    num_rounds = 0
    total_rounds = 0
    current_status = -1
    return render_template('index.html', num_players = num_players, num_rounds = num_rounds, current_status = current_status)


@app.route('/match_setup', methods=['POST'])
def match_setup():
    global current_status, num_rounds, num_players, total_rounds
    num_players = int(request.form['players'])
    total_rounds = num_rounds = int(request.form['rounds'])
    current_status = current_status + 1
    print(f"num_players {num_players}, num_rounds {num_rounds}")
    return render_template('index.html', num_players = num_players, num_rounds = num_rounds, current_status = current_status, total_rounds = total_rounds)

@app.route('/add_player', methods=['POST'])
def add_player():
    global num_players, total_players
    name = request.form['player']
    players.append({'name': name, 'scores': [], 'correct_count': 0, 'sum_score': 0, 'total_score': 0})
    num_players -= 1
    total_players += 1
    return render_template('index.html', num_players = num_players, num_rounds = num_rounds, current_status = current_status, players = players, sorted_players = players, total_players = total_players, total_rounds = total_rounds)

@app.route('/add_new_player', methods=['POST'])
def add_new_player():
    global num_players, total_players
    name = request.form['new_player']
    players.append({'name': name, 'scores': [], 'correct_count': 0, 'sum_score': 0, 'total_score': 0})
    total_players += 1
    return render_template('index.html', num_players = num_players, num_rounds = num_rounds, current_status = current_status, players = players, sorted_players = players, total_players = total_players, total_rounds = total_rounds)


@app.route('/change_rounds', methods=['POST'])
def change_rounds():
    global total_rounds, num_rounds
    total_rounds = num_rounds = int(request.form['new_rounds'])
    return render_template('index.html', num_players = num_players, num_rounds = num_rounds, current_status = current_status, players = players, sorted_players = players, total_players = total_players, total_rounds = total_rounds)

@app.route('/start_playing', methods=['POST'])
def start_playing():
    global current_status
    current_status += 1
    return render_template('index.html', num_players = num_players, num_rounds = num_rounds, current_status = current_status, players = players, sorted_players = players, total_players = total_players, total_rounds = total_rounds)

@app.route('/add_round', methods=['POST'])
def add_round():
    global num_rounds
    num_rounds -= 1
    for player in players:
        score = int(request.form[player['name']])
        if request.form["correctness " + player['name']] == "correct":
            score = (score+1)*10 + score
            player['correct_count'] += 1
        else:
            score = 0
        player['scores'].append(score)
        player['sum_score'] += score
    # print(players)
    # print()
    sortPlayers()
    return render_template('index.html', num_players = num_players, num_rounds = num_rounds, current_status = current_status, players = players, sorted_players = sorted_players, total_players = total_players, total_rounds = total_rounds)


@app.route('/calculate_scores', methods=['POST'])
def calculate_scores():
    for player in players:
        player['total_score'] = sum(player['scores'])
    return render_template('index.html', num_players = num_players, num_rounds = num_rounds, current_status = current_status, players = players, sorted_players = sorted_players, total_players = total_players, total_rounds = total_rounds)

if __name__ == '__main__':
    app.run(debug=True)
