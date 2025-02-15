import requests
from base64 import b64encode
from Utils import Auth2Utils
from Services import RedisService


#code = ""

# Twitter 的 Token 端点
token_url = "https://api.twitter.com/2/oauth2/token"
user_info_url = "https://api.twitter.com/2/users/me"

# 准备请求参数
client_id = "RGNiQnRSb1dJTC1IX1liWnZzN3o6MTpjaQ"
client_secret = "3VYjmVWFWfCE6OE3oMJ8Rvnn11_nGMqND91Qg2mzjJrqCzgAFf"
redirect_uri = "https://www.baidu.com"
code_verifier = Auth2Utils.generate_code_verifier()

#前端调用接口获得code_verifier和code_challenge，
#前端用code_verifier作为state去获取code,
#回调时，将state传给后端
def get_state_code_challenge():
    code_verifier = Auth2Utils.generate_code_verifier()
    code_challenge = Auth2Utils.generate_code_challenge(code_verifier)
    return code_verifier,code_challenge

#获取某用户的推文
def get_user_tweets(access_token, user_id, max_results=5):
    """
    使用 Twitter API 获取某用户的最新推文
    :param access_token: OAuth 2.0 的 access_token
    :param user_id: 用户的 Twitter ID
    :param max_results: 返回的推文数量（默认 5 条）
    :return: 推文列表
    """
    # Twitter API 端点
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    # 请求头
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    # 请求参数
    params = {
        "max_results": max_results,  # 返回的推文数量
        "tweet.fields": "created_at,public_metrics",  # 返回的推文字段
        "exclude": "retweets,replies"  # 排除转推和回复
    }
    # 发送 GET 请求
    response = requests.get(url, headers=headers, params=params)
    # 检查响应状态
    if response.status_code == 200:
        tweets = response.json()
        print("推文获取成功！")
        return tweets.get("data", [])
    else:
        print(f"错误: {response.status_code}, {response.text}")
        return None

#转发推文
def retweet_tweet(access_token, user_id, tweet_id):
    """
    使用 Twitter API 转发推文
    :param access_token: OAuth 2.0 的 access_token
    :param user_id: 转发推文的用户 ID
    :param tweet_id: 要转发的推文 ID
    :return: API 响应数据
    """
    # Twitter API 端点
    url = f"https://api.twitter.com/2/users/{user_id}/retweets"
    # 请求头
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    # 请求体
    payload = {
        "tweet_id": tweet_id
    }
    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=payload)
    # 检查响应状态
    if response.status_code == 200:
        print("推文转发成功！")
        return response.json()
    else:
        print(f"错误: {response.status_code}, {response.text}")
        return None

#点赞推文
def like_tweet(access_token, user_id, tweet_id):
    """
    使用 Twitter API 给推文点赞
    :param access_token: OAuth 2.0 的 access_token
    :param user_id: 要点赞的用户 ID
    :param tweet_id: 要点赞的推文 ID
    :return: API 响应数据
    """
    # Twitter API 端点
    url = f"https://api.twitter.com/2/users/{user_id}/likes"
    # 请求头
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    # 请求体
    payload = {
        "tweet_id": tweet_id
    }
    # 发送 POST 请求
    response = requests.post(url, headers=headers, json=payload)
    # 检查响应状态
    if response.status_code == 200:
        print("推文点赞成功！")
        return response.json()
    else:
        print(f"错误: {response.status_code}, {response.text}")
        return None

#获取用户信息
def get_twitter_user_info(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(user_info_url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        user_id = user_data["data"]["id"]
        user_name = user_data["data"]["username"]
        return user_id, user_name
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None, None

#保存用户token
def save_user_token(code):
    access_token, refresh_token = get_access_token(code)
    user_id, user_name = get_twitter_user_info(access_token)
    RedisService.set_key_with_ttl(f"ACCESS_TOKEN:{user_id}:{user_name}",access_token,5400)
    RedisService.set_key_with_ttl(f"REFRESH_TOKEN:{user_id}:{user_name}", refresh_token, 60*24*3600)

#获取access_toke,refresh_token
def get_access_token(code,state):
    # 使用 code 换取 access_token 和 refresh_token
    # 构建请求头
    credentials = f"{client_id}:{client_secret}"
    credentials_b64 = b64encode(credentials.encode('utf-8')).decode('utf-8')
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {credentials_b64}"
    }
    # 构建请求体
    data = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_verifier": state
    }
    # 发送请求
    response = requests.post(token_url, headers=headers, data=data)
    token_data = response.json()
    print(token_data)
    # 提取 access_token 和 refresh_token
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)
    return access_token, refresh_token

#使用refresh_token获取access_token
def refresh_access_token(refresh_token):
    """
    使用 refresh_token 刷新 access_token
    :param client_id: Twitter 开发者应用的客户端 ID
    :param client_secret: Twitter 开发者应用的客户端密钥
    :param refresh_token: 用于刷新 access_token 的令牌
    :return: 新的 access_token 和 refresh_token
    """
    # Twitter API 端点
    url = "https://api.twitter.com/2/oauth2/token"

    # 请求头
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = b64encode(credentials.encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # 请求体
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    # 发送 POST 请求
    response = requests.post(url, headers=headers, data=data)

    # 检查响应状态
    if response.status_code == 200:
        token_data = response.json()
        new_access_token = token_data.get("access_token")
        new_refresh_token = token_data.get("refresh_token")
        print("Access token 刷新成功！")
        return new_access_token, new_refresh_token
    else:
        print(f"错误: {response.status_code}, {response.text}")
        return None, None