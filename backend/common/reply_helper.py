"""
    文字回覆助手模塊
    https://platform.openai.com/docs/guides/speech-to-text api範例
"""
import requests

class Reply:
    def __init__(self,send_meaasge):
        self.send_meaasge = send_meaasge
    @staticmethod
    def replyMessage(payload,HEADER):
        url = "https://api.line.me/v2/bot/message/reply"
        response = requests.post(url, headers=HEADER, json=payload)  
        return "OK"
