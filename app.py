#Goal : app.py to mongoDB
#At : heroku-test sever
import os
import subprocess as sp
from flask import Flask, request, abort
import cv2
import numpy as np
import pyimgur

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

# Channel https
app = Flask(__name__)
# Channel Access Token
line_bot_api = LineBotApi('Add yours')# Channel Secret
handler = WebhookHandler('Add yours')
#Imgur client ID
client_id= 'Add yours'
#Imgur client secret:
client_secret = 'Add yours'

def upload2imgure(PATH):
    ##upload image to Imgur
    im = pyimgur.Imgur(client_id)
    upload_img = im.upload_image(PATH,title="Upload via pyimgur")
    print(upload_img.link)
    return upload_img.link

def get_imgurl(rgb):
    if not os.path.exists('color_fig'):
        print("Creat Directort:color_fig")
        os.mkdir('color_fig')
    img = np.zeros((100, 100, 3))  # build a picture size
    color = rgb[::-1]   # get b, g, r color value
    print(color)
    color = [int(e) for e in color]
    for i in range(len(color)):  # fill the color into picture
        for j in range(100):
            for k in range(100):
                img[j][k][i] = color[i]
    PATH = './color_fig/b{0}g{1}r{2}.jpg'.format(color[0], color[1], color[2])
    cv2.imwrite(PATH ,img)  # save as jpg
    img_link = upload2imgure(PATH)
    return img_link

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
def handle_message(event):  # 收到訊息時
    msg = event.message.text.lower()

    if msg == 'hi': #起始
        message = TemplateSendMessage(
        alt_text='電腦版可手動輸入:\"start\"',
        template=ButtonsTemplate(
        #thumbnail_image_url='https://i0.wp.com/www.womstation.com/wp-content/uploads/2018/11/%E9%9F%93%E5%9C%8B4.png?w=1280&ssl=1',
        title='按鈕輸入',
        text='點擊開始測量',
        actions=[
            MessageTemplateAction(
                    label='開始(Start)',
                    text='start'
            ),
            MessageTemplateAction(
                    label='說明(Help)',
                    text='help'
            ),
            ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    elif msg == 'start' or msg == 'start ': #開始說明
        message = "請依照此格式輸入\"R G B\""
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
    elif msg == 'result' or msg == 'result ':  # 獲取結果的情況
        upload_text = event.source.user_id
        p = sp.Popen(['python3', 'Calculation.py'], stdout=sp.PIPE, stdin=sp.PIPE)
        p.stdin.write(upload_text.encode(encoding="utf-8"))  # 傳
        out = p.communicate()[0]  # status
        out = out.decode('utf-8')
        result = out.split('\n')
        message = []
        if len(result) == 1:  # data error occur
            message.append(TextSendMessage(text=result[0]))
        else:
            rgb = result[0].split()
            img_link = get_imgurl(rgb)
            message.append(ImageSendMessage(original_content_url=img_link, preview_image_url=img_link))
            message.append(TextSendMessage(text='Measure(RGB): ({0}, {1}, {2})'.format(*rgb)))
            suggest = '\n'.join(result[1:])
            # print(suggest)
            message.append(TextSendMessage(text=suggest))
        p.stdin.close()
        # print('----test----', *message, sep='\n\n')
        line_bot_api.reply_message(event.reply_token, message)
        
    elif len(msg.split()) == 3:  # 輸入RGB的情況
        error = 0
        rgb = msg.split()
        for x in rgb:
            if int(x) > 255 or int(x) < 0:
                message = "格式錯誤 或是 數值錯誤"
                error = 1
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))
                break
        if error == 0:  # 輸入正確時
            user_id = event.source.user_id
            color_str = " ".join(rgb)
            upload_text = user_id + " " + color_str  # 要傳給app2mongodn.py的參數
            
            p = sp.Popen(['python3', 'app2mongodb.py'], stdout=sp.PIPE, stdin=sp.PIPE)
            p.stdin.write(upload_text.encode(encoding="utf-8"))
            out = p.communicate()  # status
            print(out)  # heroku上output
            
            img_link = get_imgurl(rgb)
            message1 = ImageSendMessage(original_content_url=img_link, preview_image_url=img_link)
            message2 = TextSendMessage(text=out[0].decode('utf-8'))
            p.stdin.close()
            line_bot_api.reply_message(event.reply_token, [message1,message2])
            
    elif msg == 'debug':
        img_link = get_imgurl([1, 2, 111])
        # message = TextSendMessage(text="debugging")
        message = ImageSendMessage(original_content_url=img_link, preview_image_url=img_link)
        line_bot_api.reply_message(event.reply_token, message)
        
    else:
        message = TextSendMessage(text='輸入格式錯誤 請輸入\"hi\"以重新開始')
        line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
