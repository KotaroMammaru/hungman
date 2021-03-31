from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import os
import scrape as sc
from argparse import ArgumentParser

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ['''W5sP5DGfu6tI7bYSI6+SaMqqDUh5HQgaawcJ
                                        yld+CbRJTGPcv+/dmTcr57SlU1zk1gWMmhulaVR
                                        uGopvTWjWYa6F3heEu0/GvcXSc8NiECbpxssk58
                                        DzuD3S//BnTFvUrLw9lAMJBdtTpKbicIEZqAdB0
                                        4t89/1O/w1cDnyilFU=''']
YOUR_CHANNEL_SECRET = os.environ["170af48620776cf734048ab0e552c46b"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event == 'ダウ':
        result = sc.get_movement()
    else:
        result = 'それは対応していません'
    line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=result)
    )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
