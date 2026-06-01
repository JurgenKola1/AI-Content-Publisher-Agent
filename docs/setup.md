# Setup

Follow these steps to run the AI Content Publisher Agent on your computer.

## Requirements

- Python 3.10 or newer
- An OpenAI API key
- A Dev.to API key
- Internet connection (for API calls)

## 1. Clone or Download the Project

Open the project folder in your terminal:

```powershell
cd "AI Content Publisher Agent"
```

## 2. Create a Virtual Environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

## 4. Configure Environment Variables

Copy the example file:

```powershell
Copy-Item .env.example .env
```

Open `.env` and add your keys:

```env
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-5-mini
OPENAI_IMAGE_MODEL=gpt-image-1
ENABLE_ARTICLE_IMAGES=true
DEVTO_API_KEY=your-devto-api-key-here
```

### Where to Get API Keys

| Service | Where to get the key |
|---------|----------------------|
| OpenAI | https://platform.openai.com/api-keys |
| Dev.to | Dev.to → Settings → Extensions → DEV Community API Keys |

## 5. Run the App

```powershell
python app.py
```

Open your browser at:

```
http://127.0.0.1:5000
```

## 6. Verify It Works

1. Enter a short test topic.
2. Click **Generate Draft**.
3. Check that a new file appears in `drafts/`.
4. Open https://dev.to/dashboard and confirm a new draft exists.

## Troubleshooting

| Problem | Likely fix |
|---------|------------|
| `Missing OPENAI_API_KEY` | Add the key to `.env` and restart Flask |
| Image model error | Set `OPENAI_IMAGE_MODEL=gpt-image-1` or `ENABLE_ARTICLE_IMAGES=false` |
| Dev.to API error | Check your Dev.to API key |
| Empty topic queue | Add topics in the UI or edit `data/topics.json` |

## Before Sharing Publicly

- Remove real API keys from `.env`
- Keep `.env` out of Git (already in `.gitignore`)
- Optionally clear personal drafts from `drafts/`
