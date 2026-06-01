# How It Works

This page explains what happens when you use the Content Publisher Agent.

## Short Project Flow

```
User enters a topic
  → frontend sends it to the backend
  → backend loads a prompt template
  → OpenAI generates the article (and one image)
  → content is saved locally
  → content is sent to Dev.to as a draft
  → user reviews the result in the browser and on Dev.to
```

## Manual Generation

1. **You enter a topic** in the top form.
2. **Flask receives the POST request** in `backend/routes.py`.
3. **`publish_topic()` runs** in `backend/publisher.py`.
4. **OpenAI writes the article** using `prompts/generate_article.txt`.
5. **Optional: one image is created** using `prompts/plan_image.txt` and the OpenAI Image API.
6. **A local `.md` file is saved** in `drafts/`.
7. **Dev.to receives the draft** with `published: false`.
8. **The results page shows** the title, tags, image preview, and Markdown.

## Topic Queue Automation

The queue does **not** run on a timer. You control it from the UI.

### Adding a Topic

1. You type a topic and click **Add Topic**.
2. The backend appends a record to `data/topics.json` with status `unused`.

### Generating the Next Draft

1. You click **Generate Next Draft**.
2. The backend finds the first `unused` topic in `data/topics.json`.
3. It runs the same pipeline as manual generation.
4. On success: status becomes `used`, `used_at` and `dev_url` are saved.
5. On failure: status becomes `failed`, and the error message is stored.

## What Gets Generated

Each article includes:

| Field | Description |
|-------|-------------|
| Title | Article headline |
| Subtitle | One-line description |
| Body | Full Markdown content |
| Tags | Up to 4 Dev.to tags |
| Image | One PNG placed after the key paragraph |

## Where Output Is Stored

| Output | Location |
|--------|----------|
| Markdown draft | `drafts/YYYYMMDD-HHMMSS-title.md` |
| Image file | `drafts/images/YYYYMMDD-HHMMSS-title.png` |
| Topic history | `data/topics.json` |
| Dev.to draft | Your Dev.to dashboard (online) |

## Image Handling

1. OpenAI generates a PNG and saves it locally.
2. The image is uploaded to **catbox.moe** to get a public URL.
3. That URL is inserted into the Markdown for Dev.to.
4. The local draft uses a relative path: `images/filename.png`.

If public upload fails, the article still publishes to Dev.to — without the image — and a warning is shown.

## Dev.to Draft Links

After publishing, use **https://dev.to/dashboard** to edit your draft. The API may return a temporary URL that 404s until you publish the post.
