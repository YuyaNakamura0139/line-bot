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
    db_add_menu_name,
    db_add_menu_time,
    db_add_last_sentence,
    db_add_url,
)

from db.db_practice_menu import (
    db_get_practice_menu_by_practice_period,
    db_get_url_by_practice_name,
)

from button_template import (
    start_button_template,
    select_day_template,
    final_check_button,
    practice_check_button,
    select_practice_template,
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
            user = await db_register(user_id)

            practice_name_list_period_1 = await db_get_practice_menu_by_practice_period(
                "1"
            )
            practice_name_list_period_2 = await db_get_practice_menu_by_practice_period(
                "2"
            )
            practice_name_list_period_3 = await db_get_practice_menu_by_practice_period(
                "3"
            )
            practice_name_list_period_4 = await db_get_practice_menu_by_practice_period(
                "4"
            )
            practice_name_list_period_5 = await db_get_practice_menu_by_practice_period(
                "5"
            )

            # キャンセル処理
            if user["context"] != "0" and text == "キャンセル":
                message = start_button_template()
                line_api.reply_message(e.reply_token, message)
                await db_reset_status(user_id)

            # スタート処理
            elif user["context"] == "0":
                if text == "スタート":
                    message = select_day_template()
                    line_api.reply_message(e.reply_token, message)
                    await db_update_context(user_id=user_id, context="1")
                else:
                    message = start_button_template()
                    await line_api.reply_message(e.reply_token, message)

            # 練習予定日の選択
            elif user["context"] == "1":
                await db_update_day(user_id=user_id, day=text)
                line_api.reply_message(
                    e.reply_token, TextMessage(text="次は練習メニューを選択していくよ！\nまずはアップメニューから！")
                )
                await db_update_context(user_id=user_id, context="2")
                message = select_practice_template(practice_name_list_period_1)
                line_api.push_message(user_id, message)

            # 第1ピリオド
            elif user["context"] == "2":
                await db_add_menu_name(user_id, text)
                line_api.reply_message(
                    e.reply_token, TextMessage(text="練習時間を入力してね！\n例)15分2セット→(15分×2)")
                )
                await db_update_context(user_id=user_id, context="3")

            elif user["context"] == "3":
                await db_add_menu_time(user_id, text)
                message = practice_check_button()
                line_api.reply_message(e.reply_token, message)
                await db_update_context(user_id=user_id, context="4")

            elif user["context"] == "4":
                if text == "はい":
                    await db_update_context(user_id=user_id, context="2")
                    line_api.push_message(user_id, TextMessage(text="追加のメニューを選んでね！"))
                    message = select_practice_template(practice_name_list_period_1)
                    line_api.reply_message(e.reply_token, message)
                elif text == "いいえ":
                    line_api.reply_message(
                        e.reply_token, TextMessage(text="次にシュート練習のメニューを選んでね！")
                    )
                    message = select_practice_template(practice_name_list_period_2)
                    line_api.push_message(user_id, message)
                    await db_update_context(user_id=user_id, context="5")

            # 第2ピリオド
            elif user["context"] == "5":
                await db_add_menu_name(user_id, text)
                line_api.reply_message(
                    e.reply_token, TextMessage(text="練習時間を入力してね！\n例)15分2セット→(15分×2)")
                )
                await db_update_context(user_id=user_id, context="6")

            elif user["context"] == "6":
                await db_add_menu_time(user_id, text)
                message = practice_check_button()
                line_api.reply_message(e.reply_token, message)
                await db_update_context(user_id=user_id, context="7")

            elif user["context"] == "7":
                if text == "はい":
                    await db_update_context(user_id=user_id, context="5")
                    line_api.push_message(user_id, TextMessage(text="追加のメニューを選んでね！"))
                    message = select_practice_template(practice_name_list_period_2)
                    line_api.reply_message(e.reply_token, message)
                elif text == "いいえ":
                    line_api.reply_message(
                        e.reply_token, TextMessage(text="次にトランジッションの練習メニューを選んでね！")
                    )
                    message = select_practice_template(practice_name_list_period_3)
                    line_api.push_message(user_id, message)
                    await db_update_context(user_id=user_id, context="8")

            # 第3ピリオド
            elif user["context"] == "8":
                await db_add_menu_name(user_id, text)
                line_api.reply_message(
                    e.reply_token, TextMessage(text="練習時間を入力してね！\n例)15分2セット→(15分×2)")
                )
                await db_update_context(user_id=user_id, context="9")

            elif user["context"] == "9":
                await db_add_menu_time(user_id, text)
                message = practice_check_button()
                line_api.reply_message(e.reply_token, message)
                await db_update_context(user_id=user_id, context="10")

            elif user["context"] == "10":
                if text == "はい":
                    await db_update_context(user_id=user_id, context="8")
                    line_api.push_message(user_id, TextMessage(text="追加のメニューを選んでね！"))
                    message = select_practice_template(practice_name_list_period_3)
                    line_api.reply_message(e.reply_token, message)
                elif text == "いいえ":
                    line_api.reply_message(
                        e.reply_token, TextMessage(text="次に定位置攻撃・守備の練習メニューを選んでね！")
                    )
                    message = select_practice_template(practice_name_list_period_4)
                    line_api.push_message(user_id, message)
                    await db_update_context(user_id=user_id, context="11")

            # 第4ピリオド
            elif user["context"] == "11":
                await db_add_menu_name(user_id, text)
                line_api.reply_message(
                    e.reply_token, TextMessage(text="練習時間を入力してね！\n例)15分2セット→(15分×2)")
                )
                await db_update_context(user_id=user_id, context="12")

            elif user["context"] == "12":
                await db_add_menu_time(user_id, text)
                message = practice_check_button()
                line_api.reply_message(e.reply_token, message)
                await db_update_context(user_id=user_id, context="13")

            elif user["context"] == "13":
                if text == "はい":
                    await db_update_context(user_id=user_id, context="11")
                    line_api.push_message(user_id, TextMessage(text="追加のメニューを選んでね！"))
                    message = select_practice_template(practice_name_list_period_4)
                    line_api.reply_message(e.reply_token, message)
                elif text == "いいえ":
                    line_api.reply_message(
                        e.reply_token, TextMessage(text="次にセットプレーの練習メニューを選んでね！")
                    )
                    message = select_practice_template(practice_name_list_period_5)
                    line_api.push_message(user_id, message)
                    await db_update_context(user_id=user_id, context="14")

            # 第5ピリオド
            elif user["context"] == "14":
                await db_add_menu_name(user_id, text)
                line_api.reply_message(
                    e.reply_token, TextMessage(text="練習時間を入力してね！\n例)15分2セット→(15分×2)")
                )
                await db_update_context(user_id=user_id, context="15")

            elif user["context"] == "15":
                await db_add_menu_time(user_id, text)
                message = practice_check_button()
                line_api.reply_message(e.reply_token, message)
                await db_update_context(user_id=user_id, context="16")

            elif user["context"] == "16":
                if text == "はい":
                    await db_update_context(user_id=user_id, context="14")
                    line_api.push_message(user_id, TextMessage(text="追加のメニューを選んでね！"))
                    message = select_practice_template(practice_name_list_period_5)
                    line_api.reply_message(e.reply_token, message)
                elif text == "いいえ":
                    line_api.reply_message(
                        e.reply_token,
                        TextMessage(text="次にゲーム時間を入力してね！\n例)(30分×2, 20分×1)"),
                    )
                    await db_update_context(user_id=user_id, context="18")
                    await db_add_menu_name(user_id, "ゲーム")

            elif user["context"] == "18":
                menu_time_list = user["menu_time"]
                menu_time_list.append(text)
                await db_add_menu_time(user_id, text)
                line_api.reply_message(
                    e.reply_token, TextMessage(text="最後に、次の練習で意識すること、目的など、自由に記入してください。")
                )
                await db_update_context(user_id=user_id, context="19")

            elif user["context"] == "19":
                await db_add_last_sentence(user_id, text)
                message = final_check_button(
                    user["day"], user["menu_name"], user["menu_time"]
                )
                line_api.reply_message(e.reply_token, message)
                await db_update_context(user_id=user_id, context="20")

            elif user["context"] == "20":
                message = start_button_template()
                if text == "はい":
                    # message = practice_info_template(
                    #     user["menu_name"][:-1], user["url"]
                    # )
                    # line_api.push_message(user_id, message)
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
