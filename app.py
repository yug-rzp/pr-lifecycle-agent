import os
import hmac, hashlib
from flask import Flask, jsonify, request

from core.orchestrator import dispatch
from handlers.slack_interactivity import verify as verify_slack, handle as handle_slack

app = Flask(__name__)


@app.post("/webhooks/github")
def github_webhook():
    secret = os.getenv("GITHUB_WEBHOOK_SECRET")
    if not secret:
        return jsonify(error="GITHUB_WEBHOOK_SECRET is required"), 500
    if secret:
        expected = "sha256=" + hmac.new(secret.encode(), request.get_data(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(request.headers.get("X-Hub-Signature-256", ""), expected):
            return jsonify(error="invalid webhook signature"), 401
    payload = request.get_json(silent=True) or {}
    event = request.headers.get("X-GitHub-Event", "ping")
    return jsonify(dispatch(event, payload))


@app.get("/health")
def health():
    return jsonify(status="ok")

@app.post('/webhooks/slack')
def slack_webhook():
    body=request.get_data(as_text=True)
    if not verify_slack(request.headers, body): return jsonify(error='invalid Slack signature'), 401
    return jsonify(handle_slack(request.form))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
