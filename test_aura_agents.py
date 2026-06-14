import os, json, requests
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("NEO4J_API_KEY")
api_secret = os.getenv("NEO4J_API_SECRET")
endpoint = os.getenv("RESOURCE_AGENT_ENDPOINT")

# Get token
r = requests.post(
    'https://api.neo4j.io/oauth/token',
    auth=(api_key, api_secret),
    headers={'Content-Type': 'application/x-www-form-urlencoded'},
    data={'grant_type': 'client_credentials'},
    timeout=10
)
print("Token status:", r.status_code)
if r.status_code != 200:
    print("Token error:", r.text[:200])
    exit(1)
token = r.json()['access_token']

question = "Where can I find job_training services in Alameda County?"
resp = requests.post(
    endpoint,
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    },
    json={"input": question},
    timeout=60
)
print("Agent status:", resp.status_code)
if resp.status_code == 200:
    result = resp.json()
    print("Top-level keys:", list(result.keys()))
    print("Full structure (truncated):")
    print(json.dumps(result, indent=2)[:3000])
else:
    print("Error:", resp.text[:500])