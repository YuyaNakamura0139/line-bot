import datetime
import locale

from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    ConfirmTemplate,
    CarouselTemplate,
    CarouselColumn,
    MessageAction,
    URIAction,
)


def get_last_4_days():
    locale.setlocale(locale.LC_TIME, "ja_JP.UTF-8")

    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days=1)
    day_after_tomorrow = today + datetime.timedelta(days=2)
    two_days_after_tomorrow = today + datetime.timedelta(days=3)

    return [
        today.strftime("%Y年%m月%d日(%a)"),
        tomorrow.strftime("%Y年%m月%d日(%a)"),
        day_after_tomorrow.strftime("%Y年%m月%d日(%a)"),
        two_days_after_tomorrow.strftime("%Y年%m月%d日(%a)"),
    ]


def start_button_template():
    """スタートボタン"""

    buttons_template_message = TemplateSendMessage(
        alt_text="Buttons Template",
        template=ButtonsTemplate(
            title="練習メニュー通知くん",
            text="スタートボタンを押してね!\n「キャンセル」と入力するといつでもやり直せるよ。",
            actions=[
                MessageAction(label="スタート", text="スタート"),
            ],
        ),
    )

    return buttons_template_message


def select_day_template():
    """日付選択ボタン"""

    today, tomorrow, day_after_tomorrow, two_days_after_tomorrow = get_last_4_days()
    buttons_template_message = TemplateSendMessage(
        alt_text="Buttons Template",
        template=ButtonsTemplate(
            title="練習予定日を選択してね!",
            text="以下から選択",
            actions=[
                MessageAction(label=today, text=today),
                MessageAction(label=tomorrow, text=tomorrow),
                MessageAction(label=day_after_tomorrow, text=day_after_tomorrow),
                MessageAction(
                    label=two_days_after_tomorrow, text=two_days_after_tomorrow
                ),
            ],
        ),
    )

    return buttons_template_message


def final_check_button(day, menu_list, time_list):
    """最終確認ボタン"""

    menu_and_time = ""
    for menu, time in zip(menu_list, time_list):
        menu_and_time += f"・{menu}({time})\n"

    confirm_template_message = TemplateSendMessage(
        alt_text="Confirm template",
        template=ConfirmTemplate(
            text=f"以下の内容で通知しても良いかな？\n練習予定日: {day}\n練習メニュー:\n{menu_and_time}",
            actions=[
                MessageAction(label="はい", text="はい"),
                MessageAction(label="いいえ", text="いいえ"),
            ],
        ),
    )

    return confirm_template_message


def practice_check_button():
    """練習内容確認ボタン"""

    confirm_template_message = TemplateSendMessage(
        alt_text="Confirm template",
        template=ConfirmTemplate(
            text="練習メニューを追加しますか？",
            actions=[
                MessageAction(label="はい", text="はい"),
                MessageAction(label="いいえ", text="いいえ"),
            ],
        ),
    )

    return confirm_template_message


def select_practice_template(menu_name_list):
    columns_list = []
    for menu in menu_name_list:
        columns_list.append(
            CarouselColumn(
                title=f"{menu}",
                text=f"{menu}",
                actions=[MessageAction(label="追加する", text=f"{menu}")],
            )
        )

    carousel_template_message = TemplateSendMessage(
        alt_text="Carousel template",
        template=CarouselTemplate(
            columns=columns_list,
        ),
    )
    return carousel_template_message


def practice_info_template(menu_name_list, url_list):
    columns_list = []
    for menu, url in zip(menu_name_list, url_list):
        columns_list.append(
            CarouselColumn(
                title=f"{menu}",
                text=f"{menu}",
                actions=[URIAction(label="ドキュメント", uri=f"{url}")],
            )
        )

    carousel_template_message = TemplateSendMessage(
        alt_text="Carousel template",
        template=CarouselTemplate(
            columns=columns_list,
        ),
    )
    return carousel_template_message
