import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import ApiClient, Configuration
from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from debugger import enable_debugger_if
from model.anime_dto import AnimeDto
from service.anime_service import AnimeService
from service.line_service import LineService
from util import split_by_chunk_size

load_dotenv()
enable_debugger_if()

app = FastAPI()

handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))
configuration = Configuration(access_token=os.getenv('LINE_ACCESS_TOKEN'))

logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    """
    AWS Lambda handler function to process LINE webhook events.
    """
    signature = event['headers']['x-line-signature']
    body = event['body']
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {'statusCode': 400}

    return {'statusCode': 200}


@app.post("/callback")
async def callback(request: Request):
    """
    FastAPI endpoint to handle LINE webhook requests.
    """
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body_bytes = await request.body()
    body_text = body_bytes.decode("utf-8")

    # handle webhook body
    try:
        handler.handle(body_text, signature)
    except InvalidSignatureError:
        logger.info(
            "Invalid signature. Please check your channel "
            + "access token/channel secret.")
        return Response(status_code=400)

    return Response(status_code=200)


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    """
    Common message handler for LINE text messages.
    """
    anime_service = AnimeService(
        api_url=os.getenv("ANNICT_API_URL"),
        access_token=os.getenv("ANNICT_ACCESS_TOKEN")
    )
    with ApiClient(configuration) as api_client:
        line_service = LineService(api_client)

        anime_items: list[AnimeDto] = \
            anime_service.fetch_current_season_anime()
        reply_message_items: list[str] = []
        # 5件ずつのアニメ情報を一つのメッセージにまとめる
        for anime_chunk in split_by_chunk_size(anime_items, 5):
            reply_message = ""
            for anime in anime_chunk:
                reply_message += f"{anime.title}\n"
                if anime.official_site_url:
                    reply_message += f"{anime.official_site_url}\n"
                reply_message += "\n"
            reply_message_items.append(reply_message)

        line_service.push_message(
            event.source.user_id,
            reply_message_items)

    return "OK"
