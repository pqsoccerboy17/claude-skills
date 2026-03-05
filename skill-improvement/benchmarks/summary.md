# Skill Benchmark Summary - 13 Skills

**Date**: 2026-03-05
**Model**: Claude Opus 4.6
**Methodology**: 3 runs per eval per config (with_skill vs without_skill), graded against 4-5 expectations per eval
**Total runs**: ~162 executor runs + ~162 grading runs

## Results (sorted by delta)

| Skill | Tier | With Skill | Without Skill | Delta | Variance |
|-------|------|-----------|---------------|-------|----------|
| agent-dashboard | C | 100% | 0% | +100pp | 0% |
| factory-pm | A | 100% | 10% | +90pp | 0% |
| ecosystem-status | B | 100% | 10% | +90pp | 0% |
| gemini-api | B | 100% | 20% | +80pp | 0% |
| notifications | B | 100% | 30% | +70pp | 0% |
| ecosystem-config | B | 100% | 33% | +67pp | 0% |
| last30days | B | 90% | 30% | +60pp | 0% |
| pdf | C | 100% | 54% | +46pp | 0% |
| xlsx | C | 100% | 57% | +43pp | 0% |
| mcp-builder | A | 100% | 60% | +40pp | 0% |
| file-organizer | A | 100% | 63% | +37pp | 0% |
| internal-comms | A | 100% | 78% | +22pp | 0% |
| csv-data-summarizer | A | 100% | 80% | +20pp | 0% |

## Aggregate Statistics

- **Average with_skill pass rate**: 99.2%
- **Average without_skill pass rate**: 40.4%
- **Average delta**: +58.8pp
- **Variance**: Near-zero across all skills (3 runs showed consistent results)

## Key Findings

### 1. User-specific infrastructure skills show the largest gains
Skills that encode knowledge about custom tools, file paths, and configurations (agent-dashboard, ecosystem-status, ecosystem-config) show +67-100pp deltas. Without the skill, the agent has zero awareness of these tools.

### 2. Workflow discipline skills are highly valuable
factory-pm (+90pp) enforces a spec-before-code workflow. Without it, agents jump straight to implementation, skipping clarifying questions, specs, and approval gates entirely.

### 3. API-specific skills prevent wrong tool selection
gemini-api (+80pp) and notifications (+70pp) prevent agents from defaulting to wrong APIs (OpenAI instead of Gemini) or wrong notification backends (macOS instead of Pushover).

### 4. Domain knowledge skills add incremental value
Skills for common tasks (csv-data-summarizer, internal-comms) show +20-22pp - still meaningful, primarily adding best practices like pandas usage, data quality checks, and tone/formatting conventions.

### 5. Technical skills enforce modern practices
pdf (+46pp) and xlsx (+43pp) steer agents toward modern libraries (pypdf not PyPDF2) and professional standards (color coding, zero formula errors, LibreOffice recalc).

## Tier Analysis

| Tier | Avg Delta | Description |
|------|----------|-------------|
| Infrastructure (B) | +73pp | Skills encoding user-specific tools and paths |
| Workflow (A - factory-pm) | +90pp | Skills enforcing process discipline |
| Technical (A/C) | +38pp | Skills teaching tool-specific best practices |
| Domain (A) | +21pp | Skills adding business conventions |

## Eval Quality Notes

- last30days "includes links" assertion always fails in simulated mode (no actual web search) - consider adjusting for offline eval
- agent-dashboard 100% delta may be inflated since the tool is completely unknown without the skill
- Low variance (0% stddev) across runs suggests evals are deterministic - consider adding more ambiguous prompts for future variance testing

## File Inventory

Each skill directory contains:
- `benchmark.json` - Machine-readable results with full run data
- `benchmark.md` - Human-readable summary table
- `eval-{id}/{config}/run-{n}/outputs/output.md` - Executor outputs
- `eval-{id}/{config}/run-{n}/outputs/metrics.json` - Execution metrics
- `eval-{id}/{config}/run-{n}/grading.json` - Grading results
- `eval-{id}/eval_metadata.json` - Eval definitions
