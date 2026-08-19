import json, os, subprocess
class GhError(RuntimeError): pass
def run(*args, repo=None, check=True):
    cmd=['gh',*args] + (['--repo',repo] if repo else [])
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=int(os.getenv('GH_TIMEOUT','30')))
    if check and r.returncode: raise GhError(r.stderr.strip() or 'gh command failed')
    return r.stdout.strip()
def json_run(*args, repo=None):
    out=run(*args,repo=repo); return json.loads(out) if out else {}
