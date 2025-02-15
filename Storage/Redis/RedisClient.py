# Storage/Redis/RedisClient.py
import redis

def get_redis_client(app):
    return redis.StrictRedis(
        host=app.config.get("REDIS_HOST", "103.126.211.100"),
        port=app.config.get("REDIS_PORT", 6379),
        db=app.config.get("REDIS_DB", 0),
        password=app.config.get("REDIS_PASSWORD",""),
        decode_responses=True  # 自动解码返回值
    )