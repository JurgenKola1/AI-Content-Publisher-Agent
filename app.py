"""
AI Content Publisher Agent — entry point.

Run locally with: python app.py
"""

from backend.routes import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
