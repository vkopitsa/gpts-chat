from pydantic import BaseModel
from datetime import datetime
import json


class Room(BaseModel):
    name: str
    instruction: str = ""
    date: datetime | None = None


class Message(BaseModel):
    nickname: str = "Anon"
    text: str
    instruction: str = ""


class ListMessage(BaseModel):
    nickname: str = ""
    text: str = ""
    instruction: str = ""
    date: datetime | None = None

    def from_msg(self, msg: Message) -> None:
        self.nickname = msg.nickname
        self.text = msg.text
        self.instruction = msg.instruction
        self.date = datetime.now()

    def to_json(self) -> str:
        return json.dumps({
            "nickname": self.nickname,
            "text": self.text,
            "instruction": self.instruction,
            "date": self.date.isoformat() if self.date else "",
        })

    @staticmethod
    def from_json(s: str) -> 'ListMessage':
        data = json.loads(s)
        return ListMessage(
            nickname=data["nickname"],
            text=data["text"],
            date=datetime.fromisoformat(data["date"]),
            instruction=data["instruction"] if "instruction" in data else "",
        )
