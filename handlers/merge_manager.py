def handle(payload):
    if payload.get('comment', {}).get('body', '').strip().lower() not in {'/merge-master', '/merge master'}: return {'status': 'ignored'}
    return {'status': 'planned', 'action': 'merge master and detect conflicts'}
