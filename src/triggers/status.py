import json # 用于解析 JSON 数据
from src.conf import triggerConf

#简道云智能助手回调触发器
# 该触发器用于监听简道云智能助手的回调，并根据回调内容返回相应的结果
#配置回调触发地址
url = triggerConf.get('url')

# e签宝回调的JSON 数据
body = triggerConf.get('body')

# 解析 JSON 数据
data = json.loads(body)

# 获取body 中的 action 的值
# 当 action 为 SIGN_FILE_RESCINDED 时，表示文件已解约
action = data.get("action")

# 根据 action 的值返回相应的结果
if action == "SIGN_FILE_RESCINDED":
    status = "已解约"
else:
    status = "解约中"

print(status)
# 简道云 API 要求返回 JSON 数据，因此这里直接返回字典数据
# return {
#     "status": status
# }
