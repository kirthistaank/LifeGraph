import os, requests
from dotenv import load_dotenv
from typing import Optional, Tuple

load_dotenv('.env')

def parse_agent_response(result):
    if not isinstance(result, dict) or 'error' in result:
        return None, None
    response_parts, reasoning_parts = [], []
    content = result.get('content')
    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            block_type = block.get('type')
            if block_type == 'text' and block.get('text'):
                response_parts.append(block['text'])
            elif block_type == 'thinking' and block.get('thinking'):
                reasoning_parts.append(block['thinking'])
        if response_parts:
            return '\n\n'.join(response_parts), '\n\n'.join(reasoning_parts) if reasoning_parts else None
    return None, None

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
text, reasoning = parse_agent_response(result)
print('Has response:', bool(text))
print('Response preview:', (text or '')[:200])
print('Has reasoning:', bool(reasoning))