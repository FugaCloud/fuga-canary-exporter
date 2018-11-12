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
                titles.append(key)
                data.append(value)

        return create_dict(titles, data)

    def create_page(self):
        return convert2txt(self.fetch_data())
