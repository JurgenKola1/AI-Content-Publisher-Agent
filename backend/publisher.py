"""Save drafts locally and publish to Dev.to."""

from datetime import datetime

import requests

from backend.config import (
    DEVTO_ARTICLES_URL,
    DEVTO_DASHBOARD_URL,
    DRAFTS_DIR,
    get_required_env,
)
from backend.generator import build_article_from_topic
from backend.topics import find_first_unused_topic, load_topics, mark_topic_failed, mark_topic_used
from backend.utils import insert_image_after_paragraph, slugify


def local_body_markdown(article):
    body = article["body_markdown"]
    if not article.get("image_filename"):
        return body

    local_ref = f"images/{article['image_filename']}"
    if article.get("image_public_url") and article["image_public_url"] in body:
        return body.replace(article["image_public_url"], local_ref)

    return insert_image_after_paragraph(
        body,
        article.get("image_paragraph_index", 0),
        article.get("image_alt", "Illustration"),
        local_ref,
    )


def save_local_draft(article):
    DRAFTS_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}-{slugify(article['title'])}.md"
    draft_path = DRAFTS_DIR / filename

    draft_markdown = f"""# {article['title']}

> {article['subtitle']}

{local_body_markdown(article)}

---

Tags: {", ".join(article["tags"])}
"""
    draft_path.write_text(draft_markdown, encoding="utf-8")
    return draft_path


def send_to_devto(article):
    payload = {
        "article": {
            "title": article["title"],
            "description": article["subtitle"],
            "body_markdown": article["body_markdown"],
            "tags": article["tags"],
            "published": False,
        }
    }

    response = requests.post(
        DEVTO_ARTICLES_URL,
        headers={
            "api-key": get_required_env("DEVTO_API_KEY"),
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )

    if not response.ok:
        raise RuntimeError(
            f"Dev.to API error ({response.status_code}): {response.text}"
        )

    return response.json()


def devto_result_from_response(devto_response):
    return {
        "devto_id": devto_response.get("id"),
        "devto_url": DEVTO_DASHBOARD_URL,
    }


def dev_url_for_display(url):
    if not url or "temp-slug" in url:
        return DEVTO_DASHBOARD_URL
    return url


def publish_topic(topic_text):
    article = build_article_from_topic(topic_text)
    draft_path = save_local_draft(article)
    devto_response = send_to_devto(article)
    devto_info = devto_result_from_response(devto_response)

    return {
        "article": article,
        "draft_path": draft_path,
        "image_warning": article.get("image_devto_warning"),
        **devto_info,
    }


def process_next_queued_topic():
    topics = load_topics()
    queued_topic = find_first_unused_topic(topics)

    if not queued_topic:
        raise RuntimeError("No unused topics in the queue. Add a topic first.")

    topic_id = queued_topic["id"]
    topic_text = queued_topic["topic"]

    try:
        result = publish_topic(topic_text)
        mark_topic_used(topic_id, result["devto_url"])
        result["queue_topic"] = queued_topic
        return result
    except Exception as exc:
        mark_topic_failed(topic_id, str(exc))
        raise
