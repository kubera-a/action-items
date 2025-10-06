"""Email data models for structured email representation."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Email:
    """Represents a Gmail email message."""

    id: str
    thread_id: str
    subject: str
    sender: str
    sender_email: str
    recipient: str
    date: datetime
    snippet: str
    body: str
    labels: list[str]
    is_unread: bool

    def __str__(self) -> str:
        """Human-readable string representation."""
        return (
            f"From: {self.sender} <{self.sender_email}>\n"
            f"Date: {self.date.strftime('%Y-%m-%d %H:%M')}\n"
            f"Subject: {self.subject}\n"
            f"Preview: {self.snippet[:100]}..."
        )
