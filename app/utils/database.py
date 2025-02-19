import redis

from app import app_config

def get_redis() -> redis.StrictRedis:
    redis_config = app_config.redis_config
    redis_host = redis_config.host
    redis_password = redis_config.password
    redis_db = redis_config.db
    redis_port = redis_config.port
    redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db, password=redis_password, decode_responses=True)
    return redis_conn