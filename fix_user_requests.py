import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update font imports to include Poppins
old_fonts = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&display=swap" rel="stylesheet">'
new_fonts = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@200;300;400;500;600;700&family=Poppins:wght@200;300;400;500;600;700&display=swap" rel="stylesheet">'
html = html.replace(old_fonts, new_fonts)

# 2. Update .nt-bg to use background image
old_bg = """        .nt-bg {
            background: linear-gradient(135deg, #0d0f18 0%, #111827 40%, #0d1117 70%, #161c2a 100%) !important;
            animation: none !important;
        }"""
new_bg = """        .nt-bg {
            background: url('images/backround.jpg') center/cover no-repeat !important;
            animation: none !important;
        }"""
html = html.replace(old_bg, new_bg)

# 3. Update .nt-brand font-family
old_brand = """            font-family: 'Inter', var(--ui), sans-serif;
            text-transform: lowercase;
            opacity: 0.88;
            text-indent: 0.55em;"""
new_brand = """            font-family: 'Poppins', 'Inter', var(--ui), sans-serif !important;
            text-transform: lowercase;
            opacity: 0.88;
            text-indent: 0.55em;"""
html = html.replace(old_brand, new_brand)

# 4. Z-index for .nt-engine-dropdown
old_dropdown = """        .nt-engine-dropdown {
            position: absolute;
            top: calc(100% + 8px);"""
new_dropdown = """        .nt-engine-dropdown {
            position: absolute;
            z-index: 999;
            top: calc(100% + 8px);"""
html = html.replace(old_dropdown, new_dropdown)

# 5. Fix updateTabUrl
old_updateTabUrl = """            function updateTabUrl(url) {
                const tab = getActiveTab();
                if (tab) {
                    tab.url = url;
                    tab.history = [...hist];
                    tab.historyIndex = histIdx;
                    saveTabs();
                    renderTabs(); 
                }
            }"""
new_updateTabUrl = """            function updateTabUrl(url) {
                const tab = getActiveTab();
                if (tab) {
                    if (url && typeof url === 'string' && url.includes('playhop')) tab._gamesOverride = true;
                    if (tab._gamesOverride) {
                        url = "rift://games";
                        urlInput.value = url;
                    }
                    tab.url = url;
                    tab.history = [...hist];
                    tab.historyIndex = histIdx;
                    saveTabs();
                    renderTabs(); 
                }
            }"""
html = html.replace(old_updateTabUrl, new_updateTabUrl)

# 6. Fix setTabTitle
old_setTabTitle = """            function setTabTitle(text) {
                const title = text || "New Tab";
                if (tabTitle) tabTitle.textContent = title;
                const tab = getActiveTab();
                if (tab) {
                    tab.title = title;
                    renderTabs();
                    saveTabs();
                }
            }"""
new_setTabTitle = """            function setTabTitle(text) {
                let title = text || "New Tab";
                const tab = getActiveTab();
                if (tab && tab._gamesOverride) title = "Games";
                if (tabTitle) tabTitle.textContent = title;
                if (tab) {
                    tab.title = title;
                    renderTabs();
                    saveTabs();
                }
            }"""
html = html.replace(old_setTabTitle, new_setTabTitle)

# 7. Hack to also catch direct input modifications inside `d.t === "n"` and `d.t === "uc"`
# Instead of replacing specific chunks, we can add a mutation observer or just replace `urlInput.value =` with a wrapper.
# A simpler way is to just wrap `urlInput.value =` where it occurs in the message listener.
# Let's replace the listener assignment directly.
html = html.replace("urlInput.value = cleaned;", "urlInput.value = (getActiveTab() && getActiveTab()._gamesOverride) ? 'rift://games' : cleaned;")
html = html.replace("urlInput.value = d.u;", "if (d.u.includes('playhop')) { const _t = getActiveTab(); if(_t) _t._gamesOverride = true; } urlInput.value = (getActiveTab() && getActiveTab()._gamesOverride) ? 'rift://games' : d.u;")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done!")
