import statistics
import uuid

from app.models import SignalEvent, SkillScore
from app.scoring.common import confidence_from_trials

ACTIVITY = "stars_not_clouds"


def score_stars_not_clouds(
    events: list[SignalEvent], child_id: uuid.UUID, is_baseline: bool = False
) -> list[SkillScore]:
    taps = [e for e in events if e.activity == ACTIVITY and e.event_type == "tap"]

    # Correctness is derived from `target`, not trusted from the client's own `correct`
    # field — scoring must be server-authoritative (PROJECT.md rule #7: explainable/traceable).
    false_alarms = [e for e in taps if e.payload.get("target") == "cloud"]
    go_taps = [e for e in taps if e.payload.get("target") == "star"]
    # A tap with a missing/garbled target is neither — exclude it from the denominator too,
    # rather than let it silently deflate the false-alarm rate and inflate the score.
    valid_taps = false_alarms + go_taps
    if not valid_taps:
        return []

    scores = [_impulse_control_score(child_id, valid_taps, false_alarms, is_baseline)]

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
        confidence=confidence_from_trials(len(taps)),
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
        confidence=confidence_from_trials(len(reaction_times)),
        is_baseline=is_baseline,
        evidence={
            "event_ids": [str(e.event_id) for e in go_taps],
            "n_go_responses": len(reaction_times),
            "reaction_time_std_ms": round(reaction_std, 1),
        },
    )
