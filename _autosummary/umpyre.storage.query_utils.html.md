# umpyre.storage.query_utils

Helper utilities for working with umpyre metrics storage.

### Functions

| [`filter_by_date_range`](#umpyre.storage.query_utils.filter_by_date_range)(history_dir[, ...])        | Get metrics files within a date range.              |
|--------------------------------------------------------------------------------------------------|-----------------------------------------------------|
| [`find_metrics_by_commit`](#umpyre.storage.query_utils.find_metrics_by_commit)(history_dir, commit_sha) | Find metrics file for a specific commit.            |
| [`find_metrics_by_version`](#umpyre.storage.query_utils.find_metrics_by_version)(history_dir, version)   | Find all metrics files for a specific PyPI version. |
| [`get_all_versions`](#umpyre.storage.query_utils.get_all_versions)(history_dir)                   | Get all unique PyPI versions found in metrics.      |
| [`get_latest_metric_for_version`](#umpyre.storage.query_utils.get_latest_metric_for_version)(history_dir, ...) | Get the most recent metrics file for a version.     |
| [`parse_metric_filename`](#umpyre.storage.query_utils.parse_metric_filename)(filename)                 | Parse metric filename into components.              |

### umpyre.storage.query_utils.filter_by_date_range(history_dir, start_date=None, end_date=None)

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

### umpyre.storage.query_utils.find_metrics_by_commit(history_dir, commit_sha)

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

### umpyre.storage.query_utils.find_metrics_by_version(history_dir, version)

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

### umpyre.storage.query_utils.get_all_versions(history_dir)

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

### umpyre.storage.query_utils.get_latest_metric_for_version(history_dir, version)

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

### umpyre.storage.query_utils.parse_metric_filename(filename)

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
