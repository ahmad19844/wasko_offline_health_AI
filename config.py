"""
config.py

WASKO Health AI
Configuration
"""

from pathlib import Path

# ==========================================================
# PROJECT PATH
# ==========================================================

# config.py is already in the project root

BASE_DIR = Path(__file__).resolve().parent

# ==========================================================
# KNOWLEDGE BASE
# ==========================================================

KNOWLEDGE_DIR = BASE_DIR / "knowledge_base"

KB_EN = KNOWLEDGE_DIR / "english"

KB_HA = KNOWLEDGE_DIR / "hausa"

# ==========================================================
# MODEL
# ==========================================================

MODEL_DIR = BASE_DIR / "models"

MODEL_NAME = "TinyLlama GGUF"

MODEL_FILE = "tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"

MODEL_PATH = MODEL_DIR / MODEL_FILE

# ==========================================================
# APP
# ==========================================================

APP_NAME = "WASKO Health AI"

VERSION = "2.0"

OFFLINE_MODE = True

DEFAULT_LANGUAGE = "Auto"

SUPPORTED_LANGUAGES = [

    "Auto",

    "English",

    "Hausa"

]

# ==========================================================
# RETRIEVAL
# ==========================================================

TOP_K = 1

MIN_SCORE = 1

MAX_CONTEXT_CHARS = 2024

# ==========================================================
# LLM
# ==========================================================

MAX_NEW_TOKENS = 180

MAX_CONTEXT_CHARS = 1200

TEMPERATURE = 0.3

TOP_P = 0.9

REPEAT_PENALTY = 1.15

CONTEXT_WINDOW = 2048

# ==========================================================
# FILE TYPES
# ==========================================================

SUPPORTED_EXTENSIONS = [".md"]

# ==========================================================
# EMERGENCY
# ==========================================================

EMERGENCY_KEYWORDS = {

    "cannot breathe",

    "difficulty breathing",

    "stroke",

    "heart attack",

    "chest pain",

    "seizure",

    "unconscious",

    "severe bleeding",

    "ba ya numfashi",

    "wahalar numfashi",

    "bugun zuciya",

    "ciwon kirji",

    "ya suma",

    "farfadiya",

    "jini mai yawa"

}

# ==========================================================
# VERIFY
# ==========================================================

def verify():

    print("\n========== WASKO CONFIG ==========")

    print("BASE_DIR :", BASE_DIR)

    print("English  :", KB_EN)

    print("Hausa    :", KB_HA)

    print("Model    :", MODEL_PATH)

    print("==================================")

    print("English Exists :", KB_EN.exists())

    print("Hausa Exists   :", KB_HA.exists())

    print("Model Exists   :", MODEL_PATH.exists())


if __name__ == "__main__":

    verify()
