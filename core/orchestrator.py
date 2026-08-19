from handlers import approval_tracker, ci_diagnosis, labeling, merge_manager
HANDLERS = {"pull_request": labeling.handle, "check_run": ci_diagnosis.handle, "pull_request_review": approval_tracker.handle, "issue_comment": merge_manager.handle}
def dispatch(event, payload):
    handler = HANDLERS.get(event)
    return handler(payload) if handler else {"status": "ignored", "event": event}
