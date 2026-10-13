# umpyre

Umpyre - Code analysis and quality metrics tracking.

### Functions

| [`modules_info_gen`](#umpyre.modules_info_gen)(root[, filepath_filt, on_error])   | Yields statistics (as dicts) of modules under the root module or directory of a python package.   |
|------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| [`modules_info_df`](#umpyre.modules_info_df)(root[, filepath_filt, ...])         | A pandas DataFrame of stats of the root (package or directory thereof).                           |
| [`modules_info_df_stats`](#umpyre.modules_info_df_stats)(root[, filepath_filt, ...])   | A pandas Series of statistics over all modules of some root (package or directory thereof).       |
| [`stats_of`](#umpyre.stats_of)(modules[, filepath_filt, ...])             | A dataframe of stats of the input modules.                                                        |
| `get_objs`(root, k)                                                                                  |                                                                                                   |
| [`serialize_metrics`](#umpyre.serialize_metrics)(data, output_path[, format])      | Serialize metrics to file.                                                                        |
| [`deserialize_metrics`](#umpyre.deserialize_metrics)(file_path[, format])            | Deserialize metrics from file.                                                                    |

### Classes

| [`Config`](#umpyre.Config)([config_path, config_dict])             | Configuration manager for umpyre metrics collection.           |
|-------------------------------------------------------------------------------------------------|----------------------------------------------------------------|
| [`MetricSchema`](#umpyre.MetricSchema)([version])                        | Versioned schema for metrics storage with migration support.   |
| [`MetricCollector`](#umpyre.MetricCollector)()                              | Abstract base for metric collectors using Mapping interface.   |
| [`CollectorRegistry`](#umpyre.CollectorRegistry)()                            | Registry for managing available collectors.                    |
| [`UmpyreCollector`](#umpyre.UmpyreCollector)([root_path, exclude_dirs])     | Collect code statistics using AST parsing (no code execution). |
| [`WorkflowStatusCollector`](#umpyre.WorkflowStatusCollector)(repo[, token, ...])    | Collect GitHub workflow status using GitHub API.               |
| [`WilyCollector`](#umpyre.WilyCollector)([repo_path, max_revisions, ...]) | Collect complexity metrics using wily.                         |
| [`CoverageCollector`](#umpyre.CoverageCollector)([repo_path, source, ...])    | Collect test coverage metrics from coverage reports.           |
| [`GitBranchStorage`](#umpyre.GitBranchStorage)(repo_path[, remote, token])   | Store metrics in a separate git branch.                        |

### *class* umpyre.CollectorRegistry

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

### *class* umpyre.Config(config_path=None, config_dict=None)

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Configuration manager for umpyre metrics collection.

#### collector_config(collector_name)

Get configuration for a specific collector.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

#### *classmethod* from_dict(config)

Create config from dictionary.

* **Return type:**
  [`Config`](umpyre.config.html.md#umpyre.config.Config)

#### *classmethod* from_file(path)

Load config from YAML file.

* **Return type:**
  [`Config`](umpyre.config.html.md#umpyre.config.Config)

#### get(\*keys, default=None)

Get nested config value.

* **Parameters:**
  * **\*keys** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Nested keys (e.g., ‘collectors’, ‘wily’, ‘enabled’)
  * **default** ([`Any`](https://docs.python.org/3/library/typing.html#typing.Any)) – Default value if key not found
* **Return type:**
  [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)
* **Returns:**
  Config value or default

```pycon
>>> config = Config(config_dict={'collectors': {'wily': {'enabled': True}}})
>>> config.get('collectors', 'wily', 'enabled')
True
>>> config.get('collectors', 'missing', default='default_value')
'default_value'
```

#### is_collector_enabled(collector_name)

Check if a collector is enabled.

* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)

#### *property* retention_strategy *: [str](https://docs.python.org/3/builtins/stdtypes.html#str)*

Get data retention strategy.

#### *property* storage_branch *: [str](https://docs.python.org/3/builtins/stdtypes.html#str)*

Get the storage branch name.

#### *property* storage_formats *: [list](https://docs.python.org/3/builtins/stdtypes.html#list)[[str](https://docs.python.org/3/builtins/stdtypes.html#str)]*

Get enabled storage formats.

#### to_dict()

Export config as dictionary.

* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)

### *class* umpyre.CoverageCollector(repo_path=None, source='pytest-cov', coverage_file=None)

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

### *class* umpyre.GitBranchStorage(repo_path, remote='origin', , token=None)

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

### *class* umpyre.MetricCollector

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

### *class* umpyre.MetricSchema(version='1.0')

Bases: [`object`](https://docs.python.org/3/builtins/functions.html#object)

Versioned schema for metrics storage with migration support.

#### *classmethod* create_metric_data(commit_sha, metrics, commit_message=None, python_version=None, workflow_status=None, collection_duration=None)

Create a standardized metric data structure.

* **Parameters:**
  * **commit_sha** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Git commit SHA
  * **metrics** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)) – Dictionary of collected metrics
  * **commit_message** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional commit message
  * **python_version** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`str`](https://docs.python.org/3/builtins/stdtypes.html#str)]) – Optional Python version string
  * **workflow_status** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)]) – Optional workflow status dict
  * **collection_duration** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`float`](https://docs.python.org/3/builtins/functions.html#float)]) – Optional collection time in seconds
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  Standardized metric dictionary

#### *classmethod* current_version()

Return the current schema version.

* **Return type:**
  [`str`](https://docs.python.org/3/builtins/stdtypes.html#str)

#### *classmethod* migrate(data, from_version)

Migrate data from old schema version to current version.

* **Parameters:**
  * **data** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)) – Metric data in old format
  * **from_version** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Version of the input data
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  Migrated data in current schema format

#### *classmethod* validate(data)

Validate that data conforms to schema.

* **Parameters:**
  **data** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)) – Metric data to validate
* **Return type:**
  [`bool`](https://docs.python.org/3/builtins/functions.html#bool)
* **Returns:**
  True if valid, raises ValueError otherwise

### *class* umpyre.UmpyreCollector(root_path=None, exclude_dirs=None)

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

### *class* umpyre.WilyCollector(repo_path=None, max_revisions=5, operators=None)

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

### *class* umpyre.WorkflowStatusCollector(repo, token=None, lookback_runs=10, workflow_name=None)

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

### umpyre.deserialize_metrics(file_path, format='json')

Deserialize metrics from file.

* **Parameters:**
  * **file_path** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to input file
  * **format** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Format (‘json’ or ‘csv’)
* **Return type:**
  [`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)
* **Returns:**
  Metric dictionary

### umpyre.modules_info_df(root, filepath_filt=<function <lambda>>, index_field=None, on_error='ignore')

A pandas DataFrame of stats of the root (package or directory thereof).

* **Parameters:**
  * **root** – module or directory path
  * **filepath_filt** – filepath filter function or regular expression
  * **index_field** – function or field string that should be used for the indexing of modules
  * **on_error** – What to do when an error occurs when extracting information from a module.
    Values are ‘ignore’, ‘print’, or ‘raise’
* **Returns:**
  A DataFrame whose rows contain information for each module

```pycon
>>> import urllib
>>> df = modules_info_df(urllib)
>>> df
                    lines  empty_lines  ...  num_of_functions  num_of_classes
urllib.error           78           18  ...                 0               3
urllib.request       2774          410  ...                23              28
urllib.__init__         1            1  ...                 0               0
urllib.response        81           24  ...                 0               4
urllib.robotparser    274           36  ...                 0               4
urllib.parse         1166          199  ...                46              16

[6 rows x 7 columns]
```

### umpyre.modules_info_df_stats(root, filepath_filt=<function <lambda>>, index_field=None, on_error='ignore')

A pandas Series of statistics over all modules of some root (package or directory thereof).

* **Parameters:**
  * **root** – module or directory path
  * **filepath_filt** – filepath filter function or regular expression
  * **index_field** – function or field string that should be used for the indexing of modules
  * **on_error** – What to do when an error occurs when extracting information from a module.
    Values are ‘ignore’, ‘print’, or ‘raise’
* **Returns:**
  A Series whose rows containing statistics

```pycon
>>> import json
>>> df = modules_info_df_stats(json)
>>> df
lines                      1301.000000
empty_lines                 178.000000
comment_lines                50.000000
docs_lines                  218.000000
function_lines              585.000000
num_of_functions             14.000000
num_of_classes                3.000000
empty_lines_ratio             0.136818
comment_lines_ratio           0.038432
function_lines_ratio          0.449654
mean_lines_per_function      41.785714
dtype: float64
>>> modules_info_df_stats('collections.abc')
lines                      1276.000000
empty_lines                 190.000000
comment_lines                73.000000
docs_lines                  133.000000
function_lines              138.000000
num_of_functions              1.000000
num_of_classes               34.000000
empty_lines_ratio             0.148903
comment_lines_ratio           0.057210
function_lines_ratio          0.108150
mean_lines_per_function     138.000000
dtype: float64
```

### umpyre.modules_info_gen(root, filepath_filt=<function <lambda>>, on_error='ignore')

Yields statistics (as dicts) of modules under the root module or directory of a python package.

* **Parameters:**
  * **root** – module instance, dot path, or directory path
  * **filepath_filt** – filepath filter function or regular expression
  * **on_error** – What to do when an error occurs when extracting information from a module.
    Values are ‘ignore’, ‘print’, ‘raise’, or ‘yield’
* **Returns:**
  A generator of dicts

### umpyre.serialize_metrics(data, output_path, format='json')

Serialize metrics to file.

* **Parameters:**
  * **data** ([`dict`](https://docs.python.org/3/builtins/stdtypes.html#dict)) – Metric dictionary
  * **output_path** ([`Path`](https://docs.python.org/3/library/pathlib.html#pathlib.Path)) – Path to output file
  * **format** ([`str`](https://docs.python.org/3/builtins/stdtypes.html#str)) – Format (‘json’ or ‘csv’)

### umpyre.stats_of(modules, filepath_filt=<function <lambda>>, index_field=None, on_error='ignore')

A dataframe of stats of the input modules.

* **Parameters:**
  * **modules** – list of importable names
  * **root** – module or directory path
  * **filepath_filt** – filepath filter function or regular expression
  * **index_field** – function or field string that should be used for the indexing of modules
  * **on_error** – What to do when an error occurs when extracting information from a module.
    Values are ‘ignore’, ‘print’, or ‘raise’
* **Returns:**

```pycon
>>> df = stats_of(['urllib', 'json', 'collections'])
>>> assert set(df.index.values).issuperset(
...     {'empty_lines_ratio', 'comment_lines_ratio', 'function_lines_ratio', 'mean_lines_per_function'})
>>> stats_of(['urllib', 'json', 'collections'])
                              urllib         json  collections
empty_lines_ratio           0.157293     0.136503     0.148090
comment_lines_ratio         0.075217     0.038344     0.061574
function_lines_ratio        0.212391     0.448620     0.107560
mean_lines_per_function    13.463768    41.785714   138.000000
lines                    4374.000000  1304.000000  1283.000000
empty_lines               688.000000   178.000000   190.000000
comment_lines             329.000000    50.000000    79.000000
docs_lines                425.000000   218.000000   133.000000
function_lines            929.000000   585.000000   138.000000
num_of_functions           69.000000    14.000000     1.000000
num_of_classes             55.000000     3.000000    34.000000
```

### Modules

| [`cli`](umpyre.cli.html.md#module-umpyre.cli)                             | Command-line interface for umpyre.                          |
|----------------------------------------------------------------------------------------------------|-------------------------------------------------------------|
| [`collectors`](umpyre.collectors.html.md#module-umpyre.collectors)               | Collectors package - metric collection implementations.     |
| [`config`](umpyre.config.html.md#module-umpyre.config)                       | Configuration loading and validation for umpyre.            |
| [`python_code_stats`](umpyre.python_code_stats.html.md#module-umpyre.python_code_stats) | Get stats about packages.                                   |
| [`schema`](umpyre.schema.html.md#module-umpyre.schema)                       | Versioned schema for metrics storage and migration support. |
| [`storage`](umpyre.storage.html.md#module-umpyre.storage)                     | Storage operations for metrics.                             |
