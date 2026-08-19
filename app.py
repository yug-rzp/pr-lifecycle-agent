import os
from flask import Flask, jsonify, request

from core.orchestrator import dispatch

app = Flask(__name__)


@app.post("/webhooks/github")
def github_webhook():
    secret = os.getenv("GITHUB_WEBHOOK_SECRET")
    if secret and request.headers.get("X-Hub-Signature-256") is None:
        return jsonify(error="missing webhook signature"), 401
    payload = request.get_json(silent=True) or {}
    event = request.headers.get("X-GitHub-Event", "ping")
    return jsonify(dispatch(event, payload))


@app.get("/health")
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
