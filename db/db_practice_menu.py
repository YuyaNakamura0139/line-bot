from pymongo import MongoClient
from typing import Union
from bson import ObjectId

from config import MONGO_API_KEY

client = MongoClient(MONGO_API_KEY)
database = client.LINE_BOT
collection_practice_menu = database.practice_menu


def practice_serializer(practice) -> dict:
    return {
        "id": str(practice["_id"]),
        "practice_period": practice["practice_period"],
        "practice_name": practice["practice_name"],
        "url": practice["url"],
    }


def db_get_practice_name_list_by_practice_period(practice_period: str) -> list:
    """practice_periodに一致するpractice_nameの要素をリストで返す"""

    return [
        practice["practice_name"]
        for practice in collection_practice_menu.find(
            {"practice_period": practice_period}
        )
    ]


def db_get_url_by_practice_name(practice_name: str) -> str:
    """practice_nameからurlを取得"""

    practice = collection_practice_menu.find_one({"practice_name": practice_name})
    return practice["url"]


def db_get_practice_menu(practice_period: str) -> dict:
    """練習メニュー情報の取得"""

    practice = collection_practice_menu.find_one({"pracitce_id": practice_period})
    return practice


def db_get_practice_menus() -> list:
    """練習メニューの一覧を取得"""

    practices = []
    for practice in collection_practice_menu.find():
        practices.append(practice_serializer(practice))
    return practices


def db_create_practice_menu(data: dict) -> Union[dict, bool]:
    """練習メニューの新規作成"""

    practice = collection_practice_menu.insert_one(data)
    new_practice = collection_practice_menu.find_one({"_id": practice.inserted_id})
    if new_practice:
        return practice_serializer(new_practice)
    return False


def db_update_practice_menu(id: str, data: dict) -> Union[dict, bool]:
    """練習メニューの更新"""

    todo = collection_practice_menu.find_one({"_id": ObjectId(id)})
    if todo:
        updated_todo = collection_practice_menu.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_todo.modified_count > 0:
            new_todo = collection_practice_menu.find_one({"_id": ObjectId(id)})
            return practice_serializer(new_todo)
    return False


def db_delete_practice_menu(id: str) -> bool:
    """練習メニューの削除"""

    practice = collection_practice_menu.find_one({"_id": ObjectId(id)})
    if practice:
        deleted_practice = collection_practice_menu.delete_one({"_id": ObjectId(id)})
        if deleted_practice.deleted_count > 0:
            return True
        return False
