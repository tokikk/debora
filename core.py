import os, datetime, tempfile, random
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
    ImageMessage,
    MessagingApiBlob
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent
)
import rekognition


app = Flask(__name__)

configuration = Configuration(access_token=os.environ['API_TOKEN'])
handler = WebhookHandler(os.environ['API_SECRET'])
key_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')


@app.route('/')
def access_root():
    return 'You are trying to access the root directory'


@app.route('/check')
def check():
    return 'OK'


@app.route("/callback", methods=['POST'])
def callback():
    print("start callback", flush=True)
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
    print("hendle TextMessageContent", flush=True)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=f"テキストメッセージを受信！！\n{event.message.text}")]
            )
        )
        
@handler.add(MessageEvent, message=ImageMessageContent)
def handle_message(event):
    try:
        print("handle ImageMessage", flush=True)
        with ApiClient(configuration) as api_client:  
            line_bot_api = MessagingApi(api_client)
            line_bot_blob_api = MessagingApiBlob(api_client)        
            message_content = line_bot_blob_api.get_message_content(event.message.id)

            # os.makedirs(static_tmp_path, exist_ok=True)
            # with tempfile.NamedTemporaryFile(dir=static_tmp_path) as tf:
            #     tf.write(message_content)
            #     destination_key = rekognition.put_to_s3_storage(tf.name , key_name)
                
            #     if destination_key == 'err': 
            #         callback_text = 'S3ストレージへの画像の保存に失敗しました'
            #     else:
            #         callback = rekognition.detect_object_by_rekognition(static_tmp_path)
            #         if callback['text'] == 'err':
            #             callback_text = 'Rekognitionによるラベル検出に失敗しました'
            #         else:
            #             rekognition.put_to_s3_storage(callback['img'], key_name)
           
            num = random.randrange(11)
            if num % 2 == 0:
                image_url = "https://sparkly-mochi-d0e122.netlify.app/azarashi.png"
            else:
                image_url = "https://sparkly-mochi-d0e122.netlify.app/penguin.png"

            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=f"画像メッセージを受信！！"),
                              ImageMessage(type= "image", originalContentUrl=image_url, previewImageUrl=image_url)]
                )
            )
    except Exception as e:
        print(e, flush=True)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8080)