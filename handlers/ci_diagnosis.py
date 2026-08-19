from core.gh import run
from core.guardrails import repo_allowed, write_enabled
from core.llm_client import diagnose
def handle(payload):
    check=payload.get('check_run',{}); repo=payload.get('repository',{}).get('full_name','')
    if not repo_allowed(repo): return {'status':'blocked','reason':'repository is not allow-listed'}
    if check.get('conclusion') not in {'failure','timed_out','cancelled'}: return {'status':'ignored'}
    diagnosis=diagnose(run('run','view',str(check.get('check_suite_id','')),'--log-failed',repo=repo,check=False))
    number=payload.get('pull_request',{}).get('number')
    if write_enabled() and number: run('pr','comment',str(number),'--body','## CI diagnosis\n'+diagnosis,repo=repo)
    return {'status':'applied' if write_enabled() and number else 'planned','diagnosis':diagnosis}
