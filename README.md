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

The existing Razorpay Slack security-review app owns the interactive Approve/Request Changes buttons and the resulting GitHub review. This agent only requests/notifies security review and reads the resulting GitHub approval status; it does not duplicate the button action.
