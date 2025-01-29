#Agents.py
import configparser
# 读取配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 配置 Kimi API
KIMI_API_KEY = config['llm_api']['kimi_api_key']
KIMI_BASE_URL = config['llm_api']['kimi_url']


# 配置 Deepseek API
DEEPSEEK_API_KEY = config['llm_api']['deepseek_api_key']
DEEPSEEK_API_URL = config['llm_api']['deepseek_url']