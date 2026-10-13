# umpyre.storage

Storage operations for metrics.

### Functions

| [`serialize_metrics`](#umpyre.storage.serialize_metrics)(data, output_path[, format])   | Serialize metrics to file.                          |
|---------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| [`deserialize_metrics`](#umpyre.storage.deserialize_metrics)(file_path[, format])         | Deserialize metrics from file.                      |
| [`parse_metric_filename`](#umpyre.storage.parse_metric_filename)(filename)                  | Parse metric filename into components.              |
| [`find_metrics_by_commit`](#umpyre.storage.find_metrics_by_commit)(history_dir, commit_sha)  | Find metrics file for a specific commit.            |
| [`find_metrics_by_version`](#umpyre.storage.find_metrics_by_version)(history_dir, version)    | Find all metrics files for a specific PyPI version. |
| [`get_latest_metric_for_version`](#umpyre.storage.get_latest_metric_for_version)(history_dir, ...)  | Get the most recent metrics file for a version.     |
| [`get_all_versions`](#umpyre.storage.get_all_versions)(history_dir)                    | Get all unique PyPI versions found in metrics.      |
| [`filter_by_date_range`](#umpyre.storage.filter_by_date_range)(history_dir[, ...])         | Get metrics files within a date range.              |

### Classes

| [`GitBranchStorage`](#umpyre.storage.GitBranchStorage)(repo_path[, remote, token])   | Store metrics in a separate git branch.   |
|-------------------------------------------------------------------------------------------------|-------------------------------------------|

### Exceptions

| [`GitBranchStorageError`](#umpyre.storage.GitBranchStorageError)   | Raised when git branch storage operations fail.   |
|--------------------------------------------------------------------------|---------------------------------------------------|

### *class* umpyre.storage.GitBranchStorage(repo_path, remote='origin', , token=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Store metrics in a separate git branch.

This provides versioned, branch-based storage without polluting
the main branch or requiring external artifacts.

### Example

```pycon
>>> storage = GitBranchStorage(repo_path="/path/to/repo")
>>> metrics = {"lines": 100, "functions": 10}
>>> storage.store_metrics(metrics, "abc123", branch="code-metrics")
```

#### store_metrics(metrics, commit_sha, branch='code-metrics', formats=None)

Store metrics to git branch.

* **Parameters:**
  * **metrics** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)) – Metric dictionary to store
  * **commit_sha** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Git commit SHA
  * **branch** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Target branch name
  * **formats** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]]) – List of formats (‘json’, ‘csv’)

### *exception* umpyre.storage.GitBranchStorageError

Bases: [`Exception`](https://docs.python.org/3/builtins/exceptions.html#Exception)

Raised when git branch storage operations fail.

### umpyre.storage.deserialize_metrics(file_path, format='json')

Deserialize metrics from file.

* **Parameters:**
  * **file_path** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to input file
  * **format** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Format (‘json’ or ‘csv’)
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  Metric dictionary

### umpyre.storage.filter_by_date_range(history_dir, start_date=None, end_date=None)

Get metrics files within a date range.

* **Parameters:**
  * **history_dir** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to history directory
  * **start_date** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime)]) – Start datetime (inclusive)
  * **end_date** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`datetime`](https://docs.python.org/3/library/datetime.html#datetime.datetime)]) – End datetime (inclusive)
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]
* **Returns:**
  List of paths within date range (sorted chronologically)

### Example

```pycon
>>> from datetime import datetime, timedelta
>>> end = datetime.now()
>>> start = end - timedelta(days=7)
>>> recent = filter_by_date_range(Path("history"), start, end)
>>> print(f"Found {len(recent)} metrics from last 7 days")
```

### umpyre.storage.find_metrics_by_commit(history_dir, commit_sha)

Find metrics file for a specific commit.

* **Parameters:**
  * **history_dir** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to history directory
  * **commit_sha** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Commit SHA (7 chars or full)
* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]
* **Returns:**
  Path to metrics file or None

### Example

```pycon
>>> metrics = find_metrics_by_commit(Path("history"), "700e012")
>>> print(metrics.name)
2025_11_14_22_45_00__700e012__0.1.0.json
```

### umpyre.storage.find_metrics_by_version(history_dir, version)

Find all metrics files for a specific PyPI version.

* **Parameters:**
  * **history_dir** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to history directory
  * **version** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – PyPI version string (e.g., “0.1.0”)
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]
* **Returns:**
  List of paths (sorted by timestamp, latest first)

### Example

```pycon
>>> metrics = find_metrics_by_version(Path("history"), "0.1.0")
>>> for m in metrics:
...     print(m.name)
2025_11_14_22_50_00__abc1234__0.1.0.json
2025_11_14_22_45_00__700e012__0.1.0.json
```

### umpyre.storage.get_all_versions(history_dir)

Get all unique PyPI versions found in metrics.

* **Parameters:**
  **history_dir** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to history directory
* **Return type:**
  [`list`](https://docs.python.org/3/builtins/stdtypes.html#list)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]
* **Returns:**
  Sorted list of versions (excluding ‘none’)

### Example

```pycon
>>> versions = get_all_versions(Path("history"))
>>> print(versions)
['0.1.0', '0.1.1', '0.2.0']
```

### umpyre.storage.get_latest_metric_for_version(history_dir, version)

Get the most recent metrics file for a version.

* **Parameters:**
  * **history_dir** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to history directory
  * **version** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – PyPI version string
* **Return type:**
  [`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]
* **Returns:**
  Path to latest metrics file or None

### Example

```pycon
>>> latest = get_latest_metric_for_version(Path("history"), "0.1.0")
>>> info = parse_metric_filename(latest.name)
>>> print(f"Latest 0.1.0 metrics from {info['timestamp_str']}")
```

### umpyre.storage.parse_metric_filename(filename)

Parse metric filename into components.

* **Parameters:**
  **filename** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Filename like “2025_11_14_22_45_00_\_700e012_\_0.1.0.json”
* **Returns:**
  {
  : “timestamp”: datetime object,
    “timestamp_str”: “2025-11-14T22:45:00”,
    “commit_sha”: “700e012”,
    “pypi_version”: “0.1.0” or None,
    “has_version”: bool,

  }
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### Example

```pycon
>>> info = parse_metric_filename("2025_11_14_22_45_00__700e012__0.1.0.json")
>>> info['commit_sha']
'700e012'
>>> info['pypi_version']
'0.1.0'
```

### umpyre.storage.serialize_metrics(data, output_path, format='json')

Serialize metrics to file.

* **Parameters:**
  * **data** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)) – Metric dictionary
  * **output_path** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to output file
  * **format** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Format (‘json’ or ‘csv’)

### Modules

| [`formats`](umpyre.storage.formats.html.md#module-umpyre.storage.formats)         | JSON and CSV serialization for metrics.                   |
|------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| [`git_branch`](umpyre.storage.git_branch.html.md#module-umpyre.storage.git_branch)   | Git branch-based storage operations.                      |
| [`query_utils`](umpyre.storage.query_utils.html.md#module-umpyre.storage.query_utils) | Helper utilities for working with umpyre metrics storage. |
