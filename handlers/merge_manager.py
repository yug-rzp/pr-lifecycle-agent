from core.gh import run, json_run
from core.guardrails import repo_allowed, write_enabled
def handle(payload):
    pr=payload.get('pull_request',{}); repo=payload.get('repository',{}).get('full_name','')
    if not repo_allowed(repo): return {'status':'blocked','reason':'repository is not allow-listed'}
    command=payload.get('comment',{}).get('body','').strip().lower()
    if command not in {'/merge-master','/merge master'}: return {'status':'ignored'}
    if pr.get('base',{}).get('ref') in {'sg_release','us_release','in_release'}: return {'status':'blocked','reason':'release branch'}
    reviews=json_run('pr','view',str(pr['number']),'--json','reviews',repo=repo).get('reviews',[])
    approved={r.get('author',{}).get('login') for r in reviews if r.get('state')=='APPROVED'}
    actor=payload.get('comment',{}).get('user',{}).get('login')
    if actor not in approved: return {'status':'blocked','reason':'explicit approval from an approved reviewer is required'}
    if not write_enabled(): return {'status':'planned','action':'update branch after human approval'}
    output=run('pr','update-branch',str(pr['number']),'--base','master',repo=repo,check=False)
    return {'status':'applied','output':output,'conflict_resolution':'gh safely updates clean branches; conflicts are escalated'}
