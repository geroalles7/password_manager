from dataclasses import dataclass, asdict
from typing import Optional
import uuid


@dataclass
class User:
    username: str
    password_hash: str
    role: str = "user"

    def to_dict(self):
        return asdict(self)


@dataclass
class PasswordEntry:
    site: str
    username: str
    password: str
    notes: Optional[str] = ""
    entry_id: str = ""

    def __post_init__(self):
        if not self.entry_id:
            self.entry_id = str(uuid.uuid4())

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data: dict):
        return PasswordEntry(
            site=data["site"],
            username=data["username"],
            password=data["password"],
            notes=data.get("notes", ""),
            entry_id=data.get("entry_id", "")
        )