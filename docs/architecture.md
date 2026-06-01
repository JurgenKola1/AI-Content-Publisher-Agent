# Architecture

## Overview

The AI Content Publisher Agent is a local web app with a simple split:

- **Frontend** — HTML form and results page (control panel)
- **Backend** — Python logic that generates and publishes content
- **Data** — JSON file for topic tracking (no database yet)
- **Drafts** — local folder for generated output

## System Flow

```
User Topic
    ↓
Frontend (templates/index.html)
    ↓
Backend (backend/routes.py)
    ↓
Prompt Logic (prompts/ + backend/prompts.py)
    ↓
AI Model (OpenAI API)
    ↓
Generated Content (article + optional image)
    ↓
Saved / Published Output (drafts/ + Dev.to)
```

## Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     Browser (User)                       │
└─────────────────────────┬───────────────────────────────┘
                          │ HTTP
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Frontend                                                │
│  templates/index.html  +  static/style.css               │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Backend (Flask)                                         │
│  app.py → backend/routes.py                              │
│       → backend/publisher.py                             │
│       → backend/generator.py                             │
│       → backend/topics.py                                │
└───────┬─────────────────────┬───────────────────────────┘
        │                     │
        ▼                     ▼
┌───────────────┐     ┌───────────────────┐
│  data/        │     │  External APIs     │
│  topics.json  │     │  OpenAI, Dev.to,   │
└───────────────┘     │  catbox.moe        │
                      └───────────────────┘
        │
        ▼
┌───────────────┐
│  drafts/      │
│  .md + images │
└───────────────┘
```

## Important Files

| File / Folder | Role |
|---------------|------|
| `app.py` | Application entry point |
| `backend/routes.py` | Flask routes and form handling |
| `backend/generator.py` | OpenAI article and image generation |
| `backend/publisher.py` | Save drafts and post to Dev.to |
| `backend/topics.py` | Topic queue read/write logic |
| `backend/prompts.py` | Loads prompt templates |
| `backend/image_hosting.py` | Uploads images for Dev.to Markdown |
| `backend/config.py` | Paths, constants, environment helpers |
| `prompts/` | Editable prompt template files |
| `data/topics.json` | Topic queue and history tracking |
| `drafts/` | Generated Markdown articles |
| `drafts/images/` | Generated PNG illustrations |
| `templates/index.html` | Web UI |
| `static/style.css` | UI styling |

## Publishing Logic

There is **no cron job or scheduler**. Publishing happens when:

1. User clicks **Generate Draft** (manual), or
2. User clicks **Generate Next Draft** (queue automation)

Both paths call the same pipeline in `backend/publisher.py`:

```
build_article_from_topic()
  → save_local_draft()
  → send_to_devto()   # always published: false
```

## Design Choices (for readers)

- **JSON over database** — keeps the project simple for learning
- **Prompts in separate files** — easy to edit without touching Python
- **Frontend as control panel** — user triggers automation manually
- **Drafts saved locally first** — content is never lost if Dev.to fails
