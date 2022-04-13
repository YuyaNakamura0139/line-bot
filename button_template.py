import datetime
import locale

from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    ConfirmTemplate,
    CarouselTemplate,
    CarouselColumn,
    MessageAction,
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


def final_check_button(day, menu):
    """最終確認ボタン"""

    confirm_template_message = TemplateSendMessage(
        alt_text="Confirm template",
        template=ConfirmTemplate(
            text="以下の内容で通知しても良いかな？\n\n練習予定日: {}\n練習メニュー:\n{}".format(day, menu),
            actions=[
                MessageAction(label="はい", text="はい"),
                MessageAction(label="いいえ", text="いいえ"),
            ],
        ),
    )

    return confirm_template_message


def select_practice_template():
    carousel_template_message = TemplateSendMessage(
        alt_text="Carousel template",
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    title="this is menu1",
                    text="description1",
                    actions=[MessageAction(label="message1", text="message text1")],
                ),
                CarouselColumn(
                    title="this is menu2",
                    text="description2",
                    actions=[MessageAction(label="message2", text="message text2")],
                ),
                CarouselColumn(
                    title="this is menu1",
                    text="description1",
                    actions=[MessageAction(label="message1", text="message text1")],
                ),
                CarouselColumn(
                    title="this is menu2",
                    text="description2",
                    actions=[MessageAction(label="message2", text="message text2")],
                ),
                CarouselColumn(
                    title="this is menu1",
                    text="description1",
                    actions=[MessageAction(label="message1", text="message text1")],
                ),
                CarouselColumn(
                    title="this is menu2",
                    text="description2",
                    actions=[MessageAction(label="message2", text="message text2")],
                ),
                CarouselColumn(
                    title="this is menu1",
                    text="description1",
                    actions=[MessageAction(label="message1", text="message text1")],
                ),
                CarouselColumn(
                    title="this is menu2",
                    text="description2",
                    actions=[MessageAction(label="message2", text="message text2")],
                ),
                CarouselColumn(
                    title="this is menu1",
                    text="description1",
                    actions=[MessageAction(label="message1", text="message text1")],
                ),
                CarouselColumn(
                    title="this is menu2",
                    text="description2",
                    actions=[MessageAction(label="message2", text="message text2")],
                ),
            ]
        ),
    )
    return carousel_template_message