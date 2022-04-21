import datetime
import calendar

from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageAction,
)


def get_last_4_days():
    """
    今日から直近4間の年月日(曜)をリストで返す
    フォーマット:YYYY年mm月dd日(a)
    """

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
    """
    日程選択ボタンテンプレート
    """

    today, tomorrow, day_after_tomorrow, two_days_after_tomorrow = get_last_4_days()
    buttons_template_message = TemplateSendMessage(
        alt_text="select day",
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
