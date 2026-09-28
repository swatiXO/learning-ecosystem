import uuid

from app.models import SignalEvent, SkillScore
from app.scoring.common import confidence_from_trials

ACTIVITY = "read_and_answer"


def score_read_and_answer(
    events: list[SignalEvent], child_id: uuid.UUID, is_baseline: bool = False
) -> list[SkillScore]:
    responses = [e for e in events if e.activity == ACTIVITY and e.event_type == "response"]
    valid = [e for e in responses if isinstance(e.payload.get("correct"), bool)]
    if not valid:
        return []

    rereads = [e for e in events if e.activity == ACTIVITY and e.event_type == "hint"]
    accuracy = sum(1 for e in valid if e.payload["correct"]) / len(valid)

    task_times = [
        e.payload["time_on_task_ms"] for e in valid if e.payload.get("time_on_task_ms") is not None
    ]

    return [
        SkillScore(
            child_id=child_id,
            dimension="reading_comprehension",
            score=round(100.0 * accuracy, 1),
            confidence=confidence_from_trials(len(valid)),
            is_baseline=is_baseline,
            evidence={
                "event_ids": [str(e.event_id) for e in valid],
                "n_trials": len(valid),
                "rereads_requested": len(rereads),
                "avg_time_on_task_ms": (
                    round(sum(task_times) / len(task_times), 1) if task_times else None
                ),
            },
        )
    ]
