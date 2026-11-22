"""umpyre CLI argument handling and error policy, without touching git or the network."""

import sys

import pytest

from umpyre import cli


def _run(monkeypatch, *argv):
    monkeypatch.setattr(sys, "argv", ["umpyre", *argv])
    return cli.main()


def test_no_command_prints_help_and_returns_1(monkeypatch, capsys):
    assert _run(monkeypatch) == 1
    assert "Code metrics collection" in capsys.readouterr().out


def test_validate_reports_not_implemented(monkeypatch, capsys):
    monkeypatch.setattr(cli, "Config", lambda config_path=None: object())
    monkeypatch.setattr(cli, "_collect_metrics", lambda config, repo_path: {})
    assert _run(monkeypatch, "validate", "--repo-path", ".") == 0
    assert "not yet implemented" in capsys.readouterr().out


def test_errors_are_fatal_locally_and_forgiven_in_ci(monkeypatch, capsys):
    def boom(args):
        raise RuntimeError("kaboom")

    monkeypatch.setattr(cli, "cmd_validate", boom)
    monkeypatch.delenv("CI", raising=False)
    monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    # set_defaults captured the original function, so patch the parser's target instead
    monkeypatch.setattr(
        cli.argparse.ArgumentParser, "parse_args",
        lambda self: type("A", (), {"command": "validate", "func": staticmethod(boom)})(),
    )
    assert cli.main() == 1
    assert "Error: kaboom" in capsys.readouterr().err
    monkeypatch.setenv("CI", "true")
    assert cli.main() == 0
    assert "non-fatal" in capsys.readouterr().err
