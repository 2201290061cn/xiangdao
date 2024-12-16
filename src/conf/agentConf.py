# agentConf.py
#通用配置
config = {
    #e签宝的appid和secret
    'appid': '5111964517',
    'secret': 'cb9aea0c8068ab883b194ce74ab6a443',
}
def get(param):
    return config.get(param)