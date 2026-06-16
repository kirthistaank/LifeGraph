# LifeGraph Design Patterns
## AI Architecture for Graph-Based Reasoning

This document outlines the design patterns that power LifeGraph, a system for navigating fragmented social services through intelligent graph reasoning.

---

## Overview

LifeGraph is built on eight core design patterns that work together to create a system that is simultaneously intelligent, reliable, and maintainable. These patterns are not unique to LifeGraph—they represent best practices in AI system design—but their specific composition creates a solution uniquely suited to the problem of reasoning over interconnected services.

---

## The Eight Core Patterns

### 1. ReAct (Reasoning + Acting)

**Pattern Name:** ReAct Loop

**Description:**
The agent follows a cycle: Reason → Act → Observe → Reason. Each step is grounded in observed facts rather than generated from memory.

**In LifeGraph:**
```
User Input
  ↓
[REASON] Agent understands the question type
  ↓
[ACT] Agent executes a Cypher query
  ↓
[OBSERVE] Agent receives results from graph
  ↓
[REASON] Agent reasons about results and next steps
  ↓
Output to User
```

**Example:**
- User: "What programs can I get?"
- Reason: "This is an eligibility question; I need TRIGGERS relationships"
- Act: Execute MATCH (event:LifeEvent)-[:TRIGGERS]->(program:Benefit)...
- Observe: Got 5 programs back
- Reason: "Should I explain what these unlock?"
- Act: Follow UNLOCKS relationships
- Return: Complete eligibility and pathway information

**Benefits:**
- Grounds every answer in verified data
- Reduces hallucination (agent responds to observations, not generates from memory)
- Transparent reasoning (you can see each step)
- Iterative refinement (agent can pursue follow-ups)

**Related Patterns:** Graph-Augmented LLM

---

### 2. Plan-Execute Decomposition

**Pattern Name:** Two-Phase Task Decomposition

**Description:**
Complex tasks are broken into two phases: Planning (what will I do?) and Execution (now do it step-by-step).

**In LifeGraph:**
The Pathway Advisor receives: "I'm 19, aged out of foster care. What's my path to stability?"

**Plan Phase:**
- Step 1: Find programs triggered by life event
- Step 2: Discover what each program unlocks
- Step 3: Find outcomes each path leads to
- Step 4: Locate organizations providing these programs

**Execute Phase:**
- Query 1: Get triggered programs
- Query 2: For each program, find UNLOCKS chains
- Query 3: Find outcomes
- Query 4: Find organization details
- Narrative assembly: Present as coherent sequence

**Benefits:**
- Forces holistic thinking before acting
- Prevents scattered, incomplete answers
- Creates coherent multi-step narratives
- Easier to debug (failures are localized to specific phases)

**Related Patterns:** Agent Orchestration

---

### 3. Agent Orchestration

**Pattern Name:** Specialized Agent Pool

**Description:**
Instead of one generalist agent, use multiple specialist agents, each an expert in one domain.

**In LifeGraph:**
Three agents handle three distinct reasoning tasks:

**Eligibility Navigator**
- Question: "What programs can I get?"
- Focus: TRIGGERS relationships (direct eligibility)
- Strength: Fast, accurate answers to basic eligibility

**Pathway Advisor**
- Question: "What's my path to stability?"
- Focus: TRIGGERS → UNLOCKS chains → outcomes
- Strength: Multi-hop reasoning, sequence discovery

**Resource Locator**
- Question: "Where can I find help?"
- Focus: SERVES and PROVIDES relationships
- Strength: Connecting abstract programs to concrete organizations

**Benefits:**
- Simpler agents (narrower domain = easier reasoning)
- Better domain expertise (specialist beats generalist)
- Easier debugging (failure isolation)
- Independent optimization (tune each agent separately)
- Graceful degradation (if one fails, others still work)

**Related Patterns:** Domain-Specific Reasoning

---

### 4. Graph-Augmented LLM

**Pattern Name:** Verified Reasoning Over Data

**Description:**
The LLM doesn't generate answers from memory. Instead, it reasons over verified data retrieved from the graph.

**Flow:**
```
User Question
  ↓
LLM: Parse intent and entities
  ↓
LLM: Generate or execute Cypher query
  ↓
Graph: Return results
  ↓
LLM: Reason over results
  ↓
LLM: Generate explanation
  ↓
User: Gets answer grounded in graph data
```

**In LifeGraph:**
- User: "Does Extended Foster Care unlock housing assistance?"
- LLM doesn't say: "I think so, based on my training"
- LLM says: "Let me check the graph"
- Query: MATCH (p1:Benefit)-[:UNLOCKS]->(p2:Benefit) WHERE p1.name = 'Extended_Foster_Care'...
- Result: Yes, confirms Extended Foster Care unlocks Transportation Assistance
- LLM: "Yes, Extended Foster Care unlocks Transportation Assistance because..."

**Benefits:**
- Eliminates hallucination (answers come from data, not generation)
- Verifiable reasoning (query is auditable)
- Current information (graph is authoritative source)
- Confidence scores (based on data presence, not probability)

**Comparison:**
- Traditional LLM: "Based on my training, I believe..."
- Graph-Augmented LLM: "The graph confirms..."

**Related Patterns:** ReAct, Template-Based Reasoning

---

### 5. Multi-Hop Traversal

**Pattern Name:** Relationship Chain Discovery

**Description:**
Following chains of relationships to discover indirect connections users wouldn't find via linear search.

**In LifeGraph:**
```
START: User qualifies for Extended Foster Care
  ↓ UNLOCKS
Step 2: Transportation Assistance (program 1)
  ↓ UNLOCKS
Step 3: Job Corps (program 2)
  ↓ LEADS_TO
Step 4: Employment (outcome)

User gets: Complete 4-step pathway, not 3 separate programs
```

**Graph Query:**
```cypher
MATCH path = (event:LifeEvent)-[:TRIGGERS]->(:Benefit)
            -[:UNLOCKS*1..3]->(:Benefit)
            -[:LEADS_TO]->(outcome:Outcome)
WHERE event.name = 'AGED_OUT_OF_FOSTER_CARE'
RETURN path
```

**The `-[:UNLOCKS*1..3]` means: follow UNLOCKS relationships 1 to 3 hops deep**

**Benefits:**
- Discovers hidden value (programs that unlock other programs)
- Reveals sequences (not just lists)
- Shows interdependencies (why programs matter together)
- Enables complete planning (user sees full path, not just next step)

**Related Patterns:** Graph-Augmented LLM, ReAct

---

### 6. Template-Based Reasoning

**Pattern Name:** Structured Query Templates

**Description:**
Pre-built Cypher templates provide structure and guarantees. The LLM fills in dynamic parts, not generates entire queries.

**Template Example:**
```cypher
MATCH (event:LifeEvent)-[:TRIGGERS]->(program:Benefit)
WHERE event.name = $life_event
RETURN program.name, program.eligibility_summary, program.description
```

**LLM's Job:**
- Understand the user's question
- Fill in `$life_event` with the matched life event
- Execute the template
- Interpret results

**LLM Does NOT Do:**
- Generate arbitrary Cypher
- Invent relationship types
- Create invalid query structures

**Benefits:**
- Guarantees syntactic correctness (all templates are valid)
- Prevents invalid relationships (can only use pre-defined templates)
- Performance (no query generation overhead)
- Auditability (see exactly what query ran)
- Safety (constrained to templates, no arbitrary queries)

**Related Patterns:** Graph-Augmented LLM

---

### 7. Conversation Context Management

**Pattern Name:** Stateful Multi-Turn Dialogue

**Description:**
Maintaining conversation state across multiple turns so follow-up questions make sense in context.

**In LifeGraph:**
```
Turn 1:
User: "What programs can I get?"
Agent: Returns eligibility info
Context stored: [user message, agent response]

Turn 2:
User: "Yes, what comes next?"
Agent: Remembers Turn 1, builds on it
Context available: Last 4 messages
Response: Explains what each program unlocks
Context stored: [previous + new exchange]
```

**Implementation:**
```python
# Store last 4 messages in context
context = "Previous conversation context:\n"
for msg in history[-4:]:
    context += f"User: {msg['user']}\nAgent: {msg['agent']}\n"

# Prepend to current question
full_input = context + f"Follow-up: {question}"
```

**Benefits:**
- Natural conversation flow (users ask follow-ups)
- Reduced ambiguity (agent understands "it" in "what does it unlock?")
- Multi-turn reasoning (agent can build on prior reasoning)
- Context-aware responses (same question has different answers depending on what came before)

**Related Patterns:** ReAct (observes prior conversation), Plan-Execute (can adjust plan based on prior answers)

---

### 8. Domain-Specific Reasoning

**Pattern Name:** Knowledge as Structure

**Description:**
Encoding domain knowledge as graph relationships, not as prompts or LLM memory.

**Traditional Approach:**
```
Agent Prompt: "Remember that Extended Foster Care unlocks Transportation 
Assistance because of California policy X which states..."
```

**Domain-Specific Approach:**
```
Graph Model:
Extended_Foster_Care -[:UNLOCKS]-> Transportation_Assistance

The relationship itself IS the domain knowledge
```

**In LifeGraph:**
Domain knowledge is the graph structure:
- TRIGGERS = What policies say you qualify for
- UNLOCKS = Which programs enable other programs
- HAS_RULE = What conditions you must meet
- REQUIRES = What documents you need
- LEADS_TO = What outcomes programs enable

**Benefits:**
- Knowledge is declarative (easier to update when policies change)
- Reasoning is transparent (relationships are explicit)
- No prompt engineering required (knowledge isn't buried in instructions)
- Version control friendly (graph changes are tracked)
- Consistency (same knowledge available to all agents)

**Related Patterns:** Graph-Augmented LLM, Multi-Hop Traversal

---

## How Patterns Work Together

These patterns don't exist in isolation. Their power comes from composition:

```
User Input
  ↓
[ReAct] Agent reasons about intent
  ↓
[Plan-Execute] Agent breaks task into phases
  ↓
[Agent Orchestration] Appropriate specialist agent selected
  ↓
[Template-Based] Pre-built query templates filled
  ↓
[Graph-Augmented] Query executed on graph
  ↓
[Multi-Hop] Relationships traversed to discover sequences
  ↓
[Domain-Specific] Reasoning grounded in domain knowledge
  ↓
[Conversation Context] Prior turns inform current response
  ↓
User: Gets coherent, contextual, verified answer
```

### Pattern Synergies

**ReAct + Graph-Augmented LLM** = Reliability
- Every answer step is grounded in verified data
- Hallucination is nearly impossible

**Plan-Execute + Agent Orchestration** = Coherence
- Complex tasks are broken down into steps
- Each step is handled by appropriate specialist

**Multi-Hop + Domain-Specific** = Discovery
- Traversing domain-modeled relationships reveals hidden sequences
- Knowledge is explicit, so traversal is meaningful

**Template-Based + Conversation Context** = Performance
- Query templates eliminate generation overhead
- Context management enables efficient multi-turn interactions

---

## When to Use These Patterns

### Apply ReAct When:
- You need transparent reasoning
- User should see the "why" not just the "what"
- You want to reduce hallucination

### Apply Plan-Execute When:
- Tasks involve multiple steps
- Order matters
- Different phases need different reasoning

### Apply Agent Orchestration When:
- Different question types require different expertise
- You want independent optimization per agent
- Failure isolation is important

### Apply Graph-Augmented LLM When:
- Accuracy matters more than speed
- You have a knowledge graph
- You want verifiable answers

### Apply Multi-Hop Traversal When:
- Indirect relationships have value
- Users benefit from seeing sequences not just lists
- Hidden connections matter

### Apply Template-Based When:
- You want to constrain what queries can run
- Performance matters
- Auditability is important

### Apply Conversation Context When:
- Multi-turn interactions are expected
- Follow-up questions are common
- State needs to carry across turns

### Apply Domain-Specific When:
- Your domain has explicit structure
- Knowledge needs to be updateable
- Multiple agents need access to same knowledge

---

## Implementation Considerations

### Performance
- ReAct adds latency (multiple round-trips)
- Multi-Hop can be expensive on dense graphs (use LIMIT)
- Template-Based improves performance vs. dynamic generation
- Conversation Context management has small overhead

### Reliability
- Graph-Augmented eliminates hallucination
- ReAct reduces failures (grounded in observation)
- Template-Based prevents query errors
- Domain-Specific ensures consistency

### Maintainability
- Multi-Hop traversals are fragile to schema changes
- Domain-Specific requires keeping graph in sync with reality
- Conversation Context requires cleanup strategy
- Plan-Execute adds complexity (more code to maintain)

### Scalability
- ReAct scales with query complexity
- Multi-Hop can cause Cartesian explosion (constrain depth)
- Template-Based scales well (no generation)
- Agent Orchestration scales (add agents as needed)

---

## Conclusion

LifeGraph's architecture demonstrates that AI systems reasoning over structured data—not just generating from memory—can be more reliable, more maintainable, and more useful than traditional LLM-only approaches.

These patterns are composable. You don't need all eight for every project, but understanding each enables informed architectural decisions.

---

## References

- **ReAct:** Reasoning + Acting in LLMs (Yao et al., 2022)
- **Graph-Augmented LLM:** Retrieval-Augmented Generation (Lewis et al., 2020)
- **Agent Orchestration:** Multi-Agent Systems (Wooldridge & Jennings, 1995)
- **Template-Based Reasoning:** Structured Prompts (Structured Prompt Engineering)
