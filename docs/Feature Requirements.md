# Feature Requirements

**Product:** Stock Price Movement  
**Document type:** Product requirements document (PRD)  
**Status:** Draft; planned capabilities, not implemented functionality  
**Created:** November 21, 2026  
**Audience:** The project owner, as its initial user and developer

## 1. Purpose

Build a personal investment research application that follows a company deeply,
analyzes its financial health and material developments, and assesses potential
implications for short-term stock performance and long-term value.

The application should answer three central questions:

1. What changed in the business or its environment?
2. How does that change compare with prior guidance and market expectations?
3. What might it imply at the current valuation, across different time horizons?

Business performance and stock performance are separate analytical targets. Strong
business results can coexist with poor stock returns when expectations or the
starting valuation are high. Predictive value must be demonstrated through
evaluation rather than assumed from persuasive explanations.

## 2. User and project objectives

### Primary user

The project owner will use the application for personal investment research.
They are comfortable with Python and LLM tool calling. The initial product does
not require customer accounts, collaboration, billing, or commercial distribution.

### Research objectives

- Reduce the effort required to review filings, earnings materials, and news.
- Build a continuously updated, source-backed understanding of a company.
- Detect material changes across documents and reporting periods.
- Connect events to revenue, costs, cash flow, financial risk, and valuation.
- Track an investment thesis, opposing evidence, and invalidation conditions.
- Explore forecasting signals without presenting unvalidated predictions as reliable.

### Learning objectives

- **LangGraph:** Implement typed state, workflow nodes, conditional routing,
  checkpoints, and recovery from interruption.
- **Agent harness:** Implement tool boundaries, context handling, retries,
  observability, budgets, and stopping conditions.
- **RAG:** Implement document preparation, metadata, retrieval, source attribution,
  and retrieval evaluation; add semantic search when useful.

Each learning objective should produce an inspectable feature and an evaluation
exercise. LangGraph can implement parts of the harness, and retrieval can be a
tool used by the workflow; these are complementary responsibilities.

## 3. Scope and product decisions

### Agreed scope

- Begin with one company: **Alphabet, Google's parent company**.
- Use **GOOGL** as the initial price series. Share company research across GOOG and
  GOOGL while keeping share-class prices and returns distinct.
- Start with a sourced comparison of consecutive earnings periods.
- Preserve facts, evidence, assumptions, and uncertainty throughout the workflow.
- Expand toward historical retrieval, bounded research, and market analysis.

### Proposed implementation defaults

Python, LangGraph, SQLite, local document storage, one LLM provider, and a
command-line interface are the proposed starting stack. These are architecture
defaults rather than a completed technology selection. Hosted vector storage is
not required for the initial local RAG implementation.

### Outside the initial scope

- Coverage of multiple target stocks or portfolio optimization.
- Automated order placement or brokerage integration.
- A hosted web interface, multi-user service, or large-scale infrastructure.
- Expensive alternative datasets before simpler sources show a specific gap.
- Guaranteed returns, precise price targets without assumptions, or unvalidated
  claims of predictive accuracy.

Competitor, sector, and market data may still be used as context for Alphabet.

## 4. Core user journeys

| Journey | User action | Expected outcome |
| --- | --- | --- |
| Establish a baseline | Request an overview of Alphabet | Business drivers, financial health, risks, competitors, and source references |
| Compare earnings | Select two reporting periods | Reproducible comparisons and an explanation of material changes |
| Investigate a question | Ask why a metric or outlook changed | Relevant evidence, competing explanations, and explicit gaps |
| Review developments | Request updates since a prior review | Deduplicated material events and their potential implications |
| Review the thesis | Inspect supporting and opposing evidence | Versioned thesis with watch items and invalidation conditions |
| Explore valuation | Supply or review scenario assumptions | Bear, base, and bull outcomes with sensitivity to assumptions |

## 5. Information requirements

### Source coverage

| Source category | Required coverage | Stage |
| --- | --- | --- |
| Official financial materials | Earnings releases; annual, quarterly, and material-event filings; financial statement notes | First milestone |
| Earnings calls | Prepared remarks and Q&A when a usable transcript is available | First milestone, availability dependent |
| Company communications | Investor relations news, presentations, product announcements, and relevant company blogs | Monitoring |
| Independent reporting | Financial developments, launches, contracts, leadership changes, litigation, financing, and growth prospects | Monitoring |
| Related companies | Competitors, suppliers, and major customers where relevant | Expanded research |
| Market data | Prices, volume, volatility, liquidity, corporate actions, sector and market benchmarks | Market analysis |
| Expectations | Historical consensus estimates, estimate revisions, and prior company guidance | Prior guidance first; consensus availability dependent |
| Economic context | Relevant interest rates, currencies, inflation, commodities, and credit conditions | Expanded research |
| Positioning and governance | Short interest, options context, insider disclosures, incentives, and ownership where useful | Optional expansion |

Primary documents should support reported company facts whenever possible.
Independent reporting should provide additional context and verification rather
than automatically being treated as inferior or superior evidence.

Providers must be assessed for coverage, timestamp quality, historical versions,
cost, access restrictions, and permitted storage or display. Missing or inaccessible
data must be disclosed; the application must not invent substitutes.

### Alphabet-specific coverage

| Area | Required questions and metrics, where disclosed |
| --- | --- |
| Search and advertising | Revenue growth, monetization, traffic acquisition costs, distribution, and competitive changes |
| Google Cloud | Revenue growth, operating profit and margin, demand indicators, and backlog where available |
| YouTube | Advertising trends and disclosed subscription or engagement measures |
| AI investment | Adoption evidence, monetization, infrastructure spending, operating costs, and depreciation |
| Financial health | Operating cash flow, capital expenditure, free cash flow, liquidity, debt maturities, and refinancing |
| Capital allocation | Buybacks, dividends, acquisitions, share-based compensation, financing, and dilution |
| Earnings quality | Cash conversion, accounting changes, unusual gains or charges, and auditor or control concerns |
| Competition and regulation | Developments affecting business economics, distribution, growth, or legal exposure |
| Other activities | Material developments in Other Bets and other disclosed business activities |

Product adoption must not be assumed to translate directly into profit. Analysis
should trace the proposed mechanism through revenue, margins, investment, and cash
flow, identifying unsupported links.

## 6. Functional requirements

### FR-01: Source ingestion and provenance

- Accept selected official documents for the first milestone; automatic discovery
  and scheduled collection may be added later.
- Preserve original content, source URL, publisher, document type, reporting
  period, publication time, retrieval time, and version or content hash.
- Retain page, section, table, or passage locations for citations.
- Distinguish publication time from the time the application first observed a source.
- Record ingestion failures and unavailable transcripts without silently omitting them.
- Deduplicate repeated ingestion and syndicated stories while retaining source links.

**Acceptance:** A report claim can be traced to the stored source version and its
location. Re-ingesting identical content does not create duplicate evidence.

### FR-02: Structured financial extraction and calculations

- Extract income statement, balance sheet, cash flow, segment, guidance, and risk
  information relevant to the research question.
- Retain metric definitions, units, currency, period boundaries, segment scope,
  and GAAP or non-GAAP status.
- Calculate changes and ratios in Python, retaining inputs and formulas.
- Support consecutive-period and year-over-year comparisons where compatible.
- Distinguish quarterly values from year-to-date values; flag incompatible periods,
  changed definitions, restatements, and invalid or zero denominators.
- Avoid treating an undisclosed value as zero or comparing unlike metrics.

**Acceptance:** Every numerical output is either directly sourced or reproducible
from identified inputs. Ambiguous extraction and incompatible comparisons are flagged.

### FR-03: Material change and event analysis

- Identify changes in results, guidance, risk disclosures, and management commitments.
- Separate new information from repeated commentary and previously disclosed events.
- Classify events by business area, potential financial mechanism, and time horizon.
- Distinguish reported facts, management claims, calculations, and interpretation.
- Show contrary evidence and avoid asserting causality solely from coincident price moves.

**Acceptance:** Each material conclusion includes evidence, a stated interpretation,
and relevant uncertainty. Conflicting sources remain visible.

### FR-04: Baseline and investment thesis

- Maintain a business overview, key drivers, financial trends, major risks, and peers.
- Record thesis statements, supporting evidence, opposing evidence, and invalidation
  conditions with timestamps and versions.
- Compare management commitments with later disclosures.
- Surface watch items and upcoming catalysts without fabricating event dates.

**Acceptance:** A later review can show what changed in the thesis and why, while
preserving the earlier view.

### FR-05: Historical retrieval and question answering

- Index document sections with company, document type, period, publication time,
  and citation metadata.
- Begin with keyword retrieval; evaluate semantic or hybrid retrieval before adoption.
- Retrieve evidence across periods for questions about changing guidance or risks.
- Query structured financial facts for numerical comparisons instead of relying only
  on prose retrieval.
- Apply a research cutoff date and exclude later publications or revisions.
- Return an explicit evidence gap when the corpus cannot answer a question.

**Acceptance:** Reviewed questions retrieve supporting passages and cite them.
Cutoff-date tests exclude future evidence. Original versions remain accessible.

### FR-06: Research reports and monitoring

- Produce a readable Markdown report with an as-of date and source coverage summary.
- Include key changes, financial comparisons, guidance changes, supporting and
  opposing evidence, potential horizon-specific implications, and watch items.
- Include references, assumptions, calculations, and missing data.
- Support updates since a previous review as monitoring is introduced.
- Make daily briefs and material-change alerts later capabilities; scheduling,
  notification channel, and materiality thresholds remain undecided.

**Acceptance:** The first report is inspectable without reading agent logs. Partial
coverage is clearly labeled, and a failed run cannot appear as a complete report.

### FR-07: Market expectations and price context

- Compare results with prior guidance and contemporaneous consensus where available.
- Retain estimate timestamps and definitions; do not label a result a consensus beat
  or miss without comparable evidence.
- Analyze GOOGL returns, volume, volatility, and performance relative to selected
  sector and market benchmarks.
- Handle corporate actions, trading calendars, and announcement timing consistently.
- Separate already-realized market response from a forecast of subsequent movement.
- Interpret positioning carefully: short interest differs from short-sale volume,
  and options-implied movement is not a direct directional forecast.

**Acceptance:** Returns and surprises specify their inputs and comparison windows;
missing historical expectations are disclosed.

### FR-08: Valuation and forecasting

- Build bear, base, and bull scenarios with explicit growth, profitability,
  reinvestment, discounting, and share-count assumptions as applicable.
- Show sensitivities and distinguish modeled value from an assured future price.
- Define forecast horizons and targets before evaluating signals.
- If probabilities are introduced, obtain them from evaluated models; do not use
  an LLM's self-reported confidence as a calibrated probability.
- Store forecasts, inputs, model versions, and timestamps before outcomes are known.

**Acceptance:** Scenario outputs can be recalculated from saved assumptions.
Forecast performance is reported against baselines with sample-size limitations.

## 7. Time horizons

The following are candidates discussed during planning, not final requirements:

| Candidate horizon | Analytical emphasis | Candidate output |
| --- | --- | --- |
| 1–5 trading days | Surprise, fresh information, liquidity, and market response | Subsequent return range or probability of sector outperformance |
| 1–3 months | Guidance, estimate revisions, operating trends, and catalysts | Evidence-backed outlook |
| 1–3 years | Cash generation, competitive position, and valuation | Bear/base/bull scenarios |

The user's holding period and final definitions remain open. The first earnings
comparison can proceed without selecting a forecasting target.

## 8. Workflow and agent requirements

The initial workflow is:

```text
Load sources -> Extract facts -> Calculate comparisons
    -> Analyze changes -> Validate evidence -> Write report
```

LangGraph state should include the company, research question, cutoff date,
document references, extracted facts, calculations, evidence gaps, validation
results, run budget, and output location.

- Use deterministic steps for calculations and explicit validation.
- Introduce conditional paths for missing or contradictory evidence.
- Persist checkpoints and resume interrupted runs without duplicating completed
  ingestion or corrupting report artifacts.
- Keep a durable evidence store separate from transient workflow state.
- Add agent-selected follow-up research only after the explicit workflow works.
- Limit research by tool permissions, steps, time, and configurable spending bounds.
- Use bounded retries and stop repeated searches that add no evidence.
- Treat source content as untrusted data, never executable instructions.
- Log tool calls, source selection, failures, model versions, and usage. Do not log secrets.
- Stop with a labeled partial result when evidence or budget is exhausted.

## 9. Logical data model

| Record | Minimum contents |
| --- | --- |
| Company/security | Company identifier, ticker, share class, exchange, and currency |
| Source document | URL, type, original content reference, period, timestamps, and version |
| Evidence passage | Document ID, section/page/table locator, and source text |
| Financial fact | Metric, value, units, period, scope, accounting basis, and evidence ID |
| Calculation | Formula, input fact IDs, output, and comparison period |
| Event/claim | Category, date, novelty, fact/claim/interpretation label, evidence, and uncertainty |
| Thesis version | Statements, support, opposition, invalidation conditions, and timestamp |
| Research run | Question, cutoff, configuration, checkpoint, usage, status, and artifacts |
| Scenario/forecast | Horizon, assumptions/features, model version, creation time, and later outcome |

This is a logical model; exact schemas and storage boundaries will be specified
during implementation. Local files and SQLite should be sufficient initially.

## 10. Quality and operational requirements

- **Auditability:** Reports link to original evidence and preserve calculation lineage.
- **Temporal integrity:** Research honors cutoff dates and distinguishes original
  disclosures from later revisions.
- **Reliability:** Failures, stale data, and incomplete coverage are visible; recovery
  does not silently skip work.
- **Reproducibility:** Save source versions, prompts/configuration, model identifiers,
  and deterministic calculations. Do not promise identical LLM prose across runs.
- **Local operation:** The initial application can run locally, with network access
  needed for external sources or hosted models. Local execution does not imply
  that content stays on the device when a model API is used.
- **Cost control:** Capture model/tool usage and apply configurable limits. Pricing,
  dollar budgets, and latency targets remain to be selected.
- **Access hygiene:** Keep credentials outside tracked files and honor provider access
  and storage terms. Do not bypass unavailable or restricted sources.

## 11. Evaluation and success criteria

### Research quality

Create a small manually reviewed set of Alphabet documents and questions. Evaluate:

- Financial extraction accuracy, including units, periods, and segment scope.
- Calculation correctness and reproducibility.
- Citation validity and whether evidence actually supports each claim.
- Retrieval relevance and ability to find contradictory or missing evidence.
- Correct handling of stale sources, restatements, and cutoff dates.
- Recovery from interruption and termination under exhausted budgets.

The first milestone requires every reported number to be traceable, every
calculation to be reproducible, and unsupported conclusions to be labeled or
removed. Quantitative evaluation thresholds beyond these checks remain open.

### Forecasting quality

- Use chronological evaluation and a prospective, timestamped forecasting record.
- Compare against simple market, sector, and price-only baselines.
- Measure the incremental contribution of document and news features.
- Evaluate calibration and interval coverage when probabilistic outputs exist.
- Account for transaction costs and execution timing if strategies are evaluated.
- Recognize the limited number of independent events for one stock and the risk
  that an LLM already knows historical outcomes.
- If coverage expands, include delisted companies and historical universes to
  address survivorship bias.

Supported explanations and accurate extraction are useful outcomes independently
of whether a statistically credible forecasting advantage is found.

## 12. Delivery milestones

| Milestone | Deliverable | Exit condition |
| --- | --- | --- |
| M1: Earnings comparison | Explicit LangGraph workflow and cited Markdown report for two consecutive periods, with year-over-year context where available | Sourced numbers, reproducible calculations, visible gaps, and reviewed claims |
| M2: Persistence and recovery | Durable checkpoints, run records, and failure handling | Interrupted runs resume without duplicate ingestion or lost evidence |
| M3: Historical RAG | Local corpus, metadata filters, retrieval, and cited cross-period answers | Reviewed retrieval questions pass evidence and cutoff-date checks |
| M4: Bounded research and monitoring | Follow-up tools, budgets, traces, thesis updates, and material-change detection | Failure cases terminate clearly and changes link to evidence |
| M5: Market and valuation analysis | Expectations comparisons, price context, scenarios, and prospective signal evaluation | Saved assumptions, defined horizons, and baseline comparisons |

Milestones are ordered by dependencies. Dates are not committed. Full automated
discovery, monitoring schedules, notification delivery, and a UI require separate
implementation decisions.

## 13. Risks and mitigations

| Risk | Planned response |
| --- | --- |
| Plausible but unsupported model output | Evidence-linked claims, calculation code, and reviewed evaluation cases |
| Promotional or duplicated news | Preserve provenance, deduplicate, and distinguish claims from verified outcomes |
| Incomplete disclosures | Report gaps instead of estimating undisclosed metrics without explicit assumptions |
| Historical information leakage | Versioned sources, cutoff filters, original estimates, and prospective evaluation |
| Narrow sample and overfitting | Simple baselines, restrained conclusions, and explicit sample limitations |
| Poor timestamp or provider coverage | Assess providers before reliance and label unavailable comparisons |
| Unbounded agent work | Step/time/cost budgets, bounded retries, and repeated-search detection |
| Premature infrastructure complexity | Start locally and add services only when requirements justify them |

## 14. Open decisions

1. Which holding periods, forecast targets, and benchmarks matter most to the user?
2. Which two earnings periods and historical depth should seed the first corpus?
3. Which LLM provider, model, and usage budget should be used?
4. Which news, transcript, price, and consensus providers meet coverage and cost needs?
5. What refresh cadence, materiality rules, and notification channel should monitoring use?
6. Which valuation methodology and assumptions should the first scenarios expose?
7. Which retrieval approach improves the reviewed questions enough to justify embeddings?
8. What numeric quality thresholds, runtime targets, and retention policy should apply?

These decisions must not be represented as settled requirements. Initial document
comparison and local workflow design can proceed independently of most of them.
