# Storage/Redis/RedisClient.py
import redis
import configparser
# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

def get_redis_client(app):
    return redis.StrictRedis(
        host=app.config.get("REDIS_HOST", config['redis']['url']),
        port=app.config.get("REDIS_PORT", config['redis']['port']),
        db=app.config.get("REDIS_DB", config['redis']['db']),
        password=app.config.get("REDIS_PASSWORD",config['redis']['password']),
        decode_responses=True  # 自动解码返回值
    )