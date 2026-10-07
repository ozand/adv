from __future__ import annotations

from collections.abc import Iterable

import pytest
from scripts.catalog_metadata_check import Budget, Response, check_repositories


class FakeClock:
    def __init__(self) -> None:
        self.value = 0.0

    def __call__(self) -> float:
        return self.value

    def advance(self, amount: float) -> None:
        self.value += amount


def test_success_receipt_is_bounded_and_sanitized() -> None:
    clock = FakeClock()
    calls: list[tuple[str, float]] = []

    def transport(repo: str, timeout: float) -> Response:
        calls.append((repo, timeout))
        clock.advance(0.25)
        return Response(200)

    result = check_repositories(
        ["Owner/Repo", "https://github.com/Other/Proj.git"], transport, clock=clock
    )
    assert result["attempt_count"] == 2
    assert calls[0][0] == "owner/repo"
    assert result["events"][0]["elapsed_seconds"] == 0.25
    assert "headers" not in str(result).lower()


@pytest.mark.parametrize(
    "status,outcome",
    [
        (200, "ok"),
        (401, "auth_error"),
        (403, "auth_error"),
        (429, "rate_limited"),
        (404, "http_error"),
    ],
)
def test_status(status: int, outcome: str) -> None:
    calls: list[str] = []

    def transport(repo: str, timeout: float) -> Response:
        calls.append(repo)
        return Response(status)

    result = check_repositories(["a/b", "c/d"], transport)
    assert result["events"][0]["outcome"] == outcome
    assert calls == (["a/b", "c/d"] if outcome == "ok" else ["a/b"])


@pytest.mark.parametrize(
    "error,outcome",
    [
        (TimeoutError(), "timeout"),
        (OSError("secret detail"), "transport_error"),
        (RuntimeError("private"), "unknown_error"),
    ],
)
def test_exception_is_sanitized_and_stops(error: Exception, outcome: str) -> None:
    def transport(repo: str, timeout: float) -> Response:
        raise error

    result = check_repositories(["a/b", "c/d"], transport)
    assert result["events"][0]["outcome"] == outcome
    assert "secret detail" not in str(result)
    assert "private" not in str(result)
    assert result["attempt_count"] == 1


def test_duplicate_canonical_keys_rejected_before_dispatch() -> None:
    calls = 0

    def transport(repo: str, timeout: float) -> Response:
        nonlocal calls
        calls += 1
        return Response(200)

    with pytest.raises(ValueError, match="duplicate"):
        check_repositories(["owner/repo", "https://github.com/OWNER/REPO.git"], transport)
    assert calls == 0


def test_attempt_limit_rejected_before_dispatch() -> None:
    calls = 0

    def transport(repo: str, timeout: float) -> Response:
        nonlocal calls
        calls += 1
        return Response(200)

    def many() -> Iterable[str]:
        yield "a/1"
        yield "b/2"

    with pytest.raises(ValueError, match="attempt budget"):
        check_repositories(many(), transport, budget=Budget(max_attempts=1))
    assert calls == 0


def test_hard_budget_maxima_cannot_be_raised() -> None:
    with pytest.raises(ValueError, match="hard maxima"):
        Budget(max_attempts=13)
    with pytest.raises(ValueError, match="hard maxima"):
        Budget(per_attempt_seconds=30.1)
    with pytest.raises(ValueError, match="hard maxima"):
        Budget(total_seconds=300.1)


def test_total_deadline_blocks_next_attempt() -> None:
    clock = FakeClock()
    calls: list[str] = []

    def transport(repo: str, timeout: float) -> Response:
        calls.append(repo)
        clock.advance(2.0)
        return Response(200)

    result = check_repositories(
        ["a/1", "b/2", "c/3"],
        transport,
        budget=Budget(max_attempts=3, per_attempt_seconds=3, total_seconds=3),
        clock=clock,
    )
    assert calls == ["a/1", "b/2"]
    assert result["attempt_count"] == 2
    assert result["events"][-1]["ordinal"] == 2
    assert result["stopped"] is True


def test_per_attempt_overrun_stops() -> None:
    clock = FakeClock()

    def transport(repo: str, timeout: float) -> Response:
        clock.advance(timeout + 0.1)
        return Response(200)

    result = check_repositories(
        ["a/b", "c/d"], transport, budget=Budget(per_attempt_seconds=1), clock=clock
    )
    assert result["attempt_count"] == 1
    assert result["stopped"] is True
