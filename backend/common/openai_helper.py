"""
    openai助手模塊
    https://platform.openai.com/docs/guides/speech-to-text api範例
"""
import openai
import configparser
# 設置API密鑰
config = configparser.ConfigParser()
config.read("./config.ini")
openai.api_key = config.get("openai", "api_key")
class Get_openAI():
    @staticmethod
    def post(text):
        print('進入openai')
        conversation = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": text},
        ]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation,
                max_tokens=150,
                temperature=0.2,
            )
            print(response)
            data = response["choices"][0]["message"]["content"]
            print(data)
            return data
        except Exception as e:
            print(e)
            return e


