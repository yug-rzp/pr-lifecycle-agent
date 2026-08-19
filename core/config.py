import os
from pathlib import Path
try:
    import yaml
except ImportError:
    yaml = None

def load():
    path=Path(__file__).parents[1]/'config.yaml'
    data={}
    if yaml and path.exists():
        data=yaml.safe_load(path.read_text()) or {}
    return data

def allowed_repos():
    configured=load().get('allowed_repos', [])
    env=[x.strip() for x in os.getenv('ALLOWED_REPOS','').split(',') if x.strip()]
    return set(env or configured)

def slack_webhook(): return os.getenv('SLACK_WEBHOOK_URL') or load().get('slack_webhook_url','')
def protected_branches(): return load().get('protected_branches', ['sg_release','us_release','in_release'])
