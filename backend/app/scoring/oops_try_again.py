import uuid

from app.models import SignalEvent, SkillScore
from app.scoring.common import confidence_from_trials

ACTIVITY = "oops_try_again"


def score_oops_try_again(
    events: list[SignalEvent], child_id: uuid.UUID, is_baseline: bool = False
) -> list[SkillScore]:
    retries = [e for e in events if e.activity == ACTIVITY and e.event_type == "retry"]
    quits = [e for e in events if e.activity == ACTIVITY and e.event_type == "quit"]
    total = len(retries) + len(quits)
    if total == 0:
        return []

    retry_rate = len(retries) / total
    retry_times = [
        e.payload["time_to_retry_ms"]
        for e in retries
        if e.payload.get("time_to_retry_ms") is not None
    ]

    return [
        SkillScore(
            child_id=child_id,
            dimension="self_confidence",
            score=round(100.0 * retry_rate, 1),
            confidence=confidence_from_trials(total),
            is_baseline=is_baseline,
            evidence={
                "event_ids": [str(e.event_id) for e in retries + quits],
                "retries": len(retries),
                "quits": len(quits),
                "avg_time_to_retry_ms": (
                    round(sum(retry_times) / len(retry_times), 1) if retry_times else None
                ),
            },
        )
    ]
