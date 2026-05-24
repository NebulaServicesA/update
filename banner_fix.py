import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update the CSS for rift-hub-card
old_css = """.rift-hub-card {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
            color: var(--tx);
        }
        .rift-hub-card:hover {
            background: var(--surface);
            border-color: rgba(255,255,255,0.15);
            transform: translateY(-2px);
        }
        .rift-hub-card .hub-icon {
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }
        .rift-hub-card span {
            font-weight: 500;
            font-size: 14px;
            flex: 1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }"""

new_css = """.rift-hub-card {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 0;
            background: var(--surface2);
            border: 2px solid transparent;
            border-radius: 14px;
            cursor: pointer;
            transition: all 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
            color: var(--tx);
            position: relative;
            overflow: hidden;
            aspect-ratio: 16 / 9;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        .rift-hub-card:hover {
            border-color: rgba(80, 180, 255, 0.5);
            transform: scale(1.05) translateY(-4px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.5);
            z-index: 10;
        }
        .rift-hub-card img.banner {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s;
        }
        .rift-hub-card:hover img.banner {
            transform: scale(1.08);
        }
        .rift-hub-card .hub-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(to top, rgba(0,0,0,0.9), transparent);
            padding: 20px 10px 8px;
            text-align: center;
            opacity: 0;
            transition: opacity 0.2s;
            pointer-events: none;
        }
        .rift-hub-card:hover .hub-overlay {
            opacity: 1;
        }
        .rift-hub-card span {
            font-weight: 700;
            font-size: 14px;
            color: #fff;
            text-shadow: 0 2px 4px rgba(0,0,0,0.8);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            display: block;
        }
        .rift-hub-card .hub-icon {
            display: none !important;
        }"""

if old_css in html:
    html = html.replace(old_css, new_css)
else:
    print("WARNING: Could not find old CSS block")

# 2. Update Grid CSS
old_grid = """.rift-hub-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 16px;
            width: 100%;
            max-width: 1100px;
            margin: 0 auto;
        }"""
new_grid = """.rift-hub-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 20px;
            width: 100%;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }"""
html = html.replace(old_grid, new_grid)

# 3. Update JavaScript innerHTML for games and apps
# We will use Bing Image Search thumbnail API to get banners dynamically.
games_regex = r"card\.innerHTML = `<img src='https://www\.google\.com/s2/favicons.*?`;"
games_new_html = r"""card.innerHTML = `<img class="banner" src="https://tse2.mm.bing.net/th?q=${encodeURIComponent(game.name + ' game thumbnail banner')}&w=320&h=180&c=7&rs=1&p=0" onerror="this.src='https://image.thum.io/get/width/320/crop/180/'+game.url"><div class="hub-overlay"><span>${game.name}</span></div>`;"""
html = re.sub(games_regex, games_new_html, html)

apps_regex = r"card\.innerHTML = `<img src='https://www\.google\.com/s2/favicons.*?`;"
# Since apps regex is same, we need to match it contextually or just let it replace both!
# Actually, the replacement for apps has app.url, game has game.url.
# Let's just do an exact replace.

html = re.sub(
    r"card\.innerHTML = `<img src='https://www\.google\.com/s2/favicons\?domain=\$\{new URL\(game\.url\)\.hostname\}&sz=64'.*?`;",
    r"card.innerHTML = `<img class=\"banner\" loading=\"lazy\" src=\"https://tse2.mm.bing.net/th?q=${encodeURIComponent(game.name + ' unblocked game banner')} &w=320&h=180&c=7&rs=1&p=0\" onerror=\"this.src='https://image.thum.io/get/width/320/crop/180/'+game.url\"><div class=\"hub-overlay\"><span>${game.name}</span></div>`;",
    html
)

html = re.sub(
    r"card\.innerHTML = `<img src='https://www\.google\.com/s2/favicons\?domain=\$\{new URL\(app\.url\)\.hostname\}&sz=64'.*?`;",
    r"card.innerHTML = `<img class=\"banner\" loading=\"lazy\" src=\"https://tse2.mm.bing.net/th?q=${encodeURIComponent(app.name + ' logo wallpaper')} &w=320&h=180&c=7&rs=1&p=0\" onerror=\"this.src='https://image.thum.io/get/width/320/crop/180/'+app.url\"><div class=\"hub-overlay\"><span>${app.name}</span></div>`;",
    html
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Banners applied!")
