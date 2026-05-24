import sys
import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# ============================================================
# 1. Handle rift://games as a special internal URL
# ============================================================
# Add GAMES_INTERNAL constant after HOME_INTERNAL
html = html.replace(
    'const HOME_INTERNAL = "rift://newtab";',
    'const HOME_INTERNAL = "rift://newtab";\n            const GAMES_INTERNAL = "rift://games";'
)

# In normUrl, recognize rift://games
html = html.replace(
    'if (/^rift:\\/\\/newtab$/i.test(u) || /^about:newtab$/i.test(u)) return HOME_INTERNAL;',
    'if (/^rift:\\/\\/newtab$/i.test(u) || /^about:newtab$/i.test(u)) return HOME_INTERNAL;\n                if (/^rift:\\/\\/games$/i.test(u)) return GAMES_INTERNAL;'
)

# In renderFavorites, make Games use rift://games
html = html.replace(
    '{ name: "Games", url: "https://playhop.com/", img: "https://play-lh.googleusercontent.com/r8BVvJL1St5IL8r0ZEMDjz8xKUEVOg9qOeuKpB9bw49Raoq9A1GAF6jaUcEL1XvsPi83=w480-h960-rw" }',
    '{ name: "Games", url: "rift://games", img: "https://play-lh.googleusercontent.com/r8BVvJL1St5IL8r0ZEMDjz8xKUEVOg9qOeuKpB9bw49Raoq9A1GAF6jaUcEL1XvsPi83=w480-h960-rw" }'
)

# In the go() function, handle rift://games - load playhop.com via proxy but show rift://games in URL
go_home_block = 'if (url === HOME_INTERNAL) {\n                    if (activeTabId === initiatorTabId) showNewTab(push);\n                    return;\n                }'
games_block = '''if (url === GAMES_INTERNAL) {
                    if (activeTabId === initiatorTabId) {
                        hideNewTab();
                        hideSettingsPage();
                        urlInput.value = "rift://games";
                        setTabTitle("Games");
                        const tab = tabs.find(t => t.id === activeTabId);
                        if (tab) { tab.title = "Games"; tab.url = "rift://games"; }
                        renderTabs();
                        // Load playhop through the proxy
                        const realUrl = "https://playhop.com/";
                        const normReal = normUrl(realUrl);
                        if (normReal) {
                            const prevCtrl = tabAbortControllers.get(activeTabId);
                            if (prevCtrl) prevCtrl.abort();
                            const ctrl = new AbortController();
                            tabAbortControllers.set(activeTabId, ctrl);
                            fetchAndRender(normReal, "GET", null, ctrl.signal);
                        }
                    }
                    return;
                }'''
html = html.replace(go_home_block, go_home_block + "\n                " + games_block)

# Make rift://games not trigger error page (not invalid internal)
html = html.replace(
    'if (!url || !url.startsWith("rift://")) return false;\n                if (url === HOME_INTERNAL || url === SETTINGS_INTERNAL) return false;',
    'if (!url || !url.startsWith("rift://")) return false;\n                if (url === HOME_INTERNAL || url === SETTINGS_INTERNAL || url === GAMES_INTERNAL) return false;'
)

# Fix security chip for games page
html = html.replace(
    'if (!url || url === HOME_INTERNAL || isSettingsPage(url) || url.startsWith("rift://")) {',
    'if (!url || url === HOME_INTERNAL || url === GAMES_INTERNAL || isSettingsPage(url) || url.startsWith("rift://")) {'
)

# ============================================================
# 2. Redesign the new tab page CSS — xylora-style
# ============================================================
old_brand_css = """.nt-brand {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 16px;
            color: var(--ac);
            font-weight: 700;
            font-size: 4.5rem;
            letter-spacing: 0.02em;
            margin-bottom: -15px;
            margin-top: 40px;
            line-height: 1;
        }"""

new_brand_css = """.nt-brand {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0;
            color: var(--ac);
            font-weight: 300;
            font-size: 5rem;
            letter-spacing: 0.45em;
            margin-bottom: 0;
            margin-top: 30px;
            line-height: 1;
            font-family: 'Inter', var(--ui), sans-serif;
            text-transform: lowercase;
            opacity: 0.92;
        }"""
html = html.replace(old_brand_css, new_brand_css)

# Remove the wind icon from brand
html = html.replace(
    '<i class="fas fa-wind gust-icon-anim" style="margin-right: -4px;"></i>\n                            <span style="letter-spacing: 3px; display:inline-flex;">',
    '<span style="letter-spacing: 0.45em; display:inline-flex;">'
)

# Update nt-search style for xylora look
old_search_css = """.nt-search {
            display: flex;
            gap: 10px;
            align-items: center;
            position: relative;
            width: min(700px, 100%);
            margin-top: 40px;
        }"""
new_search_css = """.nt-search {
            display: flex;
            gap: 10px;
            align-items: center;
            position: relative;
            width: min(640px, 92%);
            margin-top: 45px;
        }"""
html = html.replace(old_search_css, new_search_css)

# Style the nt-search input for xylora look
old_search_input = """.nt-search input {"""
# Find it in context
search_input_block_old = """        .nt-search input {"""
idx = html.find(".nt-search input {")
if idx != -1:
    end = html.find("}", idx)
    old_block = html[idx:end+1]
    new_block = """.nt-search input {
            flex: 1;
            height: 50px;
            padding: 0 20px;
            border-radius: 30px;
            border: 1px solid rgba(255, 255, 255, 0.18);
            background: rgba(255, 255, 255, 0.07);
            color: var(--tx);
            font-size: 15px;
            font-family: 'Inter', var(--ui), sans-serif;
            font-weight: 400;
            outline: none;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            transition: all 0.25s ease;
            letter-spacing: 0.01em;
        }"""
    html = html[:idx] + new_block + html[end+1:]

# Style search input focus
idx2 = html.find(".nt-search input:focus {")
if idx2 != -1:
    end2 = html.find("}", idx2)
    html = html[:idx2] + """.nt-search input:focus {
            border-color: rgba(255, 255, 255, 0.35);
            background: rgba(255, 255, 255, 0.12);
            box-shadow: 0 0 0 3px rgba(255,255,255,0.06);
        }""" + html[end2+1:]

# Style placeholder
idx3 = html.find(".nt-search input::placeholder {")
if idx3 != -1:
    end3 = html.find("}", idx3)
    html = html[:idx3] + """.nt-search input::placeholder {
            color: rgba(255, 255, 255, 0.35);
            font-weight: 300;
        }""" + html[end3+1:]

# ============================================================
# 3. Remove "Made with love" Nautilus credit
# ============================================================
html = html.replace(
    '<div id="gustCredit"',
    '<div id="gustCredit" style="display:none!important;"'
)

# ============================================================
# 4. Inject a Google Fonts Inter link into the FIRST <head>
# ============================================================
font_link = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&display=swap" rel="stylesheet">'
# Only inject if not already present
if 'fonts.googleapis.com' not in html[:html.find('</head>') + 20]:
    first_head_end = html.find('</head>')
    html = html[:first_head_end] + '\n    ' + font_link + '\n' + html[first_head_end:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done!")
