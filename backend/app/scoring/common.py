"""Shared helpers for scoring extractors. Score/confidence scaling constants throughout
are placeholders pending Phase 0 pilot data, per PROJECT.md §6's own caveat on the plan
engine's thresholds — the same rule applies here."""

# How many trials before confidence reaches 1.0.
MIN_TRIALS_FOR_FULL_CONFIDENCE = 20


def confidence_from_trials(n: int) -> float:
    return round(min(1.0, n / MIN_TRIALS_FOR_FULL_CONFIDENCE), 2)
