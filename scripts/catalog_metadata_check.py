"""Run bounded metadata checks through an injected, timeout-aware transport.

No live HTTP adapter is provided. The injected transport must honor timeout;
elapsed-time checks cannot interrupt a blocked call.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from time import monotonic
from urllib.parse import urlsplit

DEFAULT_MAX_ATTEMPTS = 12
DEFAULT_PER_ATTEMPT_SECONDS = 30.0
DEFAULT_TOTAL_SECONDS = 300.0


@dataclass(frozen=True)
class Budget:
    max_attempts: int = DEFAULT_MAX_ATTEMPTS
    per_attempt_seconds: float = DEFAULT_PER_ATTEMPT_SECONDS
    total_seconds: float = DEFAULT_TOTAL_SECONDS

    def __post_init__(self) -> None:
        if (
            self.max_attempts < 1
            or self.per_attempt_seconds <= 0
            or self.total_seconds <= 0
            or self.max_attempts > DEFAULT_MAX_ATTEMPTS
            or self.per_attempt_seconds > DEFAULT_PER_ATTEMPT_SECONDS
            or self.total_seconds > DEFAULT_TOTAL_SECONDS
        ):
            raise ValueError("budgets must be positive and cannot exceed hard maxima")


@dataclass(frozen=True)
class Response:
    status: int


Transport = Callable[[str, float], Response]
Clock = Callable[[], float]
DEFAULT_BUDGET = Budget()


def canonical_repo(value: str) -> str:
    """Return a normalized GitHub owner/repository key; reject other URLs."""
    raw = value if "://" in value else f"https://github.com/{value}"
    parsed = urlsplit(raw)
    parts = parsed.path.strip("/").removesuffix(".git").split("/")
    if (
        parsed.scheme != "https"
        or parsed.hostname != "github.com"
        or parsed.port is not None
        or parsed.username is not None
        or parsed.password is not None
        or len(parts) != 2
        or not all(parts)
        or any(part in {".", ".."} for part in parts)
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("expected a canonical GitHub owner/repository")
    return "/".join(part.lower() for part in parts)


def check_repositories(
    repositories: Iterable[str],
    transport: Transport,
    *,
    budget: Budget = DEFAULT_BUDGET,
    clock: Clock = monotonic,
) -> dict[str, object]:
    """Return a sanitized in-memory receipt; never retries or persists results."""
    started = clock()
    keys: list[str] = []
    seen: set[str] = set()
    for repository in repositories:
        key = canonical_repo(repository)
        if key in seen:
            raise ValueError("duplicate canonical repository")
        if len(keys) >= budget.max_attempts:
            raise ValueError("attempt budget exceeded before dispatch")
        keys.append(key)
        seen.add(key)
    events: list[dict[str, object]] = []
    stopped = False
    for ordinal, key in enumerate(keys, 1):
        remaining = budget.total_seconds - (clock() - started)
        if remaining <= 0:
            events.append({"ordinal": ordinal, "outcome": "total_budget"})
            stopped = True
            break
        limit = min(budget.per_attempt_seconds, remaining)
        before = clock()
        try:
            response = transport(key, limit)
        except TimeoutError:
            status, outcome = None, "timeout"
        except OSError:
            status, outcome = None, "transport_error"
        except Exception:
            status, outcome = None, "unknown_error"
        else:
            status = response.status
            outcome = "ok" if 200 <= status < 300 else "http_error"
            if status in (401, 403):
                outcome = "auth_error"
            elif status == 429:
                outcome = "rate_limited"
        duration = max(0.0, clock() - before)
        events.append(
            {
                "ordinal": ordinal,
                "repository": key,
                "status": status,
                "outcome": outcome,
                "elapsed_seconds": round(duration, 3),
            }
        )
        if (
            outcome != "ok"
            or duration > limit
            or clock() - started >= budget.total_seconds
        ):
            stopped = True
            break
    return {
        "attempt_count": sum("repository" in event for event in events),
        "max_attempts": budget.max_attempts,
        "per_attempt_seconds": budget.per_attempt_seconds,
        "total_seconds": budget.total_seconds,
        "stopped": stopped,
        "events": events,
    }
