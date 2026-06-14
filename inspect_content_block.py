import os, json, requests
from dotenv import load_dotenv
load_dotenv('.env')

api_key = os.getenv('NEO4J_API_KEY')
api_secret = os.getenv('NEO4J_API_SECRET')
endpoint = os.getenv('RESOURCE_AGENT_ENDPOINT')

r = requests.post('https://api.neo4j.io/oauth/token', auth=(api_key, api_secret),
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
    data={'grant_type': 'client_credentials'}, timeout=10)
token = r.json()['access_token']

resp = requests.post(endpoint,
    headers={'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'Bearer {token}'},
    json={'input': 'Where can I find job_training services in Alameda County?'}, timeout=60)
result = resp.json()
for i, block in enumerate(result.get('content', [])):
    print(f'Block {i}: type={block.get(\"type\")}, keys={list(block.keys())}')
    if block.get('type') == 'text':
        print('TEXT:', block.get('text', '')[:300])
    elif block.get('type') == 'thinking':
        print('THINKING:', block.get('thinking', '')[:200])