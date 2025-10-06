"""Email module for Gmail integration."""

from src.email.gmail_client import fetch_emails
from src.email.models import Email

__all__ = ["fetch_emails", "Email"]
