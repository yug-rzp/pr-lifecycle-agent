import json, os, time, hmac, hashlib
from urllib.parse import parse_qs
from core.config import load
from core.gh import run

def verify(headers, body):
    secret=os.getenv('SLACK_SIGNING_SECRET')
    if not secret: return False
    ts=headers.get('X-Slack-Request-Timestamp','')
    if not ts or abs(time.time()-int(ts))>300: return False
    base='v0:%s:%s'%(ts,body)
    expected='v0='+hmac.new(secret.encode(),base.encode(),hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected,headers.get('X-Slack-Signature',''))

def handle(form):
    raw=form.get('payload','{}'); payload=json.loads(raw) if isinstance(raw,str) else raw
    user=payload.get('user',{}); allowed=set(load().get('security_slack_users',[]))
    identity={user.get('id'),user.get('username'),user.get('name'),user.get('real_name')}
    if allowed and not identity.intersection(allowed): return {'response_type':'ephemeral','text':'You are not configured as a security approver.'}
    action=(payload.get('actions') or [{}])[0]
    label=(action.get('text') or {}).get('text','').lower(); value=action.get('value','')
    # Button value should be repo|number, but accept the PR URL format too.
    if '|' in value: repo,number=value.split('|',1)
    else:
        import re
        m=re.search(r'github\.com/([^/]+/[^/]+)/pull/(\d+)',value)
        if not m: return {'response_type':'ephemeral','text':'This approval button has no valid PR reference.'}
        repo,number=m.group(1),m.group(2)
    if label=='approve':
        run('pr','review',number,'--approve','--body','Approved from the verified security Slack workflow.',repo=repo)
        result='approved'
    elif 'request changes' in label:
        run('pr','review',number,'--request-changes','--body','Changes requested from the security Slack workflow.',repo=repo)
        result='request changes'
    else: return {'response_type':'ephemeral','text':'Unsupported security action.'}
    return {'response_type':'in_channel','text':'Security review %s for %s#%s by %s.'%(result,repo,number,user.get('name') or user.get('username','approver'))}
