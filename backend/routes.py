"""Flask web routes — the frontend control panel."""

from flask import Flask, render_template, request, send_from_directory

from backend.config import IMAGES_DIR
from backend.publisher import dev_url_for_display, process_next_queued_topic, publish_topic
from backend.topics import add_topic_to_queue, topics_by_status


def create_app():
    app = Flask(__name__)

    @app.template_filter("devto_link")
    def devto_link_filter(url):
        return dev_url_for_display(url)

    @app.route("/", methods=["GET", "POST"])
    def index():
        error = None
        success = None
        result = None

        if request.method == "POST":
            action = request.form.get("action", "manual")

            if action == "manual":
                topic = request.form.get("topic", "").strip()
                if not topic:
                    error = "Please enter an article topic."
                else:
                    try:
                        result = publish_topic(topic)
                    except Exception as exc:
                        error = str(exc)

            elif action == "add_topic":
                topic = request.form.get("queue_topic", "").strip()
                if not topic:
                    error = "Please enter a topic to add to the queue."
                else:
                    add_topic_to_queue(topic)
                    success = f'Added to queue: "{topic}"'

            elif action == "generate_next":
                try:
                    result = process_next_queued_topic()
                    success = (
                        f'Generated draft for queue topic #{result["queue_topic"]["id"]}: '
                        f'"{result["queue_topic"]["topic"]}"'
                    )
                except Exception as exc:
                    error = str(exc)

        return render_template(
            "index.html",
            error=error,
            success=success,
            result=result,
            queue_unused=topics_by_status("unused"),
            queue_used=topics_by_status("used"),
            queue_failed=topics_by_status("failed"),
        )

    @app.route("/drafts/images/<path:filename>")
    def serve_draft_image(filename):
        return send_from_directory(IMAGES_DIR, filename)

    return app
