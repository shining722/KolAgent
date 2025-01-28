#AuthRoutes.py

from flask import Blueprint
import tweepy

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/twitter/auth')
def twitter_auth():
    bearer_token = '你的Bearer Token'
    client = tweepy.Client(bearer_token=bearer_token)
    # 使用Client对象进行操作，例如搜索推文
    tweets = client.search_recent_tweets(query='twitter', max_results=10)
    for tweet in tweets.data:
        print(tweet.text)



@auth_bp.route('/login')
def login():
    return 'Login page'

@auth_bp.route('/logout')
def logout():
    return 'Logout page'

@auth_bp.app_errorhandler(404)
def not_found_error(error):
    return '404 Not Found', 404

