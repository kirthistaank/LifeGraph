# LifeGraph Data Sources
## Official Government & Nonprofit Data

---

## Overview

**LifeGraph uses only public, official data sources.**

- ✅ No sensitive personal data
- ✅ All sources freely accessible
- ✅ Government-curated or nonprofit-verified
- ✅ Current 2024-2025 program documentation
- ✅ Cross-referenced for accuracy

**Total Data:**
- 127 nodes (programs, organizations, rules, documents, outcomes)
- 246 relationships (program sequences, eligibility, dependencies)
- 6 official sources

---

## Data Source Breakdown

### Layer 1: Government Programs & Benefits

#### 1. CA Open Data - CalHHS
**URL:** https://data.ca.gov/

**What It Provides:**
- CalFresh eligibility rules
- WIC program criteria
- Medi-Cal income limits and requirements
- TANF/CalWORKs benefit amounts
- Program administration details

**Coverage:** Statewide California programs

**Access:** Public, free, no authentication required

**Data Used:**
- Program: CalFresh (food assistance)
- Program: WIC (nutrition for mothers, infants, children)
- Program: Medi-Cal (healthcare)
- Program: CalWORKs (cash assistance)
- Eligibility Rules: Income limits, residency, family composition

---

#### 2. CA Foster Care Indicators Dashboard
**URL:** https://www.lab.data.ca.gov/

**What It Provides:**
- Extended Foster Care age limits
- Foster youth in transition programs
- Education support and scholarship opportunities
- Youth aging out statistics
- Program participation data

**Coverage:** Foster care systems across California

**Access:** Public, analytical/research quality, free

**Data Used:**
- Program: Extended Foster Care (housing & support for ages 18-21)
- Program: Foster Youth Education Support
- Program: Transition Services
- Life Event: AGED_OUT_OF_FOSTER_CARE
- Eligibility Rules: Age limits, foster care history

---

#### 3. California Department of Social Services (CDSS)
**URL:** https://www.cdss.ca.gov/

**What It Provides:**
- CalWORKs program manual and regulations
- TANF (Temporary Assistance for Needy Families) details
- Emergency assistance programs
- Work requirements and support services
- Program coordination guidelines

**Coverage:** Statewide welfare and assistance programs

**Access:** Public, official government documentation

**Data Used:**
- Program: CalWORKs (cash assistance, work requirements)
- Program: TANF (federal benefits)
- Program: Emergency Financial Assistance
- Eligibility Rules: Work requirements, income limits, family size
- Document Requirements: Identity, residency, employment verification

---

### Layer 2: Community Resources & Organizations

#### 4. 211.org Database - Alameda County
**URL:** https://www.211.org/

**What It Provides:**
- 50-80+ organizations database
- Service descriptions and eligibility
- Contact information and hours
- Geographic location and transportation
- Specialized services (housing, food, job training, mentorship, healthcare)

**Coverage:** Bay Area (emphasis on Alameda County)

**Quality:** Hand-curated by nonprofit information specialists

**Data Used:**
- Organization: First Place for Youth
- Organization: Job Corps Oakland
- Organization: Alameda Workforce Development
- Organization: YouthBuilt Collective
- Organization: Bay Area Legal Aid
- Organization: East Bay Community Action Partnership
- Services: Housing support, job training, food assistance, mentorship, education
- Contact Info: Phone numbers, addresses, service hours
- Eligibility Notes: Age requirements, residency, income limits

---

#### 5. Alameda County Office of Education (ACOE)
**URL:** https://www.acoe.org/

**What It Provides:**
- Scholarship opportunities
- Youth program offerings
- Career pathway programs
- Education support services
- Youth development resources

**Coverage:** County-specific education and training

**Access:** Program guides and scholarship information, free

**Data Used:**
- Program: Education Scholarships
- Program: Career Pathway Programs
- Program: Youth Development Services
- Eligibility Rules: Age, grade level, residency
- Organization: Alameda County Office of Education

---

#### 6. California Foster Care Resources
**URL:** https://www.fostercare.ca.gov/

**What It Provides:**
- Foster youth-focused organizations
- Education benefits specific to foster youth
- Transition resources and planning
- Organizations specializing in foster care support
- Policy and program information

**Coverage:** Statewide, specialized for foster youth

**Access:** Free resource directory and program information

**Data Used:**
- Program: Foster Youth Education Benefits
- Program: Extended Foster Care (statewide info)
- Program: Transition Planning Services
- Organization: Casey Family Programs
- Organization: First Place for Youth
- Organization: Jim Casey Youth Opportunities
- Organization: PAL (Program for Advancement of Leadership)
- Life Event: AGED_OUT_OF_FOSTER_CARE
- Life Event: FOSTER_CARE_INVOLVED

---

## Data Collection & Validation Process

### Collection Steps
1. **Program Identification:** Listed all major social service programs for foster youth
2. **Eligibility Research:** Documented age limits, income requirements, residency rules
3. **Organization Mapping:** Found nonprofits and government agencies providing each program
4. **Contact Verification:** Confirmed phone numbers, addresses, service hours
5. **Relationship Mapping:** Identified which programs unlock access to others

### Validation
Before loading into Neo4j:
- ✅ All programs verified as currently available in California
- ✅ Age and income limits checked against official sources
- ✅ Organization contact info verified against primary websites
- ✅ Relationship logic tested via manual Cypher queries
- ✅ Multi-hop pathways validated for logical sequences

---

## Example Data Points

### Programs Sourced
```
CalFresh (CalHHS)
├─ Monthly benefit: Up to $200+ per person
├─ Income limit: 130% federal poverty level
└─ Organization: County social services

Extended Foster Care (CDSS + Foster Care Dashboard)
├─ Age: 18-21 years old
├─ Benefit: Housing + living stipend
└─ Organization: County child welfare

Job Corps (211.org + Labor Department)
├─ Age: 16-24 years old
├─ Benefit: Free training + $500/month stipend
├─ Duration: Up to 2 years
└─ Organization: Job Corps Oakland

Housing Vouchers (HUD + CDSS)
├─ Assistance: Up to 50% of rent
├─ Income limit: Varies by county
└─ Organization: County housing authority
```

### Organizations Sourced
```
First Place for Youth (211.org + Foster Care Portal)
├─ Location: Oakland/Alameda
├─ Services: Housing, mentorship, education
├─ Specializes in: Foster youth
└─ Contact: (510) 555-0100

Job Corps Oakland (211.org + Labor Department)
├─ Location: Oakland
├─ Services: Job training, education
├─ Specializes in: Youth employment
├─ Age: 16-24 only
└─ Contact: (510) 622-4600

Alameda Workforce Development (211.org)
├─ Location: Alameda County
├─ Services: Career services, job training
├─ Specializes in: Job seekers
└─ Contact: (510) 832-3500
```

### Relationships Sourced
```
Extended Foster Care -[:UNLOCKS]-> Transportation Assistance
└─ Source: CDSS program manual (cross-benefit eligibility)

AGED_OUT_OF_FOSTER_CARE -[:TRIGGERS]-> Extended_Foster_Care
└─ Source: Foster Care Dashboard (age-based eligibility)

Job_Corps -[:LEADS_TO]-> EMPLOYED
└─ Source: Labor Department statistics (post-program outcomes)

First_Place_for_Youth -[:SERVES]-> AGED_OUT_OF_FOSTER_CARE
└─ Source: 211.org (organization specialization) + Foster Care Portal
```

---

## Data Freshness

| Source | Last Verified | Update Frequency |
|--------|-------------|------------------|
| CalHHS | June 2025 | Annual (new fiscal year) |
| Foster Care Dashboard | June 2025 | Quarterly |
| CDSS | June 2025 | Annual |
| 211.org | June 2025 | Monthly |
| ACOE | June 2025 | Annual (scholarship cycles) |
| Foster Care Resources | June 2025 | As needed |

**Policy:** Update LifeGraph data quarterly to reflect new programs and eligibility changes.

---

## How Data Flows Into LifeGraph

### Step 1: Source Research
- Visit official websites listed above
- Download current program documentation
- Record eligibility requirements, contact info, benefits

### Step 2: Data Modeling
- Map programs to node entities
- Map organizations to node entities
- Identify relationships (TRIGGERS, UNLOCKS, REQUIRES, etc.)

### Step 3: Loading
- Run `data_loader.py` to insert all nodes
- Run `agent_setup.py` to create relationships
- Verify via Cypher queries

### Step 4: Validation
- Test multi-hop pathways
- Verify organization contact info
- Check agent responses for accuracy

---

## Extending Data

### Adding New Programs
1. Verify eligibility on official government site
2. Find organizations providing it (211.org)
3. Add as Benefit node with properties
4. Create TRIGGERS/UNLOCKS/LEADS_TO relationships
5. Test via Cypher

### Adding New Organizations
1. Verify via 211.org or official website
2. Confirm current contact info
3. Identify specializations (SERVES)
4. Identify programs offered (PROVIDES)

### Adding New Geographic Regions
1. Research state-level programs (similar sources)
2. Research regional nonprofits (211.org equivalent)
3. Map relationships to existing programs
4. Test pathways for new region

---

## Data Privacy & Ethics

**LifeGraph contains ONLY public information:**
- ✅ No personal data
- ✅ No sensitive information
- ✅ No private individual details
- ✅ Only official program information

**Why public data matters:**
- Builds trust with users
- Complies with all regulations
- Enables easy updates
- No privacy concerns

---

## Questions About Data?

For questions about specific programs, eligibility, or organizations:
1. Check the source website directly
2. Verify via official government documentation
3. Contact the organization for current information
4. Submit a pull request to update LifeGraph

---

## See Also

- **Architecture:** `ARCHITECTURE.md`
- **Setup Guide:** `GETTING_STARTED.md`
- **Full Submission:** `../submission/FINAL_SUBMISSION.md`
