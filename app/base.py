
from app.config.app_config import AppConfig
from app.utils.log import LogManager, LogBroker
from app.utils.database import get_redis


app_config = AppConfig()
logger = LogManager.GetLogger(log_name='app')
redis_client = get_redis()


