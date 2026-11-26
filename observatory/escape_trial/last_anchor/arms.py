"""Frozen paired decisions; run on already selected lineups only."""
from observatory.escape_trial.reentry_membership import classes_at, inspect


def first_issue(weights, denominator):
    classes = classes_at(weights, denominator)
    for sign in (1, -1):
        time, _ = inspect(classes, denominator, sign)
        if time is not None:
            return sign, time
    return None
