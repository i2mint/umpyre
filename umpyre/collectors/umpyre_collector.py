"""Collector using existing umpyre python_code_stats module."""

import os
from pathlib import Path
from typing import Optional

from umpyre.collectors.base import MetricCollector, registry
from umpyre.python_code_stats import modules_info_df_stats


class UmpyreCollector(MetricCollector):
    """
    Collect code statistics using umpyre's python_code_stats module.

    Provides metrics like:
    - Number of functions and classes
    - Lines of code (total, empty, comments, docs)
    - Code ratios (comment/empty/function lines)
    - Mean lines per function

    Example:
        >>> import tempfile
        >>> import os
        >>> # Create a simple Python file for testing
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     test_file = Path(tmpdir) / "test.py"
        ...     test_file.write_text('''
        ... def hello():
        ...     \"\"\"Say hello.\"\"\"
        ...     return "hello"
        ... ''')
        ...     collector = UmpyreCollector(tmpdir)
        ...     metrics = collector.collect()
        ...     'num_functions' in metrics
        True
    """

    def __init__(
        self, root_path: Optional[str] = None, exclude_dirs: Optional[list[str]] = None
    ):
        """
        Initialize collector.

        Args:
            root_path: Root directory to analyze (defaults to current directory)
            exclude_dirs: List of directory names to exclude (e.g., ['tests', 'examples'])
        """
        super().__init__()
        self.root_path = root_path or os.getcwd()
        self.exclude_dirs = exclude_dirs or []

    def collect(self) -> dict:
        """
        Collect code statistics from root directory.

        Returns:
            Dictionary with metrics:
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
        """

        # Build filepath filter
        def filepath_filt(path: str) -> bool:
            """Filter out excluded directories."""
            if not path.endswith('.py'):
                return False

            path_parts = Path(path).parts
            for exclude_dir in self.exclude_dirs:
                if exclude_dir in path_parts:
                    return False

            return True

        try:
            stats = modules_info_df_stats(
                self.root_path, filepath_filt=filepath_filt, on_error='ignore'
            )

            # Convert pandas Series to dict with standardized names
            return {
                "num_functions": int(stats.get('num_of_functions', 0)),
                "num_classes": int(stats.get('num_of_classes', 0)),
                "total_lines": int(stats.get('lines', 0)),
                "empty_lines": int(stats.get('empty_lines', 0)),
                "comment_lines": int(stats.get('comment_lines', 0)),
                "docs_lines": int(stats.get('docs_lines', 0)),
                "function_lines": int(stats.get('function_lines', 0)),
                "empty_lines_ratio": float(stats.get('empty_lines_ratio', 0)),
                "comment_lines_ratio": float(stats.get('comment_lines_ratio', 0)),
                "function_lines_ratio": float(stats.get('function_lines_ratio', 0)),
                "mean_lines_per_function": float(
                    stats.get('mean_lines_per_function', 0)
                ),
            }
        except Exception as e:
            # Return empty metrics on error
            return {
                "num_functions": 0,
                "num_classes": 0,
                "total_lines": 0,
                "empty_lines": 0,
                "comment_lines": 0,
                "docs_lines": 0,
                "function_lines": 0,
                "empty_lines_ratio": 0.0,
                "comment_lines_ratio": 0.0,
                "function_lines_ratio": 0.0,
                "mean_lines_per_function": 0.0,
                "error": str(e),
            }


# Register collector
registry.register("umpyre_stats", UmpyreCollector)
