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
handler = WebhookHandler('3c33edbbb50c3386ebd4160ba6b1dfd5')
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
    #message = TextSendMessage(text=event.message.text)
    #line_bot_api.reply_message(event.reply_token, message)
    text=event.message.text
    if(text.startswith('#')):
        text = text[1:]
        if(len(re.split(r' ',text))==4):
            x,y,z,k=re.split(r' ',text)
        elif(len(re.split(r' ',text))==3):
            x,y,z=re.split(r' ',text)
            k=0
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='重新輸入'))
            x=''
        
        #content=str(re.split(r' ',text))
        if x!='':
            content = ''
            x=int(x)
            y1=float(y)/100.0+1
            y0=float(y)/100.0
            z=int(z)
            k=int(k)
            dt = datetime.now(tz).date()
            dtt = dt + timedelta(days = z)
            content+="貓咪價錢：\t{:06.2f}".format(x)
            content+="\n"
            content+="出售價錢：\t{:06.2f}".format((x*y1))
            content+="\n"
            content+="利潤：\t{:06.2f}".format((x*y0))
            if(k!=0):
                content+="\n"
                content+="{}成賺：\t{:06.2f}(轉{:06.2f})".format(k,(x*y0*k/10.0),((x*y1)-(x*y0*k/10.0)))
        #content+=str(x*y1)
        #content+="\n"
        #content+=str(x*y0)
            content+="\n"
            content+="抓貓時間\t {}年 {}月 {}日 {}時".format(dt.year, dt.month, dt.day ,datetime.now(tz).hour)
            content+='\n'
            content+="賣貓時間\t {}年 {}月 {}日 {}時".format(dtt.year, dtt.month, dtt.day ,datetime.now(tz).hour)
            if x!='':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
    elif(text.startswith('+')):
        text = text[1:]
        text1=re.split(r' ',text)
        sum=0
        for i in range(len(text1)):
          sum=sum+int(text1[i])
        content=sum
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
    elif(text.lower() == 'time'):
        content = ''
        content=str(datetime.now(tz))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))
    elif(text.lower() == 'help'):
        content = '#金額 幾趴 幾天 (幾成)'
        #content=str(datetime.now(tz))
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=content))

import os
import time
from datetime import timedelta, datetime
import pytz
import re
pytz.country_timezones('tw')
tz = pytz.timezone('Asia/Taipei')
dt = datetime.now(tz).date()
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
#if __name__ == "__main__":
#    app.run()    
