"""
LifeGraph: AI Social Resource Navigator
Neo4j Aura Agent Hackathon Submission
Streamlit Web Application — Design 4: Conversational Chat
"""

import streamlit as st
import requests
from typing import Optional, Tuple
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="LifeGraph - AI Social Resource Navigator",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    },
}

AGENT_META = {
    "eligibility_navigator": {
        "label":      "Eligibility Navigator",
        "short":      "Eligibility",
        "question":   "What programs can I get?",
        "initials":   "EN",
        "dot":        "#7f77dd",
        "avatar_bg":  "#1a1630",
        "avatar_fg":  "#b19cd9",
        "welcome": (
            "Hello! I'm your **Eligibility Navigator**. "
            "Fill in your profile in the sidebar, then hit **Ask Agent** — "
            "I'll find every program you qualify for using the LifeGraph knowledge graph."
        ),
    },
    "pathway_advisor": {
        "label":      "Pathway Advisor",
        "short":      "Pathway",
        "question":   "What's my path to stability?",
        "initials":   "PA",
        "dot":        "#1d9e75",
        "avatar_bg":  "#0d1e18",
        "avatar_fg":  "#5dcaa5",
        "welcome": (
            "Hi! I'm your **Pathway Advisor**. "
            "Set your situation and goals in the sidebar, then hit **Ask Agent** — "
            "I'll map the best step-by-step sequence of programs to get you to stability."
        ),
    },
    "resource_locator": {
        "label":      "Resource Locator",
        "short":      "Resources",
        "question":   "Where can I find help?",
        "initials":   "RL",
        "dot":        "#ba7517",
        "avatar_bg":  "#1a1408",
        "avatar_fg":  "#ef9f27",
        "welcome": (
            "Hey! I'm your **Resource Locator**. "
            "Choose a service type and county in the sidebar, then hit **Ask Agent** — "
            "I'll surface organizations and nonprofits that can help you directly."
        ),
    },
}

# ============================================================================
# BACKEND — unchanged from original
# ============================================================================

@st.cache_data
def get_bearer_token(api_key: str, api_secret: str) -> Optional[str]:
    try:
        response = requests.post(
            "https://api.neo4j.io/oauth/token",
            auth=(api_key, api_secret),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"grant_type": "client_credentials"},
            timeout=10,
        )
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    except Exception as e:
        st.error(f"Token error: {e}")
        return None


def call_agent(agent_name: str, question: str, include_history: bool = True) -> dict:
    config = AGENT_CONFIG.get(agent_name)
    if not config or not config.get("endpoint"):
        return {
            "error": f"Agent '{agent_name}' not configured. Missing endpoint.",
            "hint": "Set env vars: {}_ENDPOINT, NEO4J_API_KEY, NEO4J_API_SECRET".format(
                agent_name.upper()
            ),
        }

    bearer_token = get_bearer_token(config["api_key"], config["api_secret"])
    if not bearer_token:
        return {"error": "Failed to authenticate with Neo4j API"}

    # Build context from conversation history
    context = ""
    if include_history:
        history = get_history(agent_name)
        if history:
            context = "Previous conversation context:\n"
            for msg in history[-4:]:  # Last 4 messages for context
                role = "User" if msg["role"] == "user" else "Agent"
                context += f"{role}: {msg['content']}\n"
            context += "\n"

    # Append question to context
    full_input = context + f"Follow-up: {question}" if context else question

    try:
        print(f"DEBUG - endpoint: {config['endpoint']}")
        print(f"DEBUG - question: {question}")
        response = requests.post(
            config["endpoint"],
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {bearer_token}",
            },
            json={"input": full_input},
            timeout=60,
        )
        print(f"DEBUG - status: {response.status_code}")

        # Handle token expiration (422 error)
        if response.status_code == 422:
            print("DEBUG - Token expired, refreshing...")
            st.cache_data.clear()  # Clear token cache
            bearer_token = get_bearer_token(config["api_key"], config["api_secret"])

            # Retry with fresh token
            response = requests.post(
                config["endpoint"],
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {bearer_token}",
                },
                json={"input": question},
                timeout=60,
            )
            print(f"DEBUG - retry status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"DEBUG - response: {str(result)[:500]}")
            return result
        else:
            print(f"DEBUG - error: {response.text}")
            return {
                "error": f"Agent returned status {response.status_code}",
                "details": response.text,
            }
    except requests.Timeout:
        return {"error": "Agent request timed out (>60s). Agent may be slow or offline."}
    except Exception as e:
        return {"error": f"Connection error: {str(e)}"}


def parse_agent_response(result: dict) -> Tuple[Optional[str], Optional[str]]:
    if not isinstance(result, dict) or "error" in result:
        return None, None
    response_parts, reasoning_parts = [], []
    content = result.get("content")
    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text" and block.get("text"):
                response_parts.append(block["text"])
            elif block.get("type") == "thinking" and block.get("thinking"):
                reasoning_parts.append(block["thinking"])
        if response_parts:
            return (
                "\n\n".join(response_parts),
                "\n\n".join(reasoning_parts) if reasoning_parts else None,
            )
    for key in ["response", "output", "text", "answer", "message", "result"]:
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
# SESSION STATE
# ============================================================================

def init_session():
    if "active_agent" not in st.session_state:
        st.session_state.active_agent = "eligibility_navigator"
    for key in AGENT_META:
        if f"history_{key}" not in st.session_state:
            st.session_state[f"history_{key}"] = []


def get_history(agent: str) -> list:
    return st.session_state.get(f"history_{agent}", [])


def push(agent: str, role: str, content: str, reasoning: str = None):
    st.session_state[f"history_{agent}"].append({
        "role": role,
        "content": content,
        "reasoning": reasoning,
        "ts": datetime.now().strftime("%H:%M"),
    })


def clear(agent: str):
    st.session_state[f"history_{agent}"] = []

# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar() -> Tuple[str, str]:
    with st.sidebar:

        # Logo + wordmark
        try:
            st.image("Images/pathfinderpulse-logo.png", width=48)
        except Exception:
            pass
        st.markdown(
            '<div class="lg-wordmark">LifeGraph</div>'
            '<div class="lg-tagline">AI Social Resource Navigator</div>',
            unsafe_allow_html=True,
        )

        # ── Agent switcher ──────────────────────────────────────
        st.markdown(
            '<span class="lg-section-label">Select an agent</span>'
            '<div style="font-size:0.75em; color:#5a5a7e; margin-bottom:8px; margin-top:2px;">'
            'Choose which AI agent to talk to</div>',
            unsafe_allow_html=True,
        )

        agent_labels = {
            "eligibility_navigator": "📋  Eligibility — What programs can I get?",
            "pathway_advisor":       "🗺️  Pathway — What's my path to stability?",
            "resource_locator":      "📍  Resources — Where can I find help?",
        }
        selected = st.radio(
            label="agent_select",
            options=list(AGENT_META.keys()),
            format_func=lambda k: agent_labels[k],
            index=list(AGENT_META.keys()).index(st.session_state.active_agent),
            key="agent_radio",
            label_visibility="collapsed",
        )
        if selected != st.session_state.active_agent:
            st.session_state.active_agent = selected
            st.rerun()

        # ── Profile inputs ──────────────────────────────────────
        st.markdown('<hr class="lg-divider">', unsafe_allow_html=True)
        st.markdown('<span class="lg-section-label">Your profile</span>', unsafe_allow_html=True)

        active = st.session_state.active_agent
        question = ""

        if active == "eligibility_navigator":
            age_col, _ = st.columns([1, 1])
            with age_col:
                age = st.number_input("Age", min_value=18, max_value=80, value=19, step=1, key="en_age")
            location = st.selectbox(
                "County",
                ["Alameda", "Los Angeles", "San Francisco", "Sacramento", "Other"],
                key="en_location",
            )
            life_event = st.selectbox(
                "Situation",
                ["AGED_OUT_OF_FOSTER_CARE","LOST_JOB","HAD_CHILD","STARTED_COLLEGE",
                 "HOMELESSNESS_RISK","DOMESTIC_VIOLENCE","SUBSTANCE_RECOVERY","OTHER"],
                key="en_event",
            )
            question = (
                f"I am {age} years old, in {location} County, "
                f"and I am experiencing {life_event}. What programs can I get?"
            )

        elif active == "pathway_advisor":
            age_col, _ = st.columns([1, 1])
            with age_col:
                age = st.number_input("Age", min_value=18, max_value=80, value=19, step=1, key="pa_age")
            location = st.text_input("County", value="Alameda", key="pa_location")
            life_event = st.selectbox(
                "Situation",
                ["AGED_OUT_OF_FOSTER_CARE","LOST_JOB","HAD_CHILD","STARTED_COLLEGE",
                 "HOMELESSNESS_RISK","DOMESTIC_VIOLENCE","SUBSTANCE_RECOVERY","OTHER"],
                key="pa_event",
            )
            goals = st.multiselect(
                "I need help with",
                ["Housing", "Employment", "Education", "Food", "Healthcare", "Childcare"],
                key="pa_goals",
            )
            goals_text = ", ".join(goals) if goals else "stability"
            question = (
                f"I am {age} years old in {location} County, experiencing {life_event}. "
                f"I need help with {goals_text}. Show me the best pathway to stability."
            )

        else:  # resource_locator
            services = st.multiselect(
                "Services needed",
                ["housing_support","job_training","food_assistance","mental_health",
                 "legal_aid","education_support","mentorship"],
                default=["housing_support"],
                key="rl_service",
            )
            location = st.text_input("County", value="Alameda", key="rl_location")
            services_text = ", ".join(services) if services else "general support"
            question = f"Where can I find {services_text} services in {location} County?"

        # Custom prompt option
        st.markdown('<div style="margin-top: 1.2em;"></div>', unsafe_allow_html=True)
        use_custom = st.checkbox("✏️ Edit question", key=f"custom_{active}")

        if use_custom:
            question = st.text_area(
                "Edit your question",
                value=question,
                placeholder="e.g., What programs help people with housing and employment?",
                height=80,
                key=f"custom_prompt_{active}"
            )

        # Query preview
        st.markdown(
            f'<div class="lg-query-preview">{question if question else "(No question entered)"}</div>',
            unsafe_allow_html=True,
        )

        # Status indicator
        st.markdown(
            '<div class="lg-status">'
            '<span class="lg-status-dot"></span>3 agents online · Neo4j Aura'
            '</div>',
            unsafe_allow_html=True,
        )

    return st.session_state.active_agent, question

# ============================================================================
# CHAT RENDERING
# ============================================================================

def render_chat_header(agent: str):
    meta = AGENT_META[agent]
    header_left, header_right = st.columns([5, 1])

    with header_left:
        st.markdown(
            f"""<div class="lg-chat-header">
                  <div class="lg-chat-avatar"
                       style="background:{meta['avatar_bg']}; color:{meta['avatar_fg']};">
                    {meta['initials']}
                  </div>
                  <div>
                    <div class="lg-chat-name">{meta['label']}</div>
                    <div class="lg-chat-online">Online · Neo4j knowledge graph</div>
                  </div>
                </div>""",
            unsafe_allow_html=True,
        )

    with header_right:
        st.markdown('<div style="text-align: right; padding-top: 8px;">', unsafe_allow_html=True)
        if st.button("🗑️ Clear", key="clear_header_btn", use_container_width=True):
            clear(agent)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def render_messages(agent: str):
    meta   = AGENT_META[agent]
    history = get_history(agent)

    if not history:
        # Welcome bubble
        st.markdown(
            f"""<div class="lg-msg-wrap">
                  <div class="lg-avatar"
                       style="background:{meta['avatar_bg']}; color:{meta['avatar_fg']};">
                    {meta['initials']}
                  </div>
                  <div>
                    <div class="lg-bubble agent">{meta['welcome']}</div>
                    <div class="lg-ts">Now</div>
                  </div>
                </div>""",
            unsafe_allow_html=True,
        )
        return

    for msg in history:
        role    = msg["role"]
        content = msg["content"]
        ts      = msg.get("ts", "")
        reasoning = msg.get("reasoning")

        if role == "user":
            st.markdown(
                f"""<div class="lg-msg-wrap user">
                      <div class="lg-avatar" style="background:#1e1640; color:#b0a0e0;">You</div>
                      <div>
                        <div class="lg-bubble user">{content}</div>
                        <div class="lg-ts">{ts}</div>
                      </div>
                    </div>""",
                unsafe_allow_html=True,
            )

        elif role == "agent":
            # Avatar + open bubble wrapper
            st.markdown(
                f"""<div class="lg-msg-wrap">
                      <div class="lg-avatar"
                           style="background:{meta['avatar_bg']}; color:{meta['avatar_fg']};">
                        {meta['initials']}
                      </div>
                      <div style="flex:1; min-width:0;">
                        <div class="lg-bubble agent">""",
                unsafe_allow_html=True,
            )
            # Let Streamlit render markdown natively (respects bold, lists, etc.)
            st.markdown(content)
            st.markdown("</div>", unsafe_allow_html=True)  # close .lg-bubble

            if reasoning:
                with st.expander("📖 View graph reasoning"):
                    st.markdown(
                        f'<div class="lg-reasoning">{reasoning}</div>',
                        unsafe_allow_html=True,
                    )

            st.markdown(
                f'<div class="lg-ts">{ts}</div></div></div>',
                unsafe_allow_html=True,
            )

        elif role == "error":
            st.markdown(
                f"""<div class="lg-msg-wrap">
                      <div class="lg-avatar"
                           style="background:{meta['avatar_bg']}; color:{meta['avatar_fg']};">
                        {meta['initials']}
                      </div>
                      <div>
                        <div class="lg-bubble error">❌ {content}</div>
                        <div class="lg-ts">{ts}</div>
                      </div>
                    </div>""",
                unsafe_allow_html=True,
            )

        elif role == "raw":
            st.markdown(
                """<div class="lg-msg-wrap">
                     <div class="lg-avatar" style="background:#160808; color:#e08080;">!</div>
                     <div>
                       <div class="lg-bubble error">
                         ⚠️ Response received but no text could be extracted.
                       </div>
                     </div>
                   </div>""",
                unsafe_allow_html=True,
            )
            with st.expander("Raw API response"):
                st.json(content)

# ============================================================================
# MAIN
# ============================================================================

def main():
    init_session()

    active_agent, question = render_sidebar()
    meta = AGENT_META[active_agent]

    # Config gate
    if not all(AGENT_CONFIG[a].get("endpoint") for a in AGENT_CONFIG):
        st.markdown(
            """<div class="lg-config-warning">
               ⚠️ <strong>Agents not configured.</strong><br><br>
               Set these environment variables:<br>
               <code>ELIGIBILITY_AGENT_ENDPOINT</code>&nbsp;
               <code>PATHWAY_AGENT_ENDPOINT</code>&nbsp;
               <code>RESOURCE_AGENT_ENDPOINT</code><br>
               <code>NEO4J_API_KEY</code>&nbsp;
               <code>NEO4J_API_SECRET</code><br><br>
               See <code>STREAMLIT_SETUP_GUIDE.md</code> for instructions.
               </div>""",
            unsafe_allow_html=True,
        )
        return

    # ── Chat header bar ─────────────────────────────────────────
    render_chat_header(active_agent)

    # ── Status placeholder (for processing indicator) ──────────────
    status_placeholder = st.empty()

    # ── Scrollable message area ─────────────────────────────────
    # Reduced height to keep input bar visible
    msg_container = st.container(height=380, border=False)
    with msg_container:
        render_messages(active_agent)


    # ── Get conversation history ──────────────────────────────────
    history = get_history(active_agent)
    has_conversation = len(history) > 0

    # ── Input section ──────────────────────────────────────────────
    st.markdown('<div class="lg-input-bar">', unsafe_allow_html=True)

    if not has_conversation:
        # INITIAL QUESTION - Pre-populated with sidebar selections
        st.markdown('<span style="font-size:0.85em; color:#8892a4; margin-bottom:8px; display:block;">Your question</span>', unsafe_allow_html=True)
        user_input = st.text_area(
            "question_input",
            value=question,
            placeholder="Edit or ask your question...",
            height=80,
            key="initial_question",
            label_visibility="collapsed"
        )

        col_submit, col_clear = st.columns([4, 1])
        with col_submit:
            ask = st.button("Ask Agent ›", key="ask_btn", type="primary", use_container_width=True)
        with col_clear:
            if st.button("Reset", key="reset_btn", use_container_width=True):
                clear(active_agent)
                st.rerun()

        question_to_ask = user_input if user_input.strip() else question
    else:
        # FOLLOW-UP QUESTION - After conversation started
        st.markdown('<span style="font-size:0.85em; color:#8892a4; margin-bottom:8px; display:block;">Follow-up question</span>', unsafe_allow_html=True)
        question_to_ask = st.text_area(
            "followup_input",
            value="",
            placeholder="Ask a follow-up question...",
            height=60,
            key="followup_question",
            label_visibility="collapsed"
        )

        col_submit, col_clear = st.columns([4, 1])
        with col_submit:
            ask = st.button("Ask Agent ›", key="ask_btn", type="primary", use_container_width=True)
        with col_clear:
            if st.button("New Conversation", key="new_conv_btn", use_container_width=True):
                clear(active_agent)
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)  # close lg-input-bar

    # ── Handle ask ──────────────────────────────────────────────
    if ask and question_to_ask.strip():
        push(active_agent, "user", question_to_ask)

        # Show processing status at the top
        status_placeholder.markdown(
            f'<div style="background:#1a1630; border-left:3px solid #b19cd9; '
            f'padding:12px 16px; border-radius:6px; color:#c9d1d9; font-size:0.9em; margin-bottom:12px;">'
            f'⏳ <strong>Processing...</strong> Querying {meta["label"]}'
            f'</div>',
            unsafe_allow_html=True,
        )

        result = call_agent(active_agent, question_to_ask)

        # Clear the status placeholder
        status_placeholder.empty()

        if "error" in result:
            err = result["error"]
            if "hint" in result:
                err += f"<br><small style='opacity:0.7'>{result['hint']}</small>"
            push(active_agent, "error", err)
        else:
            text, reasoning = parse_agent_response(result)
            if text:
                push(active_agent, "agent", text, reasoning=reasoning)
            else:
                push(active_agent, "raw", result)

        st.rerun()

    # ── Footer ──────────────────────────────────────────────────
    st.markdown(
        """<div class="lg-footer">
           LifeGraph © 2026 &nbsp;·&nbsp; Neo4j Aura Agent Hackathon<br>
           Powered by Neo4j · Aura Agent · Claude AI
           </div>""",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()