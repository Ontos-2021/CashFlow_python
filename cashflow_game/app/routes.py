from flask import current_app, redirect, render_template, request, session, url_for

from .game_engine import apply_action, new_game, profession_choices

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
