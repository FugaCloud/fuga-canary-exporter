import redis
from omniconf import config
from prometheus_connection import PrometheusQuery
from multiprocessing import Pool
import logging
logger = logging.getLogger(__name__)

class RedisPrometheus:
    def __init__(self):
        prom_url = config('fuga.exporter.prometheus.url')
        self.prometheus = PrometheusQuery(prom_url)
        self.redis = redis.from_url(config('fuga.exporter.redis'), decode_responses=True)
        logger.warning(self.redis)

    def gather_data_and_put_in_redis(self):
        # pool = Pool()
        # for item in self.queries:
        #     logger.warning(item)
        #     pool.apply_async(self.fetch_and_put, args=(item, ))
        # pool.close()
        # pool.join()
        for item in self.queries:
            self.fetch_and_put(item)

    def fetch_and_put(self,item):
        # self.redis.sadd('prometheus', item)
        data = self.prometheus.get_from_query(item)
        # self.redis.set(item, data[-1])

        self.redis.hset('prometheus', item, data[-1])

    @property
    def queries(self):
        return self.get_queries()
        # the queries to run
        # queries = []
        # queries.extend(self.prometheus.find_query("go"))

        # return queries

    def set_expiry(self):
        # time_in_seconds = 1
        time_in_seconds = config('fuga.exporter.prometheus.expirekeys')
        self.redis.setex("prometheus_expiry", "1", time_in_seconds)

    def remove_cached_data(self):
        del self.redis['prometheus_queries']
        del self.redis['prometheus']

    def load_queries_from_file(self):
        def strip_empty_lines(q):
            return [x.strip() for x in q if x]

        with open('queries.txt', "r") as f:
            queries = f.readlines()
        return strip_empty_lines(queries)

    def load_queries_from_redis(self):
        # queries = self.redis.smembers('prometheus_queries')
        queries = self.redis.lrange('prometheus_queries', 0, -1)
        return queries

    def set_queries(self, queries):
        # for q in queries:
        #     self.redis.sadd('prometheus_queries', q)
        self.redis.lpush('prometheus_queries', *queries)

    def get_queries(self):
        is_expired = True if self.redis.get('prometheus_expiry') is None else False
        if is_expired:
            logger.warning('expired')
            self.remove_cached_data()
            queries = self.load_queries_from_file()
            self.set_queries(queries)
            self.set_expiry()
        return self.load_queries_from_redis()
