# umpyre.collectors

Collectors package - metric collection implementations.

### Classes

| [`MetricCollector`](#umpyre.collectors.MetricCollector)()                              | Abstract base for metric collectors using Mapping interface.   |
|-------------------------------------------------------------------------------------------------|----------------------------------------------------------------|
| [`CollectorRegistry`](#umpyre.collectors.CollectorRegistry)()                            | Registry for managing available collectors.                    |
| [`UmpyreCollector`](#umpyre.collectors.UmpyreCollector)([root_path, exclude_dirs])     | Collect code statistics using AST parsing (no code execution). |
| [`WorkflowStatusCollector`](#umpyre.collectors.WorkflowStatusCollector)(repo[, token, ...])    | Collect GitHub workflow status using GitHub API.               |
| [`WilyCollector`](#umpyre.collectors.WilyCollector)([repo_path, max_revisions, ...]) | Collect complexity metrics using wily.                         |
| [`CoverageCollector`](#umpyre.collectors.CoverageCollector)([repo_path, source, ...])    | Collect test coverage metrics from coverage reports.           |

### *class* umpyre.collectors.CollectorRegistry

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Registry for managing available collectors.

#### get(name)

Get collector class by name.

* **Return type:**
  [`type`](https://docs.python.org/3/builtins/functions.html#type)[[`MetricCollector`](umpyre.collectors.base.html.md#umpyre.collectors.base.MetricCollector)]

#### list_collectors()

List all registered collector names.

* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]

#### register(name, collector_class)

Register a collector class.

* **Parameters:**
  * **name** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Collector identifier
  * **collector_class** ([`type`](https://docs.python.org/3/builtins/functions.html#type)[[`MetricCollector`](umpyre.collectors.base.html.md#umpyre.collectors.base.MetricCollector)]) – MetricCollector subclass

### *class* umpyre.collectors.CoverageCollector(repo_path=None, source='pytest-cov', coverage_file=None)

Bases: [`MetricCollector`](umpyre.collectors.base.html.md#umpyre.collectors.base.MetricCollector)

Collect test coverage metrics from coverage reports.

Supports:

- coverage.py JSON reports
- coverage.py XML reports (Cobertura format)

Tracks:

- Line coverage percentage
- Branch coverage percentage (if available)
- Statements covered/total

### Example

```pycon
>>> # This requires coverage report files
>>> # Skip in doctest as it requires actual test runs
>>> True
```

#### collect()

Collect coverage metrics from report files.

* **Returns:**
  - line_coverage: Line coverage percentage
  - branch_coverage: Branch coverage percentage (may be 0 if not tracked)
  - statements_covered: Number of statements covered
  - statements_total: Total number of statements
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### *class* umpyre.collectors.MetricCollector

Bases: [`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping), [`ABC`](https://docs.python.org/3/library/abc.html#abc.ABC)

Abstract base for metric collectors using Mapping interface.

Collectors implement the Mapping protocol to provide dict-like access
to collected metrics, enabling flexible composition and iteration.

### Example

```pycon
>>> class SimpleCollector(MetricCollector):
...     def collect(self) -> dict:
...         return {'lines': 100, 'functions': 10}
>>> collector = SimpleCollector()
>>> collector['lines']
100
>>> list(collector)
['lines', 'functions']
```

#### *abstractmethod* collect()

Collect metrics and return as dictionary.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  Dictionary of metric names to values

#### refresh()

Force re-collection of metrics.

#### to_dict()

Export all metrics as dictionary.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### *class* umpyre.collectors.UmpyreCollector(root_path=None, exclude_dirs=None)

Bases: [`MetricCollector`](umpyre.collectors.base.html.md#umpyre.collectors.base.MetricCollector)

Collect code statistics using AST parsing (no code execution).

Provides metrics like:

- Number of functions and classes
- Lines of code (total, empty, comments, docs)
- Code ratios (comment/empty/function lines)
- Mean lines per function

Uses AST parsing instead of dynamic imports for safety.

### Example

```pycon
>>> import tempfile
>>> from pathlib import Path
>>> # Create a simple Python file for testing
>>> with tempfile.TemporaryDirectory() as tmpdir:
...     test_file = Path(tmpdir) / "test.py"
...     test_file.write_text('''def hello():
...     """Say hello."""
...     return "hello"
...
... class Greeter:
...     """A greeter."""
...     pass
... ''')
...     collector = UmpyreCollector(tmpdir)
...     metrics = collector.collect()
...     metrics['num_functions'] >= 1 and metrics['num_classes'] >= 1
True
```

#### collect()

Collect code statistics from root directory using AST parsing.

* **Returns:**
  - num_functions: Total number of functions
  - num_classes: Total number of classes
  - total_lines: Total lines of code
  - empty_lines: Number of empty lines
  - comment_lines: Number of comment lines
  - docs_lines: Number of documentation lines
  - function_lines: Lines in functions
  - empty_lines_ratio: Ratio of empty lines
  - comment_lines_ratio: Ratio of comment lines
  - function_lines_ratio: Ratio of function lines
  - mean_lines_per_function: Average lines per function
  - files_analyzed: Number of files successfully analyzed
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### *class* umpyre.collectors.WilyCollector(repo_path=None, max_revisions=5, operators=None)

Bases: [`MetricCollector`](umpyre.collectors.base.html.md#umpyre.collectors.base.MetricCollector)

Collect complexity metrics using wily.

Tracks:

- Cyclomatic complexity (average)
- Maintainability index
- Total lines of code
- Files analyzed

#### NOTE
Limited to recent commits (max_revisions) for performance.

### Example

```pycon
>>> # This requires wily to be installed and a git repo
>>> # Skip in doctest as it requires git setup
>>> True
```

#### collect()

Collect complexity metrics using wily.

* **Returns:**
  - cyclomatic_avg: Average cyclomatic complexity
  - maintainability_index: Maintainability index score
  - total_loc: Total lines of code
  - files_analyzed: Number of files analyzed
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### *class* umpyre.collectors.WorkflowStatusCollector(repo, token=None, lookback_runs=10, workflow_name=None)

Bases: [`MetricCollector`](umpyre.collectors.base.html.md#umpyre.collectors.base.MetricCollector)

Collect GitHub workflow status using GitHub API.

Tracks:

- Last workflow run status (success/failure)
- Last successful run timestamp
- Recent failure count
- Workflow run URL

### Example

```pycon
>>> # Mock test (requires actual GitHub API)
>>> import os
>>> if os.getenv('GITHUB_TOKEN'):
...     collector = WorkflowStatusCollector(
...         repo="thorwhalen/astate",
...         token=os.getenv('GITHUB_TOKEN')
...     )
...     metrics = collector.collect()
...     'last_run_status' in metrics
... else:
...     True  # Skip if no token
True
```

#### collect()

Collect workflow status from GitHub API.

* **Returns:**
  - last_run_status: ‘success’, ‘failure’, or ‘other’
  - last_success_timestamp: ISO timestamp or None
  - recent_failure_count: Number of failures in lookback window
  - run_url: URL of last run
  - total_runs_analyzed: Number of runs examined
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### Modules

| [`base`](umpyre.collectors.base.html.md#module-umpyre.collectors.base)                             | Base collector class with Mapping interface.                       |
|-----------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| [`coverage_collector`](umpyre.collectors.coverage_collector.html.md#module-umpyre.collectors.coverage_collector) | Collector for test coverage metrics.                               |
| [`umpyre_collector`](umpyre.collectors.umpyre_collector.html.md#module-umpyre.collectors.umpyre_collector)     | Collector using AST-based code analysis (safe, no code execution). |
| [`wily_collector`](umpyre.collectors.wily_collector.html.md#module-umpyre.collectors.wily_collector)         | Collector for complexity metrics using wily.                       |
| [`workflow_status`](umpyre.collectors.workflow_status.html.md#module-umpyre.collectors.workflow_status)       | Collector for GitHub workflow status using GitHub API.             |
