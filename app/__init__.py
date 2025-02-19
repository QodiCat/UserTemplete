
from app.config.app_config import AppConfig
from utils.log import LogManager, LogBroker
from utils.database import get_redis


app_config = AppConfig()
logger = LogManager.GetLogger(log_name='astrbot')
redis_client = get_redis()


