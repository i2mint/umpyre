# umpyre

Code analysis and quality metrics tracking system for CI/CD pipelines.

## Overview

`umpyre` provides automated code metrics collection and tracking for Python projects, designed to integrate seamlessly with GitHub Actions CI/CD pipelines. Track code quality trends over time with minimal overhead.

**Key Features:**
- 🎯 **Pluggable collectors**: Workflow status, complexity (wily), coverage, code statistics
- 📊 **Git-based storage**: Metrics stored in separate branch, no external dependencies
- ⚙️ **Config-driven**: Customize via YAML configuration
- 🚀 **Fast & lightweight**: Limited history tracking for speed
- 🔌 **GitHub Action**: Drop-in integration for existing workflows

## Installation

```bash
pip install umpyre
```

## Quick Start

### 1. Create Configuration

Create `.github/umpyre-config.yml`:

```yaml
schema_version: "1.0"

collectors:
  workflow_status:
    enabled: true
    lookback_runs: 10
  
  coverage:
    enabled: true
    source: pytest-cov
  
  umpyre_stats:
    enabled: true
    exclude_dirs: [tests, examples, scrap]

storage:
  branch: code-metrics
  formats: [json, csv]
```

### 2. Add to GitHub Actions

In your `.github/workflows/ci.yml` (after successful PyPI publish):

```yaml
- name: Track Code Metrics
  if: success()
  uses: i2mint/umpyre/actions/track-metrics@master
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
```

### 3. View Metrics

Metrics are stored in the `code-metrics` branch:
- `metrics.json` - Latest snapshot
- `metrics.csv` - Flat format for analysis
- `history/YYYY-MM/` - Historical records

## CLI Usage

```bash
# Collect and store metrics
python -m umpyre.cli collect

# Collect with custom config
python -m umpyre.cli collect --config my-config.yml

# Dry run (don't store)
python -m umpyre.cli collect --no-store

# Validate against thresholds (coming soon)
python -m umpyre.cli validate
```

## Available Collectors

### WorkflowStatusCollector
Tracks GitHub CI/CD health via API:
- Last run status (success/failure)
- Recent failure count
- Last successful run timestamp

### CoverageCollector
Extracts test coverage from pytest-cov or coverage.py:
- Line coverage %
- Branch coverage %
- Supports JSON and XML formats

### WilyCollector
Complexity metrics using wily (requires installation):
- Cyclomatic complexity
- Maintainability index
- Limited to recent commits for speed

### UmpyreCollector
Code statistics using built-in analyzer:
- Function/class counts
- Line metrics (total, empty, comments, docs)
- Code ratios and averages

## Configuration Reference

See `.github/umpyre-config.yml` for full options:

```yaml
schema_version: "1.0"  # Required

collectors:
  workflow_status:
    enabled: true
    lookback_runs: 10  # Number of recent runs to analyze
  
  wily:
    enabled: true
    max_revisions: 5  # Limit for performance
    operators: [cyclomatic, maintainability]
  
  coverage:
    enabled: true
    source: pytest-cov  # or 'coverage'
  
  umpyre_stats:
    enabled: true
    exclude_dirs: [tests, examples, scrap]

storage:
  branch: code-metrics  # Branch name for metrics
  formats: [json, csv]  # Output formats
  retention:
    strategy: all  # or: last_n_days, last_n_commits

visualization:  # Coming in Phase 2
  generate_plots: true
  generate_readme: true
  plot_metrics: [maintainability, coverage, loc]

thresholds:  # Coming in Phase 3
  enabled: false

aggregation:  # Coming in Phase 2
  enabled: false
```

## Architecture

```
umpyre/
├── collectors/          # Metric collectors (pluggable)
│   ├── base.py         # Abstract Collector with Mapping interface
│   ├── workflow_status.py
│   ├── wily_collector.py
│   ├── coverage_collector.py
│   └── umpyre_collector.py
├── storage/            # Persistence layer
│   ├── git_branch.py  # Git-based storage
│   └── formats.py     # JSON/CSV serialization
├── config.py           # YAML config loading
├── schema.py           # Versioned metric schema
└── cli.py              # Command-line interface
```

## Metric Schema (v1.0)

```json
{
  "schema_version": "1.0",
  "timestamp": "2025-01-15T10:30:00Z",
  "commit_sha": "abc123...",
  "commit_message": "Fix bug in parser",
  "python_version": "3.10",
  "workflow_status": {
    "last_run_status": "success",
    "recent_failure_count": 0
  },
  "metrics": {
    "complexity": {
      "cyclomatic_avg": 3.2,
      "maintainability_index": 75.3
    },
    "coverage": {
      "line_coverage": 87.5,
      "branch_coverage": 82.1
    },
    "code_stats": {
      "num_functions": 342,
      "num_classes": 28
    }
  },
  "collection_duration_seconds": 12.3
}
```

## Roadmap

**Phase 1 (✅ Complete)**: Core tracking system
- Config-driven collectors
- Git branch storage
- CLI and GitHub Action

**Phase 2 (Planned)**: Visualization & Aggregation
- Plot generation (matplotlib/plotly)
- Auto-generated README with charts
- Cross-repository aggregation
- Organization-wide dashboards

**Phase 3 (Planned)**: Advanced Features
- Security metrics (bandit)
- Docstring coverage (interrogate)
- Threshold validation with custom validators
- Data pruning and compression
- Schema migration utilities

## Contributing

Contributions welcome! See `misc/CHANGELOG.md` for recent changes.

## Original Code Statistics Feature

Get stats about packages (existing functionality preserved):

```python
from umpyre import modules_info_df, stats_of
import collections

# Analyze a single package
modules_info_df(collections)

# Compare multiple packages
stats_of(['urllib', 'json', 'collections'])
```

See original README examples above for detailed usage.

## License

Apache-2.0
