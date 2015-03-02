from flask.ext.script import Manager, Server

from app import app


manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", port=5000, debug=True))


@manager.command
def show_urls():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.unquote("{:50s} {:20s} {}".format(
            rule.endpoint, methods, rule))
        output.append(line)
    for line in sorted(output):
        print(line)


if __name__ == "__main__":
    manager.run()
