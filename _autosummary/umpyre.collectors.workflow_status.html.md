# umpyre.collectors.workflow_status

Collector for GitHub workflow status using GitHub API.

### Classes

| [`WorkflowStatusCollector`](#umpyre.collectors.workflow_status.WorkflowStatusCollector)(repo[, token, ...])   | Collect GitHub workflow status using GitHub API.   |
|------------------------------------------------------------------------------------------------|----------------------------------------------------|

### *class* umpyre.collectors.workflow_status.WorkflowStatusCollector(repo, token=None, lookback_runs=10, workflow_name=None)

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
