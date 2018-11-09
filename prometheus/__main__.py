from settings import load_config
from redis_prometheus import RedisPrometheus
import time
import logging

load_config()
logger = logging.getLogger(__name__)

r = RedisPrometheus()
while True:
    logger.warning('spinning round right round like a record baby round round round round')

    r.gather_data_and_put_in_redis()
    time.sleep(1)