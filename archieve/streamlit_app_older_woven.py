"""
LifeGraph: AI Social Resource Navigator
Neo4j Aura Agent Hackathon Submission
Streamlit Web Application
"""

import streamlit as st
import requests
from typing import Optional, Tuple
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# PAGE CONFIG & STYLING
# ============================================================================

st.set_page_config(
    page_title="LifeGraph - AI Social Resource Navigator",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS from separate file (easy to swap themes)

with open("css/styles_woven_thread.css") as css_file:
    st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
# ============================================================================
# AGENT CONFIGURATION
# ============================================================================

AGENT_CONFIG = {
    "eligibility_navigator": {
        "endpoint": os.getenv("ELIGIBILITY_AGENT_ENDPOINT", ""),
        "api_key": os.getenv("NEO4J_API_KEY", ""),
        "api_secret": os.getenv("NEO4J_API_SECRET", ""),
    },
    "pathway_advisor": {
        "endpoint": os.getenv("PATHWAY_AGENT_ENDPOINT", ""),
        "api_key": os.getenv("NEO4J_API_KEY", ""),
        "api_secret": os.getenv("NEO4J_API_SECRET", ""),
    },
    "resource_locator": {
        "endpoint": os.getenv("RESOURCE_AGENT_ENDPOINT", ""),
        "api_key": os.getenv("NEO4J_API_KEY", ""),
        "api_secret": os.getenv("NEO4J_API_SECRET", ""),
    }
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

@st.cache_data
def get_bearer_token(api_key: str, api_secret: str) -> Optional[str]:
    """Exchange API credentials for bearer token"""
    try:
        response = requests.post(
            'https://api.neo4j.io/oauth/token',
            auth=(api_key, api_secret),
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            data={'grant_type': 'client_credentials'},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get('access_token')
        return None
    except Exception as e:
        st.error(f"Token error: {e}")
        return None

def call_agent(agent_name: str, question: str) -> dict:
    """Call an Aura Agent via REST API"""
    config = AGENT_CONFIG.get(agent_name)

    if not config or not config.get("endpoint"):
        return {
            "error": f"Agent '{agent_name}' not configured. Missing endpoint.",
            "hint": "Set environment variables: {}_ENDPOINT, NEO4J_API_KEY, NEO4J_API_SECRET".format(agent_name.upper())
        }

    bearer_token = get_bearer_token(config["api_key"], config["api_secret"])
    if not bearer_token:
        return {"error": "Failed to authenticate with Neo4j API"}

    try:
        print(f"DEBUG - Calling agent endpoint: {config['endpoint']}")
        print(f"DEBUG - Question: {question}")
        response = requests.post(
            config["endpoint"],
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {bearer_token}"
            },
            json={"input": question},
            timeout=60
        )

        print(f"DEBUG - Agent response status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"DEBUG - Agent response: {str(result)[:500]}")
            return result
        else:
            print(f"DEBUG - Agent error response: {response.text}")
            return {
                "error": f"Agent returned status {response.status_code}",
                "details": response.text
            }
    except requests.Timeout:
        print("DEBUG - Agent request timed out")
        return {"error": "Agent request timed out (>60 seconds). Agent may be slow or offline."}
    except Exception as e:
        print(f"DEBUG - Connection error: {str(e)}")
        return {"error": f"Connection error: {str(e)}"}

def parse_agent_response(result: dict) -> Tuple[Optional[str], Optional[str]]:
    """Extract assistant reply and reasoning from Neo4j Aura Agent API payloads."""
    if not isinstance(result, dict) or "error" in result:
        return None, None

    response_parts = []
    reasoning_parts = []

    content = result.get("content")
    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            block_type = block.get("type")
            if block_type == "text" and block.get("text"):
                response_parts.append(block["text"])
            elif block_type == "thinking" and block.get("thinking"):
                reasoning_parts.append(block["thinking"])

        if response_parts:
            response_text = "\n\n".join(response_parts)
            reasoning_text = "\n\n".join(reasoning_parts) if reasoning_parts else None
            return response_text, reasoning_text

    priority_keys = ["response", "output", "text", "answer", "message", "result"]
    for key in priority_keys:
        value = result.get(key)
        if isinstance(value, str) and value.strip():
            reasoning = result.get("reasoning") or result.get("thought")
            return value, reasoning if isinstance(reasoning, str) else None

    for key, value in result.items():
        if key not in ["reasoning", "thought", "error", "hint", "usage", "status", "type", "role", "end_reason"]:
            if isinstance(value, str) and value.strip():
                reasoning = result.get("reasoning") or result.get("thought")
                return value, reasoning if isinstance(reasoning, str) else None

    return None, None

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    if "agent_response" not in st.session_state:
        st.session_state.agent_response = None
    if "agent_reasoning" not in st.session_state:
        st.session_state.agent_reasoning = None
    if "agent_error" not in st.session_state:
        st.session_state.agent_error = None
    if "agent_raw_result" not in st.session_state:
        st.session_state.agent_raw_result = None

    # Header with Crystal Structure theme logo
    logo_col, title_col = st.columns([0.15, 0.85])
    with logo_col:
        #st.image("LifeGraph/logo-banner-options/cyrtsalsturcture-logo.png", width=80)
        st.image("Images/pathfinderpulse-logo.png", width=80)
    with title_col:
        st.markdown('<div class="main-title">LifeGraph</div>', unsafe_allow_html=True)

    st.markdown('<div class="subtitle">AI Social Resource Navigator for Life Transitions</div>', unsafe_allow_html=True)

    # Introduction
    with st.expander("ℹ️ About LifeGraph", expanded=False):
        st.markdown("""
        **LifeGraph** uses Neo4j knowledge graphs and AI agents to help people navigate complex social services.

        Instead of searching for programs individually, LifeGraph shows you:
        - What you qualify for (based on your situation)
        - The best sequence to apply (programs unlock each other)
        - Where to find help (organizations and contact info)

        **Three AI agents work together:**
        1. **Eligibility Navigator** - Answers: "What programs can I get?"
        2. **Pathway Advisor** - Answers: "What's my path to stability?"
        3. **Resource Locator** - Answers: "Where can I find help?"
        """)

    # Configuration Check
    if not all([AGENT_CONFIG[agent].get("endpoint") for agent in AGENT_CONFIG]):
        st.warning("""
        ⚠️ **Agents not configured!**

        To use this app, you need to:
        1. Enable External access on your Aura Agents
        2. Set environment variables:
           - `ELIGIBILITY_AGENT_ENDPOINT`
           - `PATHWAY_AGENT_ENDPOINT`
           - `RESOURCE_AGENT_ENDPOINT`
           - `NEO4J_API_KEY`
           - `NEO4J_API_SECRET`

        See STREAMLIT_SETUP_GUIDE.md for instructions.
        """)
        return

    # Main Interface
    st.markdown("---")

    # Sidebar: Agent Selection & Input
    with st.sidebar:
        st.markdown('<div style="color: #b19cd9; font-size: 1.3em; font-weight: 700; margin-bottom: 1em;">🎯 Select Agent</div>', unsafe_allow_html=True)

        agent_choice = st.radio(
            "Which agent would you like to talk to?",
            options=[
                "eligibility_navigator",
                "pathway_advisor",
                "resource_locator"
            ],
            format_func=lambda x: {
                "eligibility_navigator": "📋 Eligibility Navigator",
                "pathway_advisor": "🗺️ Pathway Advisor",
                "resource_locator": "📍 Resource Locator"
            }.get(x, x)
        )

        st.markdown("---")

        descriptions = {
            "eligibility_navigator": '<div style="color: #c9d1d9;"><strong style="color: #b19cd9;">What programs can I get?</strong><br><br>Tell me about your situation (age, location, life event), and I\'ll identify all the programs you might qualify for.</div>',
            "pathway_advisor": '<div style="color: #c9d1d9;"><strong style="color: #b19cd9;">What\'s my path to stability?</strong><br><br>I\'ll map out a recommended sequence - which program to apply to first, what it unlocks, and how it leads to your goals.</div>',
            "resource_locator": '<div style="color: #c9d1d9;"><strong style="color: #b19cd9;">Where can I find help?</strong><br><br>I\'ll find organizations, nonprofits, and services that match your needs in your area.</div>'
        }
        st.markdown(descriptions.get(agent_choice, ""), unsafe_allow_html=True)

    # Agent Interface
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown(f"<div class='agent-section'>", unsafe_allow_html=True)

        if agent_choice == "eligibility_navigator":
            st.markdown('<h3 style="color: #b19cd9; margin-bottom: 0.5em;">📋 Eligibility Navigator</h3>', unsafe_allow_html=True)
            st.markdown('<p style="color: #c9d1d9; font-size: 0.95em; margin-bottom: 1.2em;">Tell me about your situation</p>', unsafe_allow_html=True)

            col_inputs = st.columns(3)
            with col_inputs[0]:
                age = st.number_input("Age", min_value=18, max_value=80, value=19, step=1)
            with col_inputs[1]:
                location = st.selectbox(
                    "County",
                    ["Alameda", "Los Angeles", "San Francisco", "Sacramento", "Other"]
                )
            with col_inputs[2]:
                life_event = st.selectbox(
                    "Situation",
                    [
                        "AGED_OUT_OF_FOSTER_CARE",
                        "LOST_JOB",
                        "HAD_CHILD",
                        "STARTED_COLLEGE",
                        "HOMELESSNESS_RISK",
                        "DOMESTIC_VIOLENCE",
                        "SUBSTANCE_RECOVERY",
                        "OTHER"
                    ]
                )

            question = f"I am {age} years old, in {location} County, and I am experiencing {life_event}. What programs can I get?"

        elif agent_choice == "pathway_advisor":
            st.markdown('<h3 style="color: #b19cd9; margin-bottom: 0.5em;">🗺️ Pathway Advisor</h3>', unsafe_allow_html=True)
            st.markdown('<p style="color: #c9d1d9; font-size: 0.95em; margin-bottom: 1.2em;">What\'s your goal?</p>', unsafe_allow_html=True)

            col_inputs = st.columns(2)
            with col_inputs[0]:
                age = st.number_input("Age", min_value=18, max_value=80, value=19, step=1)
            with col_inputs[1]:
                location = st.text_input("County", value="Alameda")

            goals = st.multiselect(
                "What do you need help with?",
                ["Housing", "Employment", "Education", "Food", "Healthcare", "Childcare"]
            )

            goals_text = ", ".join(goals) if goals else "stability"
            question = f"I am {age} years old in {location} County. I need help with {goals_text}. Show me the best pathway to stability."

        else:  # resource_locator
            st.markdown('<h3 style="color: #b19cd9; margin-bottom: 0.5em;">📍 Resource Locator</h3>', unsafe_allow_html=True)
            st.markdown('<p style="color: #c9d1d9; font-size: 0.95em; margin-bottom: 1.2em;">What kind of help are you looking for?</p>', unsafe_allow_html=True)

            col_inputs = st.columns(2)
            with col_inputs[0]:
                service_type = st.selectbox(
                    "Service",
                    [
                        "housing_support",
                        "job_training",
                        "food_assistance",
                        "mental_health",
                        "legal_aid",
                        "education_support",
                        "mentorship"
                    ]
                )
            with col_inputs[1]:
                location = st.text_input("County", value="Alameda")

            question = f"Where can I find {service_type} services in {location} County?"

        st.markdown("</div>", unsafe_allow_html=True)

        # Submit Button
        st.markdown("")
        if st.button("🚀 Ask Agent", use_container_width=True, type="primary"):
            with st.spinner(f"Querying {agent_choice.replace('_', ' ').title()}..."):
                result = call_agent(agent_choice, question)

            if "error" in result:
                st.session_state.agent_error = result
                st.session_state.agent_response = None
                st.session_state.agent_reasoning = None
                st.session_state.agent_raw_result = None
            else:
                response_text, reasoning_text = parse_agent_response(result)
                st.session_state.agent_error = None
                st.session_state.agent_response = response_text
                st.session_state.agent_reasoning = reasoning_text
                st.session_state.agent_raw_result = None if response_text else result

        if st.session_state.agent_error:
            error = st.session_state.agent_error
            st.markdown("---")
            st.markdown(f"<div class='error-box'>❌ {error['error']}</div>", unsafe_allow_html=True)
            if "hint" in error:
                st.info(error["hint"])
            if "details" in error:
                with st.expander("Error details"):
                    st.code(error["details"])

        elif st.session_state.agent_response:
            st.markdown("---")
            st.markdown('<div class="response-box">', unsafe_allow_html=True)
            st.markdown(st.session_state.agent_response)
            st.markdown("</div>", unsafe_allow_html=True)

            if st.session_state.agent_reasoning:
                with st.expander("📊 View Reasoning", expanded=False):
                    st.markdown('<div class="reasoning-box">', unsafe_allow_html=True)
                    st.markdown(st.session_state.agent_reasoning)
                    st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown(f"✅ **Response received** at {datetime.now().strftime('%H:%M:%S')}")
            st.markdown("</div>", unsafe_allow_html=True)

        elif st.session_state.agent_raw_result:
            st.markdown("---")
            st.markdown(
                "<div class='error-box'>⚠️ No response text found. Raw data:</div>",
                unsafe_allow_html=True,
            )
            st.json(st.session_state.agent_raw_result)

    with col2:
        st.markdown('<div style="margin-top: 0.8em;"></div>', unsafe_allow_html=True)
        st.markdown('<div style="color: #b19cd9; font-weight: 700; margin-bottom: 0.8em;">📝 Your Query</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="query-box">{question}</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #4a5568; font-size: 0.85em;'>
    <p>LifeGraph © 2026 | Neo4j Aura Agent Hackathon</p>
    <p>Powered by Neo4j, Aura Agent, and Claude AI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
