import re
import redis
from omniconf import config
from settings import load_config
from prometheus_metrics import create_dict, convert2txt
import logging

logger = logging.getLogger(__name__)

class RedisConnection:

    def __init__(self):
        self.redis = redis.from_url(config('fuga.exporter.redis'), decode_responses=True)
        self.applications = config('fuga.exporter.exporters')

    # def get_applications_keys(self):
    #     keys = []
    #     for app in self.applications:
    #         for item in self.redis.smembers(app):
    #             keys.append(item)
    #     return keys

    # def fetch_data(self):
    #     titles = []
    #     data = []
    #     for key in self.get_applications_keys():
    #         titles.append(key)
    #         data.append(self.redis.get(key))
    #     return create_dict(titles, data)

    def get_applications_keys(self):
        keys = []
        for app in self.applications:
            hashmap = self.redis.hgetall(app)
            keys.extend(hashmap.keys())
        return keys

    def fetch_data(self):
        titles = []
        data = []
        for app in self.applications:
            hashmap = self.redis.hgetall(app)
            for key, value in hashmap.items():
                titles.append(self.convert_query_to_label(key))
                data.append(value)

        return create_dict(titles, data)

    def create_page(self):
        return convert2txt(self.fetch_data())


    @staticmethod
    def convert_query_to_label(query):
        reg = re.compile("(.*)({.*})")
        label = reg.search(query).group(1) if reg.search(query) else query
        extra = reg.search(query).group(2) if reg.search(query) else None

        tokens = "[]() ,"
        for t in tokens:
            label = label.replace(t, "_")
        label = label.strip("_")
        label = "_".join(re.split("_+", label))
        if extra:
            label += extra
        return label


def test_convert_query_to_label():
    load_config()
    r = RedisConnection()
    assert "do_testing_cool" == r.convert_query_to_label("do_testing_cool")
    assert "rate_go_memstats_frees_total_5m" == r.convert_query_to_label("rate(go_memstats_frees_total[5m])")
    assert "sum_rate_go_memstats_frees_total_5m" == r.convert_query_to_label("sum(rate(go_memstats_frees_total[5m]))")
    assert "topk_3_sum_rate_instance_cpu_time_ns_5m_by_app_proc" == r.convert_query_to_label("topk(3, sum(rate(instance_cpu_time_ns[5m])) by (app, proc))")
    assert 'instance_cpu_time_ns{app="lion", proc="web", rev="34d0f99", env="prod", job="cluster-manager"}' == r.convert_query_to_label('instance_cpu_time_ns{app="lion", proc="web", rev="34d0f99", env="prod", job="cluster-manager"}')
