"""Paths, constants, and environment helpers for the Content Publisher Agent."""

import os
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DRAFTS_DIR = ROOT_DIR / "drafts"
IMAGES_DIR = DRAFTS_DIR / "images"
PROMPTS_DIR = ROOT_DIR / "prompts"
TOPICS_FILE = DATA_DIR / "topics.json"

DEVTO_ARTICLES_URL = "https://dev.to/api/articles"
DEVTO_IMAGE_UPLOAD_URL = "https://dev.to/api/image_uploads"
DEVTO_DASHBOARD_URL = "https://dev.to/dashboard"
CATBOX_UPLOAD_URL = "https://catbox.moe/user/api.php"

DEFAULT_TEXT_MODEL = "gpt-5-mini"
DEFAULT_IMAGE_MODEL = "gpt-image-1"
IMAGE_MODEL_FALLBACKS = ["gpt-image-2", "gpt-image-1", "gpt-image-1-mini"]

STATUS_UNUSED = "unused"
STATUS_USED = "used"
STATUS_FAILED = "failed"


def get_required_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing {name}. Add it to your .env file.")
    return value


def images_enabled():
    return os.getenv("ENABLE_ARTICLE_IMAGES", "true").lower() == "true"


def today_string():
    return datetime.now().strftime("%Y-%m-%d")
