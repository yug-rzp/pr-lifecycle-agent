from core.gh import run
from core.guardrails import repo_allowed, write_enabled
from core.llm_client import diagnose
def handle(payload):
    check=payload.get('check_run',{}); repo=payload.get('repository',{}).get('full_name','')
    if not repo_allowed(repo): return {'status':'blocked','reason':'repository is not allow-listed'}
    if check.get('conclusion') not in {'failure','timed_out','cancelled'}: return {'status':'ignored'}
    sha=check.get('head_sha'); name=check.get('name','')
    runs=run('run','list','--commit',sha,'--json','databaseId,name,conclusion',repo=repo,check=False) if sha else ''
    import json
    run_id=''
    try:
        candidates=json.loads(runs or '[]'); run_id=next((str(x['databaseId']) for x in candidates if x.get('name')==name), str(candidates[0]['databaseId']) if candidates else '')
    except (ValueError,TypeError,KeyError): pass
    logs=run('run','view',run_id,'--log-failed',repo=repo,check=False) if run_id else 'No workflow run found for check run '+str(check.get('id',''))
    diagnosis=diagnose(logs)
    prs=run('pr','list','--search',sha,'--json','number',repo=repo,check=False)
    number=None
    try: number=json.loads(prs or '[]')[0].get('number')
    except (ValueError,IndexError,TypeError): pass
    if write_enabled() and number: run('pr','comment',str(number),'--body','## CI diagnosis\n'+diagnosis,repo=repo)
    return {'status':'applied' if write_enabled() and number else 'planned','diagnosis':diagnosis}
