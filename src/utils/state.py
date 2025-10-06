"""State management for tracking last run timestamps."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


STATE_FILE = ".last_run.json"


def get_last_run() -> Optional[datetime]:
    """Get the timestamp of the last run.

    Returns:
        datetime of last run, or None if never run before
    """
    if not os.path.exists(STATE_FILE):
        return None

    try:
        with open(STATE_FILE, "r") as f:
            data = json.load(f)
            timestamp = data.get("last_run")
            if timestamp:
                return datetime.fromtimestamp(timestamp)
    except (json.JSONDecodeError, KeyError, ValueError):
        return None

    return None


def save_last_run(timestamp: Optional[datetime] = None) -> None:
    """Save the last run timestamp.

    Args:
        timestamp: Timestamp to save (defaults to now)
    """
    if timestamp is None:
        timestamp = datetime.now()

    data = {"last_run": timestamp.timestamp(), "last_run_readable": timestamp.isoformat()}

    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✓ Saved last run: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")


def reset_last_run() -> None:
    """Reset the last run timestamp (delete state file)."""
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
        print(f"✓ Reset last run timestamp")
    else:
        print("No state file to reset")
