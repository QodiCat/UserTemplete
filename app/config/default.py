""" 
存储默认的配置文件
"""
from .secert import *

DEFAULT_CONFIG={
    "mysql_config": {
        "connections": {
            "default": {
                "engine": "tortoise.backends.mysql",
                "credentials": {
                    "host": mysql_server,
                    "port": mysql_port,
                    "user": mysql_user,
                    "password": mysql_password,
                    "database": mysql_database,
                }
            },
        }, 
        "apps": {
            "models": {
                "models": [
                    "app.models.user",
                    "app.models.role",
                    "app.models.cakey", 
                    "app.models.cakey_vip", 
                    "app.models.llm_history",
                    "aerich.models"
                ],
                "default_connection": "default",
            }
        },       
    },
    "redis_config": {
        "host": redis_host,
        "password": redis_password,
        "db": redis_db,
        "port": redis_pord
    },
    "jwt_config": {
        "jwt_secret_key": jwt_secrect_config,
    },
    "verification_code_config": {
        "alibaba_cloud_accesskey_id": alibaba_cloud_accesskey_iD,
        "alibaba_cloud_accesskey_secret": alibaba_cloud_accesskey_secret
    }
}

