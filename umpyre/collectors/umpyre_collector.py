"""Collector using AST-based code analysis (safe, no code execution)."""

import os
import ast
from pathlib import Path
from typing import Optional

from umpyre.collectors.base import MetricCollector, registry


class UmpyreCollector(MetricCollector):
    """
    Collect code statistics using AST parsing (no code execution).

    Provides metrics like:
    - Number of functions and classes
    - Lines of code (total, empty, comments, docs)
    - Code ratios (comment/empty/function lines)
    - Mean lines per function

    Uses AST parsing instead of dynamic imports for safety.

    Example:
        >>> import tempfile
        >>> from pathlib import Path
        >>> # Create a simple Python file for testing
        >>> with tempfile.TemporaryDirectory() as tmpdir:
        ...     test_file = Path(tmpdir) / "test.py"
        ...     test_file.write_text('''def hello():
        ...     \"\"\"Say hello.\"\"\"
        ...     return "hello"
        ...
        ... class Greeter:
        ...     \"\"\"A greeter.\"\"\"
        ...     pass
        ... ''')  # doctest: +SKIP
        ...     collector = UmpyreCollector(tmpdir)
        ...     metrics = collector.collect()
        ...     metrics['num_functions'] >= 1 and metrics['num_classes'] >= 1
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

    def _analyze_file(self, filepath: Path) -> dict:
        """
        Analyze a single Python file using AST (no code execution).

        Args:
            filepath: Path to Python file

        Returns:
            Dictionary with file metrics
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            tree = ast.parse(content, filename=str(filepath))

            # Count functions and classes
            num_functions = 0
            num_classes = 0
            function_lines = 0
            docs_lines = 0

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    num_functions += 1
                    # Count lines in function (end_lineno - lineno)
                    if hasattr(node, 'end_lineno') and node.end_lineno:
                        function_lines += node.end_lineno - node.lineno + 1
                    # Extract docstring lines
                    docstring = ast.get_docstring(node)
                    if docstring:
                        docs_lines += len(docstring.split('\n'))

                elif isinstance(node, ast.ClassDef):
                    num_classes += 1
                    # Extract class docstring
                    docstring = ast.get_docstring(node)
                    if docstring:
                        docs_lines += len(docstring.split('\n'))

            # Count empty and comment lines
            empty_lines = sum(1 for line in lines if not line.strip())
            comment_lines = sum(1 for line in lines if line.strip().startswith('#'))

            return {
                'num_functions': num_functions,
                'num_classes': num_classes,
                'total_lines': len(lines),
                'empty_lines': empty_lines,
                'comment_lines': comment_lines,
                'docs_lines': docs_lines,
                'function_lines': function_lines,
            }

        except Exception as e:
            # Return zeros on error but track the file
            return {
                'num_functions': 0,
                'num_classes': 0,
                'total_lines': 0,
                'empty_lines': 0,
                'comment_lines': 0,
                'docs_lines': 0,
                'function_lines': 0,
                'error': str(e),
            }

    def _should_analyze(self, filepath: Path) -> bool:
        """Check if file should be analyzed."""
        if not filepath.suffix == '.py':
            return False

        # Check exclude directories
        for exclude_dir in self.exclude_dirs:
            if exclude_dir in filepath.parts:
                return False

        return True

    def collect(self) -> dict:
        """
        Collect code statistics from root directory using AST parsing.

        Returns:
            Dictionary with aggregated metrics:
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
        """
        root = Path(self.root_path)

        # Aggregate metrics across all files
        total_metrics = {
            'num_functions': 0,
            'num_classes': 0,
            'total_lines': 0,
            'empty_lines': 0,
            'comment_lines': 0,
            'docs_lines': 0,
            'function_lines': 0,
        }

        files_analyzed = 0
        errors = []

        try:
            # Walk through all Python files
            for filepath in root.rglob('*.py'):
                if not self._should_analyze(filepath):
                    continue

                file_metrics = self._analyze_file(filepath)

                if 'error' in file_metrics:
                    errors.append(f"{filepath.name}: {file_metrics['error']}")
                    continue

                files_analyzed += 1

                # Aggregate
                for key in total_metrics:
                    total_metrics[key] += file_metrics.get(key, 0)

            # Calculate ratios
            total_lines = total_metrics['total_lines']

            result = {
                **total_metrics,
                'empty_lines_ratio': (
                    total_metrics['empty_lines'] / total_lines
                    if total_lines > 0
                    else 0.0
                ),
                'comment_lines_ratio': (
                    total_metrics['comment_lines'] / total_lines
                    if total_lines > 0
                    else 0.0
                ),
                'function_lines_ratio': (
                    total_metrics['function_lines'] / total_lines
                    if total_lines > 0
                    else 0.0
                ),
                'mean_lines_per_function': (
                    total_metrics['function_lines'] / total_metrics['num_functions']
                    if total_metrics['num_functions'] > 0
                    else 0.0
                ),
                'files_analyzed': files_analyzed,
            }

            if errors:
                result['errors'] = errors[:10]  # Keep first 10 errors
                result['total_errors'] = len(errors)

            return result

        except Exception as e:
            # Return empty metrics on catastrophic error
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
                "files_analyzed": 0,
                "error": str(e),
            }


# Register collector
registry.register("umpyre_stats", UmpyreCollector)
