"""OpenAI article and image generation."""

import base64
import json
import os
from datetime import datetime

import requests
from openai import OpenAI

from backend.config import (
    DEFAULT_IMAGE_MODEL,
    DEFAULT_TEXT_MODEL,
    IMAGES_DIR,
    IMAGE_MODEL_FALLBACKS,
    get_required_env,
    images_enabled,
)
from backend.image_hosting import resolve_public_image_url
from backend.prompts import article_prompt, image_plan_prompt
from backend.utils import (
    clean_json_text,
    insert_image_after_paragraph,
    normalize_tags,
    slugify,
    split_paragraphs,
)


def generate_article(topic):
    client = OpenAI(api_key=get_required_env("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", DEFAULT_TEXT_MODEL)

    response = client.responses.create(
        model=model,
        input=article_prompt(topic),
    )

    article = json.loads(clean_json_text(response.output_text))
    return {
        "title": article["title"].strip(),
        "subtitle": article["subtitle"].strip(),
        "body_markdown": article["body_markdown"].strip(),
        "tags": normalize_tags(article.get("tags", [])),
    }


def plan_image_placement(article):
    client = OpenAI(api_key=get_required_env("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", DEFAULT_TEXT_MODEL)

    response = client.responses.create(
        model=model,
        input=image_plan_prompt(article["title"], article["body_markdown"]),
    )
    plan = json.loads(clean_json_text(response.output_text))

    paragraphs = split_paragraphs(article["body_markdown"])
    paragraph_index = int(plan["paragraph_index"])
    paragraph_index = max(0, min(paragraph_index, max(len(paragraphs) - 1, 0)))

    return {
        "paragraph_index": paragraph_index,
        "image_prompt": plan["image_prompt"].strip(),
        "alt_text": plan["alt_text"].strip(),
    }


def image_models_to_try():
    configured = os.getenv("OPENAI_IMAGE_MODEL", DEFAULT_IMAGE_MODEL).strip()
    models = []
    for model in [configured, *IMAGE_MODEL_FALLBACKS]:
        if model and model not in models:
            models.append(model)
    return models


def save_generated_image(image_data, image_path):
    if getattr(image_data, "b64_json", None):
        image_path.write_bytes(base64.b64decode(image_data.b64_json))
        return None

    if getattr(image_data, "url", None):
        download = requests.get(image_data.url, timeout=60)
        download.raise_for_status()
        image_path.write_bytes(download.content)
        return image_data.url

    raise RuntimeError("OpenAI returned no image data.")


def generate_image_file(image_prompt, filename_stem):
    client = OpenAI(api_key=get_required_env("OPENAI_API_KEY"))
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    image_path = IMAGES_DIR / f"{filename_stem}.png"

    last_error = None
    for image_model in image_models_to_try():
        for extra_options in [{"quality": "medium"}, {}]:
            try:
                response = client.images.generate(
                    model=image_model,
                    prompt=image_prompt,
                    size="1024x1024",
                    n=1,
                    **extra_options,
                )
                openai_url = save_generated_image(response.data[0], image_path)
                return image_path, openai_url
            except Exception as exc:
                last_error = exc

    raise RuntimeError(
        "Could not generate an image with any supported OpenAI image model. "
        f"Last error: {last_error}"
    )


def add_article_image(article):
    plan = plan_image_placement(article)
    filename_stem = f"{datetime.now().strftime('%Y%m%d-%H%M%S')}-{slugify(article['title'])}"
    image_path, openai_url = generate_image_file(plan["image_prompt"], filename_stem)
    public_url = resolve_public_image_url(image_path, openai_url)

    article["image_filename"] = image_path.name
    article["image_alt"] = plan["alt_text"]
    article["image_paragraph_index"] = plan["paragraph_index"]
    article["image_devto_warning"] = None

    if public_url:
        article["image_public_url"] = public_url
        article["body_markdown"] = insert_image_after_paragraph(
            article["body_markdown"],
            plan["paragraph_index"],
            plan["alt_text"],
            public_url,
        )
    else:
        article["image_devto_warning"] = (
            "Image saved locally in drafts/images/, but no public URL was available. "
            "The Dev.to draft was posted without the image."
        )

    return article


def build_article_from_topic(topic_text):
    article = generate_article(topic_text)
    if images_enabled():
        article = add_article_image(article)
    return article
