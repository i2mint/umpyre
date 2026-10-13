# umpyre.collectors.umpyre_collector

Collector using AST-based code analysis (safe, no code execution).

### Classes

| [`UmpyreCollector`](#umpyre.collectors.umpyre_collector.UmpyreCollector)([root_path, exclude_dirs])   | Collect code statistics using AST parsing (no code execution).   |
|-----------------------------------------------------------------------------------------------|------------------------------------------------------------------|

### *class* umpyre.collectors.umpyre_collector.UmpyreCollector(root_path=None, exclude_dirs=None)

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
