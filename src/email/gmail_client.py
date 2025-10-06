"""Gmail API client for fetching and managing emails."""

import base64
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
from typing import Optional

from src.auth.gmail_auth import get_gmail_service
from src.email.models import Email


def build_query(
    after: Optional[datetime] = None,
    before: Optional[datetime] = None,
    days: Optional[int] = None,
    unread_only: bool = True,
    labels: Optional[list[str]] = None,
) -> str:
    """Build Gmail API query string from filters.

    Args:
        after: Fetch emails after this date
        before: Fetch emails before this date
        days: Fetch emails from last N days (alternative to after/before)
        unread_only: Only fetch unread emails
        labels: Filter by Gmail labels (e.g., ['INBOX', 'IMPORTANT'])

    Returns:
        Gmail API query string

    Examples:
        >>> build_query(days=7, unread_only=True)
        'is:unread after:2025/09/29'

        >>> build_query(after=datetime(2025, 10, 1), labels=['INBOX'])
        'is:unread label:INBOX after:2025/10/01'
    """
    query_parts = []

    # Unread filter
    if unread_only:
        query_parts.append("is:unread")

    # Date filters
    if days:
        # Calculate date N days ago
        target_date = datetime.now() - timedelta(days=days)
        query_parts.append(f"after:{target_date.strftime('%Y/%m/%d')}")
    else:
        if after:
            query_parts.append(f"after:{after.strftime('%Y/%m/%d')}")
        if before:
            query_parts.append(f"before:{before.strftime('%Y/%m/%d')}")

    # Label filters
    if labels:
        for label in labels:
            query_parts.append(f"label:{label}")

    return " ".join(query_parts)


def parse_email_address(header: str) -> tuple[str, str]:
    """Parse email header into name and email address.

    Args:
        header: Email header string (e.g., "John Doe <john@example.com>")

    Returns:
        Tuple of (name, email_address)

    Examples:
        >>> parse_email_address("John Doe <john@example.com>")
        ('John Doe', 'john@example.com')

        >>> parse_email_address("jane@example.com")
        ('jane@example.com', 'jane@example.com')
    """
    if "<" in header and ">" in header:
        # Format: "Name <email@example.com>"
        name = header.split("<")[0].strip().strip('"')
        email = header.split("<")[1].split(">")[0].strip()
        return name, email
    else:
        # Just email address
        email = header.strip()
        return email, email


def get_header_value(headers: list[dict], name: str) -> str:
    """Extract header value by name from Gmail headers list.

    Args:
        headers: List of Gmail header dicts
        name: Header name to find (case-insensitive)

    Returns:
        Header value or empty string if not found
    """
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return ""


def get_email_body(payload: dict) -> str:
    """Extract email body from Gmail message payload.

    Args:
        payload: Gmail message payload

    Returns:
        Email body text (plain text preferred, HTML if no plain text)
    """
    body = ""

    # Check if payload has body data
    if "body" in payload and "data" in payload["body"]:
        body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
        return body

    # Check for multipart message
    if "parts" in payload:
        for part in payload["parts"]:
            mime_type = part.get("mimeType", "")

            # Prefer plain text
            if mime_type == "text/plain" and "data" in part.get("body", {}):
                body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
                return body

            # Fallback to HTML
            if mime_type == "text/html" and "data" in part.get("body", {}):
                body = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")

            # Recursively check nested parts
            if "parts" in part:
                nested_body = get_email_body(part)
                if nested_body:
                    return nested_body

    return body


def fetch_emails(
    after: Optional[datetime] = None,
    before: Optional[datetime] = None,
    days: Optional[int] = 7,
    unread_only: bool = True,
    labels: Optional[list[str]] = None,
    max_results: int = 100,
) -> list[Email]:
    """Fetch emails from Gmail based on filters.

    Args:
        after: Fetch emails after this date
        before: Fetch emails before this date
        days: Fetch emails from last N days (default: 7)
        unread_only: Only fetch unread emails (default: True)
        labels: Filter by Gmail labels
        max_results: Maximum number of emails to fetch (default: 100)

    Returns:
        List of Email objects

    Example:
        >>> # Fetch unread emails from last 7 days
        >>> emails = fetch_emails(days=7)
        >>> for email in emails:
        ...     print(f"{email.subject} from {email.sender}")
    """
    service = get_gmail_service()

    # Build query
    query = build_query(after=after, before=before, days=days, unread_only=unread_only, labels=labels)
    print(f"Gmail query: {query}")

    # Fetch message IDs
    results = service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()

    messages = results.get("messages", [])

    if not messages:
        print("No messages found matching the criteria.")
        return []

    print(f"Found {len(messages)} messages. Fetching details...")

    # Fetch full message details
    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"], format="full").execute()

        # Parse headers
        headers = msg_data["payload"]["headers"]
        subject = get_header_value(headers, "Subject")
        from_header = get_header_value(headers, "From")
        to_header = get_header_value(headers, "To")
        date_header = get_header_value(headers, "Date")

        # Parse sender info
        sender_name, sender_email = parse_email_address(from_header)

        # Parse date
        date = parsedate_to_datetime(date_header) if date_header else datetime.now()

        # Get body
        body = get_email_body(msg_data["payload"])

        # Create Email object
        email = Email(
            id=msg_data["id"],
            thread_id=msg_data["threadId"],
            subject=subject or "(No subject)",
            sender=sender_name,
            sender_email=sender_email,
            recipient=to_header,
            date=date,
            snippet=msg_data.get("snippet", ""),
            body=body,
            labels=msg_data.get("labelIds", []),
            is_unread="UNREAD" in msg_data.get("labelIds", []),
        )
        emails.append(email)

    return emails
