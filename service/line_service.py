from linebot.v3.messaging import (
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhooks import MessageEvent


class LineService:
    def __init__(
            self,
            api_client: ApiClient,
            event: MessageEvent):
        self.api_client = api_client
        self.event = event

    def push_message(self, reply_message: str):
        line_bot_api = MessagingApi(self.api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=self.event.reply_token,
                messages=[TextMessage(text=reply_message)]
            )
        )
