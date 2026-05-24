import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

print("Step 1: Expose functions globally...")
# Find the end of the IIFE and expose the functions before it closes
iife_end = html.rfind("init();\n        })();")
if iife_end != -1:
    exposure_code = """init();
            window.go = go;
            window.createTab = createTab;
            window.closeActiveTab = closeActiveTab;
        })();"""
    html = html[:iife_end] + exposure_code + html[iife_end+len("init();\n        })();"):]
    print("  Functions exposed.")
else:
    print("  WARNING: Could not find IIFE end.")

print("Step 2: Hide .nt-content when a hub is active...")
html = html.replace(
    'const hubGames = document.getElementById("hubGames");',
    'const hubGames = document.getElementById("hubGames");\n                const ntContent = document.querySelector(".nt-content");'
)
html = html.replace(
    'if (hubGames) { hubGames.classList.add("active"); populateGamesHub(); }',
    'if (hubGames) { hubGames.classList.add("active"); populateGamesHub(); }\n                    if (ntContent) ntContent.style.display = "none";'
)
html = html.replace(
    'if (hubApps) { hubApps.classList.add("active"); populateAppsHub(); }',
    'if (hubApps) { hubApps.classList.add("active"); populateAppsHub(); }\n                    if (ntContent) ntContent.style.display = "none";'
)

# And make sure it is shown again when returning to newtab
html = html.replace(
    'if (hubApps) hubApps.classList.remove("active");\n                _origShowNewTab(push);',
    'if (hubApps) hubApps.classList.remove("active");\n                const ntContent = document.querySelector(".nt-content");\n                if (ntContent) ntContent.style.display = "";\n                _origShowNewTab(push);'
)
print("  .nt-content hide/show added.")

print("Step 3: Change themes to Blue...")
html = html.replace('color: #6a9c78;', 'color: #5a8bd8;')
html = html.replace('background: rgba(100, 255, 150, 0.1);', 'background: rgba(80, 180, 255, 0.1);')
html = html.replace('color: #8fdfa8;', 'color: #85c2ff;')
html = html.replace('background: rgba(100, 255, 150, 0.15);', 'background: rgba(80, 180, 255, 0.15);')
html = html.replace('color: #bbfadd;', 'color: #bde0ff;')
html = html.replace('border: 1px solid rgba(100, 255, 150, 0.15);', 'border: 1px solid rgba(80, 180, 255, 0.15);')
html = html.replace('background: rgba(100, 255, 150, 0.15);', 'background: rgba(80, 180, 255, 0.15);')
print("  Dock theme changed to blue.")

print("Step 4: Update renderFavorites default items...")
old_items_code = """items = [
            { name: "Games", url: "rift://games", bg: "#1a1a1a", color: "#fff", icon: '<i class="fas fa-gamepad" style="font-size:18px;color:#a040ff;"></i> <span style="font-weight:700;">Games</span>' },
            { name: "Apps", url: "rift://apps", bg: "#1a1a1a", color: "#fff", icon: '<i class="fas fa-grip-vertical" style="font-size:18px;color:#40a0ff;"></i> <span style="font-weight:700;">Apps</span>' },"""
new_items_code = """items = [
            { name: "Games", url: "https://playhop.com", bg: "#1a1a1a", color: "#fff", icon: '<i class="fas fa-gamepad" style="font-size:18px;color:#40a0ff;"></i> <span style="font-weight:700;">Games</span>' },"""
html = html.replace(old_items_code, new_items_code)
print("  Apps removed from home, Games goes to Playhop.")

print("Step 5: Inject real icons for hubs...")
# In populateGamesHub, instead of emoji, inject an image if available, else emoji
img_html_games = "`<img src='https://www.google.com/s2/favicons?domain=${new URL(game.url).hostname}&sz=64' onerror='this.style.display=\"none\";this.nextElementSibling.style.display=\"flex\";' style='width:32px;height:32px;border-radius:8px;'><div class=\"hub-icon\" style=\"display:none;background:${game.color};\">${game.icon}</div><span>${game.name}</span>`"
html = html.replace(
    'card.innerHTML = `<div class="hub-icon" style="background:${game.color};">${game.icon}</div><span>${game.name}</span>`;',
    f'card.innerHTML = {img_html_games};'
)

img_html_apps = "`<img src='https://www.google.com/s2/favicons?domain=${new URL(app.url).hostname}&sz=64' onerror='this.style.display=\"none\";this.nextElementSibling.style.display=\"flex\";' style='width:32px;height:32px;border-radius:8px;'><div class=\"hub-icon\" style=\"display:none;background:${app.color};color:${app.textColor || '#fff'}\">${app.icon}</div><span>${app.name}</span>`"
html = html.replace(
    'card.innerHTML = `<div class="hub-icon" style="background:${app.color};color:${app.textColor || \'#fff\'};">${app.icon}</div><span>${app.name}</span>`;',
    f'card.innerHTML = {img_html_apps};'
)
print("  Hub cards updated to use real favicons.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done!")
