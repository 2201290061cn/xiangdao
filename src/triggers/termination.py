import time  # 导入时间模块
import requests  # 导入请求模块
from src.conf import agentConf  # 导入agentConf配置
import json  # 导入json模块
import hashlib  # 导入hashlib模块
import base64  # 导入base64模块
import hmac  # 导入hmac模块
from datetime import datetime  # 导入datetime模块
from src.conf import triggerConf  # 导入triggerConf配置

# 配置开放平台开发者应用ID和应用Secret及请求地址URL
app_id = agentConf.get('appid')
secret_key = agentConf.get('secret')
base_url = "https://openapi.esign.cn"  # e签宝正式环境开放平台请求地址


# base_url = "https://openapi.esign.sit.cn" # e签宝测试环境开放平台请求地址
# 获取当前时间戳
def generate_timestamp():
    return int(time.time() * 1000)


# 生成签名
def generate_signature(method, accept, md5_base64, content_type, date, path, secret):
    # 待签名字符串拼接
    str_to_sign = f"{method}\n{accept}\n{md5_base64}\n{content_type}\n{date}\n{path}"
    print("待签名字符串拼接:\n" + str_to_sign)
    # 计算签名值
    hash_obj = hmac.new(secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256)
    hash_digest = hash_obj.digest()
    hash_in_base64 = base64.b64encode(hash_digest).decode('utf-8')
    return hash_in_base64


# 生成Body的MD5值并转换为Base64编码Content-MD5
def generate_content_md5(data):
    # 计算MD5值并转换为Base64编码
    md5_hash = hashlib.md5(data.encode('utf-8')).digest()
    md5_base64 = base64.b64encode(md5_hash).decode('utf-8')
    return md5_base64


# 获取当前时间并格式化为GMT时间
def get_gmt_date():
    return datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')


org_name = triggerConf.get('orgName')
psn_account = triggerConf.get('psnAccount')

# 获取orgId
timestamp = generate_timestamp()
date = get_gmt_date()
path = f"/v3/organizations/identity-info?orgName={org_name}"
accept = "*/*"
content_type = "application/json"
md5_base64 = ""  # GET请求通常不需要Content-MD5

signature = generate_signature("GET", accept, md5_base64, content_type, date, path, secret_key)
url = f"{base_url}{path}"

# 设置请求头
headers = {
    "X-Tsign-Open-App-Id": app_id,
    "Content-Type": content_type,
    "Accept": accept,
    "X-Tsign-Open-Auth-Mode": "Signature",
    "X-Tsign-Open-Ca-Timestamp": str(timestamp),
    "X-Tsign-Open-Ca-Signature": signature,
    "Date": date
}

# 发送GET请求
response = requests.get(url, headers=headers)

# 检查响应状态码
if response.status_code == 200:
    # 解析返回的JSON数据
    result = response.json()
    if result["code"] == 0:
        org_id = result["data"]["orgId"]
        print("Org ID:", org_id)
    else:
        print("Error:", result["message"])
else:
    print("Failed to get response:", response.status_code, response.text)

# 获取psnId
timestamp = generate_timestamp()
date = get_gmt_date()
path = f"/v3/persons/identity-info?psnAccount={psn_account}"
accept = "*/*"
content_type = "application/json"
md5_base64 = ""  # GET请求通常不需要Content-MD5

signature = generate_signature("GET", accept, md5_base64, content_type, date, path, secret_key)
url = f"{base_url}{path}"

# 设置请求头
headers = {
    "X-Tsign-Open-App-Id": app_id,
    "Content-Type": content_type,
    "Accept": accept,
    "X-Tsign-Open-Auth-Mode": "Signature",
    "X-Tsign-Open-Ca-Timestamp": str(timestamp),
    "X-Tsign-Open-Ca-Signature": signature,
    "Date": date
}

# 发送GET请求
response = requests.get(url, headers=headers)

if response.status_code == 200:
    result = response.json()
    if result["code"] == 0:
        psn_id = result["data"]["psnId"]
        print("Psn ID:", psn_id)
    else:
        print("Error:", result["message"])
else:
    print("Failed to get response:", response.status_code, response.text)

# 动态入参
sign_flow_id = triggerConf.get('signFlowId')

# 获取请求方法
method = "GET"

# Accept的值，建议统一为*/*
accept = "*/*"

# 对于GET请求，body_str为空字符串
body_str = ""

# Content-Type的值，建议统一：application/json; charset=UTF-8
content_type = "application/json; charset=UTF-8"

# 获取Date
date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

# 构建完整的URL
url = f"{base_url}/v3/sign-flow/{sign_flow_id}/detail"

# 获取路径
index = url.find(".cn")
length = len(".cn")
path = url[index + length:]

# 对于GET请求，Content-MD5为空字符串
md5_base64 = ""

# 待签名字符串拼接
str_to_sign = f"{method}\n{accept}\n{md5_base64}\n{content_type}\n{date}\n{path}"
print("待签名字符串拼接:\n" + str_to_sign)

# 计算签名值
hash_obj = hmac.new(secret_key.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256)
hash_digest = hash_obj.digest()
hash_in_base64 = base64.b64encode(hash_digest).decode('utf-8')

# 设置请求头
headers = {
    "X-Tsign-Open-App-Id": app_id,
    "Content-Type": content_type,
    "Accept": accept,
    "X-Tsign-Open-Auth-Mode": "Signature",
    "X-Tsign-Open-Ca-Timestamp": str(generate_timestamp()),
    "X-Tsign-Open-Ca-Signature": hash_in_base64,
    "Date": date
}

# 发送GET请求
response = requests.get(url, headers=headers)

# 检查响应状态码
if response.status_code == 200:
    # 解析返回的JSON数据
    result = response.json()
    # print("Response:", result)
    if result["code"] == 0:
        # 提取docs数组中的fileId
        docs = result["data"].get("docs", [])
        file_ids = [doc["fileId"] for doc in docs]
        print("File IDs:", file_ids)
    else:
        print("Error:", result["message"])
else:
    print("Failed to get response:", response.status_code, response.text)

# 动态入参
sign_flow_id = triggerConf.get('signFlowId')
org_name = triggerConf.get('orgName')
psn_account = triggerConf.get('psnAccount')
rescind_reason = triggerConf.get('rescindReason')
rescind_reason_notes = triggerConf.get('rescindReasonNotes')
# 获取请求方法
method = "POST"

# Accept的值，建议统一为*/*
accept = "*/*"

# 构建请求体
request_body = {
    "rescindReason": rescind_reason,
    "rescindFileList": file_ids,
    "rescindReasonNotes": rescind_reason_notes,
    "rescissionInitiator": {
        "orgInitiator": {
            "orgId": org_id,
            "transactor": {
                "psnId": psn_id
            }
        }
    },
    "signFlowConfig": {
        "chargeConfig": {
            "chargeMode": 1
        },
        "noticeConfig": {
            "noticeTypes": "1,2",
            "examineNotice": True
        },
        "notifyUrl": triggerConf.get('notifyUrl')
    },
    "orgSignerTransactor": [
        {
            "orgName": org_name,
            "transactorInfo": {
                "psnAccount": psn_account
            }
        }
    ]
}

# 将请求体转换为JSON字符串
body_str = json.dumps(request_body)

# Content-Type的值，建议统一：application/json; charset=UTF-8
content_type = "application/json; charset=UTF-8"

# 获取Date
date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')

# 构建完整的URL
url = f"{base_url}/v3/sign-flow/{sign_flow_id}/initiate-rescission"

# 获取路径
index = url.find(".cn")
length = len(".cn")
path = url[index + length:]

# 计算Content-MD5
md5_hash = hashlib.md5(body_str.encode('utf-8')).digest()
md5_base64 = base64.b64encode(md5_hash).decode('utf-8')

# 待签名字符串拼接
str_to_sign = f"{method}\n{accept}\n{md5_base64}\n{content_type}\n{date}\n{path}"
print("待签名字符串拼接:\n" + str_to_sign)

# 计算签名值
hash_obj = hmac.new(secret_key.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256)
hash_digest = hash_obj.digest()
hash_in_base64 = base64.b64encode(hash_digest).decode('utf-8')

# 设置请求头
headers = {
    "X-Tsign-Open-App-Id": app_id,
    "Content-Type": content_type,
    "Accept": accept,
    "X-Tsign-Open-Auth-Mode": "Signature",
    "X-Tsign-Open-Ca-Timestamp": str(generate_timestamp()),
    "X-Tsign-Open-Ca-Signature": hash_in_base64,
    "Date": date,
    "Content-MD5": md5_base64
}

# 发送POST请求
response = requests.post(url, headers=headers, data=body_str)

# 检查响应状态码
if response.status_code == 200:
    # 解析返回的JSON数据
    result = response.json()
    if result["code"] == 0:
        # 提取signFlowId
        sign_flow_id_from_response = result["data"]["signFlowId"]
        sign_flow_id = result["data"]["signFlowId"]
        print("Sign Flow ID:", sign_flow_id_from_response)
    else:
        print("Error:", result["message"])
else:
    print("Failed to get response:", response.status_code, response.text)

# 简道云 API 要求返回 JSON 数据，因此这里直接返回字典数据
# return {
#     "sign_flow_id": sign_flow_id
# }
