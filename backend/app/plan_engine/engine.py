from dataclasses import dataclass

from app.plan_engine.rules import RULES, Profile, Rule

# Fallback when no rule fires (PROJECT.md §6).
FALLBACK_MODULES = {"confidence_builder": 0.5, "focus_attention": 0.5}
MAX_MODULES = 3


@dataclass
class PlanResult:
    modules: dict[str, float]
    rules_fired: list[str]


def build_plan(profile: Profile, rules: list[Rule] | None = None) -> PlanResult:
    rules = rules if rules is not None else RULES

    raw_weights: dict[str, float] = {}
    rules_fired: list[str] = []

    for rule in rules:
        if rule.when(profile):
            rules_fired.append(rule.name)
            for module, weight in rule.add.items():
                raw_weights[module] = raw_weights.get(module, 0.0) + weight

    if not raw_weights:
        return PlanResult(modules=dict(FALLBACK_MODULES), rules_fired=["fallback_no_rules_fired"])

    top_modules = dict(
        sorted(raw_weights.items(), key=lambda kv: kv[1], reverse=True)[:MAX_MODULES]
    )
    total = sum(top_modules.values())
    normalized = {module: round(weight / total, 3) for module, weight in top_modules.items()}

    return PlanResult(modules=normalized, rules_fired=rules_fired)
