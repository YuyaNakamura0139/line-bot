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
    db_add_practice_name,
    db_add_practice_time,
    db_add_url,
)

from db.db_practice_menu import (
    db_get_practice_name_list_by_practice_period,
    db_get_url_by_practice_name,
)

from button_template import (
    start_button_template,
    select_day_template,
    final_check_button,
    select_parent_practice_template,
    select_child_practice_template,
    practice_check_button,
    practice_info_template,
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
                if not user["practice_name"]:
                    db_update_day(user_id=user_id, day=text)
                    line_api.push_message(
                        user_id, TextMessage(text="これから練習メニューを選んでいくよ！")
                    )
                elif text == "はい":
                    line_api.push_message(user_id, TextMessage(text="追加のメニューを選んでいくよ！"))
                elif text == "いいえ":
                    line_api.reply_message(
                        e.reply_token,
                        TextMessage(text="ゲーム時間を入力してね！\n例)(30分×2, 20分×1)"),
                    )
                    db_add_practice_name(user_id=user_id, practice_name="ゲーム")
                    db_update_context(user_id=user_id, context="5")
                    break
                line_api.reply_message(e.reply_token, select_parent_practice_template())
                db_update_context(user_id=user_id, context="2")

            # 親メニュー選択処理
            elif user["context"] == "2":
                if text == "アップTR":
                    practice_period = "1"
                elif text == "シュートTR":
                    practice_period = "2"
                elif text == "トランジッションTR":
                    practice_period = "3"
                elif text == "定位置攻撃・守備TR":
                    practice_period = "4"
                elif text == "セットプレーTR":
                    practice_period = "5"
                child_practice_name_list = db_get_practice_name_list_by_practice_period(
                    practice_period=practice_period
                )
                line_api.reply_message(
                    e.reply_token,
                    select_child_practice_template(
                        child_practice_name_list=child_practice_name_list
                    ),
                )
                db_update_context(user_id=user_id, context="3")

            # 子メニュー選択処理
            elif user["context"] == "3":
                db_add_practice_name(user_id=user_id, practice_name=text)
                db_add_url(user_id=user_id, url=db_get_url_by_practice_name(text))
                line_api.reply_message(
                    e.reply_token,
                    TextMessage(text=f"{text}の練習時間を入力してね！\n例)15分2セット→(15分×2)"),
                )
                db_update_context(user_id=user_id, context="4")

            # 練習時間入力処理
            elif user["context"] == "4":
                db_add_practice_time(user_id=user_id, practice_time=text)
                line_api.reply_message(e.reply_token, practice_check_button())
                db_update_context(user_id=user_id, context="1")

            elif user["context"] == "5":
                db_add_practice_time(user_id=user_id, practice_time=text)
                line_api.reply_message(
                    e.reply_token,
                    TextMessage(text="最後に、次の練習で意識することなど、メンバーに伝えたいことを自由に入力してください。"),
                )
                db_update_context(user_id=user_id, context="7")

            elif user["context"] == "7":
                db_update_last_sentence(user_id=user_id, last_sentence=text)
                line_api.reply_message(
                    e.reply_token,
                    final_check_button(
                        user["day"], user["practice_name"], user["practice_time"]
                    ),
                )
                db_update_context(user_id=user_id, context="8")

            # 最終確認・通知処理
            elif user["context"] == "8":
                if text == "はい":
                    line_api.push_message(
                        user_id,
                        practice_info_template(user["practice_name"][:-1], user["url"]),
                    )
                    line_api.reply_message(
                        e.reply_token, TextMessage(text="お疲れ様！\n全体ラインに通知しておいたよ！")
                    )
                    line_api.push_message(user_id, start_button_template())
                    db_reset_status(user_id)
                elif text == "いいえ":
                    line_api.reply_message(
                        e.reply_token, TextMessage(text="最初からやり直してね")
                    )
                    line_api.push_message(user_id, start_button_template())
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
