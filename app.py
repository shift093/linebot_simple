from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('m6kmELzKEDsaShFsadmBADDG4Ht62m89sRV9bJwWVRfg4TWWw+VrXwMCYAS0R0KqeqLJJL8BJQm6HFxojsHA7nwKu5QQxI6d5TKIiNer8LtdvrXSnoKRQjAM7xhZPSrpxi35CUQdzBPdGt/XpNh9EwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('c239f52f96b89c8f4e756fe8dcbcdc1c')
#c239f52f96b89c8f4e756fe8dcbcdc1c
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
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
