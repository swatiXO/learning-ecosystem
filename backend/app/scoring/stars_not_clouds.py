import statistics
import uuid

from app.models import SignalEvent, SkillScore

ACTIVITY = "stars_not_clouds"

# How many trials before confidence reaches 1.0. Placeholder pending Phase 0 pilot data,
# same as the plan engine thresholds in PROJECT.md §6.
MIN_TRIALS_FOR_FULL_CONFIDENCE = 20


def score_stars_not_clouds(
    events: list[SignalEvent], child_id: uuid.UUID, is_baseline: bool = False
) -> list[SkillScore]:
    taps = [e for e in events if e.activity == ACTIVITY and e.event_type == "tap"]
    if not taps:
        return []

    # Correctness is derived from `target`, not trusted from the client's own `correct`
    # field — scoring must be server-authoritative (PROJECT.md rule #7: explainable/traceable).
    false_alarms = [e for e in taps if e.payload.get("target") == "cloud"]
    go_taps = [e for e in taps if e.payload.get("target") == "star"]

    scores = [_impulse_control_score(child_id, taps, false_alarms, is_baseline)]

    reaction_times = [
        e.payload["reaction_ms"] for e in go_taps if e.payload.get("reaction_ms") is not None
    ]
    if len(reaction_times) >= 2:
        scores.append(_sustained_attention_score(child_id, go_taps, reaction_times, is_baseline))

    return scores


def _impulse_control_score(
    child_id: uuid.UUID,
    taps: list[SignalEvent],
    false_alarms: list[SignalEvent],
    is_baseline: bool,
) -> SkillScore:
    false_alarm_rate = len(false_alarms) / len(taps)
    return SkillScore(
        child_id=child_id,
        dimension="impulse_control",
        score=round(100.0 * (1 - false_alarm_rate), 1),
        confidence=round(min(1.0, len(taps) / MIN_TRIALS_FOR_FULL_CONFIDENCE), 2),
        is_baseline=is_baseline,
        evidence={
            "event_ids": [str(e.event_id) for e in taps],
            "n_taps": len(taps),
            "false_alarms": len(false_alarms),
        },
    )


def _sustained_attention_score(
    child_id: uuid.UUID,
    go_taps: list[SignalEvent],
    reaction_times: list[float],
    is_baseline: bool,
) -> SkillScore:
    reaction_std = statistics.stdev(reaction_times)
    # ms-of-variability-to-points scaling is a placeholder, same caveat as above.
    score = max(0.0, 100.0 - reaction_std / 10.0)
    return SkillScore(
        child_id=child_id,
        dimension="sustained_attention",
        score=round(score, 1),
        confidence=round(min(1.0, len(reaction_times) / MIN_TRIALS_FOR_FULL_CONFIDENCE), 2),
        is_baseline=is_baseline,
        evidence={
            "event_ids": [str(e.event_id) for e in go_taps],
            "n_go_responses": len(reaction_times),
            "reaction_time_std_ms": round(reaction_std, 1),
        },
    )
