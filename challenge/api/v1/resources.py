from flask.ext import restful


class GameResource(restful.Resource):
    def get(self):
        return {'pk': 7}
