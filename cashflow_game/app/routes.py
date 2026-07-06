from uuid import uuid4

from flask import current_app, redirect, render_template, request, session, url_for

from .game_engine import apply_action, cut_expenses, enrich_state, new_game, pay_down_debt_action, profession_choices, sell_one_asset, start_month


GAME_STORE = {}


def get_game_state():
    legacy_state = session.pop('game_state', None)
    if legacy_state:
        game_id = session.get('game_id') or uuid4().hex
        session['game_id'] = game_id
        GAME_STORE[game_id] = legacy_state
        session.modified = True
        return legacy_state

    game_id = session.get('game_id')
    if not game_id:
        return None
    return GAME_STORE.get(game_id)


def save_game_state(state):
    game_id = session.get('game_id') or uuid4().hex
    session['game_id'] = game_id
    GAME_STORE[game_id] = state
    session.modified = True

@current_app.route('/')
def index():
    return render_template('index.html', professions=profession_choices())


@current_app.route('/new-game', methods=['POST'])
def new_game_route():
    profession_id = request.form.get('profession')
    valid_professions = {profession['id'] for profession in profession_choices()}
    if profession_id not in valid_professions:
        profession_id = 'administrativo'
    save_game_state(new_game(profession_id))
    return redirect(url_for('game'))

@current_app.route('/game')
def game():
    state = get_game_state()
    if not state:
        return redirect(url_for('index'))
    if state.get('status') != 'playing':
        return redirect(url_for('report'))
    if not state.get('current_event'):
        start_month(state)
        state = enrich_state(state)
        save_game_state(state)
    return render_template('game.html', state=state)


@current_app.route('/action/<action_id>', methods=['POST'])
def action(action_id):
    state = get_game_state()
    if not state:
        return redirect(url_for('index'))
    state = apply_action(state, action_id)
    save_game_state(state)
    if state.get('status') == 'playing':
        return redirect(url_for('game'))
    return redirect(url_for('report'))


@current_app.route('/sell-asset', methods=['POST'])
def sell_asset_route():
    state = get_game_state()
    if not state or state.get('status') != 'playing':
        return redirect(url_for('index'))
    if state.get('action_used_this_month', {}).get('sell'):
        return redirect(url_for('game'))
    try:
        asset_index = int(request.form.get('asset_index', -1))
        percent = float(request.form.get('percent', 0.5))
    except (ValueError, TypeError):
        return redirect(url_for('game'))
    percent = max(0.1, min(1.0, percent))
    result = sell_one_asset(state, asset_index, percent)
    if result:
        state.setdefault('action_used_this_month', {})['sell'] = True
        state['last_discretionary_feedback'] = {
            'title': 'Activo vendido',
            'message': f'Vendiste {int(percent * 100)}% de {result["name"]} por ${result["proceeds"]:,.0f}.',
        }
        save_game_state(enrich_state(state))
    return redirect(url_for('game'))


@current_app.route('/cut-expenses', methods=['POST'])
def cut_expenses_route():
    state = get_game_state()
    if not state or state.get('status') != 'playing':
        return redirect(url_for('index'))
    if state.get('action_used_this_month', {}).get('cut_expenses'):
        return redirect(url_for('game'))
    result = cut_expenses(state)
    if result:
        state.setdefault('action_used_this_month', {})['cut_expenses'] = True
        state['last_discretionary_feedback'] = {
            'title': 'Gastos recortados',
            'message': f'Recortaste ${result["reduction"]:,.0f} de gastos mensuales. Stress +12.',
        }
        save_game_state(enrich_state(state))
    return redirect(url_for('game'))


@current_app.route('/pay-debt', methods=['POST'])
def pay_debt_route():
    state = get_game_state()
    if not state or state.get('status') != 'playing':
        return redirect(url_for('index'))
    if state.get('action_used_this_month', {}).get('pay_debt'):
        return redirect(url_for('game'))
    result = pay_down_debt_action(state)
    if result:
        state.setdefault('action_used_this_month', {})['pay_debt'] = True
        state['last_discretionary_feedback'] = {
            'title': 'Deuda reducida',
            'message': f'Pagaste ${result["payment"]:,.0f} de {result["name"]}. Credito +3.',
        }
        save_game_state(enrich_state(state))
    return redirect(url_for('game'))


@current_app.route('/report')
def report():
    state = get_game_state()
    if not state:
        return redirect(url_for('index'))
    return render_template('report.html', state=state)


@current_app.route('/reset', methods=['POST'])
def reset():
    game_id = session.pop('game_id', None)
    if game_id:
        GAME_STORE.pop(game_id, None)
    session.pop('game_state', None)
    return redirect(url_for('index'))
