# Agent Evaluation Framework — Design Spec

## 1. Purpose

A 5-level evaluation framework that tests the analytical agent end-to-end against a deterministic banking dataset. Each level targets a different capability tier — from basic rendering to stress-test endurance. Grading uses a multi-dimensional rubric (process + output) with A/B/C scores per dimension, combining deterministic checks and LLM-judged qualitative criteria.

## 2. Test Dataset — "First National Bank"

5 tables in DuckDB (`data/duckdb/eval.db`), seeded deterministically via `backend/scripts/seed_eval_data.py` with `SEED=42`. Separate from the main analytical database. Idempotent — running the seed script twice produces identical data.

### 2.1 `customers` (~200 rows)

| Column | Type | Notes |
|--------|------|-------|
| customer_id | INT PK | 1-200 |
| name | VARCHAR | Faker-generated, deterministic seed |
| segment | VARCHAR | retail / business / premium |
| region | VARCHAR | northeast / southeast / midwest / west |
| join_date | DATE | 2020-01-01 to 2025-12-31 |
| credit_score | INT | 580-850, correlated with segment (premium higher) |
| is_active | BOOLEAN | ~90% true |

### 2.2 `accounts` (~400 rows)

| Column | Type | Notes |
|--------|------|-------|
| account_id | INT PK | 1-400 |
| customer_id | INT FK | → customers |
| account_type | VARCHAR | checking / savings / money_market |
| opened_date | DATE | >= customer join_date |
| balance | DECIMAL(12,2) | segment-correlated (premium higher) |
| status | VARCHAR | active / dormant / closed |

### 2.3 `transactions` (~5,000 rows)

| Column | Type | Notes |
|--------|------|-------|
| txn_id | INT PK | 1-5000 |
| account_id | INT FK | → accounts |
| txn_date | DATE | 2025-01-01 to 2025-12-31 |
| amount | DECIMAL(12,2) | signed (+deposit, -withdrawal) |
| category | VARCHAR | payroll / utilities / transfer / merchant / atm / wire |
| counterparty | VARCHAR | employer name / merchant / bank |
| description | VARCHAR | free text |
| is_flagged | BOOLEAN | internal risk flag (Level 3 ground truth marker) |

#### Planted anomalies (Level 3 ground truth)

| ID | Type | True anomaly? | Story |
|----|------|---------------|-------|
| A1 | Amount spike | YES | $47,000 wire from dormant account — stolen credentials |
| A2 | Frequency burst | YES | 12 ATM withdrawals in 2 hours across 3 cities — card cloning |
| A3 | New counterparty | YES | Series of transfers to a shell company never seen before |
| A4 | Seasonal spike | NO (false positive) | $15,000 deposit in July — annual bonus (also deposited same week in prior years) |
| A5 | Large round transfer | NO (false positive) | $50,000 savings→checking — customer closing savings to buy a house |
| A6 | Weekend burst | NO (false positive) | 8 small merchant charges on Saturday — normal shopping trip |

All anomalies occur during Q3 2025 (July-September) so Level 3's prompt targeting Q3 captures all of them.

### 2.4 `loans` (~80 rows)

| Column | Type | Notes |
|--------|------|-------|
| loan_id | INT PK | 1-80 |
| customer_id | INT FK | → customers |
| loan_type | VARCHAR | personal / auto / mortgage / business |
| principal | DECIMAL(12,2) | $5K-$500K |
| interest_rate | DECIMAL(4,2) | 3.5%-18%, inversely correlated with credit_score |
| term_months | INT | 12-360 |
| origination_date | DATE | 2021-2025 |
| status | VARCHAR | current / delinquent / default / paid_off |
| monthly_payment | DECIMAL(10,2) | calculated from principal/rate/term |

### 2.5 `daily_rates` (~365 rows)

| Column | Type | Notes |
|--------|------|-------|
| rate_date | DATE PK | 2025-01-01 to 2025-12-31 |
| fed_funds_rate | DECIMAL(4,2) | realistic path with 2 rate cuts |
| prime_rate | DECIMAL(4,2) | fed_funds + 3.0 |
| mortgage_30y | DECIMAL(4,2) | loosely tracks prime |
| savings_apy | DECIMAL(4,2) | 3.5-4.5% range |

### 2.6 Planted relationships (for Level 4 discovery)

- Credit score strongly predicts loan default rate (primary driver)
- Region effect on delinquency: southeast > midwest > northeast > west
- Premium customers: lower default rate but higher average loan amounts (exposure paradox)
- Seasonal transaction patterns: holiday spending spike (Nov-Dec), annual bonus deposits (July)
- Fed rate cuts correlate with savings balance growth
- Dormant accounts correlate with older join dates

## 3. Evaluation Levels

### Level 1: Basic Rendering

**Prompt:** "Show me the monthly transaction volume and total amount for 2025 as a bar chart. Also show the top 10 customers by total deposits as a table. Finally, draw the relationship between the 5 tables as a mermaid ERD."

**Tests:** Chart generation, table formatting, mermaid diagram rendering — basic skill usage.

**Grading dimensions:**

| Dimension | Weight | Type | C (minimally ok) | B (pretty useful) | A (excellent) |
|-----------|--------|------|-------------------|-------------------|---------------|
| chart_correctness | 0.3 | llm_judge | Bar chart renders with 12 months, values roughly correct | Axes labeled, amounts accurate, months in order | Formatted amounts, clear title, color-coded volume vs amount |
| table_correctness | 0.3 | hybrid | Table with 10 rows, customer names and amounts present | Correct ranking order, properly formatted currency | Includes account types, percentage of total, clean alignment |
| mermaid_erd | 0.2 | deterministic | Renders without syntax error, shows 5 tables | Correct FK relationships, correct cardinality notation | Column names in entities, PK/FK marked, clean layout |
| process_quality | 0.2 | llm_judge | Ran queries and produced output | Reasonable query design (not SELECT *) | Efficient queries, no redundant calls |

### Level 2: Multi-Step Exploration

**Prompt:** "Which customer segment has the highest loan default rate, and is that driven by credit score, loan type, or region? Walk me through your analysis."

**Tests:** Multi-step analytical chaining (4-5 steps), error recovery, supported conclusions.

**Expected reasoning chain:**
1. Calculate default rate by segment
2. Break down by credit score distribution per segment
3. Break down by loan type distribution per segment
4. Break down by region per segment
5. Identify credit score as primary driver (planted ground truth)

**Grading dimensions:**

| Dimension | Weight | Type | C | B | A |
|-----------|--------|------|---|---|---|
| logical_chain | 0.25 | llm_judge | At least 3 steps, reaches a conclusion | 4-5 steps in sensible order, considers multiple factors | Systematic elimination, explicitly rules out confounders |
| correctness | 0.30 | hybrid | Identifies the right segment | Correctly identifies credit score as primary driver | Quantifies effect size, notes interaction with loan type |
| error_recovery | 0.20 | llm_judge | Completes despite any query errors | Notices and corrects analytical missteps | Proactively validates intermediate results |
| communication | 0.25 | llm_judge | States a conclusion | Explains reasoning at each step | Clear narrative arc, caveats noted, actionable summary |

### Level 3: Anomaly Detection + False Positive Screening

**Prompt:** "Run anomaly detection on all transactions from Q3 2025. Flag statistical outliers, then manually review the raw data for each flag to identify false positives. Give me a final list of confirmed anomalies with your reasoning for each inclusion/exclusion."

**Tests:** Statistical tool usage → raw data inspection → judgment-based filtering. Two-pass methodology.

**Ground truth:** A1, A2, A3 are true anomalies. A4, A5, A6 are false positives.

**Grading dimensions:**

| Dimension | Weight | Type | C | B | A |
|-----------|--------|------|---|---|---|
| detection_recall | 0.30 | deterministic | Flags at least 2/3 true anomalies | Flags all 3 true anomalies | Flags all 3 with correct anomaly type classification |
| false_positive_handling | 0.30 | hybrid | Acknowledges some flags might be benign | Correctly dismisses at least 2/3 FPs with reasoning | Dismisses all 3 FPs with specific evidence (annual bonus pattern, house purchase, shopping trip) |
| methodology | 0.20 | llm_judge | Uses at least one statistical method | Statistical detection then inspects raw records | Two-pass explicit, documents thresholds, explains method |
| final_report | 0.20 | llm_judge | Lists anomalies | Structured report with flag/dismiss decisions | Per-item reasoning, confidence levels, recommended actions |

### Level 4: Free Exploration for Insights

**Prompt:** "Explore this banking dataset freely. Profile the data, find the most interesting correlations and causal relationships, and identify the strongest predictors of loan default. Surprise me with what you find."

**Tests:** Unsupervised exploration — data profiling, correlation discovery, hypothesis generation.

**Planted discoveries** (agent should find at least some):
- Credit score → default rate (strongest predictor)
- Region effect on delinquency (southeast > others)
- Premium customers: lower default but higher exposure
- Seasonal transaction patterns
- Rate environment ↔ savings balance correlation
- Dormant accounts correlate with older customers

**Grading dimensions:**

| Dimension | Weight | Type | C | B | A |
|-----------|--------|------|---|---|---|
| breadth | 0.20 | llm_judge | Profiles at least 2 tables, finds 1 insight | Profiles 3+ tables, finds 3+ insights | Systematic profiling of all 5 tables, cross-table analysis |
| depth | 0.25 | llm_judge | Surface-level stats (means, counts) | Correlation analysis with quantified relationships | Distinguishes correlation from causation, controls for confounders |
| discovery_quality | 0.30 | hybrid | Finds the obvious (credit score → default) | Finds 2-3 planted relationships | Finds planted + at least 1 non-obvious insight |
| presentation | 0.25 | llm_judge | Lists findings | Structured by importance with evidence | Narrative with visualizations, ranked by actionability |

### Level 5: Stress Test — State Tracking Under Compounding Mutations

**Prompt sequence (8 sequential instructions):**

1. "Summarize the loans table — count, average principal, default rate by loan_type"
2. "Edit the result: remove the 'auto' row and add a column for average credit score per loan type"
3. "Now summarize transactions — monthly total by category for Q4 2025 only"
4. "Edit: combine the 'atm' and 'merchant' categories into 'cash_and_retail'"
5. "Combine these two summary tables into one view — loan metrics alongside transaction metrics, joined by month where applicable"
6. "Calculate a new column: ratio of monthly transaction volume to outstanding loan principal per customer segment"
7. "Modify the combined table: filter to only segments where that ratio exceeds 0.5"
8. "Compare this final filtered table to the original loans summary from step 1 — what changed and what does it mean?"

**Tests:** State tracking across 8 mutations, correct table versioning, loop avoidance, efficiency.

**Token budget:** Initial estimate: ~4,000 tokens of agent output optimal. Budget ceiling is 2x (8,000 tokens). These values should be calibrated after the first real agent runs and adjusted in the rubric YAML.

**Grading dimensions:**

| Dimension | Weight | Type | C | B | A |
|-----------|--------|------|---|---|---|
| step_completion | 0.25 | deterministic | Completes at least 6/8 steps | Completes all 8 steps | All 8 with correct output at each stage |
| state_correctness | 0.30 | hybrid | Mostly references correct table versions | All references correct, no stale data | Explicitly labels versions (e.g., "loans_summary_v1") |
| efficiency | 0.20 | deterministic | Finishes within 2x optimal token budget | Within 1.5x optimal | Within 1.2x optimal, no redundant queries |
| final_comparison | 0.25 | llm_judge | Produces some comparison | Correctly identifies changes between step 1 and 8 | Explains why changes matter analytically |

## 4. Eval Runner Architecture

### 4.1 File layout

```
backend/
├── scripts/
│   └── seed_eval_data.py              # Deterministic dataset → DuckDB
├── tests/
│   └── evals/
│       ├── conftest.py                # Fixtures: db, agent stub, LLM judge
│       ├── rubrics/
│       │   ├── level1_rendering.yaml
│       │   ├── level2_exploration.yaml
│       │   ├── level3_anomaly.yaml
│       │   ├── level4_free_explore.yaml
│       │   └── level5_stress.yaml
│       ├── test_level1.py
│       ├── test_level2.py
│       ├── test_level3.py
│       ├── test_level4.py
│       └── test_level5.py
└── app/
    └── evals/
        └── judge.py                   # LLM judge wrapper
```

### 4.2 Agent interface protocol

```python
class AgentInterface(Protocol):
    async def run(self, prompt: str, db_path: str) -> AgentTrace: ...

@dataclass
class AgentTrace:
    queries: list[str]           # SQL queries executed
    intermediate: list[Any]      # Intermediate results/artifacts
    final_output: str            # Final response text
    token_count: int             # Total tokens used
    duration_ms: int             # Wall clock time
    errors: list[str]            # Errors encountered and recovered from
```

Initially backed by a mock that returns canned responses. When the real LangGraph agent ships, the mock is swapped — no eval code changes needed.

### 4.3 LLM judge

`judge.py` wraps calls to local Ollama model. For each qualitative dimension:
- Input: agent trace + rubric criteria (A/B/C descriptions)
- Output: grade (A/B/C) + one-sentence justification
- Temperature: 0 for reproducibility
- Model: uses `default_model` from config (qwen3.5:9b)

### 4.4 Grade rollup

Each dimension gets a numeric score: A=1.0, B=0.7, C=0.4, F=0.0. Weighted by dimension weights. Overall level grade:
- A: weighted_score >= 0.85
- B: weighted_score >= 0.60
- C: weighted_score >= 0.40
- F: weighted_score < 0.40

Overall eval grade: average of 5 level scores using same thresholds.

### 4.5 Rubric YAML format

```yaml
level: 1
name: "Basic Rendering"
prompt: "Show me the monthly transaction volume..."
dimensions:
  chart_correctness:
    weight: 0.3
    type: llm_judge
    criteria:
      A: "Formatted amounts, clear title, color-coded"
      B: "Axes labeled, amounts accurate, months in order"
      C: "Bar chart renders with 12 months, values roughly correct"
  table_correctness:
    weight: 0.3
    type: hybrid
    deterministic:
      - "output contains exactly 10 rows"
      - "rows sorted descending by deposit amount"
    criteria:
      A: "Includes account types, percentage of total"
      B: "Correct ranking, formatted currency"
      C: "10 rows with names and amounts"
grading:
  A: 0.85
  B: 0.60
  C: 0.40
```

### 4.6 Make targets

```bash
make seed-eval              # Generate/refresh eval dataset
make eval                   # Run all 5 levels
make eval level=3           # Run specific level
```

### 4.7 Output format

```
Level 1 — Basic Rendering:      B  (chart:B  table:A  erd:A  process:C)
Level 2 — Multi-Step Explore:   A  (chain:A  correct:A  recovery:B  comms:A)
Level 3 — Anomaly Detection:    B  (recall:A  fp:B  method:B  report:C)
Level 4 — Free Exploration:     B  (breadth:B  depth:B  discovery:A  present:C)
Level 5 — Stress Test:          C  (steps:B  state:C  efficiency:C  compare:B)
Overall:                        B
```

## 5. Seed Script Requirements

`backend/scripts/seed_eval_data.py`:
- Uses `random.seed(42)` and `faker.Faker(seed=42)` for determinism
- Creates `data/duckdb/eval.db` (creates `data/duckdb/` directory if needed)
- Drops and recreates all 5 tables on each run (idempotent)
- Plants the 6 anomaly records with specific `is_flagged=True` markers
- Plants the correlation structures (credit_score↔default, region effects, etc.)
- Prints summary stats after seeding: row counts per table, anomaly count

## 6. Dependencies

Add to `backend/pyproject.toml`:
- `faker>=33.0.0` (deterministic test data generation)

Already present:
- `duckdb>=1.2.0`
- `pytest>=8.3.0`
- `httpx>=0.28.0` (for Ollama judge calls)
