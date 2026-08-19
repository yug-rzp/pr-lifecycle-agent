import os, tempfile, subprocess
from core.gh import run
from core.guardrails import repo_allowed, write_enabled
from core.llm_client import complete
def handle(payload):
    repo=payload.get('repository',{}).get('full_name',''); body=payload.get('comment',{}).get('body','').strip().lower()
    if not body.startswith('/coverage ') or not repo_allowed(repo): return {'status':'ignored'}
    kind=body.split()[1]
    if kind not in {'unit','split'}: return {'status':'blocked','reason':'use /coverage unit or /coverage split'}
    diff=run('pr','diff',str(payload.get('issue',{}).get('number','')),repo=repo)
    patch=complete('Return ONLY a unified diff adding focused %s tests for this PR. No prose.\n%s'%(kind,diff[:12000]))
    if not os.getenv('ENABLE_COVERAGE_WRITES','false').lower()=='true': return {'status':'planned','kind':kind,'patch':patch}
    with tempfile.TemporaryDirectory() as work:
        subprocess.run(['gh','repo','clone',repo,work],check=True,capture_output=True,text=True)
        subprocess.run(['git','-C',work,'apply','--check'],input=patch,text=True,check=True)
        subprocess.run(['git','-C',work,'apply'],input=patch,text=True,check=True)
        subprocess.run(['git','-C',work,'checkout','-b','test/coverage-%s'%kind],check=True,capture_output=True)
        subprocess.run(['git','-C',work,'add','.'],check=True); subprocess.run(['git','-C',work,'commit','-m','test: improve %s coverage'%kind],check=True,capture_output=True)
        subprocess.run(['git','-C',work,'push','-u','origin','HEAD'],check=True,capture_output=True)
    return {'status':'applied','kind':kind}
