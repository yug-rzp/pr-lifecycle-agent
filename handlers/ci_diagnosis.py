def handle(payload):
    if payload.get('check_run', {}).get('conclusion') not in {'failure', 'timed_out', 'cancelled'}: return {'status': 'ignored'}
    return {'status': 'planned', 'action': 'comment CI diagnosis'}
