import redis
from omniconf import config
from prometheus_connection import PrometheusQuery
from multiprocessing import Pool
import logging
logger = logging.getLogger(__name__)

class RedisPrometheus:
    def __init__(self):
        prom_url = config('fuga.exporter.prometheus')
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
        self.redis.sadd('prometheus', item)
        data = self.prometheus.get_from_query(item)
        self.redis.set(item, data[-1])

    @property
    def queries(self):
        # the queries to run
        queries = []
        queries.extend(self.prometheus.find_query("go"))

        return queries