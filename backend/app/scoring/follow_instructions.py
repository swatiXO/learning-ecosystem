import uuid

from app.models import SignalEvent, SkillScore
from app.scoring.common import confidence_from_trials

ACTIVITY = "follow_instructions"


def score_follow_instructions(
    events: list[SignalEvent], child_id: uuid.UUID, is_baseline: bool = False
) -> list[SkillScore]:
    responses = [e for e in events if e.activity == ACTIVITY and e.event_type == "response"]
    valid = [
        e
        for e in responses
        if isinstance(e.payload.get("n_steps"), int)
        and e.payload["n_steps"] > 0
        and isinstance(e.payload.get("steps_followed"), int)
    ]
    if not valid:
        return []

    hints = [e for e in events if e.activity == ACTIVITY and e.event_type == "hint"]

    total_steps = sum(e.payload["n_steps"] for e in valid)
    followed_steps = sum(min(e.payload["steps_followed"], e.payload["n_steps"]) for e in valid)
    accuracy = followed_steps / total_steps

    hint_rate = len(hints) / len(valid)

    return [
        SkillScore(
            child_id=child_id,
            dimension="auditory_comprehension",
            score=round(100.0 * accuracy, 1),
            confidence=confidence_from_trials(len(valid)),
            is_baseline=is_baseline,
            evidence={
                "event_ids": [str(e.event_id) for e in valid],
                "n_trials": len(valid),
                "steps_followed": followed_steps,
                "steps_total": total_steps,
            },
        ),
        SkillScore(
            child_id=child_id,
            dimension="working_memory",
            score=round(100.0 * max(0.0, 1 - hint_rate), 1),
            confidence=confidence_from_trials(len(valid)),
            is_baseline=is_baseline,
            evidence={
                "event_ids": [str(e.event_id) for e in valid + hints],
                "n_trials": len(valid),
                "repeat_requests": len(hints),
            },
        ),
    ]
