# umpyre.collectors.wily_collector

Collector for complexity metrics using wily.

### Classes

| [`WilyCollector`](#umpyre.collectors.wily_collector.WilyCollector)([repo_path, max_revisions, ...])   | Collect complexity metrics using wily.   |
|---------------------------------------------------------------------------------------------------|------------------------------------------|

### *class* umpyre.collectors.wily_collector.WilyCollector(repo_path=None, max_revisions=5, operators=None)

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
