from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

class Secret():
    def get_linebot_CAT(self):
        # Channel Access Token
        line_bot_api = LineBotApi('Add yours')
        return line_bot_api
    def get_linebot_CS(self):
        # Channel Secret
        handler = WebhookHandler('e06b7a3e38834cf653900077d62ac06a')
        return handler
    def get_imgur_CI(self):
        # Imgur client ID
        client_id = 'cf5bc7cf5274324'
        return client_id
    def get_imgur_CS(self):
        # Imgur client secret:
        client_secret = '6f8e86f1dd36ee6f6f336276ad4c8248226be028'
        return client_secret
    def get_mongodb_userid(self):
        USERNAME = 's7023369667'
        return USERNAME
    def get_mongodb_password(self):
        PASSWORD = '7023369667s'
        return PASSWORD
