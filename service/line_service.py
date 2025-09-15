from linebot.v3.messaging import ApiClient, MessagingApi, PushMessageRequest

from util import split_by_chunck_size


class LineService:
    def __init__(self, api_client: ApiClient):
        self.line_bot_api = MessagingApi(api_client)

    def push_message(self, user_id: str, reply_messages: list[str]):
        for reply_message_chunk in split_by_chunck_size(reply_messages, 5):
            messages = []
            for reply_message in reply_message_chunk:
                messages.append({
                    "type": "text",
                    "text": reply_message
                })
            reply_message_dict = {
                "to": user_id,
                "messages": messages
            }
            try:
                push_message_request = PushMessageRequest.from_dict(
                    reply_message_dict)
                self.line_bot_api.push_message(
                    push_message_request=push_message_request)
            except Exception as e:
                print(f"Error occurred while pushing message: {e}")
