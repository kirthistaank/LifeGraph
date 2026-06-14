"""
LifeGraph Agent Setup - Programmatic Aura Agent Creation
Creates all three agents (Eligibility Navigator, Pathway Advisor, Resource Locator)
programmatically using Neo4j REST API
"""

import requests
import json
import os
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuraAgentSetup:
    """Setup and configure Neo4j Aura Agents programmatically"""

    def __init__(self, api_key: str, api_secret: str, neo4j_uri: str):
        """
        Initialize Aura Agent setup

        Args:
            api_key: Neo4j API key (client ID)
            api_secret: Neo4j API secret
            neo4j_uri: Neo4j Aura database URI
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.neo4j_uri = neo4j_uri
        self.token = self._get_token()

    def _get_token(self) -> str:
        """Exchange API credentials for bearer token"""
        try:
            response = requests.post(
                "https://api.neo4j.io/oauth/token",
                auth=(self.api_key, self.api_secret),
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={"grant_type": "client_credentials"},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()["access_token"]
        except Exception as e:
            logger.error(f"Failed to get token: {str(e)}")
            raise

    def _make_request(self, method: str, endpoint: str, data: Dict = None) -> Dict:
        """Make authenticated request to Aura API"""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        url = f"https://api.neo4j.io{endpoint}"

        try:
            if method == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=30)
            elif method == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json() if response.text else {}
        except Exception as e:
            logger.error(f"API request failed: {str(e)}")
            raise

    def create_agent(self, agent_config: Dict) -> Dict:
        """
        Create an agent via Neo4j Aura API

        Args:
            agent_config: Agent configuration dictionary

        Returns:
            Agent creation response
        """
        logger.info(f"Creating agent: {agent_config['name']}")

        # Note: The actual endpoint and payload format depends on Neo4j's Aura Agent API
        # This is a template showing the structure
        try:
            # Construct agent payload
            payload = {
                "name": agent_config["name"],
                "description": agent_config["description"],
                "database_uri": self.neo4j_uri,
                "tools": agent_config["tools"],
                "model": agent_config.get("model", "claude-opus-4-7"),
                "access_level": agent_config.get("access_level", "internal"),
            }

            # Make request to create agent
            # This would be implemented based on Neo4j's actual API documentation
            logger.info(f"Agent {agent_config['name']} configuration prepared")
            logger.info(f"Payload: {json.dumps(payload, indent=2)}")

            # After Aura Agent API is available, uncomment the actual call:
            # response = self._make_request("POST", "/v1/agents", payload)
            # return response

            return {
                "status": "configured",
                "agent": agent_config["name"],
                "note": "Agent configured. Use Aura Console to finalize deployment."
            }
        except Exception as e:
            logger.error(f"Error creating agent: {str(e)}")
            raise

    def create_cypher_template(self, agent_name: str, template_name: str, cypher: str, description: str) -> Dict:
        """
        Create a Cypher template tool for an agent

        Args:
            agent_name: Name of agent to add template to
            template_name: Name of the template
            cypher: Cypher query template (with $placeholders)
            description: Human-readable description

        Returns:
            Template creation response
        """
        logger.info(f"Creating Cypher template: {template_name}")

        payload = {
            "agent_name": agent_name,
            "tool_name": template_name,
            "tool_type": "cypher_template",
            "description": description,
            "cypher_query": cypher,
        }

        logger.info(f"Template {template_name} configured")
        return {"status": "configured", "template": template_name}

    def setup_all_agents(self):
        """Setup all three agents with their tools"""

        # Agent 1: Eligibility Navigator
        self.setup_eligibility_navigator()

        # Agent 2: Pathway Advisor
        self.setup_pathway_advisor()

        # Agent 3: Resource Locator
        self.setup_resource_locator()

        logger.info("✅ All agents configured successfully!")

    def setup_eligibility_navigator(self):
        """Setup Eligibility Navigator agent"""
        logger.info("\n--- Setting up Eligibility Navigator ---")

        agent_config = {
            "name": "Eligibility Navigator",
            "description": "Determines what programs a user qualifies for based on their situation",
            "tools": [
                {
                    "name": "get_programs_by_life_event",
                    "type": "cypher_template",
                    "description": "Find programs triggered by a life event in a specific county"
                },
                {
                    "name": "get_program_eligibility_details",
                    "type": "cypher_template",
                    "description": "Get detailed eligibility rules and requirements for a program"
                },
                {
                    "name": "dynamic_eligibility_query",
                    "type": "text2cypher",
                    "description": "Answer ad-hoc eligibility questions"
                }
            ]
        }

        agent = self.create_agent(agent_config)

        # Tool 1: Programs by Life Event
        template1_cypher = """
        MATCH (le:LifeEvent)-[:TRIGGERS]->(b:Benefit)-[:ADMINISTERED_BY]->(a:Agency)
        WHERE le.name = $life_event
        AND ($county IN b.county_available OR "Statewide" IN b.county_available)
        RETURN
          b.name AS program_name,
          b.description AS description,
          b.monthly_benefit_max AS monthly_benefit,
          b.income_limit_monthly AS income_limit,
          b.application_difficulty AS difficulty
        ORDER BY b.application_difficulty ASC
        LIMIT 20
        """

        self.create_cypher_template(
            agent_config["name"],
            "get_programs_by_life_event",
            template1_cypher,
            "Find programs available based on life event and location"
        )

        # Tool 2: Program Details
        template2_cypher = """
        MATCH (b:Benefit {name: $program_name})
        OPTIONAL MATCH (b)-[:REQUIRES]->(d:Document)
        OPTIONAL MATCH (b)-[:HAS_RULE]->(r:EligibilityRule)
        OPTIONAL MATCH (b)-[:ADMINISTERED_BY]->(a:Agency)
        RETURN
          b.name AS program,
          b.description AS description,
          b.monthly_benefit_max AS benefit_amount,
          b.income_limit_monthly AS income_limit,
          b.age_limit_min AS min_age,
          b.age_limit_max AS max_age,
          COLLECT(DISTINCT d.name) AS required_documents,
          COLLECT(DISTINCT r.rule_text) AS eligibility_rules,
          a.name AS administered_by
        """

        self.create_cypher_template(
            agent_config["name"],
            "get_program_eligibility_details",
            template2_cypher,
            "Get detailed eligibility requirements for a specific program"
        )

        logger.info("Eligibility Navigator configured")

    def setup_pathway_advisor(self):
        """Setup Pathway Advisor agent"""
        logger.info("\n--- Setting up Pathway Advisor ---")

        agent_config = {
            "name": "Pathway Advisor",
            "description": "Builds a sequenced action plan showing how programs unlock each other and lead to outcomes",
            "tools": [
                {
                    "name": "get_multi_hop_pathways",
                    "type": "cypher_template",
                    "description": "Find multi-hop pathways from life event through programs to outcomes"
                },
                {
                    "name": "get_program_unlocks",
                    "type": "cypher_template",
                    "description": "Show what programs a selected program unlocks"
                },
                {
                    "name": "dynamic_pathway_reasoning",
                    "type": "text2cypher",
                    "description": "Reason through complex multi-hop pathways based on user goals"
                }
            ]
        }

        agent = self.create_agent(agent_config)

        # Tool 1: Multi-hop Pathways
        template1_cypher = """
        MATCH path = (le:LifeEvent {name: $life_event})-[:TRIGGERS]->(b1:Benefit)-[:UNLOCKS]->(b2:Benefit)-[:LEADS_TO]->(o:Outcome)
        RETURN
          b1.name AS step_1_program,
          b2.name AS step_2_unlocked_program,
          o.name AS final_outcome,
          b1.description AS step_1_description,
          b2.description AS step_2_description
        LIMIT 10
        """

        self.create_cypher_template(
            agent_config["name"],
            "get_multi_hop_pathways",
            template1_cypher,
            "Discover multi-hop pathways from life event to outcomes"
        )

        # Tool 2: Program Unlocks
        template2_cypher = """
        MATCH (b1:Benefit {name: $program_name})-[:UNLOCKS]->(b2:Benefit)-[:LEADS_TO]->(o:Outcome)
        RETURN
          b2.name AS unlocked_program,
          b2.description AS description,
          o.name AS ultimate_outcome
        """

        self.create_cypher_template(
            agent_config["name"],
            "get_program_unlocks",
            template2_cypher,
            "Show what programs are unlocked by applying to a specific program"
        )

        logger.info("Pathway Advisor configured")

    def setup_resource_locator(self):
        """Setup Resource Locator agent"""
        logger.info("\n--- Setting up Resource Locator ---")

        agent_config = {
            "name": "Resource Locator",
            "description": "Finds specific organizations and services available in the user's area",
            "tools": [
                {
                    "name": "find_organizations_by_service",
                    "type": "cypher_template",
                    "description": "Find organizations providing specific services in a county"
                },
                {
                    "name": "find_organizations_by_life_event",
                    "type": "cypher_template",
                    "description": "Find organizations that serve a specific life event"
                },
                {
                    "name": "dynamic_resource_search",
                    "type": "text2cypher",
                    "description": "Search for resources based on natural language queries"
                }
            ]
        }

        agent = self.create_agent(agent_config)

        # Tool 1: Organizations by Service
        template1_cypher = """
        MATCH (org:Organization)-[:PROVIDES]->(b:Benefit)
        WHERE org.county = $county AND b.name = $service_name
        RETURN
          org.name AS organization,
          org.description AS description,
          org.phone AS phone,
          org.address AS address,
          org.type AS type,
          org.eligibility_notes AS eligibility,
          COLLECT(b.name) AS services_provided
        """

        self.create_cypher_template(
            agent_config["name"],
            "find_organizations_by_service",
            template1_cypher,
            "Find organizations providing specific services in a location"
        )

        # Tool 2: Organizations by Life Event
        template2_cypher = """
        MATCH (org:Organization)-[:SERVES]->(le:LifeEvent)
        WHERE org.county = $county AND le.name = $life_event
        RETURN
          org.name AS organization,
          org.description AS description,
          org.phone AS phone,
          org.address AS address,
          org.services_offered AS services,
          org.target_population AS target_population,
          org.eligibility_notes AS eligibility
        """

        self.create_cypher_template(
            agent_config["name"],
            "find_organizations_by_life_event",
            template2_cypher,
            "Find organizations specializing in a specific life event"
        )

        logger.info("Resource Locator configured")


def main():
    """Main entry point"""
    # Load credentials from environment variables
    api_key = os.getenv("NEO4J_API_KEY", "")
    api_secret = os.getenv("NEO4J_API_SECRET", "")
    neo4j_uri = os.getenv("NEO4J_URI", "")

    if not all([api_key, api_secret, neo4j_uri]):
        raise ValueError(
            "NEO4J_API_KEY, NEO4J_API_SECRET, and NEO4J_URI environment variables must be set"
        )

    logger.info("Starting LifeGraph Agent Setup")
    setup = AuraAgentSetup(api_key, api_secret, neo4j_uri)
    setup.setup_all_agents()

    logger.info("""
    ✅ Agent configuration complete!

    Next steps:
    1. Review agent configurations
    2. Go to Aura Console: https://console.neo4j.io
    3. Create agents manually using the configurations above
    4. Enable External Access if needed for REST API access
    5. Test agents in Aura Console chat
    """)


if __name__ == "__main__":
    main()
