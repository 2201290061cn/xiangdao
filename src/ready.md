测试文档
1. 配置 conf 中的参数
agentConf.py：包含通用参数。
triggerConf.py：包含请求参数，需根据实际情况进行修改。
2. 在简道云创建智能助手
创建智能助手后，将智能助手的 HTTP 地址复制到 triggerConf.py 中的 notifyUrl 参数中。
3. 运行 status.py
运行 status.py 文件，检查是否正常运行，并确保输出为“已解约”。
4. 获取签署流程ID
通过简道云发送签署请求后，获取签署流程ID。
将获取到的签署流程ID复制到 triggerConf.py 中的 signFlowId 参数中。
5. 输入发起方签署公司名和公司经办人手机号
提供发起方签署公司的名称。
提供公司经办人的手机号。
6. 运行 termination.py
运行 termination.py 文件，检查是否正常运行，并确保输出为解约ID。
注意：解约操作需在签署完成后才能发起,否则提示“该签署流程尚未完成”。