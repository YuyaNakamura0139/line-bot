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
    db_update_last_sentence,
    db_add_menu_name,
    db_add_menu_time,
    db_add_url,
)

from db.db_practice_menu import db_get_practice_name_list_by_practice_id

from button_template import (
    start_button_template,
    select_day_template,
    final_check_button,
    select_parent_practice_template,
    select_child_practice_template,
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
            user = db_register(user_id)

            if user["context"] != "0" and text == "キャンセル":
                line_api.reply_message(e.reply_token, start_button_template())
                db_reset_status(user_id)

            elif user["context"] == "0":
                if text == "スタート":
                    line_api.reply_message(e.reply_token, select_day_template())
                    db_update_context(user_id=user_id, context="1")
                else:
                    line_api.reply_message(e.reply_token, start_button_template())

            elif user["context"] == "1":
                db_update_day(user_id=user_id, day=text)
                line_api.reply_message(e.reply_token, select_parent_practice_template())
                db_update_context(user_id=user_id, context="2")

            # 練習メニュー選択処理
            elif user["context"] == "2":
                if text == "1":
                    child_practice_name_list = db_get_practice_name_list_by_practice_id(
                        practice_id=text
                    )
                    print(child_practice_name_list)
                    line_api.reply_message(
                        e.reply_token,
                        select_child_practice_template(
                            child_practice_name_list=child_practice_name_list
                        ),
                    )
                    db_update_context(user_id=user_id, context="3")
                elif text == "2":
                    child_practice_name_list = db_get_practice_name_list_by_practice_id(
                        practice_id=text
                    )
                    line_api.reply_message(
                        e.reply_token,
                        select_child_practice_template(
                            child_practice_name_list=child_practice_name_list
                        ),
                    )
                    db_update_context(user_id=user_id, context="3")
                elif text == "3":
                    child_practice_name_list = db_get_practice_name_list_by_practice_id(
                        practice_id=text
                    )
                    line_api.reply_message(
                        e.reply_token,
                        select_child_practice_template(
                            child_practice_name_list=child_practice_name_list
                        ),
                    )
                    db_update_context(user_id=user_id, context="3")
                elif text == "4":
                    child_practice_name_list = db_get_practice_name_list_by_practice_id(
                        practice_id=text
                    )
                    line_api.reply_message(
                        e.reply_token,
                        select_child_practice_template(
                            child_practice_name_list=child_practice_name_list
                        ),
                    )
                    db_update_context(user_id=user_id, context="3")
                elif text == "5":
                    child_practice_name_list = db_get_practice_name_list_by_practice_id(
                        practice_id=text
                    )
                    line_api.reply_message(
                        e.reply_token,
                        select_child_practice_template(
                            child_practice_name_list=child_practice_name_list
                        ),
                    )
                    db_update_context(user_id=user_id, context="3")

            # 最終確認・通知処理
            elif user["context"] == "5":
                message = start_button_template()
                if text == "はい":
                    line_api.reply_message(
                        e.reply_token, TextMessage(text="お疲れ様！\n全体ラインに通知しておいたよ！")
                    )
                    line_api.push_message(user_id, message)
                    db_reset_status(user_id)
                elif text == "いいえ":
                    line_api.reply_message(
                        e.reply_token, TextMessage(text="最初からやり直してね")
                    )
                    line_api.push_message(user_id, message)
                    db_reset_status(user_id)
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
