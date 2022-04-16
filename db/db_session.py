from decouple import config
from pymongo import MongoClient


MONGO_API_KEY = config("MONGO_API_KEY")
client = MongoClient(MONGO_API_KEY)
database = client.LINE_BOT
collection_user = database.user


def db_register(user_id: str) -> dict:
    """ユーザーのセッション登録・取得"""
    overlap_user = collection_user.find_one({"user_id": user_id})
    if overlap_user:
        return overlap_user
    user = collection_user.insert_one(
        {
            "user_id": user_id,
            "context": "0",
            "day": "",
            "menu_name": "",
            "menu_time": "",
            "last_sentence": "",
            "url": [],
        }
    )
    new_user = collection_user.find_one({"_id": user.inserted_id})
    return new_user


def db_update_context(user_id: str, context: str) -> None:
    """contextのアップデート"""
    user = collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one({"user_id": user_id}, {"$set": {"context": context}})


def db_update_day(user_id: str, day: str) -> None:
    """dayのアップデート"""
    user = collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one({"user_id": user_id}, {"$set": {"day": day}})


def db_add_menu_name(user_id: str, menu: str) -> None:
    """menu_nameへの追加"""
    user = collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one({"user_id": user_id}, {"$push": {"menu_name": menu}})


def db_add_menu_time(user_id: str, menu_time: str) -> None:
    """menu_timeへの追加"""
    user = collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one(
            {"user_id": user_id}, {"$push": {"menu_time": menu_time}}
        )


def db_update_last_sentence(user_id: str, last_sentence: str) -> None:
    """last_sentenceの更新"""
    user = collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one(
            {"user_id": user_id}, {"$set": {"last_sentence": last_sentence}}
        )


def db_add_url(user_id: str, url: str) -> None:
    """urlの追加"""
    user = collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one({"user_id": user_id}, {"$push": {"url": url}})


def db_reset_status(user_id: str) -> None:
    """ユーザーのstatusの初期化"""
    user = collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.delete_one({"user_id": user_id})
