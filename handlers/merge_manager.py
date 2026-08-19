from core.gh import run
from core.guardrails import repo_allowed, write_enabled
def handle(payload):
    pr=payload.get('pull_request',{}); repo=payload.get('repository',{}).get('full_name','')
    if not repo_allowed(repo): return {'status':'blocked','reason':'repository is not allow-listed'}
    if payload.get('comment',{}).get('body','').strip().lower() not in {'/merge-master','/merge master'}: return {'status':'ignored'}
    if pr.get('base',{}).get('ref') in {'sg_release','us_release','in_release'}: return {'status':'blocked','reason':'release branch'}
    if not write_enabled(): return {'status':'planned','action':'merge master and detect conflicts'}
    return {'status':'applied','output':run('pr','update-branch',str(pr['number']),'--base','master',repo=repo,check=False)}
