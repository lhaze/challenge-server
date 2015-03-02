from flask import (Flask, render_template, url_for)
from jinja2 import Environment
from hamlish_jinja import HamlishExtension
from werkzeug import ImmutableDict

from game.blueprint import game_blueprint


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


app.register_blueprint(game_blueprint, url_prefix='/game')


@app.route('/')
def index():
  return render_template('index.haml')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
