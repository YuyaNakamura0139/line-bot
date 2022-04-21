from linebot.models import (
    CarouselColumn,
    CarouselTemplate,
    MessageAction,
    URIAction,
    TemplateSendMessage,
)


def select_parent_practice_template():
    """
    親メニューの選択ボタンテンプレート
    """

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
    """
    子メニューの選択テンプレート
    """

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


def practice_info_template(practice_name_list, url_list):
    """
    練習メニューとドキュメントの通知用テンプレート
    """

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
