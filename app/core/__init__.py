
from wordease.config.wordease_config import WordEaseConfig
from .log import LogManager, LogBroker

wordease_config = WordEaseConfig()
logger = LogManager.GetLogger(log_name='astrbot')