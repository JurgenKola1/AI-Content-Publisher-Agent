"""Small helper functions used across the agent."""

import re


def clean_json_text(text):
    """Remove Markdown code fences if the model wraps JSON in them."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
        cleaned = re.sub(r"```$", "", cleaned).strip()
    return cleaned


def slugify(text):
    slug = text.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug or "article"


def normalize_tags(tags):
    clean_tags = []
    for tag in tags:
        tag = re.sub(r"[^a-z0-9]", "", str(tag).lower())
        if tag and tag not in clean_tags:
            clean_tags.append(tag)
    return clean_tags[:4] or ["ai", "python"]


def split_paragraphs(body_markdown):
    return [part.strip() for part in body_markdown.split("\n\n") if part.strip()]


def insert_image_after_paragraph(body_markdown, paragraph_index, alt_text, image_url):
    paragraphs = split_paragraphs(body_markdown)
    if not paragraphs:
        return f"![{alt_text}]({image_url})\n\n{body_markdown}"

    safe_index = max(0, min(paragraph_index, len(paragraphs) - 1))
    paragraphs.insert(safe_index + 1, f"![{alt_text}]({image_url})")
    return "\n\n".join(paragraphs)
