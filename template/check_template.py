from linebot.models import TemplateSendMessage, ConfirmTemplate, MessageAction


def practice_check_button():
    """
    練習内容確認テンプレート
    """

    confirm_template_message = TemplateSendMessage(
        alt_text="pracitce check",
        template=ConfirmTemplate(
            text="練習メニューを追加しますか？",
            actions=[
                MessageAction(label="はい", text="はい"),
                MessageAction(label="いいえ", text="いいえ"),
            ],
        ),
    )

    return confirm_template_message


def final_check_button(day, time, practice_name_list, practice_time_list):
    """
    最終確認テンプレート
    """

    practice_name_and_practice_time = ""
    for practice_name, practice_time in zip(practice_name_list, practice_time_list):
        practice_name_and_practice_time += f"・{practice_name}({practice_time})\n"

    confirm_template_message = TemplateSendMessage(
        alt_text="final check",
        template=ConfirmTemplate(
            text=f"これで通知しても良いかな？\n練習予定日: {day}\n練習時間帯: {time}\n練習メニュー:\n{practice_name_and_practice_time}",
            actions=[
                MessageAction(label="はい", text="はい"),
                MessageAction(label="いいえ", text="いいえ"),
            ],
        ),
    )

    return confirm_template_message
