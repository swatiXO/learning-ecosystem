import uuid

from app.models import SignalEvent, SkillScore
from app.scoring.common import confidence_from_trials

ACTIVITY = "distraction_garden"


def score_distraction_garden(
    events: list[SignalEvent], child_id: uuid.UUID, is_baseline: bool = False
) -> list[SkillScore]:
    taps = [e for e in events if e.activity == ACTIVITY and e.event_type == "tap"]
    valid = [e for e in taps if e.payload.get("target") in ("on_task", "distractor")]
    if not valid:
        return []

    off_task_taps = [e for e in valid if e.payload["target"] == "distractor"]
    off_task_rate = len(off_task_taps) / len(valid)

    return_times = [
        e.payload["return_ms"]
        for e in events
        if e.activity == ACTIVITY
        and e.event_type == "response"
        and e.payload.get("return_ms") is not None
    ]

    return [
        SkillScore(
            child_id=child_id,
            dimension="distractibility",
            score=round(100.0 * (1 - off_task_rate), 1),
            confidence=confidence_from_trials(len(valid)),
            is_baseline=is_baseline,
            evidence={
                "event_ids": [str(e.event_id) for e in valid],
                "n_taps": len(valid),
                "off_task_taps": len(off_task_taps),
                "avg_return_ms": (
                    round(sum(return_times) / len(return_times), 1) if return_times else None
                ),
            },
        )
    ]
