from typing import List, Awaitable
from app.redis import redis_client
from app.models import ListMessage, Message


class Messages:
    @staticmethod
    def save(chat: str, message: ListMessage) -> None:
        redis_client.lpush(chat, message.to_json())
        redis_client.ltrim(chat, 0, 99)

    @staticmethod
    async def retrieve(chat: str, limit: int = 50) -> List[ListMessage]:
        stored_messages = redis_client.lrange(chat, 0, limit - 1)

        if isinstance(stored_messages, Awaitable):
            stored_messages = await stored_messages

        items = [ListMessage.from_json(m) for m in stored_messages]
        items.sort(key=lambda x: x.date)  # type: ignore
        return items

    @staticmethod
    def clear(chat: str) -> None:
        redis_client.delete(chat)


class Chat:
    @staticmethod
    async def post_message(message: Message, chat: str) -> List[ListMessage]:
        msg = ListMessage()
        msg.from_msg(message)
        Messages.save(chat, msg)
        return await Messages.retrieve(chat)

    @staticmethod
    async def get_messages(chat: str) -> List[ListMessage]:
        return await Messages.retrieve(chat)

    @staticmethod
    async def clear_messages(chat: str) -> List[ListMessage]:
        Messages.clear(chat)
        return []
