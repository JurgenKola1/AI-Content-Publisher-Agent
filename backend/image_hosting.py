"""Upload generated images to a public URL for Dev.to Markdown."""

import requests

from backend.config import (
    CATBOX_UPLOAD_URL,
    DEVTO_IMAGE_UPLOAD_URL,
    get_required_env,
)


def upload_image_to_catbox(image_path):
    with image_path.open("rb") as image_file:
        response = requests.post(
            CATBOX_UPLOAD_URL,
            data={"reqtype": "fileupload"},
            files={"fileToUpload": (image_path.name, image_file, "image/png")},
            timeout=120,
        )

    if not response.ok:
        raise RuntimeError(
            f"Image host upload error ({response.status_code}): {response.text}"
        )

    public_url = response.text.strip()
    if not public_url.startswith("http"):
        raise RuntimeError(f"Unexpected image host response: {response.text}")

    return public_url


def upload_image_to_devto(image_path):
    """Fallback only — Dev.to upload usually needs a browser session."""
    devto_api_key = get_required_env("DEVTO_API_KEY")

    with image_path.open("rb") as image_file:
        response = requests.post(
            DEVTO_IMAGE_UPLOAD_URL,
            headers={"api-key": devto_api_key},
            files={"image": (image_path.name, image_file, "image/png")},
            timeout=60,
        )

    if not response.ok:
        raise RuntimeError(
            f"Dev.to image upload error ({response.status_code}): {response.text}"
        )

    data = response.json()
    links = data.get("links") or []
    if links:
        return links[0]

    return data.get("url") or data.get("image", {}).get("url")


def resolve_public_image_url(image_path, openai_image_url):
    for upload in (upload_image_to_catbox, upload_image_to_devto):
        try:
            return upload(image_path)
        except Exception:
            continue

    return openai_image_url or None
