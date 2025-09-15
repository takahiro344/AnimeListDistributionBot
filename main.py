import os

import debugpy
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)
from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhooks import FollowEvent, MessageEvent, TextMessageContent

from repository.user_json_repository import UserJsonRepository
from service.anime_service import AnimeService
from service.user_service import UserService

debugpy.listen(("0.0.0.0", 5678))
print("Waiting for debugger attach...")
debugpy.wait_for_client()

load_dotenv()

app = FastAPI()

handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
configuration = Configuration(access_token=os.getenv('LINE_ACCESS_TOKEN'))

# 共通ユーザーサービス
user_repository = UserJsonRepository(os.getenv("USER_STORAGE"))
user_service = UserService(user_repository)

# 共通アニメサービス
anime_service = AnimeService(
    api_url=os.getenv("ANNICT_API_URL"),
    access_token=os.getenv("ANNICT_ACCESS_TOKEN")
)


@app.post("/callback")
async def callback(request: Request):
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body_bytes = await request.body()
    body_text = body_bytes.decode("utf-8")

    # handle webhook body
    try:
        handler.handle(body_text, signature)
    except InvalidSignatureError:
        app.logger.info(
            "Invalid signature. Please check your channel "
            + "access token/channel secret.")
        return Response(status_code=400)

    return Response(status_code=200)


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    with ApiClient(configuration) as api_client:
        if event.type == "message":
            anime_list = anime_service.fetch_current_season_anime()

            reply_message = ""
            for anime in anime_list:
                reply_message += f"{anime.title}\n"
                if anime.official_site_url:
                    reply_message += f"{anime.official_site_url}\n"
                reply_message += "\n"

            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text=reply_message)]
                )
            )

    return "OK"


@handler.add(FollowEvent)
def handle_follow(event: FollowEvent):
    user_id = event.source.user_id
    print(f"New follower: {user_id}")

    # ユーザーを登録
    user_service.add_user(user_id)

    # LINE にメッセージ返信
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text="フォローありがとうございます！")]
            )
        )
