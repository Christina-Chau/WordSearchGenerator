import os
import sys
import json
from contextlib import contextmanager

# ── Resolve wordsearch_generator directory ─────────────────────────────────
WS_GEN_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'wordsearch_generator')
)

# Load .env before importing WordBank (which triggers config.py → load_dotenv)
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

# Put wordsearch_generator/ on sys.path so its absolute imports resolve:
#   Game.py  : "from src.Board import Board"   → needs wordsearch_generator/ on path
#   WordBank.py: "from config import client"   → needs wordsearch_generator/ on path
if WS_GEN_DIR not in sys.path:
    sys.path.insert(0, WS_GEN_DIR)

from src.Game import Game          # wordsearch_generator/src/Game.py
from src.WordBank import WordBank   # wordsearch_generator/src/WordBank.py

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wordsearch-multiplayer-2024'
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='eventlet')

# ── Constants ────────────────────────────────────────────────────────────────

MAX_PLAYERS = 10

PLAYER_COLORS = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
    '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
]

# ── CWD helper ───────────────────────────────────────────────────────────────
# WordBank.__init__ opens "src/resources/wordBank.json" relative to CWD,
# so we temporarily cd into WS_GEN_DIR while instantiating it.

@contextmanager
def wordsearch_cwd():
    orig = os.getcwd()
    os.chdir(WS_GEN_DIR)
    try:
        yield
    finally:
        os.chdir(orig)

# ── Shared game state (single game) ─────────────────────────────────────────

state = {
    'board':       [],   # 2-D list of uppercase letters (from Game.board)
    'words':       [],   # words placed on the board (uppercase, no spaces)
    'found_words': {},   # word → {player_name, player_id, positions, color}
    'players':     {},   # sid  → {name, score, color, color_index, is_host}
    'phase':       'lobby',   # 'lobby' | 'generating' | 'playing' | 'finished'
    'category':    '',
}

# ── Word-bank helpers ────────────────────────────────────────────────────────

def load_categories():
    path = os.path.join(WS_GEN_DIR, 'src', 'resources', 'wordBank.json')
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    result = {}
    for item in data['category']:
        cat = list(item.keys())[0]
        subs = [list(s.keys())[0] for s in item[cat]]
        result[cat] = subs
    return result

# ── Selection validation ──────────────────────────────────────────────────────

def validate_selection(board, r1, c1, r2, c2, remaining):
    """
    Trace the straight line from (r1,c1) → (r2,c2) on the board,
    return (word, positions) if it matches a remaining word, else None.
    """
    dr, dc = r2 - r1, c2 - c1
    if dr == 0 and dc == 0:
        return None
    if dr != 0 and dc != 0 and abs(dr) != abs(dc):
        return None  # not H / V / diagonal

    steps = max(abs(dr), abs(dc))
    sr = dr // steps if dr != 0 else 0
    sc = dc // steps if dc != 0 else 0

    n = len(board)
    letters, positions = '', []
    for i in range(steps + 1):
        r, c = r1 + i * sr, c1 + i * sc
        if not (0 <= r < n and 0 <= c < n):
            return None
        letters += board[r][c]
        positions.append([r, c])

    if letters in remaining:
        return letters, positions
    rev = letters[::-1]
    if rev in remaining:
        return rev, list(reversed(positions))
    return None

# ── State serialisation ──────────────────────────────────────────────────────

def public_state():
    return {
        'board': state['board'],
        'words': state['words'],
        'found_words': {
            w: {
                'player_name': v['player_name'],
                'color':       v['color'],
                'positions':   v['positions'],
            }
            for w, v in state['found_words'].items()
        },
        'players': {
            sid: {
                'name':    p['name'],
                'score':   p['score'],
                'color':   p['color'],
                'is_host': p['is_host'],
            }
            for sid, p in state['players'].items()
        },
        'phase':    state['phase'],
        'category': state['category'],
    }

# ── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/categories')
def categories():
    return jsonify(load_categories())

# ── Socket events ─────────────────────────────────────────────────────────────

@socketio.on('connect')
def on_connect():
    emit('game_state', public_state())


@socketio.on('join_game')
def on_join(data):
    from flask import request
    sid  = request.sid
    name = (data.get('name') or '').strip()

    if not name:
        emit('error', {'message': 'Name cannot be empty.'})
        return
    if len(state['players']) >= MAX_PLAYERS:
        emit('error', {'message': f'Game is full (max {MAX_PLAYERS} players).'})
        return
    if state['phase'] not in ('lobby',):
        emit('error', {'message': 'A game is already in progress. Please wait.'})
        return
    if any(p['name'].lower() == name.lower() for p in state['players'].values()):
        emit('error', {'message': 'That name is already taken.'})
        return

    is_first = len(state['players']) == 0
    used = {p['color_index'] for p in state['players'].values()}
    color_index = next(i for i in range(MAX_PLAYERS) if i not in used)

    state['players'][sid] = {
        'name':        name,
        'score':       0,
        'color':       PLAYER_COLORS[color_index],
        'color_index': color_index,
        'is_host':     is_first,
    }

    emit('joined', {
        'player_id': sid,
        'is_host':   is_first,
        'color':     PLAYER_COLORS[color_index],
    })
    socketio.emit('game_state', public_state())


@socketio.on('start_game')
def on_start(data):
    from flask import request
    sid = request.sid

    if sid not in state['players']:
        return
    if not state['players'][sid]['is_host']:
        emit('error', {'message': 'Only the host can start the game.'})
        return

    # ── Board size ─────────────────────────────────────────────────────────
    try:
        size = max(5, min(50, int(data.get('board_size', 10))))
    except (TypeError, ValueError):
        size = 10

    # ── Resolve words ──────────────────────────────────────────────────────
    word_mode = data.get('word_mode', 'bank')
    words = []

    try:
        if word_mode == 'bank':
            category    = data.get('category', '')
            subcategory = data.get('subcategory', '')
            with wordsearch_cwd():
                bank  = WordBank(size)
                words = bank.get_words(category, subcategory)
            if not words:
                emit('error', {'message': 'No words found for that category/subcategory.'})
                return
            label = f'{category} › {subcategory}'

        elif word_mode == 'custom':
            raw = data.get('custom_words', '')
            word_list = [w.strip() for w in raw.replace('\n', ',').split(',') if w.strip()]
            with wordsearch_cwd():
                bank  = WordBank(size)
                words = bank.validate_words(word_list)
            label = 'Custom Word List'

        elif word_mode == 'ai':
            prompt = (data.get('ai_prompt') or '').strip()
            if not prompt:
                emit('error', {'message': 'Please enter a topic for AI generation.'})
                return
            # Let all clients know generation is in progress
            state['phase'] = 'generating'
            socketio.emit('game_state', public_state())
            socketio.emit('status', {'message': f'Generating words for "{prompt}"…'})

            with wordsearch_cwd():
                bank  = WordBank(size)
                words = bank.generate_words(prompt, size)

            if not words:
                state['phase'] = 'lobby'
                socketio.emit('game_state', public_state())
                emit('error', {'message': 'Could not generate words for that topic. Try a different one.'})
                return
            label = f'AI: {prompt}'

        else:
            emit('error', {'message': 'Unknown word mode.'})
            return

    except ValueError as e:
        if state['phase'] == 'generating':
            state['phase'] = 'lobby'
        emit('error', {'message': str(e)})
        return

    # ── Build board using Game.py directly ────────────────────────────────
    game          = Game(words, size)
    board, placed = game.create_board(words)   # board is game.board (2-D list)

    if not placed:
        emit('error', {'message': 'Could not place any words. Try a smaller board or fewer words.'})
        state['phase'] = 'lobby'
        return

    state['board']       = board
    state['words']       = placed
    state['found_words'] = {}
    state['phase']       = 'playing'
    state['category']    = label

    for p in state['players'].values():
        p['score'] = 0

    socketio.emit('game_state', public_state())


@socketio.on('find_word')
def on_find_word(data):
    from flask import request
    sid = request.sid

    if sid not in state['players'] or state['phase'] != 'playing':
        return

    try:
        r1, c1 = int(data['r1']), int(data['c1'])
        r2, c2 = int(data['r2']), int(data['c2'])
    except (KeyError, ValueError, TypeError):
        emit('invalid_selection', {})
        return

    remaining = [w for w in state['words'] if w not in state['found_words']]
    result    = validate_selection(state['board'], r1, c1, r2, c2, remaining)

    if result is None:
        emit('invalid_selection', {})
        return

    word, positions = result
    player  = state['players'][sid]
    points  = len(word) * 10
    player['score'] += points

    state['found_words'][word] = {
        'player_name': player['name'],
        'player_id':   sid,
        'positions':   positions,
        'color':       player['color'],
    }

    if len(state['found_words']) == len(state['words']):
        state['phase'] = 'finished'

    socketio.emit('game_state', public_state())

    if state['phase'] == 'finished':
        winner = max(state['players'].values(), key=lambda p: p['score'])
        socketio.emit('game_over', {
            'winner': winner['name'],
            'scores': {p['name']: p['score'] for p in state['players'].values()},
        })


@socketio.on('play_again')
def on_play_again():
    from flask import request
    sid = request.sid

    if sid not in state['players']:
        return
    if not state['players'][sid]['is_host']:
        emit('error', {'message': 'Only the host can restart.'})
        return

    state['board']       = []
    state['words']       = []
    state['found_words'] = {}
    state['phase']       = 'lobby'
    state['category']    = ''

    for p in state['players'].values():
        p['score'] = 0

    socketio.emit('game_state', public_state())


@socketio.on('disconnect')
def on_disconnect():
    from flask import request
    sid = request.sid

    if sid not in state['players']:
        return

    was_host = state['players'][sid]['is_host']
    del state['players'][sid]

    if not state['players']:
        state['board']       = []
        state['words']       = []
        state['found_words'] = {}
        state['phase']       = 'lobby'
        state['category']    = ''
    elif was_host:
        new_host = next(iter(state['players']))
        state['players'][new_host]['is_host'] = True

    socketio.emit('game_state', public_state())


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_ENV') != 'production'
    print(f'Word Search multiplayer → http://localhost:{port}')
    socketio.run(app, host='0.0.0.0', debug=debug, port=port)
