"""Shared mission transactions and equipment lookup."""

import random
import sqlite3
import time

from commands.elite_missions import MISSIONS, reward_details
from commands.item_effects import ITEM_EFFECTS
from commands.jobs import DB_PATH
from commands.levels import calculate_level
from commands.shop import get_user_inventory
from commands.work import WORK_COOLDOWN


def get_compatible_items(guild_id, user_id, job_id):
    """Return owned mission items compatible with a profession."""
    inventory = get_user_inventory(guild_id, user_id)
    compatible_items = []

    for item_id, item_data, quantity in inventory:
        effect = ITEM_EFFECTS.get(item_id)

        if effect is None:
            continue

        allowed_jobs = effect["jobs"]

        if allowed_jobs != "all" and job_id not in allowed_jobs:
            continue

        compatible_items.append(
            (item_id, item_data, quantity, effect)
        )

    return compatible_items


def get_revolutionary_mission():
    """Return the first Revolutionary mission."""
    return MISSIONS["supply_convoy"]


def reserve_mission(guild_id, user_id, job_id, mission_id):
    """Reserve one mission without paying its reward."""
    now = int(time.time())
    expires_at = now + 60

    with sqlite3.connect(DB_PATH, timeout=10) as connection:
        connection.execute("BEGIN IMMEDIATE")

        result = connection.execute(
            """
            SELECT job_id, last_work
            FROM user_jobs
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        ).fetchone()

        if result is None:
            return "unemployed", 0

        current_job, last_work = result

        if current_job != job_id:
            return "wrong_job", 0

        xp = connection.execute(
            "SELECT xp FROM experience WHERE guild_id = ? AND user_id = ?",
            (guild_id, user_id)
        ).fetchone()
        level, _, _ = calculate_level(xp[0] if xp else 0)
        if level < MISSIONS[mission_id]["level"]:
            return "level", 0

        remaining = WORK_COOLDOWN - (now - last_work)

        if remaining > 0:
            return "cooldown", remaining

        active = connection.execute(
            """
            SELECT expires_at
            FROM active_missions
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        ).fetchone()

        if active is not None:
            active_remaining = active[0] - now

            if active_remaining > 0:
                return "active_mission", active_remaining

            connection.execute(
                """
                DELETE FROM active_missions
                WHERE guild_id = ? AND user_id = ?
                """,
                (guild_id, user_id)
            )

        connection.execute(
            """
            INSERT INTO active_missions (
                guild_id,
                user_id,
                job_id,
                mission_id,
                expires_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                guild_id,
                user_id,
                job_id,
                mission_id,
                expires_at
            )
        )

        return "reserved", expires_at


def complete_mission(
    guild_id, user_id, job_id, mission_id, choice, reservation_token
):
    """Complete a mission and award its reward exactly once."""
    now = int(time.time())

    mission = MISSIONS.get(mission_id)

    if (
        mission is None
        or mission["job"] != job_id
        or choice not in mission["choices"]
    ):
        return "invalid_mission", 0, False

    with sqlite3.connect(DB_PATH, timeout=10) as connection:
        connection.execute("BEGIN IMMEDIATE")

        reservation = connection.execute(
            """
            SELECT job_id, mission_id, expires_at
            FROM active_missions
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        ).fetchone()

        if reservation is None:
            return "no_mission", 0, False

        reserved_job, reserved_mission, expires_at = reservation

        if expires_at != reservation_token:
            return "wrong_mission", 0, False

        if now >= expires_at:
            connection.execute(
                """
                DELETE FROM active_missions
                WHERE guild_id = ? AND user_id = ?
                """,
                (guild_id, user_id)
            )
            return "expired", 0, False

        if (
            reserved_job != job_id
            or reserved_mission != mission_id
        ):
            return "wrong_mission", 0, False

        result = connection.execute(
            """
            SELECT job_id, last_work
            FROM user_jobs
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        ).fetchone()

        if result is None or result[0] != job_id:
            return "wrong_job", 0, False

        remaining = WORK_COOLDOWN - (now - result[1])

        if remaining > 0:
            return "cooldown", remaining, False

        settings = mission["choices"][choice]
        success = random.random() < settings["success_chance"]

        pay_range = (
            settings["success_pay"]
            if success
            else settings["failure_pay"]
        )

        reward = random.randint(*pay_range)

        connection.execute(
            """
            INSERT OR IGNORE INTO economy (guild_id, user_id)
            VALUES (?, ?)
            """,
            (guild_id, user_id)
        )

        column, _, _ = reward_details(job_id)
        connection.execute(
            f"""
            UPDATE economy
            SET {column} = {column} + ?
            WHERE guild_id = ? AND user_id = ?
            """,
            (reward, guild_id, user_id)
        )

        connection.execute(
            """
            UPDATE user_jobs
            SET last_work = ?
            WHERE guild_id = ? AND user_id = ?
            """,
            (now, guild_id, user_id)
        )

        connection.execute(
            """
            DELETE FROM active_missions
            WHERE guild_id = ? AND user_id = ?
            """,
            (guild_id, user_id)
        )

        return "success", reward, success


REVOLUTIONARY_REWARDS = MISSIONS["supply_convoy"]["choices"]
