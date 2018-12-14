import sys

import flask

from ping_exporter.ping import wanted_attributes
from ping_exporter.prometheus_metrics import (lookup_attribute_to_name,
                                              prometheus_text)


def flask_metrics():
    from ping_exporter.main import get_config_from_argv

    config, _ = get_config_from_argv()

    prom_text = prometheus_text(config)
    if "html" in flask.request.headers['Accept']:
        return '<pre style="font-size:100%;">' + prom_text + '\n</pre>'
    return prom_text + "\n"


def index():
    return "<div><a href='/metrics'>metrics</a></div>"


def names():
    names = [lookup_attribute_to_name(x) for x in wanted_attributes]
    data = {'status': 'success', 'data': names}
    return flask.jsonify(data)


def make_app(*args, **kwargs):

    sys.argv = [sys.argv[0]]
    for a in args:
        sys.argv.append("--" + a)
    for k in kwargs:
        if k in ['generate_config']:
            continue
        sys.argv.append("--" + k)
        sys.argv.append(kwargs[k])

    from ping_exporter.main import get_config_from_argv, check_config

    config, _ = get_config_from_argv()
    check_config(config)

    app = flask.Flask(__name__)
    app.add_url_rule('/', 'index', index)
    app.add_url_rule('/metrics', 'metrics', flask_metrics)
    app.add_url_rule("/api/v1/label/__name__/values", 'names', names)
    app.add_url_rule(
        '/favicon.ico', "favicon",
        redirect_to="https://cdn.fuga.cloud/"
        "fuga-assets/dist/images/favicon.ico")

    @app.errorhandler(404)
    def error_page(e):
        return "<pre>404 page not found</pre>", 404

    return app
