"""GitBranchStorage pushes to the repository's real remote, not to the local workspace (umpyre#8)."""

import os
import subprocess

import pytest

from umpyre.storage.git_branch import GitBranchStorage


def _git(*args, cwd):
    return subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=True
    ).stdout.strip()


@pytest.fixture
def workspace(tmp_path):
    """A workspace whose ``origin`` is a bare repo standing in for GitHub."""
    remote = tmp_path / "remote.git"
    work = tmp_path / "work"
    _git("init", "--bare", "-q", str(remote), cwd=tmp_path)
    _git("init", "-q", str(work), cwd=tmp_path)
    for k, v in (("user.name", "t"), ("user.email", "t@t")):
        _git("config", k, v, cwd=work)
    (work / "a.txt").write_text("a")
    _git("add", ".", cwd=work)
    _git("commit", "-qm", "init", cwd=work)
    _git("remote", "add", "origin", str(remote), cwd=work)
    return work, remote


def test_metrics_land_on_the_remote_and_accumulate(workspace):
    work, remote = workspace
    storage = GitBranchStorage(str(work))
    storage.store_metrics({"metrics": {"n": 1}}, "a" * 40, branch="code-metrics")
    # on the (bare) remote, not merely in the local workspace
    assert _git("rev-parse", "--verify", "code-metrics", cwd=remote)
    storage.store_metrics({"metrics": {"n": 2}}, "b" * 40, branch="code-metrics")
    log = _git("log", "--format=%s", "code-metrics", cwd=remote).splitlines()
    assert log == [f"Update metrics for {'b' * 7}", f"Update metrics for {'a' * 7}"]


def test_token_becomes_a_host_scoped_auth_header_not_a_url(monkeypatch):
    monkeypatch.delenv("GIT_CONFIG_COUNT", raising=False)
    monkeypatch.delenv("GITHUB_SERVER_URL", raising=False)
    storage = GitBranchStorage.__new__(GitBranchStorage)
    storage.token = "s3cret"
    env = storage._git_env("https://user@github.com/org/repo.git")
    assert int(env["GIT_CONFIG_COUNT"]) == 2
    key = "http.https://github.com/.extraheader"
    assert [env["GIT_CONFIG_KEY_0"], env["GIT_CONFIG_KEY_1"]] == [key, key]
    # an empty header first clears the one actions/checkout leaves in the config
    assert env["GIT_CONFIG_VALUE_0"] == ""
    assert env["GIT_CONFIG_VALUE_1"].startswith("AUTHORIZATION: basic ")
    assert "s3cret" not in env["GIT_CONFIG_VALUE_1"]  # base64, not plain


def test_token_header_appends_to_existing_git_config_env(monkeypatch):
    monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
    monkeypatch.delenv("GITHUB_SERVER_URL", raising=False)
    storage = GitBranchStorage.__new__(GitBranchStorage)
    storage.token = "t"
    env = storage._git_env("https://github.com/o/r")
    assert env["GIT_CONFIG_COUNT"] == "3" and "GIT_CONFIG_KEY_2" in env


def test_no_header_without_token_for_local_ssh_or_foreign_hosts(monkeypatch):
    monkeypatch.delenv("GITHUB_SERVER_URL", raising=False)
    storage = GitBranchStorage.__new__(GitBranchStorage)
    storage.token = "t"
    for url in ("/some/local/path", "git@github.com:o/r.git", None):
        assert storage._git_env(url) == dict(os.environ)
    monkeypatch.setenv("GITHUB_SERVER_URL", "https://github.com")
    assert storage._git_env("https://evil.example/o/r") == dict(os.environ)
    storage.token = None
    assert storage._git_env("https://github.com/o/r") == dict(os.environ)
