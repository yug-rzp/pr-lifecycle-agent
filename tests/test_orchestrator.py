from core.orchestrator import dispatch


def test_unknown_event_is_ignored():
    assert dispatch("push", {})["status"] == "ignored"


def test_failed_check_is_diagnosed():
    result = dispatch("check_run", {"repository": {"full_name": "org/repo"}, "check_run": {"conclusion": "failure", "name": "unit tests"}})
    assert result["status"] == "planned"


def test_merge_command_is_planned():
    result = dispatch("issue_comment", {"repository": {"full_name": "org/repo"}, "comment": {"body": "/merge-master"}})
    assert result["status"] == "blocked"
