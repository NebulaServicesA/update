import sys

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Z-index fix for .nt-search
html = html.replace('        .nt-search {\n            display: flex;\n', '        .nt-search {\n            display: flex;\n            z-index: 10;\n')

# 2. Add .nt-dock CSS
nt_dock_css = """
        .nt-dock {
            position: absolute;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 18px;
            background: rgba(15, 25, 20, 0.85);
            border: 1px solid rgba(100, 255, 150, 0.15);
            border-radius: 40px;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            z-index: 50;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        .nt-dock-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 44px;
            height: 44px;
            border-radius: 12px;
            border: none;
            background: transparent;
            color: #6a9c78;
            font-size: 20px;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(.34,1.56,.64,1);
        }
        .nt-dock-btn:hover {
            background: rgba(100, 255, 150, 0.1);
            color: #8fdfa8;
            transform: translateY(-3px) scale(1.05);
        }
        .nt-dock-btn.active {
            background: rgba(100, 255, 150, 0.15);
            color: #bbfadd;
            border-radius: 14px;
        }
        .nt-dock-divider {
            width: 1px;
            height: 24px;
            background: rgba(100, 255, 150, 0.15);
            margin: 0 4px;
        }
"""
html = html.replace("        .nt-search-engine:hover {", nt_dock_css + "\n        .nt-search-engine:hover {")

# 3. Add .nt-dock HTML inside .newtab
nt_dock_html = """
                    <div class="nt-dock">
                        <button class="nt-dock-btn" onclick="createTab('rift://newtab')" title="Home"><i class="fas fa-home"></i></button>
                        <button class="nt-dock-btn" onclick="createTab('rift://games')" title="Games"><i class="fas fa-gamepad"></i></button>
                        <button class="nt-dock-btn" onclick="createTab('rift://apps')" title="Apps"><i class="fas fa-grip-vertical"></i></button>
                        <button class="nt-dock-btn" onclick="createTab('https://discord.com')" title="Chat"><i class="fas fa-comment"></i></button>
                        <button class="nt-dock-btn" onclick="document.getElementById('ntSearchInput').focus()" title="Web"><i class="fas fa-globe"></i></button>
                        <div class="nt-dock-divider"></div>
                        <button class="nt-dock-btn" onclick="createTab('rift://settings')" title="Settings"><i class="fas fa-cog"></i></button>
                        <button class="nt-dock-btn" onclick="document.getElementById('tabCloakBtn').click()" title="Tab Cloaking"><i class="fas fa-shield-halved"></i></button>
                        <button class="nt-dock-btn" onclick="closeActiveTab()" title="Close Tab"><i class="fas fa-times"></i></button>
                    </div>
"""
# insert before <div class="nt-overlay"></div>
html = html.replace('<div class="nt-overlay"></div>', '<div class="nt-overlay"></div>\n' + nt_dock_html)


# 4. Modify showNewTab signature
old_showNewTab = "function showNewTab(push = true) {"
new_showNewTab = "function showNewTab(targetUrl = HOME_INTERNAL, push = true) {"
html = html.replace(old_showNewTab, new_showNewTab)

html = html.replace('urlInput.value = HOME_INTERNAL;', 'urlInput.value = targetUrl;')
html = html.replace('pageUrl = HOME_INTERNAL;', 'pageUrl = targetUrl;')
html = html.replace('updateSecurityChip(HOME_INTERNAL);', 'updateSecurityChip(targetUrl);')
html = html.replace('updateTabUrl(HOME_INTERNAL);', 'updateTabUrl(targetUrl);')
html = html.replace('hist.push(HOME_INTERNAL);', 'hist.push(targetUrl);')

# Also need to fix where showNewTab is called without URL but we want the current URL.
# Wait, existing calls without arguments will default to HOME_INTERNAL which is fine for the home button.
# Let's fix go() function intercept
go_games_old = """if (url === GAMES_INTERNAL) {
                    if (activeTabId === initiatorTabId) {
                        // Override: load playhop but display rift://games in bar
                        const gamesTabId = activeTabId;
                        const gTab = tabs.find(t => t.id === gamesTabId);
                        if (gTab) { gTab._gamesOverride = true; }
                        // Navigate to real URL, then patch the display
                        go("https://playhop.com/", push).then(() => {
                            const gt = tabs.find(t => t.id === gamesTabId);
                            if (gt) { gt.title = "Games"; gt.url = "rift://games"; }
                            if (activeTabId === gamesTabId) {
                                urlInput.value = "rift://games";
                                document.title = "Games";
                            }
                            renderTabs();
                        }).catch(() => {});
                    }
                    return;
                }"""
go_games_new = """if (url === GAMES_INTERNAL || url === "rift://apps") {
                    if (activeTabId === initiatorTabId) showNewTab(url, push);
                    return;
                }"""
html = html.replace(go_games_old, go_games_new)

# 5. Overhaul renderFavorites
render_fav_old_start = html.find("function renderFavorites() {")
render_fav_old_end = html.find("let _gustAnimLocked = false;")

new_renderFavs = """function renderFavorites() {
    if (!ntFavorites) return;
    ntFavorites.innerHTML = "";

    ntFavorites.style.cssText = "display:flex;flex-wrap:wrap;justify-content:center;max-width:850px;margin:40px auto 0;gap:12px;padding:0 20px;z-index:2;position:relative;";
    if (pageUrl === "rift://games" || pageUrl === "rift://apps") {
        ntFavorites.style.cssText += "max-width: 1000px; max-height: 50vh; overflow-y: auto; padding-bottom: 80px;";
    }

    let items = [];
    if (pageUrl === "rift://apps") {
        setTabTitle("Apps");
        for (let i = 1; i <= 40; i++) {
            let hue = (i * 25) % 360;
            items.push({ name: `App ${i}`, url: `https://example.com/app${i}`, bg: `hsl(${hue}, 40%, 15%)`, color: `hsl(${hue}, 80%, 80%)`, icon: `<i class="fas fa-cube" style="font-size:18px;"></i> <span style="font-weight:700;">App ${i}</span>` });
        }
        // Inject some real apps
        items[0] = { name: "Spotify", url: "https://open.spotify.com/", bg: "#1DB954", color: "#fff", icon: '<i class="fab fa-spotify" style="font-size:18px;"></i> <span style="font-weight:700;letter-spacing:-0.5px;">Spotify</span>' };
        items[1] = { name: "Discord", url: "https://discord.com/", bg: "#5865F2", color: "#fff", icon: '<i class="fab fa-discord" style="font-size:18px;"></i> <span style="font-weight:800;">Discord</span>' };
        items[2] = { name: "ChatGPT", url: "https://chat.openai.com/", bg: "#10A37F", color: "#fff", icon: '<i class="fas fa-robot" style="font-size:18px;"></i> <span style="font-weight:600;">ChatGPT</span>' };
        items[3] = { name: "GitHub", url: "https://github.com/", bg: "#000000", color: "#fff", icon: '<i class="fab fa-github" style="font-size:18px;"></i> <span style="font-weight:700;">GitHub</span>' };
        
    } else if (pageUrl === "rift://games") {
        setTabTitle("Games");
        for (let i = 1; i <= 70; i++) {
            let hue = (i * 35) % 360;
            items.push({ name: `Game ${i}`, url: `https://example.com/game${i}`, bg: `hsl(${hue}, 40%, 15%)`, color: `hsl(${hue}, 80%, 80%)`, icon: `<i class="fas fa-gamepad" style="font-size:18px;"></i> <span style="font-weight:700;">Game ${i}</span>` });
        }
        // Inject some real games
        items[0] = { name: "Playhop", url: "https://playhop.com", bg: "#1a1a1a", color: "#fff", icon: '<i class="fas fa-gamepad" style="font-size:18px;color:#a040ff;"></i> <span style="font-weight:700;">Playhop</span>' };
        items[1] = { name: "Y8", url: "https://y8.com", bg: "#CC0000", color: "#fff", icon: '<span style="font-weight:900;font-style:italic;">Y8</span>' };
        items[2] = { name: "Poki", url: "https://poki.com", bg: "#333", color: "#fff", icon: '<span style="font-weight:900;font-style:italic;">Poki</span>' };
    } else {
        items = [
            { name: "Games", url: "rift://games", bg: "#1a1a1a", color: "#fff", icon: '<i class="fas fa-gamepad" style="font-size:18px;color:#a040ff;"></i> <span style="font-weight:700;">Games</span>' },
            { name: "Apps", url: "rift://apps", bg: "#1a1a1a", color: "#fff", icon: '<i class="fas fa-grip-vertical" style="font-size:18px;color:#40a0ff;"></i> <span style="font-weight:700;">Apps</span>' },
            { name: "Google", url: "https://google.com/", bg: "#ffffff", color: "#4285F4", icon: '<i class="fab fa-google"></i> <span style="color:#EA4335">o</span><span style="color:#FBBC05">o</span><span style="color:#4285F4">g</span><span style="color:#34A853">l</span><span style="color:#EA4335">e</span>' },
            { name: "YouTube", url: "https://youtube.com/", bg: "#ffffff", color: "#000", icon: '<i class="fab fa-youtube" style="color:#FF0000;font-size:18px;"></i> <span style="font-weight:700;letter-spacing:-0.5px;">YouTube</span>' },
            { name: "Spotify", url: "https://open.spotify.com/", bg: "#1DB954", color: "#fff", icon: '<i class="fab fa-spotify" style="font-size:18px;"></i> <span style="font-weight:700;letter-spacing:-0.5px;">Spotify</span>' },
            { name: "Discord", url: "https://discord.com/", bg: "#5865F2", color: "#fff", icon: '<i class="fab fa-discord" style="font-size:18px;"></i> <span style="font-weight:800;">Discord</span>' },
            { name: "ChatGPT", url: "https://chat.openai.com/", bg: "#10A37F", color: "#fff", icon: '<i class="fas fa-robot" style="font-size:18px;"></i> <span style="font-weight:600;">ChatGPT</span>' },
            { name: "GeForce Now", url: "https://play.geforcenow.com/", bg: "#76B900", color: "#000", icon: '<span style="font-weight:900;font-style:italic;letter-spacing:-0.5px;">GEFORCE NOW</span>' },
            { name: "GitHub", url: "https://github.com/", bg: "#000000", color: "#fff", icon: '<i class="fab fa-github" style="font-size:18px;"></i> <span style="font-weight:700;">GitHub</span>' },
            { name: "Twitch", url: "https://twitch.tv/", bg: "#9146FF", color: "#fff", icon: '<i class="fab fa-twitch" style="font-size:18px;"></i> <span style="font-weight:800;">twitch</span>' },
            { name: "ESPN", url: "https://espn.com/", bg: "#CC0000", color: "#fff", icon: '<span style="font-weight:900;font-style:italic;font-size:18px;letter-spacing:-1px;">ESPN</span>' },
            { name: "TikTok", url: "https://tiktok.com/", bg: "#000000", color: "#fff", icon: '<i class="fab fa-tiktok" style="font-size:16px;"></i> <span style="font-weight:700;">TikTok</span>' }
        ];
    }

    items.forEach(app => {
        const div = document.createElement("div");
        div.style.cssText = `display:flex;align-items:center;justify-content:center;gap:8px;cursor:pointer;padding:0 24px;height:64px;border-radius:12px;background:${app.bg};color:${app.color};transition:transform 0.2s cubic-bezier(0.34,1.56,0.64,1), filter 0.2s;min-width:140px;box-shadow:0 4px 15px rgba(0,0,0,0.4);font-family:'Inter',sans-serif;`;
        
        div.onmouseenter = () => {
            div.style.transform = "translateY(-4px)";
            div.style.filter = "brightness(1.1)";
        };
        div.onmouseleave = () => {
            div.style.transform = "translateY(0)";
            div.style.filter = "brightness(1)";
        };
        div.onclick = () => go(app.url);
        
        div.innerHTML = app.icon;
        ntFavorites.appendChild(div);
    });
}
"""
html = html[:render_fav_old_start] + new_renderFavs + html[render_fav_old_end:]

# Add helper for closing active tab logic from dock
close_tab_js = """function closeActiveTab() {
    const tabId = activeTabId;
    if (tabId) {
        closeTab(tabId);
    }
}
"""
html = html.replace('function closeTab(id) {', close_tab_js + '\n            function closeTab(id) {')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done!")
