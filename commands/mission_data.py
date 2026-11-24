
"""Mission definitions for The Real Olrox."""

MISSIONS = {
    "supply_convoy": {
        "title": "The Supply Convoy",
        "job": "revolutionary",
        "level": 12,
        "description": (
            "A royal convoy is transporting supplies "
            "through the countryside.\n"
            "Your allies desperately need those resources."
        ),
        "question": "How will you approach the convoy?",
        "choices": {
            "stealth": {
                "label": "Stealth",
                "emoji": "🌙",
                "success_chance": 0.80,
                "success_pay": (125, 180),
                "failure_pay": (25, 50),
                "success_text": (
                    "You slipped through the shadows and "
                    "seized the supplies unnoticed."
                ),
                "failure_text": (
                    "A guard spotted your movements. "
                    "You escaped with only a few supplies."
                ),
            },
            "assault": {
                "label": "Direct Assault",
                "emoji": "⚔️",
                "success_chance": 0.55,
                "success_pay": (180, 250),
                "failure_pay": (0, 35),
                "success_text": (
                    "Your assault overwhelmed the royal guards. "
                    "The convoy is yours."
                ),
                "failure_text": (
                    "The guards fought back fiercely. "
                    "Your allies were forced to retreat."
                ),
            },
        },
    },
    "prison_break": {
        "title": "The Prison Break",
        "job": "revolutionary",
        "level": 12,
        "description": (
            "Several revolutionaries have been captured "
            "and imprisoned beneath a royal fortress.\n"
            "Their execution is scheduled for dawn."
        ),
        "question": "How will you free the prisoners?",
        "choices": {
            "infiltration": {
                "label": "Silent Infiltration",
                "emoji": "🌙",
                "success_chance": 0.75,
                "success_pay": (140, 195),
                "failure_pay": (20, 55),
                "success_text": (
                    "You navigated the drainage tunnels "
                    "and unlocked the prisoners' cells. "
                    "By sunrise, they were already free."
                ),
                "failure_text": (
                    "The tunnels were heavily guarded. "
                    "You managed to rescue only a few "
                    "prisoners before retreating."
                ),
            },
            "disguise": {
                "label": "Guard Disguise",
                "emoji": "🎭",
                "success_chance": 0.55,
                "success_pay": (195, 270),
                "failure_pay": (0, 35),
                "success_text": (
                    "Your disguise fooled the royal guards. "
                    "You opened the fortress gates and "
                    "led every prisoner to freedom."
                ),
                "failure_text": (
                    "An officer recognized your deception. "
                    "You barely escaped the fortress alive."
                ),
            },
        },
    },

    "royal_informant": {
        "title": "The Informant",
        "job": "revolutionary",
        "level": 12,
        "description": (
            "A trusted informant has been selling revolutionary "
            "secrets to the royal court.\n"
            "Several safehouses have already been compromised, "
            "and your allies are running out of time."
        ),
        "question": "How will you deal with the traitor?",
        "choices": {
            "interrogation": {
                "label": "Silent Interrogation",
                "emoji": "🌙",
                "success_chance": 0.80,
                "success_pay": (130, 185),
                "failure_pay": (25, 50),
                "success_text": (
                    "Under the cover of darkness, you captured "
                    "the informant and uncovered the names of "
                    "his royal contacts. The resistance is safe "
                    "for another night."
                ),
                "failure_text": (
                    "The informant sensed your approach and "
                    "escaped through a hidden passage. You "
                    "recovered a few documents, but his "
                    "secrets remain out of reach."
                ),
            },
            "exposure": {
                "label": "Public Exposure",
                "emoji": "⚔️",
                "success_chance": 0.55,
                "success_pay": (190, 260),
                "failure_pay": (0, 35),
                "success_text": (
                    "You exposed the traitor before the entire "
                    "resistance. His accomplices fled, and the "
                    "stolen intelligence was recovered. "
                    "Your allies celebrate your victory."
                ),
                "failure_text": (
                    "The accusation sparked chaos. Royal "
                    "agents hidden among the crowd attacked, "
                    "allowing the informant to disappear. "
                    "The resistance suffered a costly setback."
                ),
            },
        },
    },

    "burning_barricade": {
        "title": "The Burning Barricade",
        "job": "revolutionary",
        "level": 12,
        "description": (
            "Royal soldiers have set fire to a revolutionary "
            "barricade.\n"
            "Trapped civilians are calling for help as enemy "
            "forces advance through the smoke."
        ),
        "question": "How will you defend the barricade?",
        "choices": {
            "rescue": {
                "label": "Rescue the Civilians",
                "emoji": "🕯️",
                "success_chance": 0.80,
                "success_pay": (135, 190),
                "failure_pay": (25, 55),
                "success_text": (
                    "You guided the civilians through the "
                    "smoke while your allies held the line. "
                    "Every life saved became another reason "
                    "for the resistance to keep fighting."
                ),
                "failure_text": (
                    "The flames spread faster than expected. "
                    "You managed to escort several civilians "
                    "to safety, but the barricade was lost "
                    "to the royal forces."
                ),
            },
            "counterattack": {
                "label": "Counterattack",
                "emoji": "⚔️",
                "success_chance": 0.55,
                "success_pay": (200, 275),
                "failure_pay": (0, 35),
                "success_text": (
                    "You led a fierce counterattack through "
                    "the burning streets. The royal soldiers "
                    "retreated, and the resistance reclaimed "
                    "the barricade before dawn."
                ),
                "failure_text": (
                    "Your assault was met with overwhelming "
                    "force. The royal soldiers broke through "
                    "your defenses, forcing the resistance "
                    "to abandon the burning barricade."
                ),
            },
        },
    },

    "cathedral_watch": {
        "title": "The Cathedral Watch",
        "job": "knight",
        "level": 15,
        "description": (
            "A sacred reliquary disappeared from the Order's chapel "
            "just before nightfall, a trail of ash "
            "leads towards the catacombs"
        ),
        "question": "What will you do?",
        "choices": {
            "choice_one": {
                "label": "Follow the trail",
                "emoji": "👁️",
                "success_chance": 0.80,
                "success_pay": (175, 350),
                "failure_pay": (40, 70),
                "success_text": (
                    "You found the thief just in time "
                    "and you recovered the relic, "
                    "the piece seems to be intac."
                ),
                "failure_text": (
                    "You were too slow, the thief ran away. "
                    "You start to feel guilty because of that."
                ),
            },
            "choice_two": {
                "label": "Questioning",
                "emoji": "⚖️",
                "success_chance": 0.70,
                "success_pay": (200, 450),
                "failure_pay": (20, 35),
                "success_text": (
                    "One of the novices confessed out of fear. "
                    "They showed the hiding place, nobody was hurt."
                ),
                "failure_text": (
                    "Your constant questions started causing a stir. "
                    "The culprit made a run for it amidst the chaos, "
                    "and you've made a fool of yourself "
                    "in the eyes of the Order. "
                    "Better luck next time"
                ),
            },
        },
    },
    "machecoul_escort": {
            "title": "Escort to Machecoul",
            "job": "knight",
            "level": 15,
            "description": (
                "You must escort a messenger of the Order "
                "with sealed letters through a road taken "
                "by the revolutionaries."
            ),
            "question": "What will you do?",
            "choices": {
                "choice_one": {
                    "label": "A shortcut",
                    "emoji": "🐾",
                    "success_chance": 0.80,
                    "success_pay": (175, 350),
                    "failure_pay": (40, 70),
                    "success_text": (
                        "You avoided the crowd and the letters "
                        "were delivered before dawn."
                    ),
                    "failure_text": (
                        "Reckless vampires intercepted among the trees, "
                        "you lost a significant part of the cargo."
                    ),
                },
                "choice_two": {
                    "label": "Costume",
                    "emoji": "🎭",
                    "success_chance": 0.70,
                    "success_pay": (200, 450),
                    "failure_pay": (20, 35),
                    "success_text": (
                        "You tricked the revolutionary guard with labia and "
                        "you crossed without any suspicion."
                    ),
                    "failure_text": (
                        "The Crest of Saint John betrayed you "
                        "you have to run, leaving coins behind. "
                    ),
                },
            },
        },
    "the_confession": {
        "title": "The Blue Blood's Confession",
        "job": "knight",
        "level": 15,
        "description": (
            "An aristocrat has requested urgent protection "
            "of the knight, after they had broken a pact "
            "with Erzebet's retinue."
        ),
        "question": "What will you do?",
        "choices": {
            "choice_one": {
                "label": "Hide him",
                "emoji": "🛡️",
                "success_chance": 0.80,
                "success_pay": (175, 350),
                "failure_pay": (40, 70),
                "success_text": (
                    "You believe God has mercy for everyone. "
                    "You protected the man, and he paid well for his life."
                ),
                "failure_text": (
                    "The man attracted some vampired,"
                    "they see him as a traitor."
                    "Some men died, you couldn't do much."
                ),
            },
            "choice_two": {
                "label": "Use him",
                "emoji": "🏹",
                "success_chance": 0.70,
                "success_pay": (200, 450),
                "failure_pay": (20, 35),
                "success_text": (
                    "You used him as a bait to lure the vampire emissary "
                    "and hunt him. Nobody was hurt... "
                    "Except for the vampire."
                ),
                "failure_text": (
                    "The noble died before you could do anything "
                    "about it. You lost him, the money and your peace."
                ),
            },
        },
    },
}
