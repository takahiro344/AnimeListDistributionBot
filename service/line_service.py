from linebot.v3.messaging import ApiClient, MessagingApi, PushMessageRequest


class LineService:
    def __init__(self, api_client: ApiClient):
        self.line_bot_api = MessagingApi(api_client)

    def push_message(self, user_id: str, anime_chunk: str):
        reply_message_dict = {
            "to": user_id,
            "messages": [
                {
                    "type": "text",
                    "text": anime_chunk
                }
            ]
        }
        try:
            push_message_request = PushMessageRequest.from_dict(
                reply_message_dict)
            self.line_bot_api.push_message(
                push_message_request=push_message_request)
        except Exception as e:
            print(f"Error occurred while pushing message: {e}")
