"""
core/history.py

Conversation History Manager
for WASKO Health AI

Author:
Ahmad Muhammad
"""

import json
import uuid
from datetime import datetime
from pathlib import Path

from config import HISTORY_DIR


class HistoryManager:

    def __init__(self):

        self.history_dir = Path(HISTORY_DIR)
        self.history_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    # ----------------------------------------------------
    # Create New Session
    # ----------------------------------------------------

    def create_session(self):

        session_id = str(uuid.uuid4())

        data = {

            "session_id": session_id,

            "created_at":
                datetime.now().isoformat(),

            "updated_at":
                datetime.now().isoformat(),

            "messages": []

        }

        self.save(session_id, data)

        return session_id

    # ----------------------------------------------------
    # Save Session
    # ----------------------------------------------------

    def save(
        self,
        session_id,
        data
    ):

        data["updated_at"] = datetime.now().isoformat()

        file = self.history_dir / f"{session_id}.json"

        with open(
            file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )

    # ----------------------------------------------------
    # Load Session
    # ----------------------------------------------------

    def load(
        self,
        session_id
    ):

        file = self.history_dir / f"{session_id}.json"

        if not file.exists():

            return None

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    # ----------------------------------------------------
    # Add Message
    # ----------------------------------------------------

    def add_message(
        self,
        session_id,
        role,
        content
    ):

        history = self.load(session_id)

        if history is None:

            return

        history["messages"].append({

            "role": role,

            "content": content,

            "timestamp":
                datetime.now().isoformat()

        })

        self.save(
            session_id,
            history
        )

    # ----------------------------------------------------
    # Delete Session
    # ----------------------------------------------------

    def delete(
        self,
        session_id
    ):

        file = self.history_dir / f"{session_id}.json"

        if file.exists():

            file.unlink()

    # ----------------------------------------------------
    # List Sessions
    # ----------------------------------------------------

    def list_sessions(self):

        sessions = []

        for file in sorted(
            self.history_dir.glob("*.json"),
            reverse=True
        ):

            try:

                with open(
                    file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    data = json.load(f)

                sessions.append({

                    "session_id":
                        data["session_id"],

                    "created_at":
                        data["created_at"],

                    "updated_at":
                        data["updated_at"],

                    "messages":
                        len(data["messages"])

                })

            except Exception:

                continue

        return sessions

    # ----------------------------------------------------
    # Clear All History
    # ----------------------------------------------------

    def clear_all(self):

        for file in self.history_dir.glob("*.json"):

            file.unlink()


# Singleton
history_manager = HistoryManager()
