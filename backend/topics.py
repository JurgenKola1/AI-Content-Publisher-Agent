"""Topic queue stored in data/topics.json (no database)."""

import json

from backend.config import (
    STATUS_FAILED,
    STATUS_UNUSED,
    STATUS_USED,
    TOPICS_FILE,
    today_string,
)


def load_topics():
    if not TOPICS_FILE.exists():
        return []

    with TOPICS_FILE.open(encoding="utf-8") as file:
        content = file.read().strip()
        if not content:
            return []
        return json.loads(content)


def save_topics(topics):
    TOPICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with TOPICS_FILE.open("w", encoding="utf-8") as file:
        json.dump(topics, file, indent=2)
        file.write("\n")


def next_topic_id(topics):
    if not topics:
        return 1
    return max(topic["id"] for topic in topics) + 1


def add_topic_to_queue(topic_text):
    topics = load_topics()
    new_topic = {
        "id": next_topic_id(topics),
        "topic": topic_text,
        "status": STATUS_UNUSED,
        "created_at": today_string(),
        "used_at": None,
        "dev_url": None,
        "error": None,
    }
    topics.append(new_topic)
    save_topics(topics)
    return new_topic


def find_first_unused_topic(topics):
    for topic in topics:
        if topic["status"] == STATUS_UNUSED:
            return topic
    return None


def mark_topic_used(topic_id, dev_url):
    topics = load_topics()
    for topic in topics:
        if topic["id"] == topic_id:
            topic["status"] = STATUS_USED
            topic["used_at"] = today_string()
            topic["dev_url"] = dev_url
            topic["error"] = None
            break
    save_topics(topics)


def mark_topic_failed(topic_id, error_message):
    topics = load_topics()
    for topic in topics:
        if topic["id"] == topic_id:
            topic["status"] = STATUS_FAILED
            topic["error"] = error_message
            break
    save_topics(topics)


def topics_by_status(status):
    return [topic for topic in load_topics() if topic["status"] == status]
