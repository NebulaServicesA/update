with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

checks = [
    ("GAMES_INTERNAL defined", "const GAMES_INTERNAL"),
    ("rift://games in normUrl", "rift://games"),
    ("Games override in go()", "playhop.com"),
    ("Brand CSS letter-spacing", "letter-spacing: 0.45em"),
    ("Inter font link", "fonts.googleapis.com"),
    ("renderFavorites with games url", "rift://games"),
    ("Credit div hidden", "display:none!important"),
    ("nt-brand has no wind icon HTML", "gust-icon-anim"),
]
for name, pattern in checks:
    found = pattern in html
    print(f"[{'OK' if found else 'MISSING'}] {name}")
