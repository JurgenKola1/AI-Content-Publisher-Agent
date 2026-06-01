"""Load prompt templates from the prompts/ folder."""

from backend.config import PROMPTS_DIR


def load_prompt(filename):
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


def article_prompt(topic):
    return load_prompt("generate_article.txt").format(topic=topic)


def image_plan_prompt(title, body_markdown):
    return load_prompt("plan_image.txt").format(
        title=title,
        body_markdown=body_markdown,
    )
