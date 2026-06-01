# AI Content Publisher Agent

Support project for **Building Business AI Agents: A Technical Guide to Designing, Deploying, and Selling AI Automation Systems**.

A local Flask agent that turns article topics into Dev.to-ready drafts using OpenAI.

## What It Does

You enter a topic. The agent generates a full article (title, subtitle, Markdown body, tags), adds one AI illustration, saves everything locally, and sends a draft to Dev.to.

## Main Features

- **Manual generation** — enter one topic and create a draft immediately
- **Topic queue** — store topics in JSON and process them one at a time
- **AI article writing** — OpenAI generates Dev.to-ready Markdown
- **One AI image per article** — placed after the most important paragraph
- **Local drafts** — saved as `.md` files in `drafts/`
- **Dev.to publishing** — posts as an unpublished draft (`published: false`)

## How the Agent Works

```
User Topic → Frontend → Backend → Prompt Logic → AI Model → Generated Content → Saved / Published Output
```

1. You enter a topic in the web UI (frontend).
2. Flask receives the request (backend).
3. Prompt templates from `prompts/` are filled with your topic.
4. OpenAI generates the article (and optionally an image).
5. The result is saved to `drafts/` and sent to Dev.to as a draft.

There is **no scheduler**. The topic queue runs only when you click **Generate Next Draft**.

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env and add your API keys
python app.py
```

Open: **http://127.0.0.1:5000**

See [docs/setup.md](docs/setup.md) for full setup steps.

## Example Usage

**Manual draft**

1. Open the app in your browser.
2. Enter: `How chatbots help restaurants save time`
3. Click **Generate Draft**.
4. Review the result, open your local `.md` file in `drafts/`, and edit the draft on Dev.to.

**Topic queue**

1. Add topics in the **Topic Queue** section.
2. Click **Generate Next Draft** to process the first unused topic.
3. Check `data/topics.json` to see status updates (`unused`, `used`, `failed`).

## Project Structure

```
AI Content Publisher Agent/
├── app.py                 # Start the app here
├── backend/               # Agent logic (API, prompts, publishing)
├── prompts/               # Prompt templates (editable)
├── data/                  # Topic queue (topics.json)
├── drafts/                # Generated articles and images
├── templates/             # HTML frontend
├── static/                # CSS styles
├── docs/                  # Book documentation
├── requirements.txt       # Python dependencies
└── .env.example           # Environment variable template
```

## Documentation

| File | Purpose |
|------|---------|
| [docs/setup.md](docs/setup.md) | Install and run locally |
| [docs/how-it-works.md](docs/how-it-works.md) | Step-by-step agent flow |
| [docs/architecture.md](docs/architecture.md) | System design overview |
| [docs/customization.md](docs/customization.md) | Adapt for other businesses |
| [docs/tools-and-technologies.md](docs/tools-and-technologies.md) | Full tech stack reference |

## Environment Variables

| Variable | Purpose | Used In |
|----------|---------|---------|
| `OPENAI_API_KEY` | Authenticate OpenAI requests | `backend/generator.py` |
| `OPENAI_MODEL` | Text model for articles | `backend/generator.py` |
| `OPENAI_IMAGE_MODEL` | Image model for illustrations | `backend/generator.py` |
| `ENABLE_ARTICLE_IMAGES` | Turn image generation on/off | `backend/config.py` |
| `DEVTO_API_KEY` | Authenticate Dev.to requests | `backend/publisher.py`, `backend/image_hosting.py` |

Copy `.env.example` to `.env` and add your keys. Never commit real keys to Git.

## License / Book Use

This project is designed as teaching material. Remove or replace private API keys before sharing publicly.
