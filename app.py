from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import ConfigParser
import random

app = Flask(__name__)

config = ConfigParser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        print(body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def prettyEcho(event):

    sendString = ""
    if "AAA" in event.message.text:
        sendString = divinationBlocks()
    elif "BBB" in event.message.text or "B" in event.message.text:
        sendString = drawStraws()
    else:
        sendString = event.message.text 

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=sendString)
    )

def divinationBlocks():
    divinationBlocksList = ["A01", "A02", "A03", "A04"] 
    return divinationBlocksList[random.randint(0, len(divinationBlocksList) - 1)]

def drawStraws():
    drawStrawsList = ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08"]
    return drawStrawsList[random.randint(0, len(drawStrawsList) - 1)]

if __name__ == "__main__":
    app.run()
