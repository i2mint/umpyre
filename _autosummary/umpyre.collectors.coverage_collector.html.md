# umpyre.collectors.coverage_collector

Collector for test coverage metrics.

### Classes

| [`CoverageCollector`](#umpyre.collectors.coverage_collector.CoverageCollector)([repo_path, source, ...])   | Collect test coverage metrics from coverage reports.   |
|------------------------------------------------------------------------------------------------|--------------------------------------------------------|

### *class* umpyre.collectors.coverage_collector.CoverageCollector(repo_path=None, source='pytest-cov', coverage_file=None)

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
