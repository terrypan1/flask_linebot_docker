from __future__ import unicode_literals
from flask import Flask, request, abort, render_template
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

import requests
import json
import configparser
import os
from common.reply_helper import Reply
from common.openai_helper import Get_openAI
from urllib import parse

app = Flask(__name__, static_url_path="/static")
UPLOAD_FOLDER = "static"
ALLOWED_EXTENSIONS = set(["pdf", "png", "jpg", "jpeg", "gif"])


config = configparser.ConfigParser()
config.read("config.ini")

configuration = Configuration(
    access_token=config.get("line-bot", "channel_access_token")
)
handler = WebhookHandler(config.get("line-bot", "channel_secret"))

my_line_id = config.get("line-bot", "my_line_id")
end_point = config.get("line-bot", "end_point")
line_login_id = config.get("line-bot", "line_login_id")
line_login_secret = config.get("line-bot", "line_login_secret")
my_phone = config.get("line-bot", "my_phone")
HEADER = {
    "Content-type": "application/json",
    "Authorization": f'Bearer {config.get("line-bot", "channel_access_token")}',
}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return "ok"
    body = request.json
    print(body)
    events = body.get("events") # 得到body
    if request.method == "POST" and len(events)==0:
        return 'ok'
    else:
        event = events[0]
        replyToken = event["replyToken"]
        if "message" in event and "text" in event["message"]:
            text = event["message"]["text"]
            res_openai = Get_openAI.post(text)
            payload = {
                "replyToken": replyToken,
                "messages": [{"type": "text", "text": res_openai}],
            }
            Reply.replyMessage(payload, HEADER)
            return "OK"


@app.route("/line_login", methods=["GET"])
def line_login():
    if request.method == "GET":
        print("進入Login")
        code = request.args.get("code", None)
        state = request.args.get("state", None)

        if code and state:
            HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}
            url = "https://api.line.me/oauth2/v2.1/token"
            FormData = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": f"{end_point}/line_login",
                "client_id": line_login_id,
                "client_secret": line_login_secret,
            }
            data = parse.urlencode(FormData)
            content = requests.post(url=url, headers=HEADERS, data=data).text
            content = json.loads(content)
            url = "https://api.line.me/v2/profile"
            HEADERS = {
                "Authorization": content["token_type"] + " " + content["access_token"]
            }
            content = requests.get(url=url, headers=HEADERS).text
            content = json.loads(content)
            name = content["displayName"]
            userID = content["userId"]
            pictureURL = content["pictureUrl"]
            statusMessage = content.get["statusMessage", ""]
            print(content)
            return render_template(
                "profile.html",
                name=name,
                pictureURL=pictureURL,
                userID=userID,
                statusMessage=statusMessage,
            )
        else:
            return render_template(
                "login.html", client_id=line_login_id, end_point=end_point
            )


if __name__ == "__main__":
    app.debug = True
    app.run()


