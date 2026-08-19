from handlers import approval_tracker, ci_diagnosis, labeling, merge_manager, coverage
HANDLERS = {"pull_request": labeling.handle, "check_run": ci_diagnosis.handle, "pull_request_review": approval_tracker.handle, "issue_comment": merge_manager.handle}
def dispatch(event, payload):
    if event == 'issue_comment' and payload.get('comment',{}).get('body','').strip().lower().startswith('/coverage '): return coverage.handle(payload)
    handler = HANDLERS.get(event)
    return handler(payload) if handler else {"status": "ignored", "event": event}
