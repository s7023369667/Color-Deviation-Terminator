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
        line_bot_api = LineBotApi(
            'QwBCQUIQh5cMfUr521OLL7s1Z/SmtYCAbJ9qz41lbMXt+JxW4YBSyTEOqiSZx10UZZ4fTzbKiBkTGqJPCMbCx8O2iofmXQlrdajPpVrzu9hQ6YiJiOWMlnIJZPm37MpQJ5DgYD3BO1uJN7d3pq3+BAdB04t89/1O/w1cDnyilFU=')
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
