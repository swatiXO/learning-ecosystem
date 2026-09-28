import uuid

from app.models import SignalEvent, SkillScore
from app.scoring.common import confidence_from_trials

ACTIVITY = "mood_check_in"


def score_mood_check_in(
    events: list[SignalEvent], child_id: uuid.UUID, is_baseline: bool = False
) -> list[SkillScore]:
    """Only skip rate -> sensory_regulation. "Mood shift" (comparing before/after mood
    values) needs a defined mood-to-valence scale that doesn't exist anywhere in the
    project yet — a content decision, same class of gap as what_would_you_do/about_me."""
    moods = [e for e in events if e.activity == ACTIVITY and e.event_type == "mood"]
    skips = [e for e in events if e.activity == ACTIVITY and e.event_type == "skip"]
    total = len(moods) + len(skips)
    if total == 0:
        return []

    skip_rate = len(skips) / total

    return [
        SkillScore(
            child_id=child_id,
            dimension="sensory_regulation",
            score=round(100.0 * (1 - skip_rate), 1),
            confidence=confidence_from_trials(total),
            is_baseline=is_baseline,
            evidence={
                "event_ids": [str(e.event_id) for e in moods + skips],
                "mood_check_ins": len(moods),
                "skips": len(skips),
            },
        )
    ]
