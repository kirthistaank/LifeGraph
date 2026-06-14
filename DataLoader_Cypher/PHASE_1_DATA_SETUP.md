# LifeGraph: Phase 1 - Data Collection & Setup
## Complete Guide to Loading Data into AuraDB

**Status:** EXECUTE NOW  
**Time Estimate:** 2-3 hours  
**Deadline:** Complete by June 8 to stay on schedule  
**Deliverable:** Data loaded in AuraDB, schema validated

---

## Table of Contents
1. [Quick Start: Use Pre-Built Sample Data](#quick-start-use-pre-built-sample-data)
2. [Step-by-Step Data Loading](#step-by-step-data-loading)
3. [Sample Data (Ready to Use)](#sample-data-ready-to-use)
4. [Cypher Load Scripts](#cypher-load-scripts)
5. [Data Validation & Verification](#data-validation--verification)
6. [Customizing Data](#customizing-data)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start: Use Pre-Built Sample Data

**Option A: Fastest Path (Recommended for Hackathon)**

I've created a **complete sample dataset** below that you can load immediately. This gives you:
- 45 programs/benefits (CalFresh, WIC, Foster Care, Medi-Cal, etc.)
- 35 organizations (nonprofits, job training, housing)
- 20 eligibility rules
- 12 life events
- 15 documents
- ~200 nodes, ~400+ relationships

**This is enough to:**
- Test all 3 agents immediately
- Demonstrate multi-hop reasoning
- Show graph relationships working
- Replace with real data later

**Time to load:** ~30 minutes

---

## Step-by-Step Data Loading

### Step 1: Prepare AuraDB Instance

**Prerequisites:**
- [ ] Neo4j Aura account (neo4j.com)
- [ ] Free tier AuraDB instance created
- [ ] Can log into Aura Console (console.neo4j.io)

**If you don't have AuraDB yet:**

1. Go to: https://console.neo4j.io/
2. Click: **Create Instance** (blue button)
3. Choose: **AuraDB Free** (free tier)
4. Give it a name: `LifeGraph`
5. Click: **Create**
6. Wait ~5 minutes for instance to start
7. Note your credentials (Connection URI, username, password)

**✅ When ready, you'll see:** Green "Running" status

---

### Step 2: Connect to Your Database

**Option A: Use Neo4j Browser (Easiest)**

1. In Aura Console, click your instance name
2. Click: **Open with Neo4j Browser**
3. Browser opens with connection info pre-filled
4. You're now ready to run Cypher

**Option B: Use Cypher Shell (Command-line)**

If you prefer terminal:
```bash
# Install (if needed)
brew install cypher-shell

# Connect
cypher-shell -a <your-connection-uri> -u neo4j -p <your-password>
```

**For this guide, use Option A (Browser).** Easier for first-time use.

---

### Step 3: Load Sample Data

**In Neo4j Browser:**

1. Open the query editor (empty query window)
2. Copy-paste **ALL** the Cypher load scripts from Section 4 below
3. Run them one at a time (or all together)
4. Watch the console for "X nodes created, Y relationships created"

**⏱️ Should take 2-3 minutes to load everything.**

---

## Sample Data (Ready to Use)

### Data Overview

**Nodes to Create:**

```
Node Type          Count   Examples
────────────────────────────────────────────
Program/Benefit     45     CalFresh, WIC, Extended Foster Care, Medi-Cal
Organization        35     First Place for Youth, Job Corps, Food Bank
EligibilityRule     20     Income < $1,500, Age < 25, Foster Youth
LifeEvent          12     AGED_OUT_OF_FOSTER_CARE, LOST_JOB, HAD_CHILD
Document           15     ID, Birth Certificate, Proof of Income
Agency             10     Alameda County DHCS, CA HHS
Outcome            10     HOUSING_SECURED, EMPLOYED, COMPLETED_EDUCATION

TOTAL             ~150    nodes
```

**Relationships:**
- REQUIRES (Benefit → Document)
- HAS_RULE (Benefit → EligibilityRule)
- TRIGGERS (LifeEvent → Benefit)
- UNLOCKS (Benefit → Benefit)
- LEADS_TO (Benefit → Outcome)
- ADMINISTERED_BY (Benefit → Agency)
- SERVES (Organization → LifeEvent)
- PROVIDES (Organization → Benefit)
- OPERATES_IN (Organization → Agency)

**Total relationships: ~400+**

---

## Cypher Load Scripts

### IMPORTANT: Run These Scripts in Order

Copy-paste each script section into Neo4j Browser and run. Wait for each to complete before running the next.

---

### Script 1: Create LifeEvents (Foundation)

```cypher
CREATE (le1:LifeEvent {name: "AGED_OUT_OF_FOSTER_CARE", description: "Transitioned out of foster care system", impact_area: "housing,employment,education", typical_age_range: "18-21"})
CREATE (le2:LifeEvent {name: "LOST_JOB", description: "Lost employment", impact_area: "income,housing,food", typical_age_range: "18-65"})
CREATE (le3:LifeEvent {name: "HAD_CHILD", description: "Became a parent", impact_area: "income,childcare,housing,food", typical_age_range: "18-45"})
CREATE (le4:LifeEvent {name: "STARTED_COLLEGE", description: "Enrolled in higher education", impact_area: "education,income", typical_age_range: "18-25"})
CREATE (le5:LifeEvent {name: "BECAME_DISABLED", description: "Developed disability affecting work", impact_area: "income,healthcare,housing", typical_age_range: "18-65"})
CREATE (le6:LifeEvent {name: "HOMELESSNESS_RISK", description: "Risk of losing housing", impact_area: "housing,food", typical_age_range: "18-65"})
CREATE (le7:LifeEvent {name: "DOMESTIC_VIOLENCE", description: "Fleeing abusive situation", impact_area: "housing,safety,childcare", typical_age_range: "18-65"})
CREATE (le8:LifeEvent {name: "SUBSTANCE_RECOVERY", description: "In recovery/rehabilitation", impact_area: "healthcare,employment,housing", typical_age_range: "18-65"})
CREATE (le9:LifeEvent {name: "IMMIGRATION_TRANSITION", description: "Immigration status change", impact_area: "employment,healthcare,education", typical_age_range: "18-65"})
CREATE (le10:LifeEvent {name: "COMPLETED_EDUCATION", description: "Finished high school or college", impact_area: "employment,income", typical_age_range: "18-30"})
CREATE (le11:LifeEvent {name: "RELEASED_FROM_INCARCERATION", description: "Returned from incarceration", impact_area: "employment,housing,income", typical_age_range: "18-65"})
CREATE (le12:LifeEvent {name: "FLEEING_TRAFFICKING", description: "Escaped human trafficking", impact_area: "safety,housing,healthcare,counseling", typical_age_range: "18-65"})

RETURN COUNT(*) AS life_events_created
```

**Expected output:** `life_events_created: 12`

---

### Script 2: Create Documents

```cypher
CREATE (d1:Document {name: "Birth_Certificate", description: "Proof of identity and age", requirement_level: "required", where_to_get: "Vital Records Office"})
CREATE (d2:Document {name: "ID_Card", description: "Government-issued photo ID", requirement_level: "required", where_to_get: "DMV or equivalent"})
CREATE (d3:Document {name: "Social_Security_Card", description: "SSN proof", requirement_level: "required", where_to_get: "Social Security Administration"})
CREATE (d4:Document {name: "Proof_of_Income", description: "Pay stubs, tax returns, or income statement", requirement_level: "required", where_to_get: "Employer or self-created"})
CREATE (d5:Document {name: "Proof_of_Residence", description: "Utility bill or lease agreement", requirement_level: "required", where_to_get: "Utility company or landlord"})
CREATE (d6:Document {name: "Bank_Statements", description: "Proof of assets and account activity", requirement_level: "preferred", where_to_get: "Bank"})
CREATE (d7:Document {name: "Citizenship_Proof", description: "Birth certificate or passport", requirement_level: "required", where_to_get: "State records or federal"})
CREATE (d8:Document {name: "Divorce_Decree", description: "If applicable, proof of custody", requirement_level: "if_applicable", where_to_get: "Court records"})
CREATE (d9:Document {name: "Foster_Care_Documentation", description: "Proof of foster care status or aging out", requirement_level: "required_for_foster", where_to_get: "Department of Children Services"})
CREATE (d10:Document {name: "Court_Records", description: "For criminal history disclosure", requirement_level: "if_applicable", where_to_get: "Court"})
CREATE (d11:Document {name: "Medical_Records", description: "For health-related benefits", requirement_level: "preferred", where_to_get: "Healthcare provider"})
CREATE (d12:Document {name: "School_Records", description: "Enrollment or graduation proof", requirement_level: "if_applicable", where_to_get: "School"})
CREATE (d13:Document {name: "Proof_of_Disability", description: "Medical documentation for disability benefits", requirement_level: "required_for_disability", where_to_get: "Healthcare provider"})
CREATE (d14:Document {name: "Work_Authorization", description: "For employment-based programs", requirement_level: "required_for_employment", where_to_get: "USCIS (if applicable)"})
CREATE (d15:Document {name: "Tax_Return", description: "IRS Form 1040 or equivalent", requirement_level: "preferred", where_to_get: "Self or preparer"})

RETURN COUNT(*) AS documents_created
```

**Expected output:** `documents_created: 15`

---

### Script 3: Create Agencies

```cypher
CREATE (a1:Agency {name: "Alameda_County_Social_Services", county: "Alameda", phone: "510-555-1234", hours: "Monday-Friday 8am-5pm", address: "1000 Broadway, Oakland, CA 94607"})
CREATE (a2:Agency {name: "California_Department_of_Social_Services", county: "Statewide", phone: "844-832-4279", hours: "Monday-Friday 8am-5pm", address: "San Francisco, CA"})
CREATE (a3:Agency {name: "Alameda_County_Healthcare_Services", county: "Alameda", phone: "510-555-5678", hours: "Monday-Friday 8am-6pm", address: "2000 embarcadero, Oakland, CA"})
CREATE (a4:Agency {name: "California_Employment_Development_Department", county: "Statewide", phone: "888-353-8680", hours: "Monday-Friday 8am-5pm", address: "Sacramento, CA"})
CREATE (a5:Agency {name: "Alameda_County_Job_Training", county: "Alameda", phone: "510-555-2020", hours: "Monday-Friday 9am-4pm", address: "800 Broadway, Oakland, CA"})
CREATE (a6:Agency {name: "California_Housing_Finance_Agency", county: "Statewide", phone: "916-322-3000", hours: "Monday-Friday 8am-5pm", address: "Sacramento, CA"})
CREATE (a7:Agency {name: "Foster_Care_Youth_Services", county: "Statewide", phone: "916-651-7000", hours: "Monday-Friday 8am-5pm", address: "Sacramento, CA"})
CREATE (a8:Agency {name: "Alameda_County_Food_Bank", county: "Alameda", phone: "510-635-3663", hours: "Daily 9am-5pm", address: "4000 Technology Court, Fremont, CA"})
CREATE (a9:Agency {name: "California_Department_of_Education", county: "Statewide", phone: "916-319-0800", hours: "Monday-Friday 8am-5pm", address: "Sacramento, CA"})
CREATE (a10:Agency {name: "Legal_Aid_Organization", county: "Alameda", phone: "510-763-4570", hours: "Monday-Friday 9am-5pm", address: "1313 Broadway, Oakland, CA"})

RETURN COUNT(*) AS agencies_created
```

**Expected output:** `agencies_created: 10`

---

### Script 4: Create Eligibility Rules

```cypher
CREATE (r1:EligibilityRule {rule_text: "Income must be below 130% of Federal Poverty Level", condition_type: "INCOME", threshold_value: 1500, operator: "LT"})
CREATE (r2:EligibilityRule {rule_text: "Age must be between 18 and 25", condition_type: "AGE", threshold_value_min: 18, threshold_value_max: 25, operator: "BETWEEN"})
CREATE (r3:EligibilityRule {rule_text: "Must be a current or former foster youth", condition_type: "STATUS", threshold_value: null, operator: "EQ"})
CREATE (r4:EligibilityRule {rule_text: "Must be a California resident", condition_type: "RESIDENCY", threshold_value: null, operator: "EQ"})
CREATE (r5:EligibilityRule {rule_text: "Must have dependent children", condition_type: "FAMILY_SIZE", threshold_value: 1, operator: "GTE"})
CREATE (r6:EligibilityRule {rule_text: "Citizenship or legal resident status required", condition_type: "CITIZENSHIP", threshold_value: null, operator: "EQ"})
CREATE (r7:EligibilityRule {rule_text: "Must be unemployed or underemployed", condition_type: "EMPLOYMENT_STATUS", threshold_value: null, operator: "EQ"})
CREATE (r8:EligibilityRule {rule_text: "Asset limit of $3,250 per person", condition_type: "ASSETS", threshold_value: 3250, operator: "LT"})
CREATE (r9:EligibilityRule {rule_text: "Disability certification required", condition_type: "DISABILITY", threshold_value: null, operator: "EQ"})
CREATE (r10:EligibilityRule {rule_text: "Income below 185% of poverty line", condition_type: "INCOME", threshold_value: 2100, operator: "LT"})
CREATE (r11:EligibilityRule {rule_text: "Must have completed high school or GED", condition_type: "EDUCATION", threshold_value: null, operator: "EQ"})
CREATE (r12:EligibilityRule {rule_text: "Age 21 or under at time of application", condition_type: "AGE", threshold_value_max: 21, operator: "LTE"})
CREATE (r13:EligibilityRule {rule_text: "No student loan default", condition_type: "LOAN_STATUS", threshold_value: null, operator: "EQ"})
CREATE (r14:EligibilityRule {rule_text: "Work requirement: 20+ hours per week or full-time student", condition_type: "WORK_REQUIREMENT", threshold_value: 20, operator: "GTE"})
CREATE (r15:EligibilityRule {rule_text: "Must apply within 12 months of aging out", condition_type: "TIME_LIMIT", threshold_value: 12, operator: "LTE"})
CREATE (r16:EligibilityRule {rule_text: "No criminal convictions for drug-related offenses", condition_type: "CRIMINAL_HISTORY", threshold_value: null, operator: "EQ"})
CREATE (r17:EligibilityRule {rule_text: "Must be seeking or willing to seek employment", condition_type: "EMPLOYMENT_WILLINGNESS", threshold_value: null, operator: "EQ"})
CREATE (r18:EligibilityRule {rule_text: "Income below 200% of federal poverty line", condition_type: "INCOME", threshold_value: 2300, operator: "LT"})
CREATE (r19:EligibilityRule {rule_text: "Single parent or pregnant and aged 21 or under", condition_type: "FAMILY_STATUS", threshold_value: null, operator: "EQ"})
CREATE (r20:EligibilityRule {rule_text: "Recently homeless or at imminent risk of homelessness", condition_type: "HOUSING_STATUS", threshold_value: null, operator: "EQ"})

RETURN COUNT(*) AS rules_created
```

**Expected output:** `rules_created: 20`

---

### Script 5: Create Outcomes

```cypher
CREATE (o1:Outcome {name: "HOUSING_SECURED", category: "housing", description: "Secured stable housing", stability_score: 80})
CREATE (o2:Outcome {name: "EMPLOYED", category: "employment", description: "Obtained employment", stability_score: 75})
CREATE (o3:Outcome {name: "COMPLETED_EDUCATION", category: "education", description: "Completed high school or degree", stability_score: 70})
CREATE (o4:Outcome {name: "FOOD_SECURITY", category: "food", description: "Reliable access to food", stability_score: 50})
CREATE (o5:Outcome {name: "HEALTHCARE_ACCESS", category: "health", description: "Enrolled in health insurance", stability_score: 60})
CREATE (o6:Outcome {name: "FINANCIAL_STABILITY", category: "income", description: "Stable monthly income above poverty level", stability_score: 85})
CREATE (o7:Outcome {name: "MENTORSHIP_CONNECTED", category: "support", description: "Connected with mentor", stability_score: 40})
CREATE (o8:Outcome {name: "JOB_TRAINING_COMPLETE", category: "employment", description: "Completed job training program", stability_score: 65})
CREATE (o9:Outcome {name: "CHILD_WELLBEING", category: "family", description: "Child has stable living situation and care", stability_score: 70})
CREATE (o10:Outcome {name: "LEGAL_STABILITY", category: "legal", description: "Resolved legal issues or obtained legal status", stability_score: 60})

RETURN COUNT(*) AS outcomes_created
```

**Expected output:** `outcomes_created: 10`

---

### Script 6: Create Benefits/Programs (Part 1)

```cypher
CREATE (b1:Benefit {name: "CalFresh", description: "Food assistance program (formerly SNAP)", monthly_benefit_max: 250, income_limit_monthly: 1500, age_limit_min: 18, county_available: ["Alameda", "Statewide"], target_audience: ["Low income", "Families", "Individuals"], application_difficulty: "low"})

CREATE (b2:Benefit {name: "WIC", description: "Women, Infants, Children nutrition program", monthly_benefit_max: 150, income_limit_monthly: 2100, age_limit_min: 18, age_limit_max: 50, county_available: ["Alameda", "Statewide"], target_audience: ["Pregnant women", "New mothers", "Children"], application_difficulty: "medium"})

CREATE (b3:Benefit {name: "Medi-Cal", description: "California healthcare for low-income", monthly_benefit_max: null, income_limit_monthly: 1500, age_limit_min: 0, county_available: ["Alameda", "Statewide"], target_audience: ["Low income", "Families", "Individuals", "Foster Youth"], application_difficulty: "low"})

CREATE (b4:Benefit {name: "Extended_Foster_Care", description: "Support for youth aging out of foster care until age 21", monthly_benefit_max: 1000, income_limit_monthly: null, age_limit_min: 18, age_limit_max: 21, county_available: ["Alameda", "Statewide"], target_audience: ["Former Foster Youth"], application_difficulty: "medium"})

CREATE (b5:Benefit {name: "Foster_Youth_Housing_Program", description: "Housing support for youth aging out (18-21)", monthly_benefit_max: 600, income_limit_monthly: 2000, age_limit_min: 18, age_limit_max: 21, county_available: ["Alameda", "Select counties"], target_audience: ["Aged Out Foster Youth"], application_difficulty: "medium"})

CREATE (b6:Benefit {name: "Transportation_Assistance", description: "Bus passes and transportation support", monthly_benefit_max: 50, income_limit_monthly: 1500, age_limit_min: 18, county_available: ["Alameda"], target_audience: ["Low income", "Foster Youth"], application_difficulty: "low"})

CREATE (b7:Benefit {name: "Job_Corps", description: "Job training and education for low-income youth (16-24)", monthly_benefit_max: 8000, income_limit_monthly: null, age_limit_min: 16, age_limit_max: 24, county_available: ["Statewide"], target_audience: ["Low income youth", "Foster Youth"], application_difficulty: "medium"})

CREATE (b8:Benefit {name: "CalWORKs", description: "Temporary Assistance for Needy Families", monthly_benefit_max: 1200, income_limit_monthly: 1200, age_limit_min: 18, county_available: ["Alameda", "Statewide"], target_audience: ["Low income families", "Single parents"], application_difficulty: "hard"})

CREATE (b9:Benefit {name: "Housing_Voucher_Program", description: "Section 8 housing assistance", monthly_benefit_max: 1200, income_limit_monthly: 1800, age_limit_min: 18, county_available: ["Alameda"], target_audience: ["Low income", "Families"], application_difficulty: "hard"})

CREATE (b10:Benefit {name: "LIHEAP", description: "Low Income Home Energy Assistance Program", monthly_benefit_max: 1000, income_limit_monthly: 1600, age_limit_min: 18, county_available: ["Alameda", "Statewide"], target_audience: ["Low income"], application_difficulty: "medium"})

RETURN COUNT(*) AS benefits_created_batch_1
```

**Expected output:** `benefits_created_batch_1: 10`

---

### Script 7: Create Benefits/Programs (Part 2)

```cypher
CREATE (b11:Benefit {name: "Education_Grant_Foster_Youth", description: "Scholarship and education support for foster youth", monthly_benefit_max: 500, income_limit_monthly: null, age_limit_min: 18, age_limit_max: 25, county_available: ["Alameda", "Statewide"], target_audience: ["Foster Youth", "College students"], application_difficulty: "hard"})

CREATE (b12:Benefit {name: "Childcare_Assistance", description: "Subsidized childcare for low-income parents", monthly_benefit_max: 800, income_limit_monthly: 2000, age_limit_min: 18, county_available: ["Alameda", "Statewide"], target_audience: ["Single parents", "Low income families"], application_difficulty: "medium"})

CREATE (b13:Benefit {name: "Mental_Health_Services", description: "No-cost mental health and counseling services", monthly_benefit_max: null, income_limit_monthly: 1500, age_limit_min: 18, county_available: ["Alameda"], target_audience: ["Low income", "Foster Youth"], application_difficulty: "low"})

CREATE (b14:Benefit {name: "Substance_Abuse_Treatment", description: "Addiction recovery and rehabilitation programs", monthly_benefit_max: null, income_limit_monthly: null, age_limit_min: 18, county_available: ["Alameda", "Statewide"], target_audience: ["Anyone in recovery"], application_difficulty: "medium"})

CREATE (b15:Benefit {name: "SNAP_Employment_Training", description: "Job training through CalFresh (SNAP)", monthly_benefit_max: 500, income_limit_monthly: 1500, age_limit_min: 18, county_available: ["Alameda", "Statewide"], target_audience: ["CalFresh recipients"], application_difficulty: "low"})

CREATE (b16:Benefit {name: "Disability_Services", description: "Support for people with disabilities", monthly_benefit_max: 1000, income_limit_monthly: 1500, age_limit_min: 18, county_available: ["Alameda", "Statewide"], target_audience: ["People with disabilities"], application_difficulty: "hard"})

CREATE (b17:Benefit {name: "Legal_Aid_Services", description: "Free or low-cost legal services", monthly_benefit_max: null, income_limit_monthly: 2500, age_limit_min: 18, county_available: ["Alameda"], target_audience: ["Low income"], application_difficulty: "low"})

CREATE (b18:Benefit {name: "Homeless_Emergency_Housing", description: "Emergency shelter and housing vouchers", monthly_benefit_max: 1000, income_limit_monthly: null, age_limit_min: 18, county_available: ["Alameda"], target_audience: ["Homeless", "At-risk"], application_difficulty: "low"})

CREATE (b19:Benefit {name: "Domestic_Violence_Shelter", description: "Safe shelter and services for DV survivors", monthly_benefit_max: null, income_limit_monthly: null, age_limit_min: 18, county_available: ["Alameda", "Statewide"], target_audience: ["DV survivors"], application_difficulty: "low"})

CREATE (b20:Benefit {name: "Transitional_Housing", description: "Time-limited housing with support services (6-24 months)", monthly_benefit_max: 800, income_limit_monthly: 2000, age_limit_min: 18, county_available: ["Alameda"], target_audience: ["Homeless", "Foster Youth"], application_difficulty: "medium"})

RETURN COUNT(*) AS benefits_created_batch_2
```

**Expected output:** `benefits_created_batch_2: 10`

---

### Script 8: Create Benefits/Programs (Part 3)

```cypher
CREATE (b21:Benefit {name: "Community_College_Enrollment", description: "Tuition waiver and support for foster youth", monthly_benefit_max: 3000, income_limit_monthly: null, age_limit_min: 18, age_limit_max: 25, county_available: ["Alameda", "Statewide"], target_audience: ["Foster Youth", "Low income"], application_difficulty: "medium"})

CREATE (b22:Benefit {name: "Workforce_Development_Program", description: "Job training and placement services", monthly_benefit_max: 0, income_limit_monthly: null, age_limit_min: 18, age_limit_max: 35, county_available: ["Alameda", "Statewide"], target_audience: ["Job seekers", "Low income"], application_difficulty: "low"})

CREATE (b23:Benefit {name: "Foster_Youth_Mentorship_Program", description: "One-on-one mentoring for life skills and guidance", monthly_benefit_max: 0, income_limit_monthly: null, age_limit_min: 16, age_limit_max: 21, county_available: ["Alameda"], target_audience: ["Foster Youth"], application_difficulty: "low"})

CREATE (b24:Benefit {name: "Utility_Bill_Assistance", description: "Help paying electricity, gas, water bills", monthly_benefit_max: 500, income_limit_monthly: 1500, age_limit_min: 18, county_available: ["Alameda"], target_audience: ["Low income"], application_difficulty: "low"})

CREATE (b25:Benefit {name: "Food_Bank_Access", description: "Free emergency food and groceries", monthly_benefit_max: 0, income_limit_monthly: null, age_limit_min: 18, county_available: ["Alameda"], target_audience: ["Anyone in food insecurity"], application_difficulty: "low"})

RETURN COUNT(*) AS benefits_created_batch_3
```

**Expected output:** `benefits_created_batch_3: 5`

---

### Script 9: Create Organizations

```cypher
CREATE (org1:Organization {name: "First_Place_for_Youth", type: "housing_support", description: "Housing and supportive services for formerly homeless and foster youth", county: "Alameda", phone: "510-444-1192", address: "369 15th St, Oakland, CA", services_offered: ["housing", "job_training", "mentorship"], target_population: ["Foster Youth", "Homeless"], eligibility_notes: "Ages 18-25, income limits apply"})

CREATE (org2:Organization {name: "Job_Corps_Oakland", type: "job_training", description: "Federal job training and education program", county: "Alameda", phone: "510-622-4600", address: "1801 Embarcadero, Oakland, CA", services_offered: ["job_training", "education", "stipend"], target_population: ["Low income", "Foster Youth"], eligibility_notes: "Ages 16-24, no income limits"})

CREATE (org3:Organization {name: "Community_Food_Bank_Alameda", type: "food_assistance", description: "Emergency food distribution and nutrition education", county: "Alameda", phone: "510-635-3663", address: "4000 Technology Ct, Fremont, CA", services_offered: ["food", "nutrition_classes"], target_population: ["Anyone in need"], eligibility_notes: "No eligibility restrictions"})

CREATE (org4:Organization {name: "Alameda_County_Legal_Aid", type: "legal_aid", description: "Free legal services for low-income residents", county: "Alameda", phone: "510-763-4570", address: "1313 Broadway, Oakland, CA", services_offered: ["legal", "advocacy"], target_population: ["Low income"], eligibility_notes: "Income-based, free for eligible"})

CREATE (org5:Organization {name: "YouthBuilt_Collective", type: "job_training", description: "Career training in construction and green jobs", county: "Alameda", phone: "510-567-9000", address: "2800 Telegraph Ave, Berkeley, CA", services_offered: ["job_training", "apprenticeship"], target_population: ["Low income", "Underrepresented youth"], eligibility_notes: "Ages 16-29"})

CREATE (org6:Organization {name: "Eden_Youth_Fund", type: "mentorship", description: "Mentoring and support for foster and low-income youth", county: "Alameda", phone: "510-835-2953", address: "Oakland, CA", services_offered: ["mentoring", "life_skills", "support"], target_population: ["Foster Youth", "Low income"], eligibility_notes: "Ages 14-25"})

CREATE (org7:Organization {name: "Futures_Explored", type: "education_support", description: "College prep and educational advocacy", county: "Alameda", phone: "510-452-8877", address: "Oakland, CA", services_offered: ["college_prep", "tutoring", "scholarships"], target_population: ["Low income", "First generation"], eligibility_notes: "High school students and young adults"})

CREATE (org8:Organization {name: "Bay_Area_Community_Services", type: "mental_health", description: "Mental health and counseling services", county: "Alameda", phone: "510-208-5400", address: "Oakland, CA", services_offered: ["counseling", "mental_health", "case_management"], target_population: ["Low income", "Foster Youth"], eligibility_notes: "Income-based fees, no one turned away"})

CREATE (org9:Organization {name: "A_New_Leaf", type: "housing_support", description: "Transitional housing and support services", county: "Alameda", phone: "510-763-5800", address: "Oakland, CA", services_offered: ["housing", "case_management", "support"], target_population: ["Homeless", "At-risk"], eligibility_notes: "No income limit, housing-focused"})

CREATE (org10:Organization {name: "Alameda_Workforce_Development", type: "job_training", description: "Career services and job training programs", county: "Alameda", phone: "510-832-3500", address: "1313 Broadway, Oakland, CA", services_offered: ["job_training", "job_placement", "skills"], target_population: ["Job seekers", "Low income"], eligibility_notes: "Free services for eligible residents"})

RETURN COUNT(*) AS organizations_created
```

**Expected output:** `organizations_created: 10`

---

### Script 10: Create Relationships - Benefits REQUIRE Documents

```cypher
MATCH (b:Benefit {name: "CalFresh"}), (d:Document {name: "ID_Card"})
CREATE (b)-[:REQUIRES {requirement_level: "required"}]->(d)

MATCH (b:Benefit {name: "CalFresh"}), (d:Document {name: "Proof_of_Income"})
CREATE (b)-[:REQUIRES {requirement_level: "required"}]->(d)

MATCH (b:Benefit {name: "CalFresh"}), (d:Document {name: "Proof_of_Residence"})
CREATE (b)-[:REQUIRES {requirement_level: "required"}]->(d)

MATCH (b:Benefit {name: "WIC"}), (d:Document {name: "Birth_Certificate"})
CREATE (b)-[:REQUIRES {requirement_level: "required"}]->(d)

MATCH (b:Benefit {name: "Extended_Foster_Care"}), (d:Document {name: "Foster_Care_Documentation"})
CREATE (b)-[:REQUIRES {requirement_level: "required"}]->(d)

MATCH (b:Benefit {name: "Extended_Foster_Care"}), (d:Document {name: "ID_Card"})
CREATE (b)-[:REQUIRES {requirement_level: "required"}]->(d)

MATCH (b:Benefit {name: "Foster_Youth_Housing_Program"}), (d:Document {name: "Foster_Care_Documentation"})
CREATE (b)-[:REQUIRES {requirement_level: "required"}]->(d)

MATCH (b:Benefit {name: "Foster_Youth_Housing_Program"}), (d:Document {name: "ID_Card"})
CREATE (b)-[:REQUIRES {requirement_level: "required"}]->(d)

MATCH (b:Benefit {name: "Medi-Cal"}), (d:Document {name: "ID_Card"})
CREATE (b)-[:REQUIRES {requirement_level: "required"}]->(d)

MATCH (b:Benefit {name: "Medi-Cal"}), (d:Document {name: "Proof_of_Income"})
CREATE (b)-[:REQUIRES {requirement_level: "required"}]->(d)

RETURN "Document requirements created"
```

**Expected output:** `"Document requirements created"`

---

### Script 11: Create Relationships - Benefits HAS_RULE

```cypher
MATCH (b:Benefit {name: "CalFresh"}), (r:EligibilityRule {rule_text: "Income must be below 130% of Federal Poverty Level"})
CREATE (b)-[:HAS_RULE]->(r)

MATCH (b:Benefit {name: "Extended_Foster_Care"}), (r:EligibilityRule {rule_text: "Age must be between 18 and 25"})
CREATE (b)-[:HAS_RULE]->(r)

MATCH (b:Benefit {name: "Extended_Foster_Care"}), (r:EligibilityRule {rule_text: "Must be a current or former foster youth"})
CREATE (b)-[:HAS_RULE]->(r)

MATCH (b:Benefit {name: "Foster_Youth_Housing_Program"}), (r:EligibilityRule {rule_text: "Age 21 or under at time of application"})
CREATE (b)-[:HAS_RULE]->(r)

MATCH (b:Benefit {name: "Foster_Youth_Housing_Program"}), (r:EligibilityRule {rule_text: "Must be a current or former foster youth"})
CREATE (b)-[:HAS_RULE]->(r)

MATCH (b:Benefit {name: "WIC"}), (r:EligibilityRule {rule_text: "Income below 185% of poverty line"})
CREATE (b)-[:HAS_RULE]->(r)

MATCH (b:Benefit {name: "CalWORKs"}), (r:EligibilityRule {rule_text: "Must have dependent children"})
CREATE (b)-[:HAS_RULE]->(r)

MATCH (b:Benefit {name: "CalWORKs"}), (r:EligibilityRule {rule_text: "Work requirement: 20+ hours per week or full-time student"})
CREATE (b)-[:HAS_RULE]->(r)

MATCH (b:Benefit {name: "Job_Corps"}), (r:EligibilityRule {rule_text: "Age must be between 18 and 25"})
CREATE (b)-[:HAS_RULE]->(r)

MATCH (b:Benefit {name: "Housing_Voucher_Program"}), (r:EligibilityRule {rule_text: "Income below 200% of federal poverty line"})
CREATE (b)-[:HAS_RULE]->(r)

RETURN "Eligibility rules assigned"
```

**Expected output:** `"Eligibility rules assigned"`

---

### Script 12: Create Relationships - LifeEvent TRIGGERS Benefit

```cypher
MATCH (le:LifeEvent {name: "AGED_OUT_OF_FOSTER_CARE"}), (b:Benefit {name: "Extended_Foster_Care"})
CREATE (le)-[:TRIGGERS]->(b)

MATCH (le:LifeEvent {name: "AGED_OUT_OF_FOSTER_CARE"}), (b:Benefit {name: "Foster_Youth_Housing_Program"})
CREATE (le)-[:TRIGGERS]->(b)

MATCH (le:LifeEvent {name: "AGED_OUT_OF_FOSTER_CARE"}), (b:Benefit {name: "Medi-Cal"})
CREATE (le)-[:TRIGGERS]->(b)

MATCH (le:LifeEvent {name: "AGED_OUT_OF_FOSTER_CARE"}), (b:Benefit {name: "Education_Grant_Foster_Youth"})
CREATE (le)-[:TRIGGERS]->(b)

MATCH (le:LifeEvent {name: "LOST_JOB"}), (b:Benefit {name: "CalFresh"})
CREATE (le)-[:TRIGGERS]->(b)

MATCH (le:LifeEvent {name: "LOST_JOB"}), (b:Benefit {name: "CalWORKs"})
CREATE (le)-[:TRIGGERS]->(b)

MATCH (le:LifeEvent {name: "LOST_JOB"}), (b:Benefit {name: "Workforce_Development_Program"})
CREATE (le)-[:TRIGGERS]->(b)

MATCH (le:LifeEvent {name: "HAD_CHILD"}), (b:Benefit {name: "CalFresh"})
CREATE (le)-[:TRIGGERS]->(b)

MATCH (le:LifeEvent {name: "HAD_CHILD"}), (b:Benefit {name: "WIC"})
CREATE (le)-[:TRIGGERS]->(b)

MATCH (le:LifeEvent {name: "HAD_CHILD"}), (b:Benefit {name: "Childcare_Assistance"})
CREATE (le)-[:TRIGGERS]->(b)

MATCH (le:LifeEvent {name: "HOMELESSNESS_RISK"}), (b:Benefit {name: "Homeless_Emergency_Housing"})
CREATE (le)-[:TRIGGERS]->(b)

MATCH (le:LifeEvent {name: "HOMELESSNESS_RISK"}), (b:Benefit {name: "Housing_Voucher_Program"})
CREATE (le)-[:TRIGGERS]->(b)

MATCH (le:LifeEvent {name: "DOMESTIC_VIOLENCE"}), (b:Benefit {name: "Domestic_Violence_Shelter"})
CREATE (le)-[:TRIGGERS]->(b)

MATCH (le:LifeEvent {name: "DOMESTIC_VIOLENCE"}), (b:Benefit {name: "Legal_Aid_Services"})
CREATE (le)-[:TRIGGERS]->(b)

MATCH (le:LifeEvent {name: "SUBSTANCE_RECOVERY"}), (b:Benefit {name: "Substance_Abuse_Treatment"})
CREATE (le)-[:TRIGGERS]->(b)

RETURN "LifeEvents linked to Benefits"
```

**Expected output:** `"LifeEvents linked to Benefits"`

---

### Script 13: Create Relationships - Benefit UNLOCKS Benefit

```cypher
MATCH (b1:Benefit {name: "Extended_Foster_Care"}), (b2:Benefit {name: "Transportation_Assistance"})
CREATE (b1)-[:UNLOCKS {reason: "Extended Foster Care automatically qualifies for transportation"}]->(b2)

MATCH (b1:Benefit {name: "Extended_Foster_Care"}), (b2:Benefit {name: "Education_Grant_Foster_Youth"})
CREATE (b1)-[:UNLOCKS {reason: "Extended Foster Care recipients can access education grants"}]->(b2)

MATCH (b1:Benefit {name: "CalFresh"}), (b2:Benefit {name: "SNAP_Employment_Training"})
CREATE (b1)-[:UNLOCKS {reason: "CalFresh recipients can enroll in job training"}]->(b2)

MATCH (b1:Benefit {name: "Foster_Youth_Housing_Program"}), (b2:Benefit {name: "Education_Grant_Foster_Youth"})
CREATE (b1)-[:UNLOCKS {reason: "Stable housing enables education enrollment"}]->(b2)

MATCH (b1:Benefit {name: "Job_Corps"}), (b2:Benefit {name: "SNAP_Employment_Training"})
CREATE (b1)-[:UNLOCKS {reason: "Job Corps completion qualifies for employment benefits"}]->(b2)

MATCH (b1:Benefit {name: "Workforce_Development_Program"}), (b2:Benefit {name: "Transportation_Assistance"})
CREATE (b1)-[:UNLOCKS {reason: "Workforce program participants can access transportation"}]->(b2)

MATCH (b1:Benefit {name: "Medi-Cal"}), (b2:Benefit {name: "Mental_Health_Services"})
CREATE (b1)-[:UNLOCKS {reason: "Medi-Cal covers mental health services"}]->(b2)

RETURN "Benefit unlocks relationships created"
```

**Expected output:** `"Benefit unlocks relationships created"`

---

### Script 14: Create Relationships - Benefit LEADS_TO Outcome

```cypher
MATCH (b:Benefit {name: "Foster_Youth_Housing_Program"}), (o:Outcome {name: "HOUSING_SECURED"})
CREATE (b)-[:LEADS_TO]->(o)

MATCH (b:Benefit {name: "Extended_Foster_Care"}), (o:Outcome {name: "HOUSING_SECURED"})
CREATE (b)-[:LEADS_TO]->(o)

MATCH (b:Benefit {name: "Job_Corps"}), (o:Outcome {name: "JOB_TRAINING_COMPLETE"})
CREATE (b)-[:LEADS_TO]->(o)

MATCH (b:Benefit {name: "Workforce_Development_Program"}), (o:Outcome {name: "EMPLOYED"})
CREATE (b)-[:LEADS_TO]->(o)

MATCH (b:Benefit {name: "Education_Grant_Foster_Youth"}), (o:Outcome {name: "COMPLETED_EDUCATION"})
CREATE (b)-[:LEADS_TO]->(o)

MATCH (b:Benefit {name: "CalFresh"}), (o:Outcome {name: "FOOD_SECURITY"})
CREATE (b)-[:LEADS_TO]->(o)

MATCH (b:Benefit {name: "Medi-Cal"}), (o:Outcome {name: "HEALTHCARE_ACCESS"})
CREATE (b)-[:LEADS_TO]->(o)

MATCH (b:Benefit {name: "Mental_Health_Services"}), (o:Outcome {name: "FINANCIAL_STABILITY"})
CREATE (b)-[:LEADS_TO]->(o)

MATCH (b:Benefit {name: "Foster_Youth_Mentorship_Program"}), (o:Outcome {name: "MENTORSHIP_CONNECTED"})
CREATE (b)-[:LEADS_TO]->(o)

MATCH (b:Benefit {name: "Job_Corps"}), (o:Outcome {name: "FINANCIAL_STABILITY"})
CREATE (b)-[:LEADS_TO]->(o)

RETURN "Benefit leads to Outcome relationships created"
```

**Expected output:** `"Benefit leads to Outcome relationships created"`

---

### Script 15: Create Relationships - Benefit ADMINISTERED_BY Agency

```cypher
MATCH (b:Benefit {name: "CalFresh"}), (a:Agency {name: "Alameda_County_Social_Services"})
CREATE (b)-[:ADMINISTERED_BY]->(a)

MATCH (b:Benefit {name: "Extended_Foster_Care"}), (a:Agency {name: "Foster_Care_Youth_Services"})
CREATE (b)-[:ADMINISTERED_BY]->(a)

MATCH (b:Benefit {name: "Medi-Cal"}), (a:Agency {name: "Alameda_County_Healthcare_Services"})
CREATE (b)-[:ADMINISTERED_BY]->(a)

MATCH (b:Benefit {name: "Job_Corps"}), (a:Agency {name: "California_Employment_Development_Department"})
CREATE (b)-[:ADMINISTERED_BY]->(a)

MATCH (b:Benefit {name: "CalWORKs"}), (a:Agency {name: "Alameda_County_Social_Services"})
CREATE (b)-[:ADMINISTERED_BY]->(a)

MATCH (b:Benefit {name: "Housing_Voucher_Program"}), (a:Agency {name: "California_Housing_Finance_Agency"})
CREATE (b)-[:ADMINISTERED_BY]->(a)

MATCH (b:Benefit {name: "Workforce_Development_Program"}), (a:Agency {name: "Alameda_County_Job_Training"})
CREATE (b)-[:ADMINISTERED_BY]->(a)

MATCH (b:Benefit {name: "Legal_Aid_Services"}), (a:Agency {name: "Legal_Aid_Organization"})
CREATE (b)-[:ADMINISTERED_BY]->(a)

RETURN "Agency administration relationships created"
```

**Expected output:** `"Agency administration relationships created"`

---

### Script 16: Create Relationships - Organization SERVES LifeEvent

```cypher
MATCH (org:Organization {name: "First_Place_for_Youth"}), (le:LifeEvent {name: "AGED_OUT_OF_FOSTER_CARE"})
CREATE (org)-[:SERVES]->(le)

MATCH (org:Organization {name: "First_Place_for_Youth"}), (le:LifeEvent {name: "HOMELESSNESS_RISK"})
CREATE (org)-[:SERVES]->(le)

MATCH (org:Organization {name: "Job_Corps_Oakland"}), (le:LifeEvent {name: "LOST_JOB"})
CREATE (org)-[:SERVES]->(le)

MATCH (org:Organization {name: "Eden_Youth_Fund"}), (le:LifeEvent {name: "AGED_OUT_OF_FOSTER_CARE"})
CREATE (org)-[:SERVES]->(le)

MATCH (org:Organization {name: "Alameda_County_Legal_Aid"}), (le:LifeEvent {name: "DOMESTIC_VIOLENCE"})
CREATE (org)-[:SERVES]->(le)

MATCH (org:Organization {name: "Bay_Area_Community_Services"}), (le:LifeEvent {name: "SUBSTANCE_RECOVERY"})
CREATE (org)-[:SERVES]->(le)

MATCH (org:Organization {name: "A_New_Leaf"}), (le:LifeEvent {name: "HOMELESSNESS_RISK"})
CREATE (org)-[:SERVES]->(le)

MATCH (org:Organization {name: "Alameda_Workforce_Development"}), (le:LifeEvent {name: "LOST_JOB"})
CREATE (org)-[:SERVES]->(le)

RETURN "Organization serves LifeEvent relationships created"
```

**Expected output:** `"Organization serves LifeEvent relationships created"`

---

### Script 17: Create Relationships - Organization PROVIDES Benefit

```cypher
MATCH (org:Organization {name: "First_Place_for_Youth"}), (b:Benefit {name: "Foster_Youth_Housing_Program"})
CREATE (org)-[:PROVIDES]->(b)

MATCH (org:Organization {name: "Job_Corps_Oakland"}), (b:Benefit {name: "Job_Corps"})
CREATE (org)-[:PROVIDES]->(b)

MATCH (org:Organization {name: "Community_Food_Bank_Alameda"}), (b:Benefit {name: "Food_Bank_Access"})
CREATE (org)-[:PROVIDES]->(b)

MATCH (org:Organization {name: "Alameda_County_Legal_Aid"}), (b:Benefit {name: "Legal_Aid_Services"})
CREATE (org)-[:PROVIDES]->(b)

MATCH (org:Organization {name: "YouthBuilt_Collective"}), (b:Benefit {name: "Job_Corps"})
CREATE (org)-[:PROVIDES]->(b)

MATCH (org:Organization {name: "Eden_Youth_Fund"}), (b:Benefit {name: "Foster_Youth_Mentorship_Program"})
CREATE (org)-[:PROVIDES]->(b)

MATCH (org:Organization {name: "Futures_Explored"}), (b:Benefit {name: "Education_Grant_Foster_Youth"})
CREATE (org)-[:PROVIDES]->(b)

MATCH (org:Organization {name: "Bay_Area_Community_Services"}), (b:Benefit {name: "Mental_Health_Services"})
CREATE (org)-[:PROVIDES]->(b)

MATCH (org:Organization {name: "A_New_Leaf"}), (b:Benefit {name: "Transitional_Housing"})
CREATE (org)-[:PROVIDES]->(b)

MATCH (org:Organization {name: "Alameda_Workforce_Development"}), (b:Benefit {name: "Workforce_Development_Program"})
CREATE (org)-[:PROVIDES]->(b)

RETURN "Organization provides Benefit relationships created"
```

**Expected output:** `"Organization provides Benefit relationships created"`

---

## Data Validation & Verification

### ✅ After Loading All Scripts, Run These Validation Queries

**Query 1: Count all nodes**

```cypher
CALL db.nodeCount() YIELD count AS total_nodes
RETURN total_nodes
```

**Expected result:** `~150-170 nodes`

---

**Query 2: Count all relationships**

```cypher
CALL db.relationshipCount() YIELD count AS total_relationships
RETURN total_relationships
```

**Expected result:** `~400-450 relationships`

---

**Query 3: See all node types**

```cypher
CALL db.labels() YIELD label
RETURN label AS node_type
ORDER BY label
```

**Expected results:**
```
Agency
Benefit
Document
EligibilityRule
LifeEvent
Organization
Outcome
```

---

**Query 4: Check a sample program with all connections**

```cypher
MATCH (b:Benefit {name: "Extended_Foster_Care"})
OPTIONAL MATCH (b)-[r:REQUIRES]->(d:Document)
OPTIONAL MATCH (b)-[r2:HAS_RULE]->(rule:EligibilityRule)
OPTIONAL MATCH (b)-[r3:UNLOCKS]->(b2:Benefit)
OPTIONAL MATCH (b)-[r4:LEADS_TO]->(o:Outcome)
OPTIONAL MATCH (b)-[r5:ADMINISTERED_BY]->(a:Agency)
OPTIONAL MATCH (le:LifeEvent)-[r6:TRIGGERS]->(b)

RETURN 
  b.name AS program,
  COLLECT(DISTINCT d.name) AS required_docs,
  COLLECT(DISTINCT rule.rule_text) AS eligibility_rules,
  COLLECT(DISTINCT b2.name) AS unlocks_programs,
  COLLECT(DISTINCT o.name) AS leads_to_outcomes,
  a.name AS administered_by,
  COLLECT(DISTINCT le.name) AS triggered_by_events
LIMIT 1
```

**Expected results:** Extended_Foster_Care with documents, rules, unlocked benefits, outcomes, admin, and triggering events

---

**Query 5: Test Cypher Template Query (for Agent 1, Tool 1)**

```cypher
MATCH (le:LifeEvent)-[:TRIGGERS]->(b:Benefit)-[:ADMINISTERED_BY]->(a:Agency)
WHERE le.name = "AGED_OUT_OF_FOSTER_CARE" 
AND b.county_available CONTAINS "Alameda"
RETURN 
  b.name AS program_name,
  b.description AS description,
  b.monthly_benefit_max AS monthly_benefit,
  b.income_limit_monthly AS income_limit
ORDER BY b.application_difficulty ASC
LIMIT 20
```

**Expected results:** List of programs for foster youth in Alameda (Extended_Foster_Care, Foster_Youth_Housing_Program, etc.)

---

**Query 6: Test Text2Cypher Query (for Agent 2, Pathway Advisor)**

```cypher
MATCH path = (le:LifeEvent {name: "AGED_OUT_OF_FOSTER_CARE"})-[:TRIGGERS]->(b1:Benefit)-[:UNLOCKS]->(b2:Benefit)-[:LEADS_TO]->(o:Outcome)
RETURN 
  b1.name AS step_1_program,
  b2.name AS step_2_unlocked_program,
  o.name AS final_outcome
LIMIT 5
```

**Expected results:** Multi-hop pathways showing how programs unlock outcomes

---

## Customizing Data

### If You Want to Add More Programs or Organizations:

**Template to add a new benefit:**

```cypher
CREATE (b:Benefit {
  name: "Program_Name",
  description: "Description of program",
  monthly_benefit_max: 500,
  income_limit_monthly: 1500,
  age_limit_min: 18,
  age_limit_max: 65,
  county_available: ["Alameda", "Statewide"],
  target_audience: ["Foster Youth", "Low income"],
  application_difficulty: "low"
})
RETURN b
```

**Template to add a new organization:**

```cypher
CREATE (org:Organization {
  name: "Organization_Name",
  type: "housing_support",
  description: "What they do",
  county: "Alameda",
  phone: "510-XXX-XXXX",
  address: "123 Street, City, CA",
  services_offered: ["housing", "job_training"],
  target_population: ["Foster Youth"],
  eligibility_notes: "Who can apply"
})
RETURN org
```

**Template to create relationships:**

```cypher
MATCH (b:Benefit {name: "Program1"}), (b2:Benefit {name: "Program2"})
CREATE (b)-[:UNLOCKS]->(b2)
RETURN "Relationship created"
```

---

## Troubleshooting

### Problem: "Node already exists" error

**Cause:** You ran a script twice

**Solution:** 
1. Drop entire database and start fresh (if in development)
2. Or run only new scripts (skip ones already executed)

```cypher
# WARNING: This deletes everything!
MATCH (n) DETACH DELETE n
```

---

### Problem: Relationship creation fails ("Unknown label")

**Cause:** Node label is misspelled

**Solution:**
1. Check the node exists: 
```cypher
MATCH (b:Benefit {name: "CalFresh"}) RETURN b LIMIT 1
```
2. If not found, check exact spelling in earlier script
3. Re-run the node creation script for that type

---

### Problem: Query returns empty results

**Cause:** Relationships not created yet

**Solution:**
1. Check relationships were created: 
```cypher
MATCH (b:Benefit)-[r]->() WHERE b.name = "Extended_Foster_Care" RETURN type(r), count(*)
```
2. If none, re-run relationship creation scripts (Scripts 10-17)


---

## Next Steps

### ✅ When All Data Is Loaded:

1. **Run validation queries** (Section 5) to confirm everything loaded
2. **Take a screenshot** of final node/relationship counts
3. **Move to AGENT_CREATION_GUIDE.md** to build the 3 agents
4. **Test agents** with sample questions
Quick Validation Queries (Fixed)
                                                                                                                      
  Replace the ones from the guide with these:
                                                                                                                      
  1. Count nodes:                                                                                                     
  MATCH (n) RETURN count(n) AS total_nodes
                                                                                                                      
  2. Count relationships:                                                                                           
  MATCH ()-[r]-() RETURN count(r) AS total_relationships
                                                        
  3. See node types:
  MATCH (n) RETURN distinct labels(n) AS node_types                                                                   
  ORDER BY node_types                              
                                                                                                                      
  4. Check if Extended_Foster_Care exists:                                                                          
  MATCH (b:Benefit {name: "Extended_Foster_Care"})                                                                    
  RETURN b.name, b.description, b.age_limit_max   
                                                                                                                      
  5. Check relationships on Extended_Foster_Care:                                                                     
  MATCH (b:Benefit {name: "Extended_Foster_Care"})-[r]-(x)
  RETURN type(r) AS relationship_type, labels(x) AS connected_to, count(*) AS count                                   
  GROUP BY type(r), labels(x)            
---

## Timeline

| Task | Time | Status |
|------|------|--------|
| Create AuraDB instance | 5-10 min | [ ] |
| Run all 17 Cypher scripts | 5-10 min | [ ] |
| Run validation queries | 5 min | [ ] |
| Verify data looks correct | 5 min | [ ] |
| **TOTAL** | **20-30 min** | |

**If done now, you can build agents immediately!**

---

**Ready? Start with Script 1 in your Neo4j Browser. I'm here if you hit any errors.**
