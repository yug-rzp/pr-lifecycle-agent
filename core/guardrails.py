import os
from core.config import allowed_repos
def repo_allowed(repo):
    allowed=allowed_repos()
    return bool(repo) and (not allowed or repo in allowed)
def diff_allowed(lines): return int(lines or 0)<=int(os.getenv('MAX_DIFF_LINES','1000'))
def write_enabled(): return os.getenv('ENABLE_WRITES','false').lower()=='true'
