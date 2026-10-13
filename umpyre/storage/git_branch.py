"""Git branch-based storage operations."""

import base64
import os
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlsplit

from umpyre.storage.formats import serialize_metrics


# Where a token is sent when GITHUB_SERVER_URL does not say (a local run).
DEFAULT_GITHUB_SERVER = "https://github.com"


def _origin(parts) -> tuple:
    """(scheme, host, port) of a split URL, host lower-cased and the default port filled in."""
    try:
        port = parts.port
    except ValueError:
        return (None, None, None)
    default = {"https": 443, "http": 80}.get(parts.scheme)
    return (parts.scheme, (parts.hostname or "").lower() or None, port or default)


class GitBranchStorage:
    """
    Store metrics in a separate git branch.

    This provides versioned, branch-based storage without polluting
    the main branch or requiring external artifacts.

    Example:
        >>> storage = GitBranchStorage(repo_path="/path/to/repo")  #doctest: +SKIP
        >>> metrics = {"lines": 100, "functions": 10}  #doctest: +SKIP
        >>> storage.store_metrics(metrics, "abc123", branch="code-metrics")  #doctest: +SKIP
    """

    def __init__(
        self, repo_path: str, remote: str = "origin", *, token: Optional[str] = None
    ):
        """
        Initialize storage.

        Metrics are pushed to the URL of ``remote`` in ``repo_path`` (e.g. GitHub),
        not to ``repo_path`` itself. A separate ``remote.<name>.pushurl`` is honoured
        for the push; as in git, it must name the same repository as the fetch URL.

        Args:
            repo_path: Path to git repository
            remote: Git remote name
            token: Access token used (as an HTTP auth header scoped to the remote's
                host, never written to a URL or config) to push to an https remote.
                Without it, the push uses whatever credentials git already has.
        """
        self.repo_path = Path(repo_path)
        self.remote = remote
        self.token = token

        if not (self.repo_path / ".git").exists():
            raise ValueError(f"Not a git repository: {repo_path}")

    def store_metrics(
        self,
        metrics: dict,
        commit_sha: str,
        branch: str = "code-metrics",
        formats: Optional[list[str]] = None,
    ):
        """
        Store metrics to git branch.

        Args:
            metrics: Metric dictionary to store
            commit_sha: Git commit SHA
            branch: Target branch name
            formats: List of formats ('json', 'csv')
        """
        formats = formats or ["json", "csv"]

        # Create temporary directory for branch checkout
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Fetch and checkout metrics branch
            source_ref = self._fetch_branch(branch)
            self._checkout_branch(branch, tmpdir, source_ref=source_ref)

            # Create history directory (flat structure)
            history_dir = tmpdir / "history"
            history_dir.mkdir(exist_ok=True)

            # Build filename: YYYY_MM_DD_HH_MM_SS__shahash__version.json
            timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            commit_short = commit_sha[:7]

            # Extract pypi_version if available (use 'none' if not found)
            pypi_version = (
                metrics.get("metrics", {}).get("umpyre_stats", {}).get("pypi_version")
                or "none"
            )

            # Filename format: timestamp__sha__version (parseable, chronological)
            filename_base = f"{timestamp}__{commit_short}__{pypi_version}"

            for fmt in formats:
                if fmt == "json":
                    # Latest snapshot
                    serialize_metrics(metrics, tmpdir / "metrics.json", format="json")

                    # Historical record (flat structure, parseable filename)
                    history_file = history_dir / f"{filename_base}.json"
                    serialize_metrics(metrics, history_file, format="json")

                elif fmt == "csv":
                    serialize_metrics(metrics, tmpdir / "metrics.csv", format="csv")

            # Commit and push (to the real remote, not to the local workspace)
            self._commit_and_push(tmpdir, branch, commit_sha)

    def _remote_url(self, *, push: bool = False) -> Optional[str]:
        """URL of the real remote of ``repo_path`` (the one pushed to when ``push``,
        which ``remote.<name>.pushurl`` may make differ), or ``None`` if it has none."""
        result = subprocess.run(
            ["git", "remote", "get-url", *(["--push"] if push else []), self.remote],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip() or None if result.returncode == 0 else None

    def _git_env(self, url: Optional[str]) -> dict:
        """Environment for git commands that talk to the remote (auth header, if any)."""
        env = dict(os.environ)
        parts = urlsplit(url or "")
        # The token goes to the GitHub it was issued by, over the scheme that server
        # uses, and nowhere else: the Actions server when there is one, else github.com.
        server = urlsplit(env.get("GITHUB_SERVER_URL") or DEFAULT_GITHUB_SERVER)
        origin = _origin(parts)
        if self.token and origin[1] and origin == _origin(server):
            env["GIT_TERMINAL_PROMPT"] = "0"  # fail, don't wait for a password
            key = (
                f"http.{parts.scheme}://{parts.netloc.rsplit('@', 1)[-1]}/.extraheader"
            )
            credentials = base64.b64encode(f"x-access-token:{self.token}".encode())
            try:
                n = max(int(env.get("GIT_CONFIG_COUNT") or 0), 0)
            except ValueError:  # git would refuse it anyway; ours replaces it
                n = 0
            # actions/checkout leaves its own Authorization header in the repo config,
            # and GitHub rejects two (HTTP 400): an empty value clears earlier ones.
            for i, value in enumerate(
                ("", f"AUTHORIZATION: basic {credentials.decode()}")
            ):
                env[f"GIT_CONFIG_KEY_{n + i}"] = key
                env[f"GIT_CONFIG_VALUE_{n + i}"] = value
            env["GIT_CONFIG_COUNT"] = str(n + 2)
        return env

    def _fetch_branch(self, branch: str) -> Optional[str]:
        """Fetch the metrics branch from the remote into its remote-tracking ref.

        Returns that ref (the remote's branch is the truth, and a local branch that is
        checked out or has diverged does not get in the way), or ``None`` when the
        remote has no such branch. If the fetch fails and the remote may have the
        branch (or cannot be asked), this raises rather than orphan a branch the
        remote would then reject on every later run.
        """
        url = self._remote_url()
        env = self._git_env(url)
        tracking_ref = f"refs/remotes/{self.remote}/{branch}"
        try:
            result = subprocess.run(
                ["git", "fetch", self.remote, f"+refs/heads/{branch}:{tracking_ref}"],
                cwd=self.repo_path,
                capture_output=True,
                check=False,  # May not exist yet
                timeout=30,
                env=env,
            )
            if result.returncode == 0:
                return tracking_ref
        except subprocess.TimeoutExpired:
            pass
        if url and not self._remote_lacks_branch(branch, env):
            raise GitBranchStorageError(
                f"Could not fetch the metrics branch {branch!r} from the remote "
                f"{self.remote!r}, and it may exist there; not creating it from "
                "scratch. Check the remote and the credentials."
            )
        return None

    def _remote_lacks_branch(self, branch: str, env: dict) -> bool:
        """Whether the remote answered, and has no branch ``branch``."""
        try:
            result = subprocess.run(
                # the full ref: a bare name also matches refs/heads/any/prefix/branch
                [
                    "git",
                    "ls-remote",
                    "--exit-code",
                    self.remote,
                    f"refs/heads/{branch}",
                ],
                cwd=self.repo_path,
                capture_output=True,
                check=False,
                timeout=30,
                env=env,
            )
        except subprocess.TimeoutExpired:
            return False
        return result.returncode == 2  # 2: reachable, no matching ref

    def _checkout_branch(
        self, branch: str, target_dir: Path, *, source_ref: Optional[str] = None
    ):
        """Check the metrics branch out into ``target_dir``: from ``source_ref`` (the
        freshly fetched remote branch), else from a local branch of that name, else as
        a new orphan branch."""

        def git(*args, cwd=target_dir):
            return subprocess.run(
                ["git", *args], cwd=cwd, capture_output=True, check=False, timeout=60
            )

        if source_ref is None:
            local = git(
                "rev-parse", "--verify", f"refs/heads/{branch}", cwd=self.repo_path
            )
            source_ref = f"refs/heads/{branch}" if local.returncode == 0 else None
        subprocess.run(
            ["git", "init", "-q"], cwd=target_dir, capture_output=True, check=True
        )
        # as in a clone, `origin` is the local workspace (until pointed at the real one)
        git("remote", "add", "origin", str(self.repo_path))
        if source_ref is None:
            # a new, history-less branch
            git("symbolic-ref", "HEAD", f"refs/heads/{branch}")
            return
        for args in (
            ("fetch", "-q", str(self.repo_path), f"+{source_ref}:refs/heads/{branch}"),
            ("checkout", "-q", branch),
        ):
            result = git(*args)
            if result.returncode != 0:
                raise GitBranchStorageError(
                    f"git {args[0]} failed: {result.stderr.decode(errors='replace')}"
                )

    def _commit_and_push(self, work_dir: Path, branch: str, commit_sha: str):
        """Commit changes and push to remote."""
        # The clone's origin is the local workspace; point it at the real remote.
        remote_url = self._remote_url()
        push_url = self._remote_url(push=True)
        if remote_url:
            subprocess.run(
                ["git", "remote", "set-url", "origin", remote_url],
                cwd=work_dir,
                capture_output=True,
                check=True,
            )
        if push_url and push_url != remote_url:  # a separate remote.<name>.pushurl
            subprocess.run(
                ["git", "remote", "set-url", "--push", "origin", push_url],
                cwd=work_dir,
                capture_output=True,
                check=True,
            )
        env = self._git_env(remote_url)  # fetch/pull
        push_env = self._git_env(push_url)

        # Configure git
        subprocess.run(
            ["git", "config", "user.name", "umpyre-bot"],
            cwd=work_dir,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "umpyre@automated"],
            cwd=work_dir,
            capture_output=True,
            check=True,
        )

        # Add all files
        subprocess.run(
            ["git", "add", "."],
            cwd=work_dir,
            capture_output=True,
            check=True,
        )

        # Check if there are changes
        result = subprocess.run(
            ["git", "diff", "--cached", "--quiet"],
            cwd=work_dir,
            capture_output=True,
            check=False,
        )

        if result.returncode != 0:
            # There are changes - commit them
            commit_message = f"Update metrics for {commit_sha[:7]}"
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=work_dir,
                capture_output=True,
                check=True,
            )

            # Push with retries
            for attempt in range(3):
                try:
                    subprocess.run(
                        ["git", "push", "origin", branch],
                        cwd=work_dir,
                        capture_output=True,
                        check=True,
                        timeout=60,
                        env=push_env,
                    )
                    break
                except subprocess.CalledProcessError:
                    if attempt < 2:
                        # Pull and try again
                        subprocess.run(
                            ["git", "pull", "--rebase", "origin", branch],
                            cwd=work_dir,
                            capture_output=True,
                            check=False,
                            timeout=60,
                            env=env,
                        )
                    else:
                        raise


class GitBranchStorageError(Exception):
    """Raised when git branch storage operations fail."""
