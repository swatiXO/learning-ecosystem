import uuid

from app.models import SignalEvent, SkillScore
from app.scoring.common import confidence_from_trials

ACTIVITY = "watch_the_pond"


def score_watch_the_pond(
    events: list[SignalEvent], child_id: uuid.UUID, is_baseline: bool = False
) -> list[SkillScore]:
    responses = [e for e in events if e.activity == ACTIVITY and e.event_type == "response"]
    valid = [e for e in responses if isinstance(e.payload.get("correct"), bool)]
    if not valid:
        return []

    # Order by time_bucket (the trial's position in the 3-minute run) so "later half" is
    # meaningful, not just insertion order.
    valid.sort(key=lambda e: e.payload.get("time_bucket", 0))

    correct_flags = [bool(e.payload["correct"]) for e in valid]
    overall_accuracy = sum(correct_flags) / len(correct_flags)

    midpoint = len(correct_flags) // 2 or 1
    second_half = correct_flags[midpoint:] or correct_flags
    second_half_accuracy = sum(second_half) / len(second_half)

    longest_streak = _longest_true_streak(correct_flags)

    # Sustained attention is about holding accuracy up through the *end* of the task, not
    # the average across it — a strong start that fades is exactly what this should catch.
    score = round(100.0 * second_half_accuracy, 1)

    return [
        SkillScore(
            child_id=child_id,
            dimension="sustained_attention",
            score=score,
            confidence=confidence_from_trials(len(valid)),
            is_baseline=is_baseline,
            evidence={
                "event_ids": [str(e.event_id) for e in valid],
                "n_responses": len(valid),
                "overall_accuracy": round(overall_accuracy, 2),
                "second_half_accuracy": round(second_half_accuracy, 2),
                "longest_correct_streak": longest_streak,
            },
        )
    ]


def _longest_true_streak(flags: list[bool]) -> int:
    longest = current = 0
    for flag in flags:
        current = current + 1 if flag else 0
        longest = max(longest, current)
    return longest
