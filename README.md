# Stock Price Movement

A personal investment research service for understanding a company's financial
health, tracking material developments, and assessing their potential implications
for short-term stock performance and long-term value.

The initial focus is **Alphabet, Google's parent company**, with **GOOGL** as the
initial price series. Company research will apply to both GOOG and GOOGL, while
price analysis will keep the share classes distinct.

## Goals

- Build a deeper, continuously updated understanding of one company.
- Identify what changed, how it compares with expectations, and why it matters.
- Connect business developments to financial outcomes, valuation, and price movement.
- Maintain an investment thesis, opposing evidence, and conditions that would
  invalidate it.
- Learn and implement LangGraph, an agent harness, and retrieval-augmented
  generation (RAG) through practical features.

The Python project foundation is implemented. Research, ingestion, and forecasting
capabilities described below are planned and are not yet implemented.

## Development setup

Use [uv](https://docs.astral.sh/uv/) for Python versions, dependency management,
the local virtual environment, and reproducible dependency locking. On macOS,
install uv with Homebrew if needed:

```bash
brew install uv
```

From the repository root:

```bash
uv sync --locked
uv run stock-price-movement --help
uv run stock-price-movement config
```

The project pins Python 3.12 in `.python-version`. uv downloads it when needed and
creates `.venv`, leaving macOS's system Python unchanged. Initial setup requires
network access. Commit `pyproject.toml`, `.python-version`, and `uv.lock`; keep
`.venv`, secrets, and generated data out of version control.

The starter CLI displays help, version information, and local configuration. It
does not fetch financial data or call a model. The module entry point also works:

```bash
uv run python -m stock_price_movement config
```

### Configuration

Defaults work without a configuration file or API keys. Optionally copy
`.env.example` to `.env` and edit it. Settings are read when a command needs them;
environment variables take precedence over `.env`, which takes precedence over
defaults.

| Variable | Default | Purpose |
| --- | --- | --- |
| `SPM_DATA_DIR` | `data` | Root for future local documents, databases, and reports |
| `SPM_LOG_LEVEL` | `INFO` | One of DEBUG, INFO, WARNING, ERROR, or CRITICAL |

Run commands from the repository root so `.env` and relative paths resolve
consistently. The `config` command resolves the data path but does not create it.
If overriding the data directory, ensure that location is also excluded from Git.

### Dependencies and quality checks

```bash
uv add package-name              # Add a runtime dependency and update uv.lock
uv add --dev package-name        # Add a development dependency
uv run ruff check .
uv run ruff format --check .
uv build
```

Runtime dependencies currently provide validated environment configuration through
`pydantic-settings`. Ruff supplies development linting and formatting. LangGraph,
retrieval, model integrations, and test tooling will be added with their features.

### Project layout

```text
docs/                       Product requirements
src/stock_price_movement/
    __init__.py             Package
    __main__.py             Module entry point
    cli.py                  Command-line interface
    config.py               Validated local settings
.env.example                Optional configuration template
.python-version             Development Python version
pyproject.toml              Package metadata and dependency declarations
uv.lock                     Resolved dependency versions
```

## Research inputs

The service will combine:

- **Independent news:** financial developments, growth prospects, product launches,
  contracts, competition, litigation, and other potentially material events.
- **Company sources:** investor relations updates, official news, earnings
  releases, presentations, and earnings-call transcripts, including Q&A.
- **Financial and regulatory documents:** annual and quarterly filings, income
  statements, balance sheets, cash flow statements, accounting notes, and risk
  disclosures.
- **Market context:** prices, volume, volatility, sector and benchmark performance,
  valuation, analyst expectations and revisions where available, and economic
  conditions relevant to the business.
- **Related businesses:** competitors, suppliers, and major customers when their
  developments provide useful context for Alphabet.

Company performance and stock performance are separate analytical targets. Strong
results may already be reflected in the price. Research should therefore consider
expectations and valuation alongside reported business outcomes.

## Alphabet research focus

| Area | Questions to investigate |
| --- | --- |
| Search and advertising | How are growth, monetization, and traffic acquisition costs changing? |
| Google Cloud | Is growth translating into operating profit, and what supports future demand? |
| YouTube | What do disclosed advertising and subscription metrics tell us? |
| AI investment | What evidence connects adoption to revenue, operating costs, and capital expenditure? |
| Financial health | How are cash generation, debt, financing, buybacks, and dilution changing? |
| Competition and regulation | Which developments could change distribution, economics, or growth? |

## Intended research outputs

A sourced research brief should answer:

1. What changed, and what evidence supports it?
2. How does it compare with prior results, guidance, and market expectations?
3. Does it affect the next quarter, the next few years, or both?
4. What assumptions would justify the current valuation?
5. What contradicts the investment thesis, and what should we watch next?

Separate reported facts, management claims, calculations, and interpretation.
Make missing disclosures and uncertainty explicit. Longer-term analysis should
use bear, base, and bull scenarios with stated assumptions. Exact forecast
horizons remain to be chosen.

## First milestone: compare earnings periods

Produce a cited Markdown report comparing two consecutive Alphabet earnings
periods, including year-over-year comparisons where available to account for
seasonality.

Start with official earnings releases and filings, adding call transcripts when
available. Extract financial results, guidance, management claims, and risks into
structured records; calculate changes with Python; then explain material changes
and opposing evidence.

The initial LangGraph workflow will be:

```text
Load sources
    -> Extract facts and evidence
    -> Calculate comparisons
    -> Analyze changes
    -> Validate evidence
    -> Write report
```

This milestone is complete when:

- Every reported number traces to a source passage or table.
- Calculations are reproducible and retain units and reporting periods.
- Claims are supported by evidence or explicitly marked as assumptions.
- Missing sources and conflicting evidence are visible in the report.

## Architecture and learning roadmap

The proposed starting stack is **Python, LangGraph, SQLite, local document
storage, and one LLM provider**, with a command-line interface first. Provider and
model selection remain open.

### 1. Explicit research workflow with LangGraph

Use typed state to track the research question, cutoff date, sources, extracted
facts, evidence gaps, and final report. Add conditional routing and persistent
checkpoints so interrupted work can resume. Keep numerical calculations in Python.

### 2. Local historical retrieval with RAG

Preserve original documents and index useful sections with source metadata.
Start with SQLite metadata and full-text search; add embeddings and a local
vector index if evaluation shows they improve retrieval. A hosted vector database
is not required for the initial single-company scope.

Retrieval should support questions such as: "How has management's growth outlook
changed over the last four quarters?" Store publication and retrieval times,
document versions, reporting periods, and source locations. Historical research
must exclude information published after its cutoff date.

### 3. Bounded agent behavior and harness

Allow follow-up research when evidence is missing or contradictory. The harness
will define tools, context handling, retries, call and cost budgets, tracing, and
stopping conditions. Treat retrieved documents as evidence, never as instructions.
Test behavior with unavailable sources, stale documents, contradictory figures,
and repeated searches.

### 4. Market analysis and prospective evaluation

Add price data, expectations, valuation scenarios, and horizon-specific signals.
Compare results with simple market, sector, and price-only baselines, and record
forecasts before outcomes are known.

## Evaluation principles

Research quality and forecasting quality will be evaluated separately. Accurate
extraction, reliable retrieval, and supported explanations do not by themselves
demonstrate an ability to predict returns.

- Evaluate extraction accuracy, retrieval relevance, citation support, and
  numerical consistency using a small reviewed set of questions and documents.
- Preserve what was available at each historical point, including original
  guidance and estimates, to avoid look-ahead bias.
- Account for restatements, corporate actions, and reporting-period differences.
- Recognize that a single stock provides relatively few independent events for
  validating a forecasting model, and that LLMs may already know historical outcomes.
- Use prospective evaluation; assess calibration and forecast ranges if
  probabilistic forecasts are introduced, and costs if trading strategies are tested.

## Initial scope boundaries

The first version is a personal research tool for one company. Multi-stock
coverage, automated trading, a hosted UI, and large-scale infrastructure are
outside the initial scope. Predictive value is a hypothesis to test, not an
assumed capability.
