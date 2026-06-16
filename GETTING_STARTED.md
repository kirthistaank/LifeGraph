# LifeGraph Getting Started Guide
## Step-by-Step Setup Instructions

---

## Overview

This guide walks you through setting up LifeGraph locally on your machine. The process has three main stages:

1. **Data Loading** - Populate Neo4j database with programs, organizations, and rules
2. **Agent Configuration** - Create and configure three AI agents
3. **Web App Deployment** - Run the Streamlit dashboard

**Total Time:** 15-20 minutes (most is waiting for Neo4j operations)

**Prerequisites:**
- Python 3.8+
- Neo4j Aura account (free tier works)
- Neo4j credentials (API key + secret)
- Git (optional, for cloning repo)

---

## Prerequisites Setup

### 1. Create a Neo4j Aura Instance

If you don't have a Neo4j Aura database yet:

1. Go to https://console.neo4j.io
2. Sign up or log in
3. Click "Create Database"
4. Select "Neo4j 5.x" and "Free tier"
5. Name it "LifeGraph"
6. Note your credentials:
   - **Database URI** - Format: `neo4j+s://xxxxxxxx.databases.neo4j.io`
   - **Username** - Usually `neo4j`
   - **Password** - Generated at creation

### 2. Create Neo4j API Credentials

For the agent setup, you'll need API credentials (different from database credentials):

1. In Neo4j Console, go to **Account Settings**
2. Navigate to **API Keys** (or **Developer Tools**)
3. Create a new API key
4. Note:
   - **API Key** (Client ID)
   - **API Secret**

**Keep all credentials safe** - you'll need them for `.env` file.

---

## Installation Steps

### Step 0: Clone Repository & Install Dependencies

```bash
# Navigate to LifeGraph directory
cd LifeGraph

# Install Python dependencies
pip install -r requirements.txt
```

**What gets installed:**
- `streamlit>=1.28.0` - Web framework
- `requests>=2.31.0` - HTTP client for API calls
- `python-dotenv>=1.0.0` - Environment variable management
- Neo4j driver (installed automatically by data_loader.py)

---

### Step 1: Load Graph Data

**What this does:** Inserts 127 nodes (programs, organizations, rules, outcomes) and 246 relationships into Neo4j.

**Time:** 2-3 minutes

#### Option A: Using Environment Variables

```bash
# Set environment variables
export NEO4J_URI="neo4j+s://your-aura-database-id.databases.neo4j.io"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your-password-here"

# Run data loader
python data_loader.py
```

#### Option B: Create `.env` File (Recommended)

Create a file named `.env` in the LifeGraph directory:

```
NEO4J_URI=neo4j+s://your-aura-database-id.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password-here
NEO4J_API_KEY=your-api-key-here
NEO4J_API_SECRET=your-api-secret-here
```

Then run:
```bash
python data_loader.py
```

**The loader will:**
- Create 12 LifeEvent nodes (AGED_OUT_OF_FOSTER_CARE, LOST_JOB, etc.)
- Create 45+ Benefit nodes (CalFresh, Extended Foster Care, Job Corps, etc.)
- Create 35+ Organization nodes (First Place for Youth, Job Corps Oakland, etc.)
- Create 20+ EligibilityRule nodes (age limits, income caps, etc.)
- Create 15+ Document nodes (birth certificate, ID, proof of income, etc.)
- Create 10+ Outcome nodes (HOUSING_SECURED, EMPLOYED, etc.)
- Establish 246 relationships (TRIGGERS, UNLOCKS, REQUIRES, HAS_RULE, LEADS_TO, SERVES, PROVIDES)

**Expected Output:**
```
INFO:root:Connected to Neo4j Aura
INFO:root:Creating life events...
INFO:root:Creating benefits...
INFO:root:Creating organizations...
[... more creation steps ...]
INFO:root:Data loading complete!
INFO:root:Total nodes created: 127
INFO:root:Total relationships created: 246
```

**Troubleshooting:**
- If you get connection errors, verify your NEO4J_URI, username, and password
- If you see timeout errors, your Aura instance may still be starting (wait 1-2 minutes)
- Check that public access is enabled on your Aura instance in console

---

### Step 2: Configure Aura Agents

**What this does:** Creates three specialized AI agents that can reason over the graph:
1. **Eligibility Navigator** - Answers "What programs can I get?"
2. **Pathway Advisor** - Answers "What's my path to stability?"
3. **Resource Locator** - Answers "Where can I find help?"

**Time:** 1-2 minutes

```bash
python agent_setup.py
```

**What happens:**
- Authenticates with Neo4j API using your credentials
- Creates three agents with Cypher templates
- Configures Text2Cypher for dynamic queries
- Registers agents for use in the Streamlit app

**Expected Output:**
```
INFO:root:Creating Eligibility Navigator agent...
INFO:root:Agent created: agent-uuid-1234...
INFO:root:Creating Pathway Advisor agent...
INFO:root:Agent created: agent-uuid-5678...
INFO:root:Creating Resource Locator agent...
INFO:root:Agent created: agent-uuid-9012...
INFO:root:Agent setup complete!
```

**After this step, you need to:**
1. Go to https://console.neo4j.io
2. Navigate to **Agents** section
3. For each agent, enable **External Access** (checkbox in agent details)
4. Note the agent UUIDs and place them in `.env`

**Troubleshooting:**
- If agent creation fails, verify NEO4J_API_KEY and NEO4J_API_SECRET
- If agents don't appear in console, wait 30-60 seconds for API sync
- Check Neo4j console logs for more details

---

### Step 3: Configure Environment for Web App

Update your `.env` file with agent UUIDs from Neo4j Console:

```env
# Database credentials
NEO4J_URI=neo4j+s://your-aura-database-id.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password-here

# API credentials (for agent management)
NEO4J_API_KEY=your-api-key
NEO4J_API_SECRET=your-api-secret

# Agent UUIDs (from Neo4j Console)
ELIGIBILITY_NAVIGATOR_AGENT_ID=agent-uuid-1234
PATHWAY_ADVISOR_AGENT_ID=agent-uuid-5678
RESOURCE_LOCATOR_AGENT_ID=agent-uuid-9012

# OAuth configuration (if using)
OAUTH_CLIENT_ID=your-oauth-client-id
OAUTH_CLIENT_SECRET=your-oauth-client-secret
```

**Note:** The Streamlit app automatically loads these via `dotenv.load_dotenv()` at startup.

---

### Step 4: Run the Web Application

```bash
streamlit run streamlit_app.py
```

**Expected Output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://your-ip:8501
```

**What happens:**
1. Browser opens to http://localhost:8501
2. You see three dropdown menus on the left:
   - Life Event (AGED_OUT_OF_FOSTER_CARE, LOST_JOB, etc.)
   - Location (Oakland, Alameda County, etc.)
   - Agent (Eligibility Navigator, Pathway Advisor, Resource Locator)
3. A pre-populated question appears based on your selections
4. Click "Ask Agent" to submit
5. Agent response appears below

**First Test Query:**
1. Select Life Event: "AGED_OUT_OF_FOSTER_CARE"
2. Select Location: "Alameda"
3. Select Agent: "Pathway Advisor"
4. Click "Ask Agent"
5. You should see a multi-step pathway to stability

---

## Testing Your Setup

### Quick Verification Checklist

- [ ] Data loaded: Neo4j Console shows 127 nodes
- [ ] Agents created: 3 agents visible in Neo4j Console
- [ ] Agents enabled: "External Access" is ON for each agent
- [ ] Environment variables: `.env` file has all required variables
- [ ] Streamlit runs: `streamlit run streamlit_app.py` starts without errors
- [ ] Web app loads: http://localhost:8501 opens in browser
- [ ] Agent responds: Query returns meaningful results

### Manual Database Verification

If you want to verify data was loaded, use the Neo4j Console:

**Query 1: Count nodes by type**
```cypher
MATCH (n)
RETURN labels(n)[0] as type, count(*) as count
ORDER BY count DESC
```

**Query 2: View LifeEvent triggers**
```cypher
MATCH (event:LifeEvent)-[:TRIGGERS]->(program:Benefit)
WHERE event.name = 'AGED_OUT_OF_FOSTER_CARE'
RETURN event.name, program.name
```

**Query 3: Complete pathway**
```cypher
MATCH path = (event:LifeEvent)-[:TRIGGERS]->(:Benefit)
            -[:UNLOCKS*1..3]->(:Benefit)
            -[:LEADS_TO]->(outcome:Outcome)
WHERE event.name = 'AGED_OUT_OF_FOSTER_CARE'
RETURN path
```

---

## Troubleshooting Common Issues

### Issue: "ModuleNotFoundError: No module named 'neo4j'"

**Solution:**
```bash
pip install neo4j
```

### Issue: "Connection refused" or "Could not connect to Neo4j"

**Causes:**
- Database URI is incorrect
- Credentials are wrong
- Database is still starting up
- Network connectivity issue

**Solution:**
1. Verify URI format: `neo4j+s://xxxxx.databases.neo4j.io` (not `neo4j://`)
2. Test credentials in Neo4j Console directly
3. Wait 1-2 minutes for Aura instance to fully start
4. Check internet connection
5. Verify firewall isn't blocking Neo4j ports

### Issue: "Agent request timed out (>30 seconds)"

**Causes:**
- Agent UUID not configured
- Agent doesn't have external access enabled
- Neo4j is busy processing query

**Solution:**
1. Verify agent UUID in `.env` matches Console
2. In Neo4j Console, check "External Access" is enabled for agent
3. Wait a moment and retry

### Issue: "Token has invalid claims: token is expired"

**Causes:**
- API credentials are wrong
- Token was generated for different environment

**Solution:**
1. Regenerate API key/secret in Neo4j Console account settings
2. Update `.env` with new credentials
3. Restart Streamlit app: `Ctrl+C` then `streamlit run streamlit_app.py`

### Issue: "Agent response not displaying in UI"

**Causes:**
- Streamlit cache issue
- Agent returning unexpected format
- JavaScript issue in browser

**Solution:**
1. Clear Streamlit cache: Delete `~/.streamlit/` directory
2. Hard refresh browser: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+F5` (Windows)
3. Check browser console for JavaScript errors
4. Restart Streamlit app

### Issue: "FollowUp questions not understood"

**Problem:** User asks "yes" and agent doesn't know what question it's responding to

**Solution:** This is fixed in the current version. The app automatically includes conversation history in follow-up questions as context so agents understand multi-turn conversations.

---

## Development & Customization

### Adding New Programs

1. Edit `data_loader.py` - Add to `self.create_benefits()` method
2. Add eligibility rules in `self.create_eligibility_rules()`
3. Link to organizations in `self.create_provides_relationships()`
4. Reload: `python data_loader.py`

See `DATASOURCES.md` for guidelines on verified sources.

### Modifying Agent Behaviors

Agents are configured in `agent_setup.py` with:
- Cypher templates (hard-coded query patterns)
- Text2Cypher (dynamic question-to-Cypher conversion)
- System prompts (instructions for how agents reason)

To modify agent behavior:
1. Edit the relevant section in `agent_setup.py`
2. Re-run: `python agent_setup.py`
3. In Neo4j Console, delete old agent and create new one

### Customizing UI

The Streamlit app (`streamlit_app.py`) has:
- Sidebar dropdowns for user selection
- Custom CSS styling (`css/styles_woven_thread.css`)
- Conversation history management

Modify:
- Dropdown options: `st.sidebar.selectbox()` calls
- Styling: Edit `css/styles_woven_thread.css`
- Agent responses: Agent response parsing logic

---

## Understanding the Design Patterns

LifeGraph is built on eight core AI architecture patterns. Understanding these helps you modify and extend the system effectively.

**See `DESIGN_PATTERNS.md` for detailed documentation on:**
- **ReAct (Reasoning + Acting)** — How agents observe and reason iteratively
- **Plan-Execute Decomposition** — Multi-phase task reasoning
- **Agent Orchestration** — Why three specialist agents instead of one
- **Graph-Augmented LLM** — How the graph prevents hallucination
- **Multi-Hop Traversal** — Discovering hidden program sequences
- **Template-Based Reasoning** — Pre-built query patterns
- **Conversation Context Management** — Multi-turn dialogue
- **Domain-Specific Reasoning** — Knowledge encoded in the graph

**Quick takeaway:** These patterns work together to make LifeGraph reliable (grounded in verified data), intelligent (reasoning over relationships), and maintainable (domain knowledge is the graph structure, not buried in prompts).

For developers modifying agent behavior or extending the graph, understanding these patterns will help you make better architectural decisions.

---

## Next Steps

After setup:

1. **Test the app thoroughly** - Try all agent roles and life events
2. **Deploy to production** - See deployment options below
3. **Extend with more data** - Add new programs and organizations
4. **Add more agents** - Create agents for other user groups (veterans, single parents, etc.)

---

## Deployment Options

### Option 1: Local Testing (Development)

Already done with `streamlit run streamlit_app.py`

### Option 2: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501"]
```

Build and run:
```bash
docker build -t lifegraph .
docker run -p 8501:8501 --env-file .env lifegraph
```

### Option 3: Heroku Deployment

1. Create `Procfile`:
```
web: streamlit run streamlit_app.py --logger.level=debug --client.showErrorDetails=false
```

2. Push to Heroku:
```bash
heroku login
heroku create lifegraph-app
git push heroku main
```

### Option 4: Streamlit Cloud

1. Push repo to GitHub
2. Go to https://streamlit.io/cloud
3. Connect GitHub repo
4. Select branch and main file (`streamlit_app.py`)
5. Add environment variables in Settings
6. Deploy

---

## Performance Tuning

### Database Query Performance

Current setup handles:
- **Response time:** <100ms for multi-hop queries (127 nodes)
- **Concurrent users:** 10+ (Neo4j Aura free tier)
- **Query complexity:** Up to 4-hop pathways

To improve:
1. Add indexes in Neo4j (automatic with setup)
2. Increase Aura instance size (paid tier)
3. Cache common queries in Streamlit

### Streamlit Performance

- Clear session cache regularly: `st.cache_data.clear()`
- Use `@st.cache_data` for expensive operations
- Lazy-load agent responses (already implemented)

---

## File Reference

| File | Purpose | Created By |
|------|---------|-----------|
| `data_loader.py` | Load 127 nodes and 246 relationships | User runs this |
| `agent_setup.py` | Create 3 AI agents in Neo4j | User runs this |
| `streamlit_app.py` | Web dashboard for users | Auto-runs with `streamlit run` |
| `.env` | Environment variables (credentials) | User creates this |
| `requirements.txt` | Python dependencies | `pip install -r requirements.txt` |
| `ARCHITECTURE.md` | Graph schema and design | Reference documentation |
| `DATASOURCES.md` | Data sources and validation | Reference documentation |
| `README.md` | Project overview | Reference documentation |

---

## Getting Help

### Common Questions

**Q: Do I need a paid Neo4j plan?**
A: No, free tier (2GB) is enough for LifeGraph (127 nodes). Upgrade only if you add more data or scale to many users.

**Q: Can I use a local Neo4j instance instead of Aura?**
A: Yes, but you'd need to manually set up agents. Aura makes agent creation easier. Local Neo4j steps are similar—just use `neo4j://localhost:7687` as URI.

**Q: How long does data loading take?**
A: 2-3 minutes for all 127 nodes. The loader shows progress messages.

**Q: Can I modify agent behavior after setup?**
A: Yes. Edit `agent_setup.py`, delete old agents in Console, run setup again.

**Q: How do I delete all data and start fresh?**
A: In Neo4j Console, run `MATCH (n) DETACH DELETE n;` then re-run `data_loader.py`.

### Support

- **Data issues?** Check `DATASOURCES.md` for source information
- **Graph design questions?** Read `ARCHITECTURE.md` for schema details
- **Setup problems?** Review troubleshooting section above
- **Feature requests?** Submit pull request with changes

---

## See Also

- **Architecture:** `ARCHITECTURE.md`
- **Data Sources:** `DATASOURCES.md`
- **Project Overview:** `README.md`
- **Full Submission:** `../submission/FINAL_SUBMISSION.md`

---

**Last Updated:** June 2025 | Tested with Python 3.10, Streamlit 1.28.1, Neo4j Aura
