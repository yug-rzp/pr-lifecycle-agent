# PR Lifecycle Agent

Hackathon MVP for GitHub pull-request lifecycle automation.

## Build

- Label assignment
- CI diagnosis
- Approval reminders
- Master merge and conflict detection

## Skip for the MVP

Coverage PR generation, DevRev integration, and a full audit dashboard.

## Run

```bash
python -m pip install -r requirements.txt
python app.py
```

Set `ALLOWED_REPOS`, `GITHUB_WEBHOOK_SECRET`, and `LLM_API_KEY` before connecting a webhook. Handler functions intentionally return plans until GitHub/Slack credentials and production-side effects are configured.
