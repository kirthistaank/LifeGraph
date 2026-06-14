import os, requests
from dotenv import load_dotenv
load_dotenv('.env')
from streamlit_app import call_agent, parse_agent_response

result = call_agent('resource_locator', 'Where can I find job_training services in Alameda County?')
text, reasoning = parse_agent_response(result)
print('Has response:', bool(text))
print('Response preview:', (text or '')[:200])
print('Has reasoning:', bool(reasoning))
print('Reasoning preview:', (reasoning or '')[:120])
