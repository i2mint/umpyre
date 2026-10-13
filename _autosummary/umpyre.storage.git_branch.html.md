# umpyre.storage.git_branch

Git branch-based storage operations.

### Classes

| [`GitBranchStorage`](#umpyre.storage.git_branch.GitBranchStorage)(repo_path[, remote, token])   | Store metrics in a separate git branch.   |
|-------------------------------------------------------------------------------------------------|-------------------------------------------|

### Exceptions

| [`GitBranchStorageError`](#umpyre.storage.git_branch.GitBranchStorageError)   | Raised when git branch storage operations fail.   |
|--------------------------------------------------------------------------|---------------------------------------------------|

### *class* umpyre.storage.git_branch.GitBranchStorage(repo_path, remote='origin', , token=None)

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

### *exception* umpyre.storage.git_branch.GitBranchStorageError

Bases: [`Exception`](https://docs.python.org/3/builtins/exceptions.html#Exception)

Raised when git branch storage operations fail.
