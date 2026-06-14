# LifeGraph: AI Social Resource Navigator

**A Neo4j knowledge graph + AI agents that help foster youth navigate 25+ social programs and find their path to stability.**

---

## Quick Start

### What Problem Does This Solve?

Millions of foster youth qualify for life-changing assistance but can't find it. Programs are fragmented across agencies, eligibility rules are opaque, and crucially—**no one knows which programs unlock access to others**.

LifeGraph solves this by building relationships between programs and showing the **sequence to stability**.

### Try It Now

**Three AI agents work together:**

1. **Eligibility Navigator** - "What programs can I get?"
   - Shows programs you qualify for based on age, location, life event
   - Explains eligibility requirements and documents needed

2. **Pathway Advisor** - "What's my path to stability?"
   - Maps multi-hop sequences: Program A → unlocks Program B → leads to Outcome
   - Shows step-by-step action plan with timelines

3. **Resource Locator** - "Where can I find help?"
   - Lists organizations and nonprofits providing programs
   - Includes contact info, services, eligibility notes

---

## Try This Example

**Query:** "I'm 19, aging out of foster care in Alameda County. What's my path to stability?"

**Agent Response:**
```
Step 1: Extended Foster Care
  ✓ You qualify (age 19, aged out)
  ✓ Provides housing and benefits until age 21

Step 2: This unlocks Transportation Assistance
  ✓ Free bus passes to attend job training

Step 3: Join Job Corps (now accessible)
  ✓ Free training + $500/month stipend
  ✓ Leads to employment

Outcome: Income + housing = financial stability within 6 months
```

**How it works:** Graph traversal finds the chain: AGED_OUT → TRIGGERS Extended_Foster_Care → UNLOCKS Transportation → ENABLES Job_Corps → LEADS_TO EMPLOYED

---

## Architecture

| Layer | Component | Purpose |
|-------|-----------|---------|
| **Data** | 127 nodes, 246 relationships | Programs, eligibility rules, organizations |
| **Graph** | Neo4j Aura | Knowledge graph with 7 relationship types |
| **Reasoning** | Aura Agents (3x) | Specialized agents with Cypher templates |
| **UI** | Streamlit | Web interface for querying agents |

---

## Files

- **`LIFEGRAPH_SUBMISSION.md`** - Hackathon submission (technical details)
- **`README.md`** - This file (quick overview)
- **`DATASOURCES.md`** - Where data came from (6 official sources)
- **`ARCHITECTURE.md`** - Graph schema and relationship types
- **`GETTING_STARTED.md`** - How to set up locally
- **`data_loader.py`** - Load all 127 nodes programmatically
- **`agent_setup.py`** - Configure all 3 agents
- **`test_agents.ipynb`** - Jupyter notebook to test agents
- **`streamlit_app.py`** - Web dashboard

---

## Setup (3 Steps)

### 1. Load Data
```bash
export NEO4J_URI="neo4j+s://your-aura-db.com"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your-password"

python data_loader.py
```

### 2. Configure Agents
```bash
export NEO4J_API_KEY="your-api-key"
export NEO4J_API_SECRET="your-secret"

python agent_setup.py
```

### 3. Run Web App
```bash
streamlit run streamlit_app.py
```

---

## Data

**127 nodes from 6 official sources:**
- CalFresh, WIC, Medi-Cal, Extended Foster Care, Job Corps, Housing Vouchers, etc.
- 10 organizations (First Place for Youth, Job Corps Oakland, etc.)
- 25 benefits + 20 eligibility rules + 12 life events
- 246 relationships mapping program chains

See `DATASOURCES.md` for official sources.

---

## For Judges

1. **Open Aura Console:** https://console.neo4j.io
2. **Navigate to Agents** → LifeGraph agents
3. **Try this query:** "I'm 19 in Oakland, aged out of foster care. What's my best path?"
4. **Watch reasoning trace:** See how agents traverse the graph

---

## Key Design

### Why Graphs Matter Here

Traditional resource navigator: "You might qualify for CalFresh, Job Corps, Housing"

**LifeGraph discovers:**
- Program A unlocks B (because of relationship in graph)
- Sequence matters (apply to housing first, then training)
- Multi-hop dependencies (4+ steps to stability)

### Why 3 Agents?

1. **Focused roles** - each agent solves one problem
2. **Reusable tools** - Cypher templates shared
3. **Testable independently** - easier debugging
4. **Scalable** - add agents for veterans, single parents, etc.

---

## Tech Stack

- **Database:** Neo4j Aura (free tier)
- **Agents:** Neo4j Aura Agent Framework
- **Tools:** Cypher Templates + Text2Cypher
- **Web:** Streamlit (Python)
- **Data:** Public CA government sources

---

## What's Next?

- [ ] Load data: `python data_loader.py`
- [ ] Configure agents: `python agent_setup.py`  
- [ ] Test in notebook: `jupyter notebook test_agents.ipynb`
- [ ] Run web app: `streamlit run streamlit_app.py`
- [ ] Deploy: See `GETTING_STARTED.md`

---

## See Also

- **Full submission:** `LIFEGRAPH_SUBMISSION.md`
- **Data sources:** `DATASOURCES.md`
- **Graph design:** `ARCHITECTURE.md`
- **Setup guide:** `GETTING_STARTED.md`

---

**Neo4j Aura Agent Hackathon 2026** | Helping foster youth navigate social services through graph reasoning
