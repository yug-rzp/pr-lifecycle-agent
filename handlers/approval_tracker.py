def handle(payload):
    if payload.get('review', {}).get('state', '').lower() == 'approved': return {'status': 'ignored'}
    return {'status': 'planned', 'action': 'send Slack reminder'}
