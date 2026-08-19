import json, os
def complete(prompt):
    key=os.getenv('OPENAI_API_KEY')
    if not key: return json.dumps({'labels':[],'reason':'OPENAI_API_KEY not configured'})
    import requests
    r=requests.post('https://api.openai.com/v1/chat/completions',headers={'Authorization':'Bearer '+key},json={'model':os.getenv('LLM_MODEL','gpt-4o-mini'),'messages':[{'role':'user','content':prompt}],'temperature':0},timeout=45); r.raise_for_status(); return r.json()['choices'][0]['message']['content']
def classify(text, labels):
    try: x=json.loads(complete('Return JSON {labels:[],reason:""}. Choose labels from %s for this PR:\n%s'%(labels,text[:12000]))); return {'labels':[v for v in x.get('labels',[]) if v in labels],'reason':x.get('reason','')}
    except (ValueError,TypeError): return {'labels':[],'reason':'invalid LLM response'}
def diagnose(text): return complete('Diagnose this CI failure with root cause and fix:\n'+text[:16000])
