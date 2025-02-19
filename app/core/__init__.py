
from app.config.app_config import WordEaseConfig
from .log import LogManager, LogBroker

wordease_config = WordEaseConfig()
logger = LogManager.GetLogger(log_name='astrbot')