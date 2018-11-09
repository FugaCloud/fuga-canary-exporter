# import flask
# from omniconf import config
# from elasticsearch import Elasticsearch

# from prometheus_connection import PrometheusQuery
# from prometheus_metrics import create_dict, convert2txt
# from settings import load_config

# app = flask.Flask('prometheus_thingy')

# def gather_data_go(prometheus_thing: PrometheusQuery, search: str):
#     # items = ["go_memstats_alloc_bytes_total", "prometheus_tsdb_head_series_created_total"]
#     items = prometheus_thing.find_query(search)

#     titels = []
#     data = []
#     for item in items:
#         titels.append(item)
#         data.append(prometheus_thing.get_from_query(item)[-1])

#     return create_dict(titels, data)

# @app.route("/go")
# def go():
#     load_config()

#     prom_url = config('fuga.exporter.prometheus')
#     es_url = config('fuga.exporter.elasticsearch')

#     p = PrometheusQuery(prom_url)
#     es = Elasticsearch(es_url)

#     if p.up():
#         # print(p.get_from_query_range("go_memstats_alloc_bytes_total", ranging="11h-13h", timestep="15m"))

#         d = gather_data_go(p, "go")
#         return "<pre>" + convert2txt(d) + "</pre>"
#         # print(es)
#         # print(dir(es))
#         # print(es.search())
#     return ""

# @app.route("/search/<search>")
# def search(search):
#     load_config()

#     prom_url = config('fuga.exporter.prometheus')
#     es_url = config('fuga.exporter.elasticsearch')

#     p = PrometheusQuery(prom_url)
#     es = Elasticsearch(es_url)

#     if p.up():
#         # print(p.get_from_query_range("go_memstats_alloc_bytes_total", ranging="11h-13h", timestep="15m"))

#         d = gather_data_go(p, search)
#         return "<pre>" + convert2txt(d) + "</pre>"
#         # print(es)
#         # print(dir(es))
#         # print(es.search())
#     return ""

# def main():
#     app.run(host="0.0.0.0", port="8789", debug=True)

# if __name__ == '__main__':
#     main()