# Maps each cause to exactly one recovery action.
# This mapping is the "explainable, bounded" part — no free-form decisions.

RECOVERY_RULES = {
    "otp_timeout": "retry_nudge",
    "network_drop": "retry_nudge",
    "bank_timeout": "retry_after_cooldown",
    "method_mismatch": "suggest_alt_method",
    "insufficient_funds": "no_action",
    "success": "no_action",
    "unknown": "no_action",
}

# Simulated recovery success probability per action (used to estimate ₹ recovered later)
RECOVERY_SUCCESS_RATE = {
    "retry_nudge": 0.70,
    "retry_after_cooldown": 0.55,
    "suggest_alt_method": 0.60,
    "no_action": 0.0,
}


def get_recovery_action(cause):
    return RECOVERY_RULES.get(cause, "no_action")