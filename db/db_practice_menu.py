from decouple import config
import motor.motor_asyncio
from typing import Union, List
from bson import ObjectId

MONGO_API_KEY = config("MONGO_API_KEY")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
database = client.LINE_BOT
collection_practice_menu = database.practice_menu


def practice_serializer(practice) -> dict:
    return {
        "id": str(practice["_id"]),
        "practice_period": practice["practice_period"],
        "practice_name": practice["practice_name"],
        "url": practice["url"],
    }


async def db_get_practice_menu(practice_name: str) -> dict:
    """練習メニュー情報の取得"""

    practice = await collection_practice_menu.find_one({"pracitce_name": practice_name})
    return practice_serializer(practice)


async def db_get_practice_menu_by_practice_period(practice_period: str) -> list:
    """ピリオドから練習メニューのリストを取得"""

    practice_name_list = []
    for practice in await collection_practice_menu.find(
        {"practice_period": practice_period}
    ).to_list(length=10):
        practice_name_list.append(practice["practice_name"])
    return practice_name_list


async def db_get_url_by_practice_name(practice_name: str) -> list:
    """practice_nameからurlを取得"""

    practice = await collection_practice_menu.find_one({"practice_name": practice_name})
    return practice["url"]


async def db_get_practice_menus() -> list:
    """練習メニューの一覧を取得"""

    practices = []
    for practice in await collection_practice_menu.find().to_list(length=100):
        practices.append(practice_serializer(practice))
    return practices


async def db_create_practice_menu(data: dict) -> Union[dict, bool]:
    """練習メニューの新規作成"""

    practice = await collection_practice_menu.insert_one(data)
    new_practice = await collection_practice_menu.find_one(
        {"_id": practice.inserted_id}
    )
    if new_practice:
        return practice_serializer(new_practice)
    return False


async def db_update_practice_menu(id: str, data: dict) -> Union[dict, bool]:
    """練習メニューの更新"""

    todo = await collection_practice_menu.find_one({"_id": ObjectId(id)})
    if todo:
        updated_todo = await collection_practice_menu.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_todo.modified_count > 0:
            new_todo = await collection_practice_menu.find_one({"_id": ObjectId(id)})
            return practice_serializer(new_todo)
    return False


async def db_delete_practice_menu(id: str) -> bool:
    """練習メニューの削除"""

    practice = await collection_practice_menu.find_one({"_id": ObjectId(id)})
    if practice:
        deleted_practice = await collection_practice_menu.delete_one(
            {"_id": ObjectId(id)}
        )
        if deleted_practice.deleted_count > 0:
            return True
        return False
