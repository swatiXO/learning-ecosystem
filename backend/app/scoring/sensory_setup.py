import uuid

from app.models import SignalEvent, SkillScore
from app.scoring.common import confidence_from_trials

ACTIVITY = "sensory_setup"
# Placeholder scaling: 10 calm-mode activations floors the score at 0.
CALM_MODE_ACTIVATIONS_FOR_ZERO_SCORE = 10.0


def score_sensory_setup(
    events: list[SignalEvent], child_id: uuid.UUID, is_baseline: bool = False
) -> list[SkillScore]:
    settings_changed = [
        e for e in events if e.activity == ACTIVITY and e.event_type == "setting_changed"
    ]
    if not settings_changed:
        return []

    calm_mode_on = [
        e
        for e in settings_changed
        if e.payload.get("setting") == "calm_mode" and e.payload.get("value") == "on"
    ]

    score = max(0.0, 100.0 - 100.0 * len(calm_mode_on) / CALM_MODE_ACTIVATIONS_FOR_ZERO_SCORE)

    return [
        SkillScore(
            child_id=child_id,
            dimension="sensory_regulation",
            score=round(score, 1),
            confidence=confidence_from_trials(len(settings_changed)),
            is_baseline=is_baseline,
            evidence={
                "event_ids": [str(e.event_id) for e in settings_changed],
                "n_settings_changed": len(settings_changed),
                "calm_mode_activations": len(calm_mode_on),
            },
        )
    ]
