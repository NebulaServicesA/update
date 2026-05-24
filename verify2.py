with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

checks = [
    ("GAMES_INTERNAL defined",          "const GAMES_INTERNAL"),
    ("rift://games routed",             "go(\"https://playhop.com/\", push)"),
    ("Brand is lowercase rift",         ">r</span>"),
    ("Brand no wind icon",              "gust-icon-anim"),
    ("Inter font loaded",               "fonts.googleapis.com"),
    ("Animated background",             "brandFade"),
    ("Search bar glass pill",           "searchFade"),
    ("App icons staggered animation",   "fadeUp"),
    ("Credit removed",                  "credit removed"),
    ("Search icon injected",            "fa-magnifying-glass"),
]

for name, pattern in checks:
    found = pattern in html
    print(f"[{'OK' if found else 'MISSING'}] {name}")
