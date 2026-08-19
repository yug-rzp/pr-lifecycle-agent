from core.gh import run
from core.guardrails import diff_allowed, repo_allowed, write_enabled
from core.llm_client import classify
LABELS=['bug','feature','dependencies','breaking-change','documentation','refactor','tests']
def handle(payload):
    if payload.get('action') not in {'opened','edited','synchronize','ready_for_review'}: return {'status':'ignored','reason':'unsupported pull_request action'}
    pr=payload.get('pull_request',{}); repo=payload.get('repository',{}).get('full_name','')
    if not repo_allowed(repo): return {'status':'blocked','reason':'repository is not allow-listed'}
    if not diff_allowed(pr.get('additions',0)+pr.get('deletions',0)): return {'status':'blocked','reason':'diff exceeds limit'}
    labels=run('api','repos/%s/labels'%repo,'--jq','.[].name',repo=repo,check=False).splitlines() or LABELS
    result=classify('%s\n%s\n%s'%(pr.get('title',''),pr.get('body',''),run('pr','diff',str(pr['number']),repo=repo)),labels)
    if write_enabled():
        for label in result['labels']: run('pr','edit',str(pr['number']),'--add-label',label,repo=repo)
    return {'status':'applied' if write_enabled() else 'planned',**result}
