from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

#======python的函數庫==========
import tempfile, os
import datetime
import openai
import time
import random
import yfinance as yf
#======python的函數庫==========

app = Flask(__name__)
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')
# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
# OPENAI API Key初始化設定
# openai.api_key = os.getenv('OPENAI_API_KEY')


def GPT_response(text):
    # 接收回應
    response = openai.Completion.create(model="text-davinci-003", prompt=text, temperature=0.5, max_tokens=500)
    print(response)
    # 重組回應
    answer = response['choices'][0]['text'].replace('。','')
    return answer


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        #\\ print(body, signature)
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
      

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)

def prettyEcho(event):

    sendString = ""
    if "列表" in event.message.text:
        sendString = listYFsymbol()
    elif "BBB" in event.message.text or "B" in event.message.text:
        sendString = drawStraws()
    else:
        sendString = event.message.text 

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=sendString)
    )

def listYFsymbol():
    yfList = ["^TWII", "2330.TW", "TWD=X"] 
    history = "<List>\r"
    for symbol in yfList:
        stock = yf.Ticker(symbol)        
        data = stock.history(period="1d")["Close"].iloc[0]
        history += symbol + ":" + data.to_string() +  "\r"
    return history

def drawStraws():
    drawStrawsList = ["BB1", "BB2", "BB3", "BB4", "BB5", "BB6", "BB7", "BB8"]
    return drawStrawsList[random.randint(0, len(drawStrawsList) - 1)]
                              
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
