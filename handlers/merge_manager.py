from core.gh import run, json_run
from core.guardrails import repo_allowed, write_enabled
from core.config import protected_branches
import fnmatch
def handle(payload):
    pr=payload.get('pull_request',{}); repo=payload.get('repository',{}).get('full_name','')
    if not repo_allowed(repo): return {'status':'blocked','reason':'repository is not allow-listed'}
    command=payload.get('comment',{}).get('body','').strip().lower()
    if command not in {'/merge-master','/merge master'}: return {'status':'ignored'}
    if any(fnmatch.fnmatch(pr.get('base',{}).get('ref',''), p) for p in protected_branches()): return {'status':'blocked','reason':'protected branch'}
    if not pr.get('number'): return {'status':'blocked','reason':'pull_request context is required'}
    reviews=json_run('pr','view',str(pr['number']),'--json','reviews',repo=repo).get('reviews',[])
    approved={r.get('author',{}).get('login') for r in reviews if r.get('state')=='APPROVED'}
    actor=payload.get('comment',{}).get('user',{}).get('login')
    if actor not in approved: return {'status':'blocked','reason':'explicit approval from an approved reviewer is required'}
    if not write_enabled(): return {'status':'planned','action':'update branch after human approval'}
    output=run('pr','update-branch',str(pr['number']),'--base','master',repo=repo,check=False)
    return {'status':'applied','output':output,'conflict_resolution':'gh safely updates clean branches; conflicts are escalated'}
