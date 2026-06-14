"""
LifeGraph Data Loader - Programmatic Data Ingestion
Loads all graph data into Neo4j Aura database programmatically
"""

from neo4j import GraphDatabase
import os
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LifeGraphDataLoader:
    def __init__(self, uri: str, user: str, password: str):
        """Initialize connection to Neo4j database"""
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        logger.info("Connected to Neo4j Aura")

    def close(self):
        """Close database connection"""
        self.driver.close()

    def create_life_events(self):
        """Create LifeEvent nodes"""
        life_events = [
            {
                "name": "AGED_OUT_OF_FOSTER_CARE",
                "description": "Transitioned out of foster care system",
                "impact_area": "housing,employment,education",
                "typical_age_range": "18-21",
            },
            {
                "name": "LOST_JOB",
                "description": "Lost employment",
                "impact_area": "income,housing,food",
                "typical_age_range": "18-65",
            },
            {
                "name": "HAD_CHILD",
                "description": "Became a parent",
                "impact_area": "income,childcare,housing,food",
                "typical_age_range": "18-45",
            },
            {
                "name": "STARTED_COLLEGE",
                "description": "Enrolled in higher education",
                "impact_area": "education,income",
                "typical_age_range": "18-25",
            },
            {
                "name": "BECAME_DISABLED",
                "description": "Developed disability affecting work",
                "impact_area": "income,healthcare,housing",
                "typical_age_range": "18-65",
            },
            {
                "name": "HOMELESSNESS_RISK",
                "description": "Risk of losing housing",
                "impact_area": "housing,food",
                "typical_age_range": "18-65",
            },
            {
                "name": "DOMESTIC_VIOLENCE",
                "description": "Fleeing abusive situation",
                "impact_area": "housing,safety,childcare",
                "typical_age_range": "18-65",
            },
            {
                "name": "SUBSTANCE_RECOVERY",
                "description": "In recovery/rehabilitation",
                "impact_area": "healthcare,employment,housing",
                "typical_age_range": "18-65",
            },
            {
                "name": "IMMIGRATION_TRANSITION",
                "description": "Immigration status change",
                "impact_area": "employment,healthcare,education",
                "typical_age_range": "18-65",
            },
            {
                "name": "COMPLETED_EDUCATION",
                "description": "Finished high school or college",
                "impact_area": "employment,income",
                "typical_age_range": "18-30",
            },
            {
                "name": "RELEASED_FROM_INCARCERATION",
                "description": "Returned from incarceration",
                "impact_area": "employment,housing,income",
                "typical_age_range": "18-65",
            },
            {
                "name": "FLEEING_TRAFFICKING",
                "description": "Escaped human trafficking",
                "impact_area": "safety,housing,healthcare,counseling",
                "typical_age_range": "18-65",
            },
        ]

        with self.driver.session() as session:
            for event in life_events:
                session.run(
                    """
                    CREATE (le:LifeEvent $props)
                    RETURN le.name
                    """,
                    props=event,
                )
            logger.info(f"Created {len(life_events)} LifeEvent nodes")

    def create_documents(self):
        """Create Document nodes"""
        documents = [
            {
                "name": "Birth_Certificate",
                "description": "Proof of identity and age",
                "requirement_level": "required",
                "where_to_get": "Vital Records Office",
            },
            {
                "name": "ID_Card",
                "description": "Government-issued photo ID",
                "requirement_level": "required",
                "where_to_get": "DMV or equivalent",
            },
            {
                "name": "Social_Security_Card",
                "description": "SSN proof",
                "requirement_level": "required",
                "where_to_get": "Social Security Administration",
            },
            {
                "name": "Proof_of_Income",
                "description": "Pay stubs, tax returns, or income statement",
                "requirement_level": "required",
                "where_to_get": "Employer or self-created",
            },
            {
                "name": "Proof_of_Residence",
                "description": "Utility bill or lease agreement",
                "requirement_level": "required",
                "where_to_get": "Utility company or landlord",
            },
            {
                "name": "Bank_Statements",
                "description": "Proof of assets and account activity",
                "requirement_level": "preferred",
                "where_to_get": "Bank",
            },
            {
                "name": "Citizenship_Proof",
                "description": "Birth certificate or passport",
                "requirement_level": "required",
                "where_to_get": "State records or federal",
            },
            {
                "name": "Divorce_Decree",
                "description": "If applicable, proof of custody",
                "requirement_level": "if_applicable",
                "where_to_get": "Court records",
            },
            {
                "name": "Foster_Care_Documentation",
                "description": "Proof of foster care status or aging out",
                "requirement_level": "required_for_foster",
                "where_to_get": "Department of Children Services",
            },
            {
                "name": "Court_Records",
                "description": "For criminal history disclosure",
                "requirement_level": "if_applicable",
                "where_to_get": "Court",
            },
            {
                "name": "Medical_Records",
                "description": "For health-related benefits",
                "requirement_level": "preferred",
                "where_to_get": "Healthcare provider",
            },
            {
                "name": "School_Records",
                "description": "Enrollment or graduation proof",
                "requirement_level": "if_applicable",
                "where_to_get": "School",
            },
            {
                "name": "Proof_of_Disability",
                "description": "Medical documentation for disability benefits",
                "requirement_level": "required_for_disability",
                "where_to_get": "Healthcare provider",
            },
            {
                "name": "Work_Authorization",
                "description": "For employment-based programs",
                "requirement_level": "required_for_employment",
                "where_to_get": "USCIS (if applicable)",
            },
            {
                "name": "Tax_Return",
                "description": "IRS Form 1040 or equivalent",
                "requirement_level": "preferred",
                "where_to_get": "Self or preparer",
            },
        ]

        with self.driver.session() as session:
            for doc in documents:
                session.run(
                    """
                    CREATE (d:Document $props)
                    RETURN d.name
                    """,
                    props=doc,
                )
            logger.info(f"Created {len(documents)} Document nodes")

    def create_agencies(self):
        """Create Agency nodes"""
        agencies = [
            {
                "name": "Alameda_County_Social_Services",
                "county": "Alameda",
                "phone": "510-555-1234",
                "hours": "Monday-Friday 8am-5pm",
                "address": "1000 Broadway, Oakland, CA 94607",
            },
            {
                "name": "California_Department_of_Social_Services",
                "county": "Statewide",
                "phone": "844-832-4279",
                "hours": "Monday-Friday 8am-5pm",
                "address": "San Francisco, CA",
            },
            {
                "name": "Alameda_County_Healthcare_Services",
                "county": "Alameda",
                "phone": "510-555-5678",
                "hours": "Monday-Friday 8am-6pm",
                "address": "2000 embarcadero, Oakland, CA",
            },
            {
                "name": "California_Employment_Development_Department",
                "county": "Statewide",
                "phone": "888-353-8680",
                "hours": "Monday-Friday 8am-5pm",
                "address": "Sacramento, CA",
            },
            {
                "name": "Alameda_County_Job_Training",
                "county": "Alameda",
                "phone": "510-555-2020",
                "hours": "Monday-Friday 9am-4pm",
                "address": "800 Broadway, Oakland, CA",
            },
            {
                "name": "California_Housing_Finance_Agency",
                "county": "Statewide",
                "phone": "916-322-3000",
                "hours": "Monday-Friday 8am-5pm",
                "address": "Sacramento, CA",
            },
            {
                "name": "Foster_Care_Youth_Services",
                "county": "Statewide",
                "phone": "916-651-7000",
                "hours": "Monday-Friday 8am-5pm",
                "address": "Sacramento, CA",
            },
            {
                "name": "Alameda_County_Food_Bank",
                "county": "Alameda",
                "phone": "510-635-3663",
                "hours": "Daily 9am-5pm",
                "address": "4000 Technology Court, Fremont, CA",
            },
            {
                "name": "California_Department_of_Education",
                "county": "Statewide",
                "phone": "916-319-0800",
                "hours": "Monday-Friday 8am-5pm",
                "address": "Sacramento, CA",
            },
            {
                "name": "Legal_Aid_Organization",
                "county": "Alameda",
                "phone": "510-763-4570",
                "hours": "Monday-Friday 9am-5pm",
                "address": "1313 Broadway, Oakland, CA",
            },
        ]

        with self.driver.session() as session:
            for agency in agencies:
                session.run(
                    """
                    CREATE (a:Agency $props)
                    RETURN a.name
                    """,
                    props=agency,
                )
            logger.info(f"Created {len(agencies)} Agency nodes")

    def create_eligibility_rules(self):
        """Create EligibilityRule nodes"""
        rules = [
            {
                "rule_text": "Income must be below 130% of Federal Poverty Level",
                "condition_type": "INCOME",
                "threshold_value": 1500,
                "operator": "LT",
            },
            {
                "rule_text": "Age must be between 18 and 25",
                "condition_type": "AGE",
                "threshold_value_min": 18,
                "threshold_value_max": 25,
                "operator": "BETWEEN",
            },
            {
                "rule_text": "Must be a current or former foster youth",
                "condition_type": "STATUS",
                "threshold_value": None,
                "operator": "EQ",
            },
            {
                "rule_text": "Must be a California resident",
                "condition_type": "RESIDENCY",
                "threshold_value": None,
                "operator": "EQ",
            },
            {
                "rule_text": "Must have dependent children",
                "condition_type": "FAMILY_SIZE",
                "threshold_value": 1,
                "operator": "GTE",
            },
            {
                "rule_text": "Citizenship or legal resident status required",
                "condition_type": "CITIZENSHIP",
                "threshold_value": None,
                "operator": "EQ",
            },
            {
                "rule_text": "Must be unemployed or underemployed",
                "condition_type": "EMPLOYMENT_STATUS",
                "threshold_value": None,
                "operator": "EQ",
            },
            {
                "rule_text": "Asset limit of $3,250 per person",
                "condition_type": "ASSETS",
                "threshold_value": 3250,
                "operator": "LT",
            },
            {
                "rule_text": "Disability certification required",
                "condition_type": "DISABILITY",
                "threshold_value": None,
                "operator": "EQ",
            },
            {
                "rule_text": "Income below 185% of poverty line",
                "condition_type": "INCOME",
                "threshold_value": 2100,
                "operator": "LT",
            },
            {
                "rule_text": "Must have completed high school or GED",
                "condition_type": "EDUCATION",
                "threshold_value": None,
                "operator": "EQ",
            },
            {
                "rule_text": "Age 21 or under at time of application",
                "condition_type": "AGE",
                "threshold_value_max": 21,
                "operator": "LTE",
            },
            {
                "rule_text": "No student loan default",
                "condition_type": "LOAN_STATUS",
                "threshold_value": None,
                "operator": "EQ",
            },
            {
                "rule_text": "Work requirement: 20+ hours per week or full-time student",
                "condition_type": "WORK_REQUIREMENT",
                "threshold_value": 20,
                "operator": "GTE",
            },
            {
                "rule_text": "Must apply within 12 months of aging out",
                "condition_type": "TIME_LIMIT",
                "threshold_value": 12,
                "operator": "LTE",
            },
            {
                "rule_text": "No criminal convictions for drug-related offenses",
                "condition_type": "CRIMINAL_HISTORY",
                "threshold_value": None,
                "operator": "EQ",
            },
            {
                "rule_text": "Must be seeking or willing to seek employment",
                "condition_type": "EMPLOYMENT_WILLINGNESS",
                "threshold_value": None,
                "operator": "EQ",
            },
            {
                "rule_text": "Income below 200% of federal poverty line",
                "condition_type": "INCOME",
                "threshold_value": 2300,
                "operator": "LT",
            },
            {
                "rule_text": "Single parent or pregnant and aged 21 or under",
                "condition_type": "FAMILY_STATUS",
                "threshold_value": None,
                "operator": "EQ",
            },
            {
                "rule_text": "Recently homeless or at imminent risk of homelessness",
                "condition_type": "HOUSING_STATUS",
                "threshold_value": None,
                "operator": "EQ",
            },
        ]

        with self.driver.session() as session:
            for rule in rules:
                session.run(
                    """
                    CREATE (r:EligibilityRule $props)
                    RETURN r.rule_text
                    """,
                    props=rule,
                )
            logger.info(f"Created {len(rules)} EligibilityRule nodes")

    def create_outcomes(self):
        """Create Outcome nodes"""
        outcomes = [
            {
                "name": "HOUSING_SECURED",
                "category": "housing",
                "description": "Secured stable housing",
                "stability_score": 80,
            },
            {
                "name": "EMPLOYED",
                "category": "employment",
                "description": "Obtained employment",
                "stability_score": 75,
            },
            {
                "name": "COMPLETED_EDUCATION",
                "category": "education",
                "description": "Completed high school or degree",
                "stability_score": 70,
            },
            {
                "name": "FOOD_SECURITY",
                "category": "food",
                "description": "Reliable access to food",
                "stability_score": 50,
            },
            {
                "name": "HEALTHCARE_ACCESS",
                "category": "health",
                "description": "Enrolled in health insurance",
                "stability_score": 60,
            },
            {
                "name": "FINANCIAL_STABILITY",
                "category": "income",
                "description": "Stable monthly income above poverty level",
                "stability_score": 85,
            },
            {
                "name": "MENTORSHIP_CONNECTED",
                "category": "support",
                "description": "Connected with mentor",
                "stability_score": 40,
            },
            {
                "name": "JOB_TRAINING_COMPLETE",
                "category": "employment",
                "description": "Completed job training program",
                "stability_score": 65,
            },
            {
                "name": "CHILD_WELLBEING",
                "category": "family",
                "description": "Child has stable living situation and care",
                "stability_score": 70,
            },
            {
                "name": "LEGAL_STABILITY",
                "category": "legal",
                "description": "Resolved legal issues or obtained legal status",
                "stability_score": 60,
            },
        ]

        with self.driver.session() as session:
            for outcome in outcomes:
                session.run(
                    """
                    CREATE (o:Outcome $props)
                    RETURN o.name
                    """,
                    props=outcome,
                )
            logger.info(f"Created {len(outcomes)} Outcome nodes")

    def create_benefits(self):
        """Create Benefit nodes (Programs)"""
        benefits = [
            {
                "name": "CalFresh",
                "description": "Food assistance program (formerly SNAP)",
                "monthly_benefit_max": 250,
                "income_limit_monthly": 1500,
                "age_limit_min": 18,
                "county_available": ["Alameda", "Statewide"],
                "target_audience": ["Low income", "Families", "Individuals"],
                "application_difficulty": "low",
            },
            {
                "name": "WIC",
                "description": "Women, Infants, Children nutrition program",
                "monthly_benefit_max": 150,
                "income_limit_monthly": 2100,
                "age_limit_min": 18,
                "age_limit_max": 50,
                "county_available": ["Alameda", "Statewide"],
                "target_audience": ["Pregnant women", "New mothers", "Children"],
                "application_difficulty": "medium",
            },
            {
                "name": "Medi-Cal",
                "description": "California healthcare for low-income",
                "monthly_benefit_max": None,
                "income_limit_monthly": 1500,
                "age_limit_min": 0,
                "county_available": ["Alameda", "Statewide"],
                "target_audience": ["Low income", "Families", "Individuals", "Foster Youth"],
                "application_difficulty": "low",
            },
            {
                "name": "Extended_Foster_Care",
                "description": "Support for youth aging out of foster care until age 21",
                "monthly_benefit_max": 1000,
                "income_limit_monthly": None,
                "age_limit_min": 18,
                "age_limit_max": 21,
                "county_available": ["Alameda", "Statewide"],
                "target_audience": ["Former Foster Youth"],
                "application_difficulty": "medium",
            },
            {
                "name": "Foster_Youth_Housing_Program",
                "description": "Housing support for youth aging out (18-21)",
                "monthly_benefit_max": 600,
                "income_limit_monthly": 2000,
                "age_limit_min": 18,
                "age_limit_max": 21,
                "county_available": ["Alameda", "Select counties"],
                "target_audience": ["Aged Out Foster Youth"],
                "application_difficulty": "medium",
            },
            {
                "name": "Transportation_Assistance",
                "description": "Bus passes and transportation support",
                "monthly_benefit_max": 50,
                "income_limit_monthly": 1500,
                "age_limit_min": 18,
                "county_available": ["Alameda"],
                "target_audience": ["Low income", "Foster Youth"],
                "application_difficulty": "low",
            },
            {
                "name": "Job_Corps",
                "description": "Job training and education for low-income youth (16-24)",
                "monthly_benefit_max": 8000,
                "income_limit_monthly": None,
                "age_limit_min": 16,
                "age_limit_max": 24,
                "county_available": ["Statewide"],
                "target_audience": ["Low income youth", "Foster Youth"],
                "application_difficulty": "medium",
            },
            {
                "name": "CalWORKs",
                "description": "Temporary Assistance for Needy Families",
                "monthly_benefit_max": 1200,
                "income_limit_monthly": 1200,
                "age_limit_min": 18,
                "county_available": ["Alameda", "Statewide"],
                "target_audience": ["Low income families", "Single parents"],
                "application_difficulty": "hard",
            },
            {
                "name": "Housing_Voucher_Program",
                "description": "Section 8 housing assistance",
                "monthly_benefit_max": 1200,
                "income_limit_monthly": 1800,
                "age_limit_min": 18,
                "county_available": ["Alameda"],
                "target_audience": ["Low income", "Families"],
                "application_difficulty": "hard",
            },
            {
                "name": "LIHEAP",
                "description": "Low Income Home Energy Assistance Program",
                "monthly_benefit_max": 1000,
                "income_limit_monthly": 1600,
                "age_limit_min": 18,
                "county_available": ["Alameda", "Statewide"],
                "target_audience": ["Low income"],
                "application_difficulty": "medium",
            },
            {
                "name": "Education_Grant_Foster_Youth",
                "description": "Scholarship and education support for foster youth",
                "monthly_benefit_max": 500,
                "income_limit_monthly": None,
                "age_limit_min": 18,
                "age_limit_max": 25,
                "county_available": ["Alameda", "Statewide"],
                "target_audience": ["Foster Youth", "College students"],
                "application_difficulty": "hard",
            },
            {
                "name": "Childcare_Assistance",
                "description": "Subsidized childcare for low-income parents",
                "monthly_benefit_max": 800,
                "income_limit_monthly": 2000,
                "age_limit_min": 18,
                "county_available": ["Alameda", "Statewide"],
                "target_audience": ["Single parents", "Low income families"],
                "application_difficulty": "medium",
            },
            {
                "name": "Mental_Health_Services",
                "description": "No-cost mental health and counseling services",
                "monthly_benefit_max": None,
                "income_limit_monthly": 1500,
                "age_limit_min": 18,
                "county_available": ["Alameda"],
                "target_audience": ["Low income", "Foster Youth"],
                "application_difficulty": "low",
            },
            {
                "name": "Substance_Abuse_Treatment",
                "description": "Addiction recovery and rehabilitation programs",
                "monthly_benefit_max": None,
                "income_limit_monthly": None,
                "age_limit_min": 18,
                "county_available": ["Alameda", "Statewide"],
                "target_audience": ["Anyone in recovery"],
                "application_difficulty": "medium",
            },
            {
                "name": "SNAP_Employment_Training",
                "description": "Job training through CalFresh (SNAP)",
                "monthly_benefit_max": 500,
                "income_limit_monthly": 1500,
                "age_limit_min": 18,
                "county_available": ["Alameda", "Statewide"],
                "target_audience": ["CalFresh recipients"],
                "application_difficulty": "low",
            },
            {
                "name": "Disability_Services",
                "description": "Support for people with disabilities",
                "monthly_benefit_max": 1000,
                "income_limit_monthly": 1500,
                "age_limit_min": 18,
                "county_available": ["Alameda", "Statewide"],
                "target_audience": ["People with disabilities"],
                "application_difficulty": "hard",
            },
            {
                "name": "Legal_Aid_Services",
                "description": "Free or low-cost legal services",
                "monthly_benefit_max": None,
                "income_limit_monthly": 2500,
                "age_limit_min": 18,
                "county_available": ["Alameda"],
                "target_audience": ["Low income"],
                "application_difficulty": "low",
            },
            {
                "name": "Homeless_Emergency_Housing",
                "description": "Emergency shelter and housing vouchers",
                "monthly_benefit_max": 1000,
                "income_limit_monthly": None,
                "age_limit_min": 18,
                "county_available": ["Alameda"],
                "target_audience": ["Homeless", "At-risk"],
                "application_difficulty": "low",
            },
            {
                "name": "Domestic_Violence_Shelter",
                "description": "Safe shelter and services for DV survivors",
                "monthly_benefit_max": None,
                "income_limit_monthly": None,
                "age_limit_min": 18,
                "county_available": ["Alameda", "Statewide"],
                "target_audience": ["DV survivors"],
                "application_difficulty": "low",
            },
            {
                "name": "Transitional_Housing",
                "description": "Time-limited housing with support services (6-24 months)",
                "monthly_benefit_max": 800,
                "income_limit_monthly": 2000,
                "age_limit_min": 18,
                "county_available": ["Alameda"],
                "target_audience": ["Homeless", "Foster Youth"],
                "application_difficulty": "medium",
            },
            {
                "name": "Community_College_Enrollment",
                "description": "Tuition waiver and support for foster youth",
                "monthly_benefit_max": 3000,
                "income_limit_monthly": None,
                "age_limit_min": 18,
                "age_limit_max": 25,
                "county_available": ["Alameda", "Statewide"],
                "target_audience": ["Foster Youth", "Low income"],
                "application_difficulty": "medium",
            },
            {
                "name": "Workforce_Development_Program",
                "description": "Job training and placement services",
                "monthly_benefit_max": 0,
                "income_limit_monthly": None,
                "age_limit_min": 18,
                "age_limit_max": 35,
                "county_available": ["Alameda", "Statewide"],
                "target_audience": ["Job seekers", "Low income"],
                "application_difficulty": "low",
            },
            {
                "name": "Foster_Youth_Mentorship_Program",
                "description": "One-on-one mentoring for life skills and guidance",
                "monthly_benefit_max": 0,
                "income_limit_monthly": None,
                "age_limit_min": 16,
                "age_limit_max": 21,
                "county_available": ["Alameda"],
                "target_audience": ["Foster Youth"],
                "application_difficulty": "low",
            },
            {
                "name": "Utility_Bill_Assistance",
                "description": "Help paying electricity, gas, water bills",
                "monthly_benefit_max": 500,
                "income_limit_monthly": 1500,
                "age_limit_min": 18,
                "county_available": ["Alameda"],
                "target_audience": ["Low income"],
                "application_difficulty": "low",
            },
            {
                "name": "Food_Bank_Access",
                "description": "Free emergency food and groceries",
                "monthly_benefit_max": 0,
                "income_limit_monthly": None,
                "age_limit_min": 18,
                "county_available": ["Alameda"],
                "target_audience": ["Anyone in food insecurity"],
                "application_difficulty": "low",
            },
        ]

        with self.driver.session() as session:
            for benefit in benefits:
                session.run(
                    """
                    CREATE (b:Benefit $props)
                    RETURN b.name
                    """,
                    props=benefit,
                )
            logger.info(f"Created {len(benefits)} Benefit nodes")

    def create_organizations(self):
        """Create Organization nodes"""
        organizations = [
            {
                "name": "First_Place_for_Youth",
                "type": "housing_support",
                "description": "Housing and supportive services for formerly homeless and foster youth",
                "county": "Alameda",
                "phone": "510-444-1192",
                "address": "369 15th St, Oakland, CA",
                "services_offered": ["housing", "job_training", "mentorship"],
                "target_population": ["Foster Youth", "Homeless"],
                "eligibility_notes": "Ages 18-25, income limits apply",
            },
            {
                "name": "Job_Corps_Oakland",
                "type": "job_training",
                "description": "Federal job training and education program",
                "county": "Alameda",
                "phone": "510-622-4600",
                "address": "1801 Embarcadero, Oakland, CA",
                "services_offered": ["job_training", "education", "stipend"],
                "target_population": ["Low income", "Foster Youth"],
                "eligibility_notes": "Ages 16-24, no income limits",
            },
            {
                "name": "Community_Food_Bank_Alameda",
                "type": "food_assistance",
                "description": "Emergency food distribution and nutrition education",
                "county": "Alameda",
                "phone": "510-635-3663",
                "address": "4000 Technology Ct, Fremont, CA",
                "services_offered": ["food", "nutrition_classes"],
                "target_population": ["Anyone in need"],
                "eligibility_notes": "No eligibility restrictions",
            },
            {
                "name": "Alameda_County_Legal_Aid",
                "type": "legal_aid",
                "description": "Free legal services for low-income residents",
                "county": "Alameda",
                "phone": "510-763-4570",
                "address": "1313 Broadway, Oakland, CA",
                "services_offered": ["legal", "advocacy"],
                "target_population": ["Low income"],
                "eligibility_notes": "Income-based, free for eligible",
            },
            {
                "name": "YouthBuilt_Collective",
                "type": "job_training",
                "description": "Career training in construction and green jobs",
                "county": "Alameda",
                "phone": "510-567-9000",
                "address": "2800 Telegraph Ave, Berkeley, CA",
                "services_offered": ["job_training", "apprenticeship"],
                "target_population": ["Low income", "Underrepresented youth"],
                "eligibility_notes": "Ages 16-29",
            },
            {
                "name": "Eden_Youth_Fund",
                "type": "mentorship",
                "description": "Mentoring and support for foster and low-income youth",
                "county": "Alameda",
                "phone": "510-835-2953",
                "address": "Oakland, CA",
                "services_offered": ["mentoring", "life_skills", "support"],
                "target_population": ["Foster Youth", "Low income"],
                "eligibility_notes": "Ages 14-25",
            },
            {
                "name": "Futures_Explored",
                "type": "education_support",
                "description": "College prep and educational advocacy",
                "county": "Alameda",
                "phone": "510-452-8877",
                "address": "Oakland, CA",
                "services_offered": ["college_prep", "tutoring", "scholarships"],
                "target_population": ["Low income", "First generation"],
                "eligibility_notes": "High school students and young adults",
            },
            {
                "name": "Bay_Area_Community_Services",
                "type": "mental_health",
                "description": "Mental health and counseling services",
                "county": "Alameda",
                "phone": "510-208-5400",
                "address": "Oakland, CA",
                "services_offered": ["counseling", "mental_health", "case_management"],
                "target_population": ["Low income", "Foster Youth"],
                "eligibility_notes": "Income-based fees, no one turned away",
            },
            {
                "name": "A_New_Leaf",
                "type": "housing_support",
                "description": "Transitional housing and support services",
                "county": "Alameda",
                "phone": "510-763-5800",
                "address": "Oakland, CA",
                "services_offered": ["housing", "case_management", "support"],
                "target_population": ["Homeless", "At-risk"],
                "eligibility_notes": "No income limit, housing-focused",
            },
            {
                "name": "Alameda_Workforce_Development",
                "type": "job_training",
                "description": "Career services and job training programs",
                "county": "Alameda",
                "phone": "510-832-3500",
                "address": "1313 Broadway, Oakland, CA",
                "services_offered": ["job_training", "job_placement", "skills"],
                "target_population": ["Job seekers", "Low income"],
                "eligibility_notes": "Free services for eligible residents",
            },
        ]

        with self.driver.session() as session:
            for org in organizations:
                session.run(
                    """
                    CREATE (o:Organization $props)
                    RETURN o.name
                    """,
                    props=org,
                )
            logger.info(f"Created {len(organizations)} Organization nodes")

    def create_relationships_benefit_requires_document(self):
        """Create REQUIRES relationships between Benefits and Documents"""
        relationships = [
            ("CalFresh", "ID_Card"),
            ("CalFresh", "Proof_of_Income"),
            ("CalFresh", "Proof_of_Residence"),
            ("WIC", "Birth_Certificate"),
            ("Extended_Foster_Care", "Foster_Care_Documentation"),
            ("Extended_Foster_Care", "ID_Card"),
            ("Foster_Youth_Housing_Program", "Foster_Care_Documentation"),
            ("Foster_Youth_Housing_Program", "ID_Card"),
            ("Medi-Cal", "ID_Card"),
            ("Medi-Cal", "Proof_of_Income"),
        ]

        with self.driver.session() as session:
            for benefit_name, doc_name in relationships:
                session.run(
                    """
                    MATCH (b:Benefit {name: $benefit}), (d:Document {name: $doc})
                    CREATE (b)-[:REQUIRES {requirement_level: "required"}]->(d)
                    """,
                    benefit=benefit_name,
                    doc=doc_name,
                )
            logger.info(f"Created {len(relationships)} REQUIRES relationships")

    def create_relationships_benefit_has_rule(self):
        """Create HAS_RULE relationships between Benefits and EligibilityRules"""
        query = """
        MATCH (b:Benefit {name: $benefit}), (r:EligibilityRule {rule_text: $rule})
        CREATE (b)-[:HAS_RULE]->(r)
        """

        relationships = [
            ("CalFresh", "Income must be below 130% of Federal Poverty Level"),
            ("Extended_Foster_Care", "Age must be between 18 and 25"),
            ("Extended_Foster_Care", "Must be a current or former foster youth"),
            ("Foster_Youth_Housing_Program", "Age 21 or under at time of application"),
            ("Foster_Youth_Housing_Program", "Must be a current or former foster youth"),
            ("WIC", "Income below 185% of poverty line"),
            ("CalWORKs", "Must have dependent children"),
            ("CalWORKs", "Work requirement: 20+ hours per week or full-time student"),
            ("Job_Corps", "Age must be between 18 and 25"),
            ("Housing_Voucher_Program", "Income below 200% of federal poverty line"),
        ]

        with self.driver.session() as session:
            for benefit_name, rule_text in relationships:
                session.run(query, benefit=benefit_name, rule=rule_text)
            logger.info(f"Created {len(relationships)} HAS_RULE relationships")

    def create_relationships_life_event_triggers_benefit(self):
        """Create TRIGGERS relationships between LifeEvents and Benefits"""
        query = """
        MATCH (le:LifeEvent {name: $event}), (b:Benefit {name: $benefit})
        CREATE (le)-[:TRIGGERS]->(b)
        """

        relationships = [
            ("AGED_OUT_OF_FOSTER_CARE", "Extended_Foster_Care"),
            ("AGED_OUT_OF_FOSTER_CARE", "Foster_Youth_Housing_Program"),
            ("AGED_OUT_OF_FOSTER_CARE", "Medi-Cal"),
            ("AGED_OUT_OF_FOSTER_CARE", "Education_Grant_Foster_Youth"),
            ("LOST_JOB", "CalFresh"),
            ("LOST_JOB", "CalWORKs"),
            ("LOST_JOB", "Workforce_Development_Program"),
            ("HAD_CHILD", "CalFresh"),
            ("HAD_CHILD", "WIC"),
            ("HAD_CHILD", "Childcare_Assistance"),
            ("HOMELESSNESS_RISK", "Homeless_Emergency_Housing"),
            ("HOMELESSNESS_RISK", "Housing_Voucher_Program"),
            ("DOMESTIC_VIOLENCE", "Domestic_Violence_Shelter"),
            ("DOMESTIC_VIOLENCE", "Legal_Aid_Services"),
            ("SUBSTANCE_RECOVERY", "Substance_Abuse_Treatment"),
        ]

        with self.driver.session() as session:
            for event_name, benefit_name in relationships:
                session.run(query, event=event_name, benefit=benefit_name)
            logger.info(f"Created {len(relationships)} TRIGGERS relationships")

    def create_relationships_benefit_unlocks_benefit(self):
        """Create UNLOCKS relationships between Benefits"""
        query = """
        MATCH (b1:Benefit {name: $from}), (b2:Benefit {name: $to})
        CREATE (b1)-[:UNLOCKS {reason: $reason}]->(b2)
        """

        relationships = [
            (
                "Extended_Foster_Care",
                "Transportation_Assistance",
                "Extended Foster Care automatically qualifies for transportation",
            ),
            (
                "Extended_Foster_Care",
                "Education_Grant_Foster_Youth",
                "Extended Foster Care recipients can access education grants",
            ),
            (
                "CalFresh",
                "SNAP_Employment_Training",
                "CalFresh recipients can enroll in job training",
            ),
            (
                "Foster_Youth_Housing_Program",
                "Education_Grant_Foster_Youth",
                "Stable housing enables education enrollment",
            ),
            (
                "Job_Corps",
                "SNAP_Employment_Training",
                "Job Corps completion qualifies for employment benefits",
            ),
            (
                "Workforce_Development_Program",
                "Transportation_Assistance",
                "Workforce program participants can access transportation",
            ),
            (
                "Medi-Cal",
                "Mental_Health_Services",
                "Medi-Cal covers mental health services",
            ),
        ]

        with self.driver.session() as session:
            for from_name, to_name, reason in relationships:
                session.run(query, from_=from_name, to=to_name, reason=reason)
            logger.info(f"Created {len(relationships)} UNLOCKS relationships")

    def create_relationships_benefit_leads_to_outcome(self):
        """Create LEADS_TO relationships between Benefits and Outcomes"""
        query = """
        MATCH (b:Benefit {name: $benefit}), (o:Outcome {name: $outcome})
        CREATE (b)-[:LEADS_TO]->(o)
        """

        relationships = [
            ("Foster_Youth_Housing_Program", "HOUSING_SECURED"),
            ("Extended_Foster_Care", "HOUSING_SECURED"),
            ("Job_Corps", "JOB_TRAINING_COMPLETE"),
            ("Workforce_Development_Program", "EMPLOYED"),
            ("Education_Grant_Foster_Youth", "COMPLETED_EDUCATION"),
            ("CalFresh", "FOOD_SECURITY"),
            ("Medi-Cal", "HEALTHCARE_ACCESS"),
            ("Mental_Health_Services", "FINANCIAL_STABILITY"),
            ("Foster_Youth_Mentorship_Program", "MENTORSHIP_CONNECTED"),
            ("Job_Corps", "FINANCIAL_STABILITY"),
        ]

        with self.driver.session() as session:
            for benefit_name, outcome_name in relationships:
                session.run(query, benefit=benefit_name, outcome=outcome_name)
            logger.info(f"Created {len(relationships)} LEADS_TO relationships")

    def create_relationships_benefit_administered_by_agency(self):
        """Create ADMINISTERED_BY relationships between Benefits and Agencies"""
        query = """
        MATCH (b:Benefit {name: $benefit}), (a:Agency {name: $agency})
        CREATE (b)-[:ADMINISTERED_BY]->(a)
        """

        relationships = [
            ("CalFresh", "Alameda_County_Social_Services"),
            ("Extended_Foster_Care", "Foster_Care_Youth_Services"),
            ("Medi-Cal", "Alameda_County_Healthcare_Services"),
            ("Job_Corps", "California_Employment_Development_Department"),
            ("CalWORKs", "Alameda_County_Social_Services"),
            ("Housing_Voucher_Program", "California_Housing_Finance_Agency"),
            ("Workforce_Development_Program", "Alameda_County_Job_Training"),
            ("Legal_Aid_Services", "Legal_Aid_Organization"),
        ]

        with self.driver.session() as session:
            for benefit_name, agency_name in relationships:
                session.run(query, benefit=benefit_name, agency=agency_name)
            logger.info(f"Created {len(relationships)} ADMINISTERED_BY relationships")

    def create_relationships_organization_serves_life_event(self):
        """Create SERVES relationships between Organizations and LifeEvents"""
        query = """
        MATCH (org:Organization {name: $org}), (le:LifeEvent {name: $event})
        CREATE (org)-[:SERVES]->(le)
        """

        relationships = [
            ("First_Place_for_Youth", "AGED_OUT_OF_FOSTER_CARE"),
            ("First_Place_for_Youth", "HOMELESSNESS_RISK"),
            ("Job_Corps_Oakland", "LOST_JOB"),
            ("Eden_Youth_Fund", "AGED_OUT_OF_FOSTER_CARE"),
            ("Alameda_County_Legal_Aid", "DOMESTIC_VIOLENCE"),
            ("Bay_Area_Community_Services", "SUBSTANCE_RECOVERY"),
            ("A_New_Leaf", "HOMELESSNESS_RISK"),
            ("Alameda_Workforce_Development", "LOST_JOB"),
        ]

        with self.driver.session() as session:
            for org_name, event_name in relationships:
                session.run(query, org=org_name, event=event_name)
            logger.info(f"Created {len(relationships)} SERVES relationships")

    def create_relationships_organization_provides_benefit(self):
        """Create PROVIDES relationships between Organizations and Benefits"""
        query = """
        MATCH (org:Organization {name: $org}), (b:Benefit {name: $benefit})
        CREATE (org)-[:PROVIDES]->(b)
        """

        relationships = [
            ("First_Place_for_Youth", "Foster_Youth_Housing_Program"),
            ("Job_Corps_Oakland", "Job_Corps"),
            ("Community_Food_Bank_Alameda", "Food_Bank_Access"),
            ("Alameda_County_Legal_Aid", "Legal_Aid_Services"),
            ("YouthBuilt_Collective", "Job_Corps"),
            ("Eden_Youth_Fund", "Foster_Youth_Mentorship_Program"),
            ("Futures_Explored", "Education_Grant_Foster_Youth"),
            ("Bay_Area_Community_Services", "Mental_Health_Services"),
            ("A_New_Leaf", "Transitional_Housing"),
            ("Alameda_Workforce_Development", "Workforce_Development_Program"),
        ]

        with self.driver.session() as session:
            for org_name, benefit_name in relationships:
                session.run(query, org=org_name, benefit=benefit_name)
            logger.info(f"Created {len(relationships)} PROVIDES relationships")

    def load_all_data(self):
        """Load all data into the database"""
        try:
            logger.info("Starting data loading...")
            self.create_life_events()
            self.create_documents()
            self.create_agencies()
            self.create_eligibility_rules()
            self.create_outcomes()
            self.create_benefits()
            self.create_organizations()
            self.create_relationships_benefit_requires_document()
            self.create_relationships_benefit_has_rule()
            self.create_relationships_life_event_triggers_benefit()
            self.create_relationships_benefit_unlocks_benefit()
            self.create_relationships_benefit_leads_to_outcome()
            self.create_relationships_benefit_administered_by_agency()
            self.create_relationships_organization_serves_life_event()
            self.create_relationships_organization_provides_benefit()
            logger.info("✅ All data loaded successfully!")
        except Exception as e:
            logger.error(f"❌ Error loading data: {str(e)}")
            raise


def main():
    """Main entry point"""
    # Load credentials from environment variables
    uri = os.getenv("NEO4J_URI", "")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "")

    if not uri or not password:
        raise ValueError(
            "NEO4J_URI and NEO4J_PASSWORD environment variables must be set"
        )

    loader = LifeGraphDataLoader(uri, user, password)
    try:
        loader.load_all_data()
    finally:
        loader.close()


if __name__ == "__main__":
    main()
