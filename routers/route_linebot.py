from decouple import config

from fastapi import Request, BackgroundTasks, APIRouter
from linebot import WebhookParser
from linebot.models import TextMessage
from aiolinebot import AioLineBotApi

from config import ACCESS_TOKEN, SECRET

from db.db_session import (
    db_register,
    db_update_context,
    db_reset_status,
    db_update_day,
    db_update_menu,
)

from button_template import (
    start_button_template,
    select_day_template,
    final_check_button,
    select_practice_template,
)

router = APIRouter(prefix="/messaging_api/handle_request", tags=["line-bot"])


# APIクライアントとパーサーをインスタンス化
line_api = AioLineBotApi(channel_access_token=ACCESS_TOKEN)
parser = WebhookParser(channel_secret=SECRET)


async def handle_events(events):
    for e in events:
        try:
            text = e.message.text
            user_id = e.source.user_id

            # ユーザーのセッション情報を取得
            user = await db_register(user_id)

            if user["context"] != "0" and text == "キャンセル":
                message = start_button_template()
                line_api.reply_message(e.reply_token, message)
                await db_reset_status(user_id)

            elif user["context"] == "0":
                if text == "スタート":
                    message = select_day_template()
                    line_api.reply_message(e.reply_token, message)
                    await db_update_context(user_id=user_id, context="1")
                else:
                    message = start_button_template()
                    await line_api.reply_message(e.reply_token, message)

            elif user["context"] == "1":
                await db_update_day(user_id=user_id, day=text)
                line_api.reply_message(e.reply_token, TextMessage(text="練習メニューを入力してね！"))
                message = select_practice_template()
                line_api.push_message(user_id, message)
                await db_update_context(user_id=user_id, context="2")

            elif user["context"] == "2":
                await db_update_menu(user_id=user_id, menu=text)
                message = final_check_button(user["day"], text)
                line_api.reply_message(e.reply_token, message)
                await db_update_context(user_id=user_id, context="3")

            elif user["context"] == "3":
                message = start_button_template()
                if text == "はい":
                    line_api.reply_message(
                        e.reply_token, TextMessage(text="お疲れ様！\n全体ラインに通知しておいたよ！")
                    )
                    line_api.push_message(user_id, message)
                    await db_reset_status(user_id)
                elif text == "いいえ":
                    line_api.reply_message(
                        e.reply_token, TextMessage(text="最初からやり直してね")
                    )
                    line_api.push_message(user_id, message)
                    await db_reset_status(user_id)
                else:
                    line_api.reply_message(
                        e.reply_token, TextMessage(text="「はい」か「いいえ」で答えて欲しいな!")
                    )

        except Exception as err:
            print(err)


@router.post("")
async def handle_request(request: Request, background_tasks: BackgroundTasks):
    events = parser.parse(
        (await request.body()).decode("utf-8"),
        request.headers.get("X-Line-Signature", ""),
    )

    background_tasks.add_task(handle_events, events=events)

    return "ok"
