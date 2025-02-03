#AuthRoutes.py

from flask import Blueprint, Flask, request, jsonify, Response, stream_with_context
import tweepy
import configparser
from Services import TweepyService
from Models.Users import User

tweepy_service = TweepyService

auth_bp = Blueprint('auth', __name__)
# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

@auth_bp.route('/x/auth')
def twitter_auth():
    bearer_token = config['twitter']['bearer_token']
    client = tweepy.Client(bearer_token=bearer_token)
    # 使用Client对象进行操作，例如搜索推文
    tweets = client.search_recent_tweets(query='twitter', max_results=10)
    for tweet in tweets.data:
        print(tweet.text)


@auth_bp.route('/x/create_user')
def create_x_user():
    user_id = request.json.get('user_id')
    user_name = request.json.get('user_name')
    resp = tweepy_service.add_user(User(user_id=user_id,user_name=user_name))
    return resp


@auth_bp.route('/login')
def login():
    return 'Login page'

@auth_bp.route('/logout')
def logout():
    return 'Logout page'

@auth_bp.app_errorhandler(404)
def not_found_error(error):
    return '404 Not Found', 404

