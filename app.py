"""
app.py

WASKO Health AI
Offline English & Hausa Medical Assistant
"""

from core.conversation import Conversation


def main():
    app = Conversation()
    app.run()


if __name__ == "__main__":
    main()