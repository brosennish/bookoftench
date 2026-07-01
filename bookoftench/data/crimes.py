"""Wanted enemy crimes data.

Each crime dict has:
  - crime: str — description of the crime
  - bounty: bool — whether this crime carries a bounty reward
  - areas: list[str] — which areas this crime can occur in

Used by the bounty system when a wanted enemy is encountered.
"""

Crimes: list[dict] = [
    # === City crimes ===
    {
        "crime": "Pickpocketing unsuspecting townsfolk",
        "bounty": True,
        "areas": ["City"],
    },
    {
        "crime": "Selling counterfeit potions to tourists",
        "bounty": True,
        "areas": ["City"],
    },
    {
        "crime": "Impersonating a city official",
        "bounty": False,
        "areas": ["City"],
    },
    {
        "crime": "Stealing from the municipal treasury",
        "bounty": True,
        "areas": ["City"],
    },
    {
        "crime": "Vandalizing public property",
        "bounty": False,
        "areas": ["City"],
    },
    {
        "crime": "Running an unlicensed gambling den",
        "bounty": True,
        "areas": ["City"],
    },

    # === Forest crimes ===
    {
        "crime": "Illegal logging of protected trees",
        "bounty": True,
        "areas": ["Forest"],
    },
    {
        "crime": "Poaching endangered creatures",
        "bounty": True,
        "areas": ["Forest"],
    },
    {
        "crime": "Setting unauthorized forest fires",
        "bounty": False,
        "areas": ["Forest"],
    },
    {
        "crime": "Trespassing on sacred groves",
        "bounty": False,
        "areas": ["Forest"],
    },
    {
        "crime": "Disturbing the peace of woodland spirits",
        "bounty": True,
        "areas": ["Forest"],
    },

    # === Cave crimes ===
    {
        "crime": "Looting ancient burial chambers",
        "bounty": True,
        "areas": ["Cave"],
    },
    {
        "crime": "Hoarding precious gemstones from the public",
        "bounty": False,
        "areas": ["Cave"],
    },
    {
        "crime": "Disturbing the ecosystem of blind cave fish",
        "bounty": False,
        "areas": ["Cave"],
    },
    {
        "crime": "Illegal excavation of rare minerals",
        "bounty": True,
        "areas": ["Cave"],
    },

    # === Swamp crimes ===
    {
        "crime": "Leaking toxic sludge into the waterways",
        "bounty": True,
        "areas": ["Swamp"],
    },
    {
        "crime": "Harvesting endangered swamp herbs",
        "bounty": False,
        "areas": ["Swamp"],
    },
    {
        "crime": "Harboring fugitives in the marshes",
        "bounty": True,
        "areas": ["Swamp"],
    },
    {
        "crime": "Conducting unauthorized voodoo rituals",
        "bounty": False,
        "areas": ["Swamp"],
    },
]
