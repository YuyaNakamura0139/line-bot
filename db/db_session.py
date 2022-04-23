from pymongo import MongoClient

from config import MONGO_API_KEY

client = MongoClient(MONGO_API_KEY)
database = client.LINE_BOT
collection_user = database.user


def db_register(user_id: str) -> dict:
    """
    ユーザー情報の登録・取得
    """
    overlap_user = collection_user.find_one({"user_id": user_id})
    if overlap_user:
        return overlap_user
    user = collection_user.insert_one(
        {
            "user_id": user_id,
            "context": "0",
            "day": "",
            "time": "",
            "practice_name": [],
            "practice_time": [],
            "last_sentence": "",
            "url": [],
        }
    )
    new_user = collection_user.find_one({"_id": user.inserted_id})
    return new_user


def db_update_context(user_id: str, context: str) -> None:
    """
    contextのアップデート
    """

    user = collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one({"user_id": user_id}, {"$set": {"context": context}})


def db_update_day(user_id: str, day: str) -> None:
    """
    dayのアップデート
    """
    user = collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one({"user_id": user_id}, {"$set": {"day": day}})


def db_update_time(user_id: str, time: str) -> None:
    """
    timeのアップデート
    """
    user = collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one({"user_id": user_id}, {"$set": {"time": time}})


def db_add_practice_name(user_id: str, practice_name: str) -> None:
    """
    practice_nameへの追加
    """
    user = collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one(
            {"user_id": user_id}, {"$push": {"practice_name": practice_name}}
        )


def db_add_practice_time(user_id: str, practice_time: str) -> None:
    """
    practice_timeへの追加
    """

    user = collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one(
            {"user_id": user_id}, {"$push": {"practice_time": practice_time}}
        )


def db_update_last_sentence(user_id: str, last_sentence: str) -> None:
    """
    last_sentenceの更新
    """
    user = collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one(
            {"user_id": user_id}, {"$set": {"last_sentence": last_sentence}}
        )


def db_add_url(user_id: str, url: str) -> None:
    """
    urlの追加
    """
    user = collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.update_one({"user_id": user_id}, {"$push": {"url": url}})


def db_reset_status(user_id: str) -> None:
    """
    ユーザーのstatusの初期化
    """
    user = collection_user.find_one({"user_id": user_id})
    if user:
        collection_user.delete_one({"user_id": user_id})
