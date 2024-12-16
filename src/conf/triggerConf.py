config = {
    # 解约请求参数配置
    # 你的公司名
    'orgName': 'yourOrgName',
    # 公司经办人手机号
    'psnAccount': 'yourPsnAccount',
    # 发起签署后得到的签署ID，签署完成才可以发起解约请求
    'signFlowId': 'yourSignFlowId',
    # 解约原因，1 - 条款内容有误  2 - 印章选择错误  3  - 签署人信息错误  4  - 合作终止  5 - 其他
    'rescindReason': '1',
    'rescindReasonNotes': '无',
    # 你的简道云智能助手http回调地址
    'notifyUrl': 'https://api.jiandaoyun.com/api/v1/automation/tenant/6744282ac6493f7c06edb9a6/hooks/674439dcd979675d5a0b9cc2f4cee1310b6e27b02f14bf41',
    # 解约状态请求参数配置
    # body示例（String）解约完成自动发送的请求体，这里是测试是否正确返回解约状态
    'body': '{"action": "SIGN_FILE_RESCINDED", '
            '"timestamp": 1656313026176, '
            '"signFlowId": "d500284461e44419aa05741e60e345b3", '
            '"rescissionSignFlowId": "e7176625***e676586ff1b", '
            '"rescissionFileIds": ["a4c5e***f34c2f4"]}'
}


def get(param):
    return config.get(param)
