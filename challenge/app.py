from flask import (Flask, render_template, url_for)
from flask.ext import restful
from jinja2 import Environment
from hamlish_jinja import HamlishExtension
from werkzeug import ImmutableDict

from api.v1.resources import GameResource
from game.blueprint import game_blueprint


# Hamlish support
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

# registering submodules
app.register_blueprint(game_blueprint, url_prefix='/game')
api = restful.Api(app, prefix="/api/v1")
api.add_resource(GameResource, "/game/")


@app.route('/')
def index():
    return render_template('index.haml')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
