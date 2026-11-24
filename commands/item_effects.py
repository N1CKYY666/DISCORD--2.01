
"""Mission item effects for The Real Olrox."""

ITEM_EFFECTS = {
    "daggers": {
        "type": "success_bonus",
        "bonus": 0.10,
        "consumable": True,
        "jobs": ["revolutionary", "vampire_hunter"],
    },
    "holy_water": {
        "type": "success_bonus",
        "bonus": 0.15,
        "consumable": True,
        "jobs": ["knight", "vampire_hunter"],
    },
    "wall_chicken": {
        "type": "failure_protection",
        "consumable": True,
        "jobs": "all",
    },
    "cockade": {
        "type": "success_bonus",
        "bonus": 0.10,
        "consumable": False,
        "jobs": ["revolutionary"],
    },
    "leather_whip": {
        "type": "success_bonus",
        "bonus": 0.10,
        "consumable": False,
        "jobs": ["knight", "vampire_hunter"],
    },
    "pocket_watch": {
        "type": "reroll",
        "uses": 1,
        "consumable": False,
        "jobs": "all",
    },
    "grimoire": {
        "type": "ritual_stability",
        "consumable": False,
        "jobs": ["summoner"],
    },
    "crimson_stone": {
        "type": "secret_route",
        "consumable": False,
        "jobs": ["vampire_lieutenant"],
    },
}
