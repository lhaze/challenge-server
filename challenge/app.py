from flask import (Flask, render_template)
from jinja2 import Environment
from hamlish_jinja import HamlishExtension
from werkzeug import ImmutableDict


class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(
        extensions=[
            'jinja2.ext.autoescape',
            'jinja2.ext.with_',
            'hamlish_jinja.HamlishExtension'
        ]
    )


app = FlaskWithHamlish(__name__)
app.jinja_env.hamlish_enable_div_shortcut = True
app.jinja_env.hamlish_mode = 'debug'


@app.route('/')
def index():
    return render_template('index.haml')


@app.route('/game/<int:game_pk>/')
def show_game(game_pk):
    return render_template('game.haml')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
