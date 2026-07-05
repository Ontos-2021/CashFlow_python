from flask import current_app, redirect, render_template, request, session, url_for

from .game_engine import apply_action, cut_expenses, enrich_state, new_game, profession_choices, sell_one_asset

@current_app.route('/')
def index():
    return render_template('index.html', professions=profession_choices())


@current_app.route('/new-game', methods=['POST'])
def new_game_route():
    profession_id = request.form.get('profession')
    valid_professions = {profession['id'] for profession in profession_choices()}
    if profession_id not in valid_professions:
        profession_id = 'administrativo'
    session['game_state'] = new_game(profession_id)
    session.modified = True
    return redirect(url_for('game'))

@current_app.route('/game')
def game():
    state = session.get('game_state')
    if not state:
        return redirect(url_for('index'))
    if state.get('status') != 'playing':
        return redirect(url_for('report'))
    return render_template('game.html', state=state)


@current_app.route('/action/<action_id>', methods=['POST'])
def action(action_id):
    state = session.get('game_state')
    if not state:
        return redirect(url_for('index'))
    session['game_state'] = apply_action(state, action_id)
    session.modified = True
    if session['game_state'].get('status') == 'playing':
        return redirect(url_for('game'))
    return redirect(url_for('report'))


@current_app.route('/sell-asset', methods=['POST'])
def sell_asset_route():
    state = session.get('game_state')
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
        session['game_state'] = enrich_state(state)
        session.modified = True
    return redirect(url_for('game'))


@current_app.route('/cut-expenses', methods=['POST'])
def cut_expenses_route():
    state = session.get('game_state')
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
        session['game_state'] = enrich_state(state)
        session.modified = True
    return redirect(url_for('game'))


@current_app.route('/report')
def report():
    state = session.get('game_state')
    if not state:
        return redirect(url_for('index'))
    return render_template('report.html', state=state)


@current_app.route('/reset', methods=['POST'])
def reset():
    session.pop('game_state', None)
    return redirect(url_for('index'))
