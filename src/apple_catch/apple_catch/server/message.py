from dataclasses import dataclass
from datetime import datetime
from typing import Any

stored_format = "%Y-%m-%d %H:%M:%S.%f"

@dataclass
class Message:
    sender: str
    content: str
    timestamp: datetime

    @classmethod
    def failure(cls, sender: str):
        return cls(
            sender=sender,
            content="Failed to recieve message",
            timestamp = datetime.now()
        )


    @classmethod
    def with_timestamp(cls, sender: str, content: str):
        return cls(
            sender=sender,
            content=content,
            timestamp = datetime.now()
        )

    def to_dict(self) -> dict[str, str]:
        return {
            "sender": self.sender,
            "content": self.content,
            "timestamp": self.timestamp.strftime(stored_format)
        }

    @classmethod
    def from_dict(cls, obj: dict[str, Any]):
        return cls(
            sender=obj["sender"],
            content=obj["content"],
            timestamp=datetime.strptime(obj["timestamp"], stored_format)
        )

    def __str__(self) -> str:
        return f"{self.sender}: {self.content}"
    