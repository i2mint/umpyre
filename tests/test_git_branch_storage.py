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


def test_without_an_actions_server_the_token_goes_only_to_github(monkeypatch):
    monkeypatch.delenv("GITHUB_SERVER_URL", raising=False)
    monkeypatch.delenv("GIT_CONFIG_COUNT", raising=False)
    storage = GitBranchStorage.__new__(GitBranchStorage)
    storage.token = "t"
    for url in (
        "https://gitlab.com/o/r.git",
        "https://github.com.evil.test/o/r",
        "http://github.com/o/r",  # never in cleartext
    ):
        assert storage._git_env(url) == dict(os.environ)
    assert "GIT_CONFIG_COUNT" in storage._git_env("https://github.com/o/r")


def test_host_case_and_the_default_port_do_not_matter(monkeypatch):
    monkeypatch.setenv("GITHUB_SERVER_URL", "https://github.com")
    monkeypatch.delenv("GIT_CONFIG_COUNT", raising=False)
    storage = GitBranchStorage.__new__(GitBranchStorage)
    storage.token = "t"
    for url in ("https://GitHub.com/o/r", "https://github.com:443/o/r"):
        assert "GIT_CONFIG_COUNT" in storage._git_env(url), url
    for url in ("https://github.com:8443/o/r", "", None):
        assert storage._git_env(url) == dict(os.environ), url


# --- hardening follow-ups (umpyre#9) ---------------------------------------------


def test_a_diverged_local_branch_yields_to_the_remote(workspace):
    work, remote = workspace
    storage = GitBranchStorage(str(work))
    storage.store_metrics({"metrics": {"n": 1}}, "a" * 40)
    _git("fetch", "origin", "code-metrics:code-metrics", cwd=work)
    # a local-only commit on the metrics branch makes the plain fetch non-fast-forward
    _git("checkout", "-q", "code-metrics", cwd=work)
    (work / "local.txt").write_text("x")
    _git("add", ".", cwd=work)
    _git("commit", "-qm", "local only", cwd=work)
    _git("checkout", "-q", "-", cwd=work)
    storage.store_metrics({"metrics": {"n": 2}}, "b" * 40)
    log = _git("log", "--format=%s", "code-metrics", cwd=remote).splitlines()
    assert log == [f"Update metrics for {'b' * 7}", f"Update metrics for {'a' * 7}"]


def test_an_unreachable_remote_does_not_orphan_a_branch(workspace, tmp_path):
    from umpyre.storage import GitBranchStorageError

    work, remote = workspace
    _git("remote", "set-url", "origin", str(tmp_path / "nowhere.git"), cwd=work)
    with pytest.raises(GitBranchStorageError):
        GitBranchStorage(str(work)).store_metrics({"metrics": {}}, "a" * 40)
    assert subprocess.run(
        ["git", "rev-parse", "--verify", "code-metrics"], cwd=work, capture_output=True
    ).returncode != 0


def test_a_separate_push_url_is_pushed_to(workspace, tmp_path):
    work, remote = workspace
    push_remote = tmp_path / "push.git"
    _git("clone", "-q", "--bare", str(remote), str(push_remote), cwd=tmp_path)
    _git("remote", "set-url", "--push", "origin", str(push_remote), cwd=work)
    GitBranchStorage(str(work)).store_metrics({"metrics": {}}, "a" * 40)
    assert _git("rev-parse", "--verify", "code-metrics", cwd=push_remote)
    assert subprocess.run(
        ["git", "rev-parse", "--verify", "code-metrics"], cwd=remote, capture_output=True
    ).returncode != 0


@pytest.mark.parametrize("count", ["abc", "", "-3", "1.5"])
def test_a_non_numeric_git_config_count_does_not_crash(monkeypatch, count):
    monkeypatch.setenv("GIT_CONFIG_COUNT", count)
    monkeypatch.delenv("GITHUB_SERVER_URL", raising=False)
    storage = GitBranchStorage.__new__(GitBranchStorage)  # no repo needed
    storage.token = "t"
    out = storage._git_env("https://github.com/o/r")
    assert int(out["GIT_CONFIG_COUNT"]) >= 2
