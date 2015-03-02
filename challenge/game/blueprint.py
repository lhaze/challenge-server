from flask import Blueprint, render_template


game_blueprint = Blueprint('game', __name__)

@game_blueprint.route('/<int:game_pk>/')
def show_game(game_pk):
    return render_template('game.haml')
