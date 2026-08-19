import os, fnmatch, base64
from core.gh import json_run
from core.guardrails import repo_allowed
from core.config import slack_webhook
def parse_codeowners(text):
    owners={}
    for line in text.splitlines():
        parts=line.split('#',1)[0].split()
        if len(parts)>1: owners[parts[0]]=parts[1:]
    return owners
def required_owners(codeowners, files):
    matched=set()
    for path in files:
        best=[]
        for pattern, owners in codeowners.items():
            pattern=pattern.lstrip('/')
            if fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch('/'+path, '/'+pattern): best=owners
        matched.update(best)
    return matched
def handle(payload):
    repo=payload.get('repository',{}).get('full_name',''); pr=payload.get('pull_request',{})
    if not repo_allowed(repo): return {'status':'blocked','reason':'repository is not allow-listed'}
    number=str(pr.get('number','')); reviews=json_run('pr','view',number,'--json','reviews',repo=repo).get('reviews',[])
    approved={r.get('author',{}).get('login') for r in reviews if r.get('state')=='APPROVED'}
    missing=[]; files=[]
    try:
        data=json_run('api','repos/%s/contents/CODEOWNERS'%repo,repo=repo)
        raw=base64.b64decode(data.get('content','')).decode() if data.get('encoding')=='base64' else data.get('content','')
        files=[f.get('path','') for f in json_run('pr','view',number,'--json','files',repo=repo).get('files',[])]
        missing=sorted(required_owners(parse_codeowners(raw),files)-approved)
    except Exception: pass
    webhook=slack_webhook()
    if missing and webhook:
        import requests
        requests.post(webhook,json={'text':'PR %s needs approval from: %s'%(pr.get('html_url',number),', '.join(missing))},timeout=10).raise_for_status()
    return {'status':'applied' if missing and webhook else 'planned','missing_approvals':missing}
