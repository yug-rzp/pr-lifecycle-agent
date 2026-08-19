import os, requests
from core.config import load
from core.guardrails import repo_allowed
from core.gh import json_run

def handle(payload):
    repo=payload.get('repository',{}).get('full_name','')
    if not repo_allowed(repo): return {'status':'blocked','reason':'repository is not allow-listed'}
    configured=load().get('security_review_repos', ['razorpay/mozart','razorpay/integrations-go'])
    if repo not in configured: return {'status':'ignored','reason':'security review not configured for repository'}
    comment=payload.get('comment',{}).get('body','').strip().lower()
    if 'request-security-review' not in comment: return {'status':'ignored'}
    pr=payload.get('issue',{}); number=str(pr.get('number',''))
    if not number: return {'status':'blocked','reason':'pull request number is required'}
    reviews=json_run('pr','view',number,'--json','reviews',repo=repo).get('reviews',[])
    security_users=set(load().get('security_reviewers', []))
    approved=[r.get('author',{}).get('login') for r in reviews if r.get('state')=='APPROVED' and (not security_users or r.get('author',{}).get('login') in security_users)]
    if approved: return {'status':'approved','approver':approved[-1]}
    webhook=os.getenv('SLACK_WEBHOOK_URL') or load().get('slack_webhook_url','')
    channel=load().get('security_slack_channel','#security-mozart-pr-review')
    text='Security review requested for %s #%s: %s\nApproval must be recorded as an approved GitHub review by a security reviewer.'%(repo,number,pr.get('html_url',''))
    if webhook:
        requests.post(webhook,json={'text':text,'channel':channel},timeout=10).raise_for_status()
    return {'status':'notified' if webhook else 'planned','channel':channel,'required':'security GitHub approval'}
