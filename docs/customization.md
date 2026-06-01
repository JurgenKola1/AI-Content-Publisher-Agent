# Customization

This agent is intentionally simple so you can adapt it for different businesses and use cases.

## Change the Writing Style

Edit the prompt template:

```
prompts/generate_article.txt
```

Examples of changes:

- Target a different audience (lawyers, dentists, e-commerce owners)
- Change tone (formal, casual, technical)
- Ask for shorter or longer articles
- Request a specific structure (intro, steps, FAQ, conclusion)

No Python changes needed — just edit the text file and restart Flask.

## Change Image Behavior

| Goal | How |
|------|-----|
| Disable images | Set `ENABLE_ARTICLE_IMAGES=false` in `.env` |
| Change image model | Set `OPENAI_IMAGE_MODEL=gpt-image-1` in `.env` |
| Change image placement logic | Edit `prompts/plan_image.txt` |
| Use a different image host | Edit `backend/image_hosting.py` |

## Change the Publishing Platform

Dev.to is the default target. To publish elsewhere:

1. Copy `send_to_devto()` in `backend/publisher.py`.
2. Create a new function for your platform's API (WordPress, Medium import, LinkedIn, etc.).
3. Update `publish_topic()` to call your new function.

The generation and local save steps can stay the same.

## Adapt for a Client Business

Example: a marketing agency publishing for clients.

1. **Add client name to prompts** — include `{client_name}` in `generate_article.txt`.
2. **Separate topic queues** — use `data/client-a-topics.json` and load the right file per client.
3. **Custom tags** — add default tags in `backend/utils.py` → `normalize_tags()`.
4. **Brand voice file** — create `prompts/brand_voice.txt` and append it to the article prompt.

## Add More Automation Later

This version has no scheduler. Common next steps for a production agent:

- **Cron / Task Scheduler** — run a script on a schedule
- **Background worker** — Celery or APScheduler
- **Database** — replace `data/topics.json` with SQLite or PostgreSQL
- **Multi-user UI** — add login and per-user topic queues

## File Quick Reference

| Want to change… | Edit this |
|-----------------|-----------|
| Article prompts | `prompts/generate_article.txt` |
| Image prompts | `prompts/plan_image.txt` |
| Topic tracking | `backend/topics.py`, `data/topics.json` |
| Dev.to payload | `backend/publisher.py` → `send_to_devto()` |
| Web UI text/layout | `templates/index.html`, `static/style.css` |
| API keys / models | `.env` |
