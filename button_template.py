import datetime
import calendar

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

    weekday_dic = {
        "Sunday": "日",
        "Monday": "月",
        "Tuesday": "火",
        "Wednesday": "水",
        "Thursday": "木",
        "Friday": "金",
        "Saturday": "土",
    }

    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days=1)
    day_after_tomorrow = today + datetime.timedelta(days=2)
    two_days_after_tomorrow = today + datetime.timedelta(days=3)

    today = (
        today.strftime("%Y年%m月%d日")
        + "("
        + weekday_dic[calendar.day_name[today.weekday()]]
        + ")"
    )
    tomorrow = (
        tomorrow.strftime("%Y年%m月%d日")
        + "("
        + weekday_dic[calendar.day_name[tomorrow.weekday()]]
        + ")"
    )
    day_after_tomorrow = (
        day_after_tomorrow.strftime("%Y年%m月%d日")
        + "("
        + weekday_dic[calendar.day_name[day_after_tomorrow.weekday()]]
        + ")"
    )
    two_days_after_tomorrow = (
        two_days_after_tomorrow.strftime("%Y年%m月%d日")
        + "("
        + weekday_dic[calendar.day_name[two_days_after_tomorrow.weekday()]]
        + ")"
    )

    return [today, tomorrow, day_after_tomorrow, two_days_after_tomorrow]


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


def final_check_button(day, time, practice_name_list, practice_time_list):
    """最終確認ボタン"""

    practice_name_and_practice_time = ""
    for practice_name, practice_time in zip(practice_name_list, practice_time_list):
        practice_name_and_practice_time += f"・{practice_name}({practice_time})\n"

    confirm_template_message = TemplateSendMessage(
        alt_text="Confirm template",
        template=ConfirmTemplate(
            text=f"これで通知しても良いかな？\n練習予定日: {day}\n練習時間帯: {time}\n練習メニュー:\n{practice_name_and_practice_time}",
            actions=[
                MessageAction(label="はい", text="はい"),
                MessageAction(label="いいえ", text="いいえ"),
            ],
        ),
    )

    return confirm_template_message


def select_parent_practice_template():
    """親メニューの選択テンプレート"""

    parent_practice_name_list = [
        "アップTR",
        "シュートTR",
        "トランジッションTR",
        "定位置攻撃・守備TR",
        "セットプレーTR",
    ]
    columns_list = []
    for parent_practice_name in parent_practice_name_list:
        columns_list.append(
            CarouselColumn(
                title=f"{parent_practice_name}",
                text="下のボタンを押すと練習メニュー一覧が表示されます。",
                actions=[
                    MessageAction(label="練習の一覧を表示", text=f"{parent_practice_name}")
                ],
            )
        )

    carousel_template_message = TemplateSendMessage(
        alt_text="Carousel template",
        template=CarouselTemplate(columns=columns_list),
    )
    return carousel_template_message


def select_child_practice_template(child_practice_name_list):
    """子メニューの選択テンプレート"""

    columns_list = []
    for child_practice_name in child_practice_name_list:
        columns_list.append(
            CarouselColumn(
                title=f"{child_practice_name}",
                text="「追加」を押すと練習予定リストに追加されます。",
                actions=[MessageAction(label="追加", text=f"{child_practice_name}")],
            )
        )

    carousel_template_message = TemplateSendMessage(
        alt_text="Carousel template",
        template=CarouselTemplate(columns=columns_list),
    )
    return carousel_template_message


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


def practice_info_template(practice_name_list, url_list):
    """練習メニューとドキュメントの通知用テンプレート"""

    columns_list = []
    for menu, url in zip(practice_name_list, url_list):
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
