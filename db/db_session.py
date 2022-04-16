from decouple import config
import motor.motor_asyncio


MONGO_API_KEY = config("MONGO_API_KEY")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)
database = client.LINE_BOT
collection_user = database.user


async def db_register(user_id: str) -> dict:
    """ユーザーのセッション登録・取得"""

    overlap_user = await collection_user.find_one({"user_id": user_id})
    if overlap_user:
        return overlap_user
    user = await collection_user.insert_one(
        {
            "user_id": user_id,
            "context": "0",
            "day": "",
            "menu_name": [],
            "menu_time": [],
            "last_sentence": "",
            "url": [],
        }
    )
    new_user = await collection_user.find_one({"_id": user.inserted_id})
    return new_user


async def db_update_context(user_id: str, context: str) -> None:
    """contextのアップデート"""

    user = await collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one({"user_id": user_id}, {"$set": {"context": context}})


async def db_update_day(user_id: str, day: str) -> None:
    """dayのアップデート"""

    user = await collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one({"user_id": user_id}, {"$set": {"day": day}})


async def db_add_menu_name(user_id: str, menu_name: str) -> None:
    """menu_nameの追加"""

    user = await collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one(
            {"user_id": user_id}, {"$push": {"menu_name": menu_name}}
        )


async def db_add_menu_time(user_id: str, menu_time: str) -> None:
    """menu_timeの追加"""

    user = await collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one(
            {"user_id": user_id}, {"$push": {"menu_time": menu_time}}
        )


async def db_add_url(user_id: str, url: str) -> None:
    """urlの追加"""

    user = await collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one({"user_id": user_id}, {"$push": {"url": url}})


async def db_add_last_sentence(user_id: str, last_sentence: str) -> None:
    """last_sentenceの追加"""

    user = await collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one(
            {"user_id": user_id}, {"$set": {"last_sentence": last_sentence}}
        )


async def db_reset_status(user_id: str) -> None:
    """ユーザーのstatusの初期化"""

    user = await collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.delete_one({"user_id": user_id})
