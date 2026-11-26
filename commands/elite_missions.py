"""Elite mission rules and shared mission registry."""

from commands.elite_data import ELITE_MISSIONS
from commands.mission_data import MISSIONS as INTERACTIVE_MISSIONS

MISSIONS = {**INTERACTIVE_MISSIONS, **ELITE_MISSIONS}


def reward_details(job_id):
    """Return the database column, currency label and emoji."""
    if job_id in ("summoner", "lieutenant"):
        return "louis_dor", "Louis d'or", "<:louis_dor:1573206641422377041>"
    return "balance", "Livres", "<:livre:1573206463147544586>"
