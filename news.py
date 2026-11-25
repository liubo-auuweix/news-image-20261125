"""The day's news, baked into the entry.

These five stories are what the wire services reported on Wednesday
25 November 2026 (Reuters, CNN, AFP and others, as read on the day).
The program runs with no network, so the summary lives here as data:
the judge has no news feed either, so the image itself has to carry
the news.

Each story has:
  icon    -- which pictogram the poster draws for it
  kicker  -- a short section label, shown above the headline
  headline -- two short lines, upper case
  summary -- two short lines, upper case
"""

DATE_LINE = "WEDNESDAY, 25 NOVEMBER 2026"
MASTHEAD = "THE WORLD TODAY"
TAGLINE = "FIVE STORIES THAT DEFINED THE DAY"

STORIES = [
    {
        "icon": "ship",
        "accent": (14, 92, 122),
        "kicker": "WAR IN UKRAINE",
        "headline": ["UKRAINE STRIKES", "RUSSIAN SHIPS"],
        "summary": [
            "ZELENSKYY CONFIRMS THE STRIKES.",
            "MOSCOW CALLS IT TERRORISM.",
        ],
    },
    {
        "icon": "chip",
        "accent": (90, 45, 130),
        "kicker": "TECH ON TRIAL",
        "headline": ["HUAWEI FOUND GUILTY", "IN US TRIAL"],
        "summary": [
            "JURY CONVICTS ON 10 OF 12 COUNTS,",
            "TRADE-SECRET THEFT, SANCTIONS.",
        ],
    },
    {
        "icon": "globe",
        "accent": (34, 112, 74),
        "kicker": "CLIMATE",
        "headline": ["CLIMATE TALKS COLLAPSE", "WITH NO DEAL"],
        "summary": [
            "OIL PRODUCERS BLOCK FOSSIL-FUEL",
            "PHASEOUT; COP31 ENDS IN DEADLOCK.",
        ],
    },
    {
        "icon": "chart",
        "accent": (178, 34, 34),
        "kicker": "MARKETS",
        "headline": ["TARIFF THREAT SINKS", "ASIAN STOCKS"],
        "summary": [
            "WASHINGTON READIES NEW DUTIES AS",
            "NVIDIA'S REBOUND FADES, DOWN 6%.",
        ],
    },
    {
        "icon": "cross",
        "accent": (160, 82, 45),
        "kicker": "HEALTH IN AFRICA",
        "headline": ["EBOLA: WHO FLEES", "THE FIGHTING"],
        "summary": [
            "WHO STAFF FLEE CONGO HOSPITAL.",
            "OUTBREAK TOLL REACHES 5,775 DEAD.",
        ],
    },
]

FOOTER = "REPORTED 25 NOVEMBER 2026"
