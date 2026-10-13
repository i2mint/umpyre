"""``umpyre collect`` end to end: metrics land on the remote's branch, chosen by flag or config."""

import os
import subprocess
import sys

import pytest


def _git(*args, cwd):
    return subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=True
    ).stdout.strip()


@pytest.fixture
def workspace(tmp_path):
    remote = tmp_path / "remote.git"
    work = tmp_path / "work"
    _git("init", "--bare", "-q", str(remote), cwd=tmp_path)
    _git("init", "-q", str(work), cwd=tmp_path)
    for k, v in (("user.name", "t"), ("user.email", "t@t")):
        _git("config", k, v, cwd=work)
    (work / "m.py").write_text("def f():\n    return 1\n")
    _git("add", ".", cwd=work)
    _git("commit", "-qm", "init", cwd=work)
    _git("remote", "add", "origin", str(remote), cwd=work)
    return work, remote


def _collect(work, *args):
    env = {k: v for k, v in os.environ.items() if k not in ("CI", "GITHUB_ACTIONS")}
    env["PYTHONPATH"] = os.pathsep.join(sys.path)
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "umpyre.cli",
            "collect",
            "--repo-path",
            str(work),
            *args,
        ],
        cwd=work,
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=300,
    )


def test_collect_stores_on_the_branch_the_flag_names(workspace):
    work, remote = workspace
    r = _collect(work, "--storage-branch", "my-metrics")
    assert r.returncode == 0, r.stderr
    assert "Metrics stored to branch 'my-metrics'" in r.stdout
    assert _git("rev-parse", "--verify", "my-metrics", cwd=remote)


def test_collect_without_the_flag_uses_the_config_branch(workspace):
    work, remote = workspace
    r = _collect(work)
    assert r.returncode == 0, r.stderr
    assert "Metrics stored to branch 'code-metrics'" in r.stdout
    assert _git("rev-parse", "--verify", "code-metrics", cwd=remote)


def test_no_store_prints_and_pushes_nothing(workspace):
    work, remote = workspace
    r = _collect(work, "--no-store")
    assert r.returncode == 0, r.stderr
    assert "not stored" in r.stdout
    assert _git("branch", "--list", cwd=remote) == ""
