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

For live writes set `ENABLE_WRITES=true`; otherwise handlers perform analysis and return proposed actions. Configure `OPENAI_API_KEY` (or leave it unset for a safe fallback), `SLACK_WEBHOOK_URL`, `MAX_DIFF_LINES`, and a comma-separated `ALLOWED_REPOS` list.

Configure Slack interactivity to POST to `/webhooks/slack`, set `SLACK_SIGNING_SECRET`, and set `security_slack_users` in `config.yaml`. Button values must be `owner/repo|pull_number`. Approve/Request Changes actions create the corresponding GitHub review through `gh`.
