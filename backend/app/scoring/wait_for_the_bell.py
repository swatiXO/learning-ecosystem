import uuid

from app.models import SignalEvent, SkillScore
from app.scoring.common import confidence_from_trials

ACTIVITY = "wait_for_the_bell"


def score_wait_for_the_bell(
    events: list[SignalEvent], child_id: uuid.UUID, is_baseline: bool = False
) -> list[SkillScore]:
    taps = [e for e in events if e.activity == ACTIVITY and e.event_type == "tap"]
    valid = [e for e in taps if isinstance(e.payload.get("early"), bool)]
    if not valid:
        return []

    early_taps = [e for e in valid if e.payload["early"]]
    false_alarm_rate = len(early_taps) / len(valid)

    wait_times = [
        e.payload["wait_ms"]
        for e in valid
        if not e.payload["early"] and e.payload.get("wait_ms") is not None
    ]

    return [
        SkillScore(
            child_id=child_id,
            dimension="impulse_control",
            score=round(100.0 * (1 - false_alarm_rate), 1),
            confidence=confidence_from_trials(len(valid)),
            is_baseline=is_baseline,
            evidence={
                "event_ids": [str(e.event_id) for e in valid],
                "n_taps": len(valid),
                "early_taps": len(early_taps),
                "avg_wait_ms": round(sum(wait_times) / len(wait_times), 1) if wait_times else None,
            },
        )
    ]
