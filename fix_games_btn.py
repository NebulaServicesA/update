with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace(
    'onclick="go(\'rift://games\')" title="Games"',
    'onclick="go(\'https://playhop.com\')" title="Games"'
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated Games button link")
