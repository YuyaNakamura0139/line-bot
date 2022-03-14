import os

import asyncio

from fastapi import FastAPI, Request, BackgroundTasks
from linebot import WebhookParser
from linebot.models import TextMessage
from aiolinebot import AioLineBotApi

ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
SECRET = os.getenv("LINE_CHANNEL_SECRET")


line_api = AioLineBotApi(channel_access_token=ACCESS_TOKEN)
parser = WebhookParser(channel_secret=SECRET)

app = FastAPI()


async def handle_events(events):
    await asyncio.sleep(5)
    for e in events:
        try:
            await line_api.reply_message_async(
                e.reply_token, TextMessage(text=e.message.text)
            )
        except Exception:
            pass


@app.post("/messaging_api/handle_request")
async def handle_request(request: Request, background_tasks: BackgroundTasks):
    events = parser.parse(
        (await request.body()).decode("utf-8"),
        request.headers.get("X-Line-Signature", ""),
    )

    background_tasks.add_task(handle_events, events=events)

    return "ok"
