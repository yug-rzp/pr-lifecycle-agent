import os
def repo_allowed(repo):
    allowed={x.strip() for x in os.getenv('ALLOWED_REPOS','').split(',') if x.strip()}
    return bool(repo) and (not allowed or repo in allowed)
def diff_allowed(lines): return int(lines or 0)<=int(os.getenv('MAX_DIFF_LINES','1000'))
def write_enabled(): return os.getenv('ENABLE_WRITES','false').lower()=='true'
