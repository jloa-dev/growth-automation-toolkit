# Project: Expensify/App Adversarial Audit & Technical Intervention Pipeline

## Architecture
- **Target Repository**: `c:\Users\Loa\Downloads\GOAL\expensify_app` (Upstream: `Expensify/App`, Origin: `jloa-dev/App`).
- **Data Flow & Information Sources**:
  1. `TASK_LEDGER.md`: Initial 101-task inventory ($17,475 USD).
  2. GitHub Live API (`gh issue view`): Live status, assignees, rival count, MelvinBot activity.
  3. Upwork Escrow Protocol: Contract verification and private invite ingestion.
  4. Local Source Tree (`expensify_app/src`): Code verification against Onyx, Navigation, ReportActions, FlashList/SelectionList, SearchParser, and Policy/Cards.
- **Output Artifact**: `scratch/audit_adversarial_interventions.md`.

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | M1 Live Scan & Filtering | Live probe of all 101 tasks; isolate 37 high-priority (0-2 rivals, no bot PR) | M1 | Survey Explorers 1 & 2 |
| 2 | M2 Adversarial Inspection Batch 1 | Deep code audit of 20 Oct Sentry/HybridApp tickets (#104501, #104502, #104503, #104505, #104509, #104515, #104519) | M2 | Survey Explorers & GitHub data |
| 3 | M2 Adversarial Inspection Batch 2 | Deep code audit of Tier 1 Uncontested & Active C+ issues (#103307, #103156, #103326, #103838, #103965, #104127, #103244, #104287, #104176, #103721, #103349, #103245, #103214) | M2 | Survey Explorers & GitHub data |
| 4 | M2 Adversarial Inspection Batch 3 | Deep code audit of Key 2-Rival issues (#104221, #104165, #104162, #104161, #104159, #104138, #103961, #103876, #103824, #103802, #103779, #103778, #103533, #103240, #103183, #102730, #102683) | M2 | Survey Explorers & GitHub data |
| 5 | M3 Intervention Dossiers Drafting | Formulation of precise technical intervention comments (file paths, failing test steps, corrective patch) for user approval | M3 | R2/R3 Requirements |
| 6 | M4 Master Dossier Compilation | Construction of scratch/audit_adversarial_interventions.md (Prioritization Table, Fichas, Action Plan) | M4 | R4 Requirements |
| 7 | M4 Gate & Integrity Audit | Review by Reviewers/Challengers and Forensic Audit verifying zero-leak, zero-fake claims | M4 | Acceptance Criteria |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | M1: Live Scan & Classification | Full scan of 101 ledger tasks, isolation of 37 high-priority targets ($6,350 USD) | none | DONE |
| 2 | M2: Adversarial Proposal & Code Analysis | In-depth technical analysis of rival proposals against expensify_app code across priority batches | M1 | DONE |
| 3 | M3: Non-Intrusive Intervention Drafting | Concrete comment drafts with file locations, repro steps, and patches for user pre-approval | M2 | DONE |
| 4 | M4: Master Dossier & Verification Gate | Compile scratch/audit_adversarial_interventions.md, review and forensic audit | M3 | DONE |

## Interface Contracts
### Survey Explorer → Adversarial Analyst
- Input: JSON datasets in `scratch/` (`enriched_high_priority.json`, `refined_pipeline_results.json`, `all_expensify_tasks.json`).
- Output: Analysis report containing: Issue #, rival proposal text/link, identified defect, code reference, and test reproduction.

### Adversarial Analyst → Intervention Writer
- Input: Defect evidence chain per issue.
- Output: Formatted intervention comment adhering to Expensify guidelines:
  1. Proposal Summary & Superiority statement.
  2. Point-by-point flaw breakdown of competitor with reproduction test steps.
  3. Exact source code location (`src/...`).
  4. Non-intrusive suggested patch diff.

### Intervention Writer → Master Report Compiler
- Input: Complete intervention entries.
- Output: `scratch/audit_adversarial_interventions.md`.

## Code Layout
- Agent coordination metadata: `c:\Users\Loa\Downloads\GOAL\.agents\teamwork\`
- Final user report: `c:\Users\Loa\Downloads\GOAL\scratch\audit_adversarial_interventions.md`
- Intermediate audit datasets: `c:\Users\Loa\Downloads\GOAL\scratch\`
- Local code reference: `c:\Users\Loa\Downloads\GOAL\expensify_app\src\`
