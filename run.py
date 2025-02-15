from Storage.Redis.RedisClient import get_redis_client
from Api.AuthRoutes import auth_bp
from Api.ChatRoutes import chat_bp
from Api.TestRoutes import test_routes
from App import create_app
app = create_app()
# 配置 Redis 连接信息
app.config["REDIS_HOST"] = "103.126.211.100"

app.config["REDIS_PORT"] = 6379
app.config["REDIS_DB"] = 0
app.config["REDIS_PASSWORD"] = "q46DrEda2"

# 初始化 Redis 客户端
app.redis_client = get_redis_client(app)

#蓝图接口注册
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(chat_bp, url_prefix='/chat')
app.register_blueprint(test_routes, url_prefix='/test')


if __name__ == '__main__':
    app.run(debug=True)