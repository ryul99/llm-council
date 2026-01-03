"""Configuration for the LLM Council."""

import os
import json
from dotenv import load_dotenv

load_dotenv()

def _parse_models_env(value: str | None, default: list[str]) -> list[str]:
    if not value:
        return default
    raw = value.strip()
    if not raw:
        return default
    return [x.strip() for x in raw.split(",") if x.strip()]


# Council members (LiteLLM model names). You can override via COUNCIL_MODELS env var
# (comma-separated or JSON list).
COUNCIL_MODELS = _parse_models_env(
    os.getenv("COUNCIL_MODELS"),
    default=[
        "gpt-5",
        "gpt-5-mini",
    ],
)

# Chairman model - synthesizes final response. Defaults to the first council model.
CHAIRMAN_MODEL = os.getenv("CHAIRMAN_MODEL", COUNCIL_MODELS[0] if COUNCIL_MODELS else "gpt-5")

# Title model - generates conversation titles. Defaults to the first council model.
TITLE_MODEL = os.getenv("TITLE_MODEL", COUNCIL_MODELS[0] if COUNCIL_MODELS else "gpt-5-mini")

# Data directory for conversation storage
DATA_DIR = "data/conversations"
