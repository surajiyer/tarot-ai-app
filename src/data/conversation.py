from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Optional

from data.utils import db_connection, get_new_uuid


@dataclass
class Conversation:
    title: str
    messages: list[dict] = field(default_factory=list)
    id: str = field(default_factory=get_new_uuid)

    @classmethod
    @db_connection
    def new(cls, title: Optional[str] = None, conn=None) -> "Conversation":
        c = conn.cursor()
        if title is None:
            title = "Untitled Conversation"
        conversation = cls(title=title)
        now = datetime.now(UTC)
        c.execute(
            "INSERT INTO conversations (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (conversation.id, title, now, now),
        )
        return conversation

    @db_connection
    def update(self, title: Optional[str] = None, conn=None):
        c = conn.cursor()
        if title is not None:
            self.title = title
        now = datetime.now(UTC)
        c.execute(
            "UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?",
            (self.title, now, self.id),
        )

    @db_connection
    def add_message(self, role: str, content: str, conn=None):
        c = conn.cursor()
        now = datetime.now(UTC)
        c.execute(
            "INSERT INTO messages (conversation_id, role, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (self.id, role, content, now, now),
        )
        self.messages.append({"role": role, "content": content})

    @db_connection
    def get_messages(self, conn=None) -> list[dict]:
        c = conn.cursor()
        c.execute("SELECT role, content FROM messages WHERE conversation_id = ?", (self.id,))
        rows = c.fetchall()
        for row in rows:
            self.messages.append({"role": row[0], "content": row[1]})

    @classmethod
    @db_connection
    def get_all(cls, conn=None) -> list["Conversation"]:
        c = conn.cursor()
        c.execute("SELECT id, title FROM conversations")
        rows = c.fetchall()
        c.close()
        conversations = []
        for row in rows:
            conversation = cls(
                id=row[0],
                title=row[1],
            )
            conversations.append(conversation)
        return conversations
