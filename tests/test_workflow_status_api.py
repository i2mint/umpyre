"""The workflow-status collector asks the API of the GitHub its token belongs to."""

import pytest

import umpyre.collectors.workflow_status as ws


class _Response:
    def raise_for_status(self):
        pass

    def json(self):
        return {"workflow_runs": []}


@pytest.mark.parametrize(
    "api_url, expected",
    [
        (None, "https://api.github.com/repos/o/r/actions/runs"),
        (
            "https://ghe.example/api/v3",
            "https://ghe.example/api/v3/repos/o/r/actions/runs",
        ),
        (
            "https://ghe.example/api/v3/",
            "https://ghe.example/api/v3/repos/o/r/actions/runs",
        ),
    ],
)
def test_runs_are_fetched_from_the_tokens_own_api(monkeypatch, api_url, expected):
    if api_url is None:
        monkeypatch.delenv("GITHUB_API_URL", raising=False)
    else:
        monkeypatch.setenv("GITHUB_API_URL", api_url)
    seen = []
    monkeypatch.setattr(
        ws.requests, "get", lambda url, **kw: seen.append(url) or _Response()
    )
    ws.WorkflowStatusCollector(repo="o/r", token="t")._fetch_workflow_runs()
    assert seen == [expected]
