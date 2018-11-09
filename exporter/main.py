# import requests
# from omniconf import config
# from elasticsearch import Elasticsearch

# from prometheus_connection import PrometheusQuery
# from prometheus_metrics import create_dict, convert2txt
# from settings import load_config


# def gather_data(prometheus_thing: PrometheusQuery):
#     # items = ["go_memstats_alloc_bytes_total", "prometheus_tsdb_head_series_created_total"]
#     items = prometheus_thing.find_query("go")

#     titels = []
#     data = []
#     for item in items:
#         titels.append(item)
#         data.append(prometheus_thing.get_from_query(item)[-1])

#     return create_dict(titels, data)


# def main():
#     load_config()

#     prom_url = config('fuga.exporter.prometheus')
#     es_url = config('fuga.exporter.elasticsearch')

#     p = PrometheusQuery(prom_url)
#     es = Elasticsearch(es_url)

#     if p.up():
#         # print(p.get_from_query_range("go_memstats_alloc_bytes_total", ranging="11h-13h", timestep="15m"))

#         d = gather_data(p)
#         print(convert2txt(d))
#         # print(es)
#         # print(dir(es))
#         # print(es.search())

# if __name__ == "__main__":
#     main()


import flask

from from_redis import RedisConnection
from settings import load_config
import logging

logger = logging.getLogger(__name__)

def make_app():
    load_config()
    app = flask.Flask('prometheus_thingy')

    @app.route("/")
    def index():
        return "<div><a href='/metrics'>metrics</a></div>"

    @app.route("/metrics")
    def metrics():
        logger.warning('metrics called')
        if "html" in flask.request.headers['Accept']:
            return '<pre style="font-size:100%;">' + RedisConnection().create_page() + '\n</pre>'
        return RedisConnection().create_page() + "\n"

    @app.route("/api/v1/label/__name__/values")
    def names():
        names = RedisConnection().get_applications_keys()
        dicto = {'status': 'success', 'data': names}
        return flask.jsonify(dicto)

    return app