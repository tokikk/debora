import os, datetime, tempfile, random, textwrap
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

# Message template
room1_msg1 = textwrap.dedent('''
    ''')
room1_msg2 = textwrap.dedent('''
    チェックが完了しました。
    転倒対策が必要な家具を発見しました。
    　No.1 テレビ
    　No.2 ランプ
     
    【No.1】大型家具のテレビは転倒すると下敷きになってしまったり、
    割れた破片で怪我をする可能性があるため、優先的に対策しましょう。
    耐震ベルトと耐震マットでの固定をおすすめします。
    https://item.rakuten.co.jp/yukaiya/10001149/
    ''')
room1_msg3 = textwrap.dedent('''
    【No.2】高所にあるランプは落下すると危険です。
    耐震ジェルもしくは耐震マットで固定しましょう。
    https://item.rakuten.co.jp/firn/zt-4508-2/
    ''')
room2_msg1 = textwrap.dedent('''
    ''')
room2_msg2 = textwrap.dedent('''
    チェックが完了しました。
    転倒対策が必要な家具を発見しました。
    　No.1 本棚
    　No.2 ベット際の観葉植物
    　No.3 本棚の上の観葉植物
     
    【No.1】大型家具の本棚は転倒すると下敷きになってしまったり、
    収納した本が落下して怪我をする可能性があるため、優先的に対策しましょう。
    ストッパーで固定して、落下抑制テープで本が落ちないようにしましょう。
    https://item.rakuten.co.jp/lifemarche/26004/?iasid=07rpp_10095___ew-m4bictiy-4f-b6fe073d-1dac-4449-9697-9becdac3e6f9
    https://item.rakuten.co.jp/cocodecow/748607/
    ''')
room2_msg3 = textwrap.dedent('''
    【No.2】ベッド際の観葉植物は就寝時に落下した場合大変危険です。
    ベッドから離れた場所への配置変更をおすすめします。
    https://item.rakuten.co.jp/firn/zt-4508-2/
    ''')
room2_msg4 = textwrap.dedent('''
    【No.3】高所にある本棚の観葉植物は落下すると危険です。
    低地への配置変更をおすすめします。
    ''')
room3_msg1 = textwrap.dedent('''
    ''')
room3_msg2 = textwrap.dedent('''
    チェックが完了しました。
    転倒対策が必要な家具を発見しました。
    　No.1 本棚
    　No.2 本棚の上の観葉植物
    　No.3 デスクライト
     
    【No.1】ベッド際の大型家具の本棚は転倒すると下敷きになってしまったり、
    収納した本が落下して怪我をする可能性があるため、大変危険です。
    可能な場合は、ベッドから離れた場所への配置変更し、
    ストッパーで固定して、落下抑制テープで本が落ちないようにしましょう。
    https://item.rakuten.co.jp/lifemarche/26004/?iasid=07rpp_10095___ew-m4bictiy-4f-b6fe073d-1dac-4449-9697-9becdac3e6f9
    https://item.rakuten.co.jp/cocodecow/748607/

    ''')
room3_msg3 = textwrap.dedent('''
    【No.2】本棚上の観葉植物は落下すると危険です。
    低地への配置変更をおすすめします。
    ''')
room3_msg4 = textwrap.dedent('''
    【No.3】バランスの悪いデスクライトは転倒する可能性があります。
    特にデスク利用時に危険のため、耐震ジェルもしくは耐震マットで固定しましょう。
    https://item.rakuten.co.jp/firn/zt-4508-2/
    ''')

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
    
    if event.message.text == "exec sample1":
        image_url = "https://cool-heliotrope-f8f19e.netlify.app/room1_drw.png"
        msgs = [ImageMessage(type= "image", originalContentUrl=image_url, previewImageUrl=image_url),
                TextMessage(text=room1_msg2),
                TextMessage(text=room1_msg3)]
    elif event.message.text == "exec sample2":
        image_url = "https://cool-heliotrope-f8f19e.netlify.app/room2_drw.png"
        msgs = [ImageMessage(type= "image", originalContentUrl=image_url, previewImageUrl=image_url),
                TextMessage(text=room2_msg2),
                TextMessage(text=room2_msg3),
                TextMessage(text=room2_msg4)]
    elif event.message.text == 'exec sample3':
        image_url = "https://cool-heliotrope-f8f19e.netlify.app/room3_drw.png"
        msgs = [ImageMessage(type= "image", originalContentUrl=image_url, previewImageUrl=image_url),
                TextMessage(text=room3_msg2),
                TextMessage(text=room3_msg3),
                TextMessage(text=room3_msg4)]
    else:
        return 0
    msgs.append(TextMessage(text="よろしければ簡単なアンケートにご協力下さい\nhttps://forms.office.com/r/Q3GpxM0YeM"))
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=msgs
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