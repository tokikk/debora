import os, datetime
from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ImageMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
import rekognition


app = Flask(__name__)

configuration = Configuration(access_token=os.environ['API_TOKEN'])
handler = WebhookHandler(os.environ['API_SECRET'])
key_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')


@app.route('/')
def access_root():
    return 'You are trying to access the root directory'


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. ")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=f"テキストメッセージを受信！！\n{event.message.text}")]
            )
        )
        
@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    with ApiClient(configuration) as api_client:  
        line_bot_api = MessagingApi(api_client)
        
        message_content = line_bot_api.get_message_content(event.message.id )
        img_path = rf"./image/tmp_{key_name}.png"
        with open(img_path, "wb") as f:
            for chunk in message_content.iter_content():
                f.write(chunk)
        
        destination_key = rekognition.put_to_s3_storage(img_path, key_name)
        if destination_key == 'err': 
            callback_text = 'S3ストレージへの画像の保存に失敗しました'
        else:
            callback_text = rekognition.detect_object_by_rekognition()
            if callback_text == 'err':
                callback_text = 'Rekognitionによるラベル検出に失敗しました'

        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=f"画像メッセージを受信！！\n{callback_text}")]
            )
        )

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8080)