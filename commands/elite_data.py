"""Misiones elites del bot."""

ELITE_MISSIONS = {
    "fire_birds": {
        "title": "Call of the Firebirds",
        "job": "summoner",
        "level": 35,
        "description": (
            "A pair of vampires is surrounding a safe house used by  "
            "revolutionaries, you must defeat both threats "
            "to prevent innocent people from being hurt."
        ),
        "question": "What will you do?",
        "choices": {
            "choice_one": {
                "label": "Invoke your birds",
                "emoji": "🔥",
                "success_chance": 0.80,
                "success_pay": (1, 3),
                "failure_pay": (0, 0),
                "success_text": (
                    "The birds helped you to wipe out the vampires. "
                    "The place is safe, for now."
                ),
                "failure_text": (
                    "You lost your control out of rage, "
                    "the fire caught supplies, and now "
                    "your heart carries the burden of guilt."
                ),
            },
            "choice_two": {
                "label": "Invoke your turtle as a shield",
                "emoji": "🐢",
                "success_chance": 0.70,
                "success_pay": (1, 3),
                "failure_pay": (0, 0),
                "success_text": (
                    "Everyone escaped thanks to the turtle's barrier, "
                    "they're all safe and gratufl with you. "
                    "But safety is not "
                    "guaranteed, they might come back soon."
                ),
                "failure_text": (
                    "One of the vampires broke the turtle's shield, "
                    "you barely managed to escape, with some bruises."
                ),
            },
        },
    },
    "astral_portal": {
        "title": "The Astral Portal",
        "job": "summoner",
        "level": 35,
        "description": (
            "Your emotions get more complicated everyday "
            "grief and rage holds into your heart, "
            "your beloved ones offer their help. "
            "You managed to invoke an untamed creature."
        ),
        "question": "What will you do?",
        "choices": {
            "choice_one": {
                "label": "Force it",
                "emoji": "🌑",
                "success_chance": 0.80,
                "success_pay": (1, 3),
                "failure_pay": (0, 0),
                "success_text": (
                    "Seems to work, still the creature seems "
                    "a bit too aggresive than the others. Now you "
                    "have a wild one under your domain."
                ),
                "failure_text": (
                    "You cannot force yourself now; "
                    "it was a risky thing to do, you had to close "
                    "the portal and rest a lot after that."
                ),
            },
            "choice_two": {
                "label": "Breath through it",
                "emoji": "💜",
                "success_chance": 0.70,
                "success_pay": (1, 3),
                "failure_pay": (0, 0),
                "success_text": (
                    "With enough support, you managed to tame "
                    "your little creation. Your heart fills "
                    "with relief, but some sadness remains in there."
                ),
                "failure_text": (
                    "You can't take it anymore. It hurts to try. "
                    "you force your creature back to hell."
                ),
            },
        },
    },
    "spirit_dragon": {
        "title": "The Spirit Dragon",
        "job": "summoner",
        "level": 35,
        "description": (
            "A vampire from the upper class is blocking "
            "the main bridge to Machecoul, threatening to "
            "harm innocent people."
        ),
        "question": "What will you do?",
        "choices": {
            "choice_one": {
                "label": "Unleash your dragon",
                "emoji": "🐉",
                "success_chance": 0.80,
                "success_pay": (1, 3),
                "failure_pay": (0, 0),
                "success_text": (
                    "You and your companion defeat the vampire with "
                    "enough dedication. You're a good person, they "
                    "thanked you with a warm meal."
                ),
                "failure_text": (
                    "The dragon's power leaves you weak, an advantage to "
                    "the wounded vampire, who disappears back into the woods "
                    "Still, people thanked your courage."
                ),
            },
            "choice_two": {
                "label": "Rapid attacks with lesser spirits",
                "emoji": "✨",
                "success_chance": 0.70,
                "success_pay": (1, 3),
                "failure_pay": (0, 0),
                "success_text": (
                    "You surround him with your summons until you have him "
                    "cornered, and manage to defeat him without using up "
                    "all your energy. Good job."
                ),
                "failure_text": (
                    "The vampire catched one of your dear birds, "
                    "breaks the link, and you take the blow yourself."
                ),
            },
        },
    },
    "ancestors_whispers": {
        "title": "The Whispers of the Ancestors",
        "job": "summoner",
        "level": 35,
        "description": (
            "In the middle of the night, the voices "
            "of your ancestors echo in your head. Asking you to recover "
            "an ancient stolen relic that is in a mansion."
        ),
        "question": "What will you do?",
        "choices": {
            "choice_one": {
                "label": "Manipulate the metal in the railings",
                "emoji": "⛓️",
                "success_chance": 0.80,
                "success_pay": (1, 3),
                "failure_pay": (0, 0),
                "success_text": (
                    "The iron obeys your will, you disarm the guards in "
                    "silence and retrieve the relic from a hidden "
                    "chest, some louis d'or remain there, along with"
                    "the relic. Lucky you."
                ),
                "failure_text": (
                    "Your technique is sloppy, you lost the track "
                    "of time. The guards almost caught you, you barely "
                    "managed to escape."
                ),
            },
            "choice_two": {
                "label": "Ask for a hidden shortcut",
                "emoji": "🕯️",
                "success_chance": 0.70,
                "success_pay": (1, 3),
                "failure_pay": (0, 0),
                "success_text": (
                    "Your ancestors guide you through the place and "
                    "into a secret shortcut. You made no noise, the "
                    "chest is yours. Not a single drop of blood tonight."
                ),
                "failure_text": (
                    "You're not strong enough to communicate with them"
                    "you decide to go back to your shelter. "
                    "You lost the opportunity, for now"
                ),
            },
        },
    },
    "crossroads_ritual": {
        "title": "The Crossroads Ritual",
        "job": "summoner",
        "level": 35,
        "description": (
            "The soul of a fallen ally is trapped between the world "
            "of the living and the afterlife.\n"
            "You must perform a ritual at a crossroads at midnight "
            "to guide the soul back."
        ),
        "question": "How will you guide the soul back?",
        "choices": {
            "choice_one": {
                "label": "Draw a sacred symbol and offer tribute",
                "emoji": "🕯️",
                "success_chance": 0.80,
                "success_pay": (1, 3),
                "failure_pay": (0, 0),
                "success_text": (
                    "The spirits accept your offering. You cross the "
                    "spiritual veil and free the trapped soul. "
                    "Your efforts are rewarded."
                ),
                "failure_text": (
                    "A shadow slips through the portal, disrupting "
                    "communication and breaking your concentration. "
                    "The portal closes, leaving you dazed."
                ),
            },
            "choice_two": {
                "label": "Forge a magical iron anchor",
                "emoji": "⚓",
                "success_chance": 0.70,
                "success_pay": (1, 3),
                "failure_pay": (0, 0),
                "success_text": (
                    "The metal channels the ancestral power of your "
                    "hands like a beacon. The soul returns intact "
                    "and relieved."
                ),
                "failure_text": (
                    "The magical tension causes the iron to explode. "
                    "The ritual fails, and the blast leaves you dazed."
                ),
            },
        },
    },
    "messiahs_decree": {
        "title": "The Messiah's Decree",
        "job": "lieutenant",
        "level": 50,
        "description": "A new assignment awaits.",
        "question": "What will you do?",
        "choices": {
            "choice_one": {
                "label": "First strategy",
                "emoji": "🌙",
                "success_chance": 0.80,
                "success_pay": (2, 4),
                "failure_pay": (0, 0),
                "success_text": "The assignment was successful.",
                "failure_text": "The assignment failed.",
            },
            "choice_two": {
                "label": "Second strategy",
                "emoji": "🩸",
                "success_chance": 0.70,
                "success_pay": (3, 5),
                "failure_pay": (0, 0),
                "success_text": "The assignment was successful.",
                "failure_text": "The assignment failed.",
            },
        },
    },
    "crimson_banquet": {
        "title": "The Crimson Banquet",
        "job": "lieutenant",
        "level": 50,
        "description": "A new assignment awaits.",
        "question": "What will you do?",
        "choices": {
            "choice_one": {
                "label": "First strategy",
                "emoji": "🌙",
                "success_chance": 0.80,
                "success_pay": (2, 4),
                "failure_pay": (0, 0),
                "success_text": "The assignment was successful.",
                "failure_text": "The assignment failed.",
            },
            "choice_two": {
                "label": "Second strategy",
                "emoji": "🩸",
                "success_chance": 0.70,
                "success_pay": (3, 5),
                "failure_pay": (0, 0),
                "success_text": "The assignment was successful.",
                "failure_text": "The assignment failed.",
            },
        },
    },
    "eclipse_ritual": {
        "title": "The Eclipse Ritual",
        "job": "lieutenant",
        "level": 50,
        "description": "A new assignment awaits.",
        "question": "What will you do?",
        "choices": {
            "choice_one": {
                "label": "First strategy",
                "emoji": "🌙",
                "success_chance": 0.80,
                "success_pay": (2, 4),
                "failure_pay": (0, 0),
                "success_text": "The assignment was successful.",
                "failure_text": "The assignment failed.",
            },
            "choice_two": {
                "label": "Second strategy",
                "emoji": "🩸",
                "success_chance": 0.70,
                "success_pay": (3, 5),
                "failure_pay": (0, 0),
                "success_text": "The assignment was successful.",
                "failure_text": "The assignment failed.",
            },
        },
    },
    "defiant_lieutenant": {
        "title": "The Defiant Lieutenant",
        "job": "lieutenant",
        "level": 50,
        "description": "A new assignment awaits.",
        "question": "What will you do?",
        "choices": {
            "choice_one": {
                "label": "First strategy",
                "emoji": "🌙",
                "success_chance": 0.80,
                "success_pay": (2, 4),
                "failure_pay": (0, 0),
                "success_text": "The assignment was successful.",
                "failure_text": "The assignment failed.",
            },
            "choice_two": {
                "label": "Second strategy",
                "emoji": "🩸",
                "success_chance": 0.70,
                "success_pay": (3, 5),
                "failure_pay": (0, 0),
                "success_text": "The assignment was successful.",
                "failure_text": "The assignment failed.",
            },
        },
    },
    "scarlet_relic": {
        "title": "The Scarlet Relic",
        "job": "lieutenant",
        "level": 50,
        "description": "A new assignment awaits.",
        "question": "What will you do?",
        "choices": {
            "choice_one": {
                "label": "First strategy",
                "emoji": "🌙",
                "success_chance": 0.80,
                "success_pay": (2, 4),
                "failure_pay": (0, 0),
                "success_text": "The assignment was successful.",
                "failure_text": "The assignment failed.",
            },
            "choice_two": {
                "label": "Second strategy",
                "emoji": "🩸",
                "success_chance": 0.70,
                "success_pay": (3, 5),
                "failure_pay": (0, 0),
                "success_text": "The assignment was successful.",
                "failure_text": "The assignment failed.",
            },
        },
    },
}
