from linebot.models import TextMessage


def notification_template(day, time, practice_name_list, practice_time_list):
    """通知内容のテンプレート"""

    practice_name_and_practice_time = ""
    for practice_name, practice_time in zip(practice_name_list, practice_time_list):
        practice_name_and_practice_time += f"・{practice_name}({practice_time})\n"

    template_message = TextMessage(
        text=f"練習予定日: {day}\n練習時間帯: {time}\n練習メニュー:\n{practice_name_and_practice_time}"
    )

    return template_message


def first_statement():
    first_statement = TextMessage(
        text="メニューを開いてね！\nスタートを押すと質問が開始します。\nキャンセルを押すといつでもやり直せるよ！"
    )

    return first_statement
