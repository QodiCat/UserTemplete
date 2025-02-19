
from app.config.app_config import AppConfig
from utils.log import LogManager, LogBroker

app_config = AppConfig()
logger = LogManager.GetLogger(log_name='astrbot')

