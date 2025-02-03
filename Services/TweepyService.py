import tweepy
import configparser
from App.extensions import db
from Models.Users import User



# 读取配置文件
config = configparser.ConfigParser()
# config.read('config.ini')
config.read('config.dev.ini')

# 保存x用户信息
def add_user(User):
    db.session.add(User)
    db.session.commit()
    return "User added!"

# x用户列表
def user_list():
    # 查询所有用户
    users = User.query.all()
    return users

def get_tweepy_client():
    # bearer_token = config['twitter']['bearer_token']
    bearer_token='AAAAAAAAAAAAAAAAAAAAAO3orAEAAAAA7A7p0W108jhqavhyh4Li%2BcDr7FU%3DbUn0g4rbhR9nsMFv6pKy2AJfC3v5JkiezoiZhFxzp5VrzbpTPN'
    consumer_key='raolw5ZYL1o1AoU1WfXqqaufi'
    consumer_secret='T0ahoOhss27oOoHHowCiSootcVqTkl0YJyl2EPwaUPA0kCX029'
    access_token='1725773410264125440-neW22eJ0LqR2G7QLFoUdHfno6lPHqi'
    access_token_secret='r4MEgPAXu7CBohw8NREYbAeeeTTJHAbBwpOafuP2qZbBk'
    client = tweepy.Client(bearer_token=bearer_token,
                           consumer_key=consumer_key,
                           consumer_secret=consumer_secret,
                           access_token=access_token,
                           access_token_secret=access_token_secret)
    return client

# 通过关键字搜索推文
def search_tweets(keywords):
    client = get_tweepy_client()
    tweets = client.search_recent_tweets(query='twitter', max_results=10)
    return tweets.data

# 发布推文
def create_tweet(message):
    client = get_tweepy_client()
    response = client.create_tweet(text=message)
    return response

# 用户推文点赞
def like_tweet(user_id,tweet_id):
    client = get_tweepy_client()

    # 点赞推文
    try:
        response = client.like(tweet_id=tweet_id)
        if response.data["liked"]:
            print("点赞成功！")
        else:
            print("点赞失败。")
    except tweepy.TweepyException as e:
        print(f"发生错误: {e}")

