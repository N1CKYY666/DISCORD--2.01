"""Mission appearance and attachments."""

import random
from pathlib import Path

import discord

GIF_DIR = Path(__file__).resolve().parent.parent / "assets" / "gifs"

DIVIDER_GIF = GIF_DIR / "divider1.gif"
AURA_GIFS = [
    GIF_DIR / "aura_farming.gif",
    GIF_DIR / "power.gif",
    GIF_DIR / "hair.gif",
    GIF_DIR / "richter4.gif",
    GIF_DIR / "trevor.gif",
    GIF_DIR / "richter.gif",
    *GIF_DIR.glob("mizrak*.gif"),
    GIF_DIR / "alucard.gif",
    GIF_DIR / "summon.gif",
    GIF_DIR / "richter3.gif",
    GIF_DIR / "shove.gif",
    *GIF_DIR.glob("sypha*.gif"),
    *GIF_DIR.glob("another*.gif"),
]


SUMMONER_GIFS = [
    *GIF_DIR.glob("annte*.gif"),
    *GIF_DIR.glob("annete*.gif"),
    *GIF_DIR.glob("annette*.gif"),
    *GIF_DIR.glob("maria*.gif"),
]
LIEUTENANT_GIFS = list(GIF_DIR.glob("drolta*.gif"))


def mission_color(job_id):
    return {"summoner": 0xC5A059, "lieutenant": 0x803D56}.get(
        job_id, 0x74459A
    )


def choose_gif(job_id):
    pool = {
        "summoner": SUMMONER_GIFS,
        "lieutenant": LIEUTENANT_GIFS,
    }.get(job_id, AURA_GIFS)
    available = [path for path in pool if path.is_file()]
    if not available:
        available = [path for path in AURA_GIFS if path.is_file()]
    return random.choice(available) if available else None


def divider(job_id):
    filenames = {
        "summoner": "divider1.gif",
        "lieutenant": "divider1.gif",
    }
    path = GIF_DIR / filenames.get(job_id, "divider1.gif")
    if not path.is_file():
        print(f"[MISSIONS] Missing divider: {path}")
    return path


def decorate_mission_embed(embed, aura_gif, job_id):
    if aura_gif is not None:
        embed.set_thumbnail(url=f"attachment://{aura_gif.name}")
    path = divider(job_id)
    if path.is_file():
        embed.set_image(url=f"attachment://{path.name}")
    return embed


def get_mission_files(aura_gif, job_id):
    paths = [divider(job_id), aura_gif]
    return [
        discord.File(path, filename=path.name)
        for path in paths if path is not None and path.is_file()
    ]
