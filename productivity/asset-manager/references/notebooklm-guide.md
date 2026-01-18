# NotebookLM Setup and Usage Guide

> **Key Principle:** NotebookLM is for STATIC documents (manuals, leases, warranties). It excels at comprehension and querying. It is NOT for tracking state or anything that changes frequently.

---

## Table of Contents

1. [Notebook Structure](#notebook-structure)
2. [What to Upload](#what-to-upload)
3. [Query Patterns](#query-patterns)
4. [What NOT to Put in NotebookLM](#what-not-to-put-in-notebooklm)
5. [Integration with Notion](#integration-with-notion)

---

## Notebook Structure

### Overview

```
NotebookLM/
|
+-- Property Notebooks (one per dwelling)
|   +-- Dallas Property
|   +-- Austin Main (A)
|   +-- Austin ADU B
|   +-- Austin ADU C (when ready)
|
+-- Treehouse General
|   +-- LLC documents
|   +-- Insurance policies
|   +-- Multi-property docs
|
+-- Consulting Notebooks
    +-- Per-client notebooks
    +-- Methodologies notebook
```

### Property Notebooks (One Per Dwelling)

Create a separate notebook for each property to keep documents organized and queries focused.

| Notebook Name | Purpose | Contents |
|---------------|---------|----------|
| `Treehouse: Dallas` | Dallas property documents | Lease, manuals, warranties for Dallas |
| `Treehouse: Austin Main A` | Austin main house documents | Lease, manuals, warranties for main house |
| `Treehouse: Austin ADU B` | Austin ADU B documents | Lease, manuals, warranties for ADU B |
| `Treehouse: Austin ADU C` | Austin ADU C documents | Create when unit is ready |

**Why separate notebooks?**
- Queries return property-specific answers
- No confusion between similar appliances at different properties
- Cleaner organization as document volume grows

### Treehouse General Notebook

For documents that apply across all properties or to the LLC itself.

| Document Type | Examples |
|---------------|----------|
| LLC Formation | Articles of Organization, Operating Agreement |
| Insurance | Umbrella policy, liability coverage |
| Tax Documents | EIN letter, entity classification |
| Banking | Account agreements (reference only) |
| Contractor Agreements | Master service agreements |

### Consulting Notebooks

#### Per-Client Notebooks

Create a notebook for each client engagement:

```
Consulting: ABC Corp
Consulting: XYZ Inc
Consulting: Acme Co
```

**Contents:**
- Discovery call notes/transcripts
- Signed proposals and SOWs
- Meeting notes and recordings
- Client-provided research documents
- Final deliverables (for reference)

#### Methodologies Notebook

```
Consulting: Methodologies
```

**Contents:**
- Frameworks you use
- Case study templates
- Process documentation
- Industry research reports
- Reference materials

---

## What to Upload

### Per-Property Document Checklist

For each property notebook, upload these document types:

#### Lease and Legal

| Document | Priority | Notes |
|----------|----------|-------|
| Current lease agreement | Required | Full executed lease |
| Lease addendums | Required | Pet, parking, HOA rules |
| Move-in inspection report | Required | Baseline condition documentation |
| Property disclosure | Recommended | What was disclosed at purchase |
| HOA CC&Rs | If applicable | Covenants, conditions, restrictions |
| HOA rules and regulations | If applicable | Community guidelines |

#### HVAC System

| Document | Priority | Notes |
|----------|----------|-------|
| HVAC owner's manual | Required | Full manufacturer manual |
| HVAC installation record | Recommended | Install date, model, serial |
| HVAC warranty certificate | Required | Coverage terms and dates |
| Thermostat manual | Recommended | Programming instructions |

#### Major Appliances

Upload manuals and warranties for:

| Appliance | Manual | Warranty |
|-----------|--------|----------|
| Refrigerator | Yes | Yes |
| Dishwasher | Yes | Yes |
| Oven/Range | Yes | Yes |
| Microwave | Yes | Yes |
| Washer | Yes | Yes |
| Dryer | Yes | Yes |
| Garbage disposal | Yes | If available |
| Water heater | Yes | Yes |

#### Other Important Documents

| Document | Priority | Notes |
|----------|----------|-------|
| Home inspection report | Required | From purchase or annual |
| Roof warranty | If available | Especially if recent |
| Pest control warranty | If applicable | Termite bond, etc. |
| Pool equipment manuals | If applicable | Pump, filter, heater |
| Garage door opener manual | Recommended | Programming instructions |
| Security system manual | If applicable | Codes in Notion, not here |
| Smoke/CO detector specs | Recommended | Model numbers, placement |

### Document Naming Convention

Use this format for uploaded files:

```
{PROPERTY-CODE}_{DOCTYPE}_{ITEM}_{DATE}.pdf

Examples:
DAL_lease_current_2024-06.pdf
DAL_manual_hvac-carrier_2023-01.pdf
DAL_warranty_refrigerator-lg_2023-08.pdf
AUS-A_manual_dishwasher-bosch_2024-01.pdf
AUS-B_lease_current_2024-09.pdf
```

**Property Codes:**
- `DAL` = Dallas
- `AUS-A` = Austin Main
- `AUS-B` = Austin ADU B
- `AUS-C` = Austin ADU C

---

## Query Patterns

### Property Queries (Equipment and Maintenance)

**HVAC Questions:**
```
"What's the warranty period on the Dallas HVAC system?"
"What does the error code E4 mean on the Austin A air conditioner?"
"What's the recommended filter size for the Dallas HVAC?"
"How do I reset the thermostat at Austin ADU B?"
"What maintenance does the manufacturer recommend for the HVAC?"
```

**Appliance Questions:**
```
"What's the model number of the Dallas refrigerator?"
"How do I run the cleaning cycle on the Austin A dishwasher?"
"What water temperature setting does the manual recommend for the dryer?"
"Is the Dallas water heater still under warranty?"
"How do I troubleshoot the ice maker?"
```

**General Maintenance:**
```
"What does the inspection report say about the roof condition?"
"Were there any concerns noted in the Dallas home inspection?"
"What are the HOA rules about exterior modifications?"
```

### Lease Queries

**Tenant Terms:**
```
"What's the notice period required for Austin A?"
"What's the security deposit amount for Dallas?"
"What are the pet policy terms for Austin ADU B?"
"When does the current Dallas lease expire?"
"What are the late fee terms?"
```

**Responsibilities:**
```
"Who is responsible for lawn care at Dallas?"
"What maintenance responsibilities fall on the tenant?"
"What utilities does the tenant pay for?"
"Are tenants allowed to make modifications?"
```

**Move-out:**
```
"What are the move-out cleaning requirements?"
"What condition documentation do we have from move-in?"
"What's the security deposit return timeline?"
```

### Consulting Queries

**Client-Specific:**
```
"What were ABC Corp's main concerns from discovery?"
"What budget did XYZ Inc mention for the project?"
"What timeline did Acme Co request?"
"What stakeholders need to be involved at ABC Corp?"
"What did we propose for ABC Corp's Phase 2?"
```

**Methodology:**
```
"What's my standard discovery question framework?"
"How do I typically structure a strategy engagement?"
"What case studies are relevant for manufacturing clients?"
"What pricing model did I use for similar projects?"
```

### Query Tips

1. **Be specific about property** - Include "Dallas" or "Austin A" in property queries
2. **Reference document type** - "What does the lease say..." or "According to the manual..."
3. **Ask follow-up questions** - NotebookLM maintains context within a session
4. **Use for comprehension** - "Summarize the warranty coverage" or "Explain the HOA rules"

---

## What NOT to Put in NotebookLM

### Do NOT Upload (Use Notion Instead)

| Data Type | Why Not | Where It Belongs |
|-----------|---------|------------------|
| Maintenance logs | Changes frequently | Notion: Maintenance Log DB |
| Asset inventory | Dynamic state tracking | Notion: Asset Inventory DB |
| Service schedules | Constantly updating | Notion: Next Service Due field |
| Vendor contact info | Changes over time | Notion: Vendors DB or contacts |
| Rent payment records | Transactional data | Notion or accounting software |
| Security codes/passwords | Security risk | Password manager |
| Tenant personal info | Privacy/changes | Secure tenant management |
| Current asset photos | Updated periodically | Notion: Asset record |
| Cost tracking | Ongoing updates | Notion or spreadsheet |
| Depreciation calculations | Recalculated annually | Notion: Depreciation DB |

### The Static vs Dynamic Rule

**Ask yourself:** "Will this document change in the next 6-12 months?"

- **NO** (static) -> NotebookLM
  - Manuals don't change
  - Signed leases are fixed for their term
  - Warranties have set terms
  - Inspection reports are point-in-time

- **YES** (dynamic) -> Notion
  - Last service date changes
  - Asset status changes
  - Vendor preferences change
  - Costs accumulate

### Documents That Seem Static But Aren't

| Document | Why It's Actually Dynamic |
|----------|---------------------------|
| "Current" tenant contact info | Tenants change phones/emails |
| Vendor rate sheets | Prices update annually |
| Insurance declarations | Renews annually with changes |
| Property tax assessments | Changes yearly |

**Solution:** Upload the static policy document, but track current values in Notion.

---

## Integration with Notion

### The Document Index Concept

Create a Notion database to track what's in NotebookLM and where.

**Database: `Document Index`**

| Property | Type | Notes |
|----------|------|-------|
| Document Name | Title | "Dallas HVAC Manual" |
| Property | Select | Dallas, Austin A, Austin B, Austin C, General |
| Document Type | Select | Manual, Warranty, Lease, Inspection, HOA, Insurance |
| Related Asset | Relation | -> Asset Inventory (if applicable) |
| NotebookLM Notebook | Select | Which notebook it's in |
| Upload Date | Date | When added to NotebookLM |
| Source File | Files | Original PDF backup |
| Expiration | Date | When document expires (warranties, leases) |
| Notes | Text | Any context needed |

### Linking Assets to Documentation

In your Notion Asset Inventory database, use the `Documentation` URL field:

```
Asset: TH-HVAC-01 (Dallas AC Unit)
Documentation: [Link to NotebookLM Dallas notebook]
Notes: "Query: 'HVAC manual' or 'AC warranty'"
```

This creates a bridge:
1. Scan QR code on asset -> Opens Notion page
2. Notion page has Documentation link -> Reference to NotebookLM
3. User knows which notebook to query

### Workflow: New Asset with Documentation

```
1. RECEIVE DOCUMENTS
   - Gather manual, warranty, receipt

2. NOTION (Dynamic Tracking)
   - Create asset record in Asset Inventory
   - Fill in: cost, purchase date, warranty expiry, service interval
   - Generate and attach QR code
   - Set Documentation field note: "See NotebookLM: Dallas"

3. NOTEBOOKLM (Static Reference)
   - Upload manual to appropriate property notebook
   - Upload warranty to same notebook
   - Test query: "What's the warranty on [item]?"

4. DOCUMENT INDEX
   - Add entries for manual and warranty
   - Link to asset record
   - Note expiration dates

5. RECEIPT/INVOICE
   - Upload to NotebookLM for tax reference
   - Also keep in accounting system
```

### Workflow: Answering a Question

**Scenario:** "What does the manual say about the E4 error on the Dallas AC?"

```
1. IDENTIFY PROPERTY
   - Dallas -> Query "Treehouse: Dallas" notebook

2. QUERY NOTEBOOKLM
   - "What does the HVAC manual say about error code E4?"
   - Get explanation and troubleshooting steps

3. CHECK NOTION (if needed)
   - Asset: TH-HVAC-01
   - Last service date, warranty status
   - Service history - has this happened before?

4. TAKE ACTION
   - If DIY fix: Follow manual instructions
   - If needs service: Check Notion for vendor, log the issue
```

### Workflow: Lease Question

**Scenario:** Tenant asks about notice period for Austin A

```
1. QUERY NOTEBOOKLM
   - Notebook: "Treehouse: Austin Main A"
   - Query: "What's the required notice period for lease termination?"
   - Get specific terms from the signed lease

2. RESPOND TO TENANT
   - Cite the specific lease section
   - Provide accurate information

3. NO NOTION NEEDED
   - Lease terms are static
   - No state to track for this query
```

### Quick Reference: Where to Look

| Question Type | First Look | Second Look |
|---------------|------------|-------------|
| "How do I fix/operate...?" | NotebookLM (manual) | - |
| "What's the warranty on...?" | NotebookLM (warranty) | Notion (expiry date) |
| "What does the lease say about...?" | NotebookLM (lease) | - |
| "When was X last serviced?" | Notion (maintenance log) | - |
| "What's the model number?" | Notion (asset record) | NotebookLM (manual) |
| "Is X still under warranty?" | Notion (expiry date) | NotebookLM (terms) |
| "Who installed X?" | Notion (asset record) | NotebookLM (receipt) |
| "How much did X cost?" | Notion (asset record) | NotebookLM (receipt) |

---

## Setup Checklist

### Initial Setup

- [ ] Create notebook: `Treehouse: Dallas`
- [ ] Create notebook: `Treehouse: Austin Main A`
- [ ] Create notebook: `Treehouse: Austin ADU B`
- [ ] Create notebook: `Treehouse General`
- [ ] Create notebook: `Consulting: Methodologies`

### Per-Property Upload Checklist

**Dallas:**
- [ ] Current lease agreement
- [ ] HVAC manual and warranty
- [ ] Major appliance manuals (refrigerator, dishwasher, etc.)
- [ ] Water heater manual and warranty
- [ ] Home inspection report
- [ ] HOA documents (if applicable)

**Austin Main A:**
- [ ] Current lease agreement
- [ ] HVAC manual and warranty
- [ ] Major appliance manuals
- [ ] Water heater manual and warranty
- [ ] Home inspection report

**Austin ADU B:**
- [ ] Current lease agreement
- [ ] HVAC/mini-split manual and warranty
- [ ] Appliance manuals
- [ ] Inspection documentation

**Austin ADU C:**
- [ ] (Create when unit is ready)

### Notion Integration

- [ ] Create Document Index database
- [ ] Add Documentation field to Asset Inventory
- [ ] Document the notebook-to-property mapping

---

## Appendix: Sample Documents by Notebook

### Treehouse: Dallas

```
Documents:
- DAL_lease_current_2024-06.pdf
- DAL_manual_hvac-trane_2022-03.pdf
- DAL_warranty_hvac-trane_2022-03.pdf
- DAL_manual_refrigerator-samsung_2022-03.pdf
- DAL_warranty_refrigerator-samsung_2022-03.pdf
- DAL_manual_dishwasher-whirlpool_2022-03.pdf
- DAL_manual_waterheater-rheem_2022-03.pdf
- DAL_warranty_waterheater-rheem_2022-03.pdf
- DAL_inspection_purchase_2022-02.pdf
- DAL_hoa_ccrs_2020.pdf
- DAL_hoa_rules_2023.pdf
```

### Treehouse General

```
Documents:
- TH_llc_articles-of-organization_2022-01.pdf
- TH_llc_operating-agreement_2022-01.pdf
- TH_insurance_umbrella-policy_2024.pdf
- TH_insurance_liability_2024.pdf
- TH_tax_ein-letter.pdf
```

### Consulting: Methodologies

```
Documents:
- discovery-question-framework.pdf
- strategy-engagement-template.pdf
- pricing-models-reference.pdf
- case-study-manufacturing-client.pdf
- industry-research-2024.pdf
```

---

*Last Updated: 2024*
*Related: Asset Manager SKILL.md, naming-conventions.md*
