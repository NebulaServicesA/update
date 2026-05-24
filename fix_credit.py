import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Remove the entire gustCredit div
html = re.sub(
    r'<div id="gustCredit"[\s\S]*?Made with.*?Nautilus Labs\s*</div>',
    "<!-- credit removed -->",
    html
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done!")
