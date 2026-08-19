import os
from core.gh import json_run
from core.guardrails import repo_allowed
def parse_codeowners(text):
    owners={}
    for line in text.splitlines():
        parts=line.split('#',1)[0].split()
        if len(parts)>1: owners[parts[0]]=parts[1:]
    return owners
def handle(payload):
    repo=payload.get('repository',{}).get('full_name',''); pr=payload.get('pull_request',{})
    if not repo_allowed(repo): return {'status':'blocked','reason':'repository is not allow-listed'}
    number=str(pr.get('number','')); reviews=json_run('pr','view',number,'--json','reviews',repo=repo).get('reviews',[])
    approved={r.get('author',{}).get('login') for r in reviews if r.get('state')=='APPROVED'}
    missing=[]
    try:
        data=json_run('api','repos/%s/contents/CODEOWNERS'%repo,repo=repo); missing=sorted(set(sum(parse_codeowners(data.get('content','')).values(),[]))-approved)
    except Exception: pass
    webhook=os.getenv('SLACK_WEBHOOK_URL')
    if missing and webhook:
        import requests
        requests.post(webhook,json={'text':'PR %s needs approval from: %s'%(pr.get('html_url',number),', '.join(missing))},timeout=10).raise_for_status()
    return {'status':'applied' if missing and webhook else 'planned','missing_approvals':missing}
