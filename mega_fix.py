import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

print("Step 1: Revert showNewTab signature...")
# Revert showNewTab back to original signature - push only
html = html.replace(
    "function showNewTab(targetUrl = HOME_INTERNAL, push = true) {",
    "function showNewTab(push = true) {"
)
# Revert the targetUrl usages back to HOME_INTERNAL
html = html.replace("urlInput.value = targetUrl;", "urlInput.value = HOME_INTERNAL;")
html = html.replace("pageUrl = targetUrl;", "pageUrl = HOME_INTERNAL;")
html = html.replace("updateSecurityChip(targetUrl);", "updateSecurityChip(HOME_INTERNAL);")
html = html.replace("updateTabUrl(targetUrl);", "updateTabUrl(HOME_INTERNAL);")
html = html.replace("hist.push(targetUrl);", "hist.push(HOME_INTERNAL);")
print("  Done")

print("Step 2: Fix go() routing for games/apps...")
# Replace the bad routing with proper one that calls showHubPage
html = html.replace(
    """if (url === GAMES_INTERNAL || url === "rift://apps") {
                    if (activeTabId === initiatorTabId) showNewTab(url, push);
                    return;
                }""",
    """if (url === GAMES_INTERNAL || url === "rift://apps") {
                    if (activeTabId === initiatorTabId) showHubPage(url, push);
                    return;
                }"""
)
print("  Done")

print("Step 3: Fix switchToTab to handle hub pages...")
html = html.replace(
    """if (tab.url === HOME_INTERNAL) {
                    showNewTab(false);
                } else if (isSettingsPage(tab.url) && !tab.hasError) {""",
    """if (tab.url === HOME_INTERNAL) {
                    showNewTab(false);
                } else if (tab.url === "rift://games" || tab.url === "rift://apps") {
                    showHubPage(tab.url, false);
                } else if (isSettingsPage(tab.url) && !tab.hasError) {"""
)
print("  Done")

print("Step 4: Inject showHubPage function + hub CSS after showNewTab function...")
hub_css = """
        /* Hub Pages (Games/Apps) */
        .rift-hub {
            position: absolute;
            inset: 0;
            display: none;
            flex-direction: column;
            align-items: center;
            overflow-y: auto;
            z-index: 5;
            padding: 40px 20px 120px;
        }
        .rift-hub.active { display: flex; }
        .rift-hub-title {
            font-family: 'Poppins', sans-serif;
            font-size: 2rem;
            font-weight: 700;
            color: #fff;
            margin-bottom: 20px;
            letter-spacing: 0.05em;
        }
        .rift-hub-search {
            width: min(560px, 90%);
            padding: 12px 20px;
            border-radius: 30px;
            border: 1px solid rgba(255,255,255,0.12);
            background: rgba(15,15,20,0.7);
            backdrop-filter: blur(12px);
            color: #fff;
            font-size: 15px;
            font-family: 'Inter', sans-serif;
            outline: none;
            margin-bottom: 30px;
            transition: border-color 0.2s;
        }
        .rift-hub-search:focus { border-color: rgba(140,60,255,0.7); }
        .rift-hub-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 14px;
            width: 100%;
            max-width: 1000px;
        }
        .rift-hub-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 10px;
            padding: 20px 12px;
            border-radius: 16px;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.08);
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.34,1.56,0.64,1);
            color: #fff;
            font-family: 'Inter', sans-serif;
            font-size: 12px;
            font-weight: 600;
            text-align: center;
        }
        .rift-hub-card:hover {
            background: rgba(255,255,255,0.12);
            border-color: rgba(140,60,255,0.4);
            transform: translateY(-4px) scale(1.03);
            box-shadow: 0 8px 25px rgba(0,0,0,0.5);
        }
        .rift-hub-card img {
            width: 56px;
            height: 56px;
            border-radius: 12px;
            object-fit: contain;
            background: rgba(255,255,255,0.08);
        }
        .rift-hub-card .hub-icon {
            width: 56px;
            height: 56px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 26px;
        }
"""

# Inject CSS before closing </style> of main styles (find it near line 3600+)
hub_css_marker = "        .nt-dock {"
if hub_css_marker in html:
    html = html.replace(hub_css_marker, hub_css + "\n" + hub_css_marker)
    print("  CSS injected")
else:
    print("  WARNING: CSS marker not found")

# Inject hub HTML after the starsCanvas div
hub_html = """
                    <div class="rift-hub" id="hubGames">
                        <div class="rift-hub-title"><i class="fas fa-gamepad" style="color:#a040ff;margin-right:10px;"></i>Games</div>
                        <input class="rift-hub-search" id="hubGamesSearch" placeholder="Search games..." oninput="filterHub('games',this.value)">
                        <div class="rift-hub-grid" id="hubGamesGrid"></div>
                    </div>
                    <div class="rift-hub" id="hubApps">
                        <div class="rift-hub-title"><i class="fas fa-grip-vertical" style="color:#40a0ff;margin-right:10px;"></i>Apps</div>
                        <input class="rift-hub-search" id="hubAppsSearch" placeholder="Search apps..." oninput="filterHub('apps',this.value)">
                        <div class="rift-hub-grid" id="hubAppsGrid"></div>
                    </div>
"""
html = html.replace(
    '<div class="nt-overlay"></div>',
    '<div class="nt-overlay"></div>' + hub_html
)
print("  Hub HTML injected")

print("Step 5: Inject showHubPage JS function and hub data after showNewTab function...")
hub_js = """
            function showHubPage(url, push = true) {
                if (!newtab) return;
                window._netStall = 0;
                _dropCount = 0;
                hideSettingsPage();
                newtab.classList.add("active");
                frame.style.display = "none";
                overlay.classList.add("hidden");
                if (progressWrap) progressWrap.classList.add("hidden");
                urlInput.value = url;
                pageUrl = url;
                currentDoc = null;
                try { const _ov=$('elemHighlightOverlay'); if(_ov) _ov.style.display='none'; } catch(e) {}
                isErrorPage = false;
                updateSecurityChip(url);
                updateBookmarkButton();
                if (push) {
                    hist = hist.slice(0, histIdx + 1);
                    hist.push(url);
                    histIdx = hist.length - 1;
                    updateNav();
                }
                updateTabUrl(url);
                setStatus("idle", "Ready");

                // Hide all hubs first, then show right one
                const hubGames = document.getElementById("hubGames");
                const hubApps = document.getElementById("hubApps");
                if (hubGames) hubGames.classList.remove("active");
                if (hubApps) hubApps.classList.remove("active");

                if (url === "rift://games") {
                    setTabTitle("Games");
                    if (hubGames) { hubGames.classList.add("active"); populateGamesHub(); }
                } else if (url === "rift://apps") {
                    setTabTitle("Apps");
                    if (hubApps) { hubApps.classList.add("active"); populateAppsHub(); }
                }
            }

            // Make sure hubs are hidden when returning to newtab
            const _origShowNewTab = showNewTab;
            showNewTab = function(push = true) {
                const hubGames = document.getElementById("hubGames");
                const hubApps = document.getElementById("hubApps");
                if (hubGames) hubGames.classList.remove("active");
                if (hubApps) hubApps.classList.remove("active");
                _origShowNewTab(push);
            };

            function filterHub(type, query) {
                const gridId = type === 'games' ? 'hubGamesGrid' : 'hubAppsGrid';
                const grid = document.getElementById(gridId);
                if (!grid) return;
                const q = query.toLowerCase().trim();
                grid.querySelectorAll('.rift-hub-card').forEach(card => {
                    const name = (card.dataset.name || '').toLowerCase();
                    card.style.display = (!q || name.includes(q)) ? '' : 'none';
                });
            }

            let _gamesPopulated = false;
            function populateGamesHub() {
                const grid = document.getElementById('hubGamesGrid');
                if (!grid || _gamesPopulated) return;
                _gamesPopulated = true;

                const games = [
                    { name: "Slope", url: "https://slope.game", color: "#1a1a2e", icon: "🎮" },
                    { name: "1v1.LOL", url: "https://1v1.lol", color: "#0f3460", icon: "🔫" },
                    { name: "Smash Karts", url: "https://smashkarts.io", color: "#1a0a2e", icon: "🏎️" },
                    { name: "Shell Shockers", url: "https://shellshock.io", color: "#1a2e0a", icon: "🥚" },
                    { name: "Krunker", url: "https://krunker.io", color: "#0a1a2e", icon: "🎯" },
                    { name: "Agar.io", url: "https://agar.io", color: "#0a2e0a", icon: "🔵" },
                    { name: "Slither.io", url: "https://slither.io", color: "#2e1a0a", icon: "🐍" },
                    { name: "Moto X3M", url: "https://moto-x3m.io", color: "#2e0a0a", icon: "🏍️" },
                    { name: "Cookie Clicker", url: "https://orteil.dashnet.org/cookieclicker", color: "#2e1a00", icon: "🍪" },
                    { name: "2048", url: "https://play2048.co", color: "#2e2000", icon: "🔢" },
                    { name: "Retro Bowl", url: "https://retrobowl.me", color: "#0a2e1a", icon: "🏈" },
                    { name: "Drift Boss", url: "https://driftboss.io", color: "#2e0a1a", icon: "🚗" },
                    { name: "Paper.io", url: "https://paper-io.com", color: "#1a0a2e", icon: "📄" },
                    { name: "Diep.io", url: "https://diep.io", color: "#0a1a0a", icon: "🔵" },
                    { name: "Bonk.io", url: "https://bonk.io", color: "#2e2e0a", icon: "💥" },
                    { name: "Superhex.io", url: "https://superhex.io", color: "#0a2e2e", icon: "⬡" },
                    { name: "Little Big Snake", url: "https://littlebigsnake.com", color: "#1a2e0a", icon: "🐍" },
                    { name: "Cubecraft", url: "https://minemc.fun", color: "#0a0a2e", icon: "🟩" },
                    { name: "GeoGuessr", url: "https://geoguessr.com", color: "#0a2e0a", icon: "🌍" },
                    { name: "Chess.com", url: "https://chess.com", color: "#2e1a0a", icon: "♟️" },
                    { name: "Lichess", url: "https://lichess.org", color: "#0a0a0a", icon: "♞" },
                    { name: "Wordle", url: "https://www.nytimes.com/games/wordle/index.html", color: "#1a2e1a", icon: "🟩" },
                    { name: "Tetris", url: "https://tetris.com/play-tetris", color: "#0a1a2e", icon: "🟦" },
                    { name: "Run 3", url: "https://www.coolmathgames.com/0-run-3", color: "#2e0a2e", icon: "🏃" },
                    { name: "Fireboy & Watergirl", url: "https://www.coolmathgames.com/0-fireboy-and-watergirl", color: "#2e1a00", icon: "🔥" },
                    { name: "Bloons TD", url: "https://ninja.io", color: "#1a2e00", icon: "🎈" },
                    { name: "Minecraft Classic", url: "https://classic.minecraft.net", color: "#2e2e0a", icon: "⛏️" },
                    { name: "Gartic Phone", url: "https://garticphone.com", color: "#0a2e1a", icon: "📞" },
                    { name: "Skribbl.io", url: "https://skribbl.io", color: "#0a1a2e", icon: "✏️" },
                    { name: "Jackbox", url: "https://jackboxgames.com", color: "#2e0a0a", icon: "🎭" },
                    { name: "Town of Salem", url: "https://blankmediagames.com", color: "#1a0a0a", icon: "🧙" },
                    { name: "Catan Universe", url: "https://catanuniverse.com", color: "#2e1a00", icon: "🎲" },
                    { name: "Sploop.io", url: "https://sploop.io", color: "#0a2e0a", icon: "⚔️" },
                    { name: "ZombsRoyale", url: "https://zombsroyale.io", color: "#2e0a0a", icon: "🧟" },
                    { name: "Warbrokers", url: "https://warbrokers.io", color: "#0a0a2e", icon: "💣" },
                    { name: "Yohoho.io", url: "https://yohoho.io", color: "#2e2e00", icon: "🏴‍☠️" },
                    { name: "Bruh.io", url: "https://bruh.io", color: "#0a2e2e", icon: "😂" },
                    { name: "Defly.io", url: "https://defly.io", color: "#1a0a2e", icon: "🚁" },
                    { name: "Starblast.io", url: "https://starblast.io", color: "#0a0a1a", icon: "🚀" },
                    { name: "Astro Assault", url: "https://astroassault.io", color: "#0a0a2e", icon: "🌌" },
                    { name: "Wanderers.io", url: "https://wanderers.io", color: "#2e1a0a", icon: "🗡️" },
                    { name: "Generals.io", url: "https://generals.io", color: "#0a1a0a", icon: "🗺️" },
                    { name: "Tetr.io", url: "https://tetr.io", color: "#0a0a2e", icon: "🟣" },
                    { name: "Curvefever Pro", url: "https://curvefever.pro", color: "#2e0a1a", icon: "〰️" },
                    { name: "Poki Games", url: "https://poki.com", color: "#1a1a1a", icon: "🎮" },
                    { name: "Y8 Games", url: "https://y8.com", color: "#2e0a0a", icon: "👾" },
                    { name: "Coolmath Games", url: "https://coolmathgames.com", color: "#0a2e0a", icon: "🧮" },
                    { name: "Miniclip", url: "https://miniclip.com", color: "#0a0a2e", icon: "🕹️" },
                    { name: "Kongregate", url: "https://kongregate.com", color: "#2e1a2e", icon: "🎮" },
                    { name: "Armor Games", url: "https://armorgames.com", color: "#2e0a0a", icon: "🛡️" },
                    { name: "Newgrounds", url: "https://newgrounds.com", color: "#2e1a00", icon: "🎨" },
                    { name: "Tank Trouble", url: "https://tanktrouble.com", color: "#1a2e0a", icon: "🪖" },
                    { name: "Kingdom Rush", url: "https://kingdomrush.com", color: "#2e0a00", icon: "🗼" },
                    { name: "Pacman", url: "https://freepacman.org", color: "#2e2e00", icon: "👻" },
                    { name: "Snake Game", url: "https://playsnake.org", color: "#0a2e0a", icon: "🐍" },
                    { name: "Space Invaders", url: "https://freeinvaders.org", color: "#0a0a2e", icon: "👾" },
                    { name: "Sudoku", url: "https://sudoku.com", color: "#2e2e2e", icon: "🔢" },
                    { name: "Mahjong", url: "https://mahjong.gg", color: "#2e1a00", icon: "🀄" },
                    { name: "Freecell", url: "https://freecell.net", color: "#0a2e0a", icon: "🃏" },
                    { name: "8 Ball Pool", url: "https://miniclip.com/games/8-ball-pool-multiplayer", color: "#0a1a0a", icon: "🎱" },
                    { name: "Playhop", url: "https://playhop.com", color: "#1a0a2e", icon: "🎮" },
                    { name: "Roblox", url: "https://roblox.com", color: "#2e0a0a", icon: "🟥" },
                    { name: "Among Us Web", url: "https://www.innersloth.com/games/among-us", color: "#1a0a2e", icon: "🚀" },
                    { name: "Sporcle", url: "https://sporcle.com", color: "#0a1a2e", icon: "🧠" },
                    { name: "Kahoot", url: "https://kahoot.it", color: "#2e0a1a", icon: "❓" },
                    { name: "Quizlet", url: "https://quizlet.com", color: "#0a1a2e", icon: "📚" },
                    { name: "Spades", url: "https://spades.com", color: "#1a0a0a", icon: "♠️" },
                ];

                games.forEach(game => {
                    const card = document.createElement('div');
                    card.className = 'rift-hub-card';
                    card.dataset.name = game.name.toLowerCase();
                    card.innerHTML = `<div class="hub-icon" style="background:${game.color};">${game.icon}</div><span>${game.name}</span>`;
                    card.onclick = () => go(game.url);
                    grid.appendChild(card);
                });
            }

            let _appsPopulated = false;
            function populateAppsHub() {
                const grid = document.getElementById('hubAppsGrid');
                if (!grid || _appsPopulated) return;
                _appsPopulated = true;

                const apps = [
                    { name: "Google", url: "https://google.com", color: "#ffffff", icon: "🔍", textColor: "#333" },
                    { name: "YouTube", url: "https://youtube.com", color: "#ff0000", icon: "▶️" },
                    { name: "Spotify", url: "https://open.spotify.com", color: "#1DB954", icon: "🎵" },
                    { name: "Discord", url: "https://discord.com", color: "#5865F2", icon: "💬" },
                    { name: "ChatGPT", url: "https://chat.openai.com", color: "#10A37F", icon: "🤖" },
                    { name: "GitHub", url: "https://github.com", color: "#24292e", icon: "🐙" },
                    { name: "Twitch", url: "https://twitch.tv", color: "#9146FF", icon: "🎮" },
                    { name: "Netflix", url: "https://netflix.com", color: "#e50914", icon: "🎬" },
                    { name: "Reddit", url: "https://reddit.com", color: "#ff4500", icon: "🤖" },
                    { name: "Twitter/X", url: "https://x.com", color: "#000000", icon: "✖️" },
                    { name: "Instagram", url: "https://instagram.com", color: "#e1306c", icon: "📸" },
                    { name: "TikTok", url: "https://tiktok.com", color: "#010101", icon: "🎵" },
                    { name: "Pinterest", url: "https://pinterest.com", color: "#e60023", icon: "📌" },
                    { name: "Snapchat", url: "https://web.snapchat.com", color: "#fffc00", icon: "👻" },
                    { name: "Google Drive", url: "https://drive.google.com", color: "#1565c0", icon: "📁" },
                    { name: "Google Docs", url: "https://docs.google.com", color: "#1a73e8", icon: "📄" },
                    { name: "Google Slides", url: "https://slides.google.com", color: "#f9ab00", icon: "📊" },
                    { name: "Google Sheets", url: "https://sheets.google.com", color: "#0f9d58", icon: "📋" },
                    { name: "Gmail", url: "https://mail.google.com", color: "#ea4335", icon: "✉️" },
                    { name: "Google Meet", url: "https://meet.google.com", color: "#1a73e8", icon: "📹" },
                    { name: "Zoom", url: "https://zoom.us", color: "#2d8cff", icon: "🎥" },
                    { name: "Amazon", url: "https://amazon.com", color: "#ff9900", icon: "📦" },
                    { name: "eBay", url: "https://ebay.com", color: "#e53238", icon: "🏷️" },
                    { name: "ESPN", url: "https://espn.com", color: "#cc0000", icon: "🏈" },
                    { name: "BBC News", url: "https://bbc.com/news", color: "#bb1919", icon: "📰" },
                    { name: "Wikipedia", url: "https://wikipedia.org", color: "#202122", icon: "📖" },
                    { name: "Stack Overflow", url: "https://stackoverflow.com", color: "#f48024", icon: "💻" },
                    { name: "GeForce Now", url: "https://play.geforcenow.com", color: "#76b900", icon: "🎮" },
                    { name: "SoundCloud", url: "https://soundcloud.com", color: "#ff3300", icon: "🎧" },
                    { name: "Deezer", url: "https://deezer.com", color: "#a238ff", icon: "🎶" },
                    { name: "Canva", url: "https://canva.com", color: "#00c4cc", icon: "🎨" },
                    { name: "Figma", url: "https://figma.com", color: "#f24e1e", icon: "🖌️" },
                    { name: "Notion", url: "https://notion.so", color: "#1f1f1f", icon: "📝" },
                    { name: "Trello", url: "https://trello.com", color: "#0052cc", icon: "📋" },
                    { name: "Duolingo", url: "https://duolingo.com", color: "#58cc02", icon: "🦜" },
                    { name: "Khan Academy", url: "https://khanacademy.org", color: "#14bf96", icon: "🎓" },
                    { name: "Desmos", url: "https://desmos.com", color: "#6039ff", icon: "📐" },
                    { name: "WolframAlpha", url: "https://wolframalpha.com", color: "#dd1100", icon: "🧮" },
                    { name: "Replit", url: "https://replit.com", color: "#f26207", icon: "💾" },
                    { name: "CodePen", url: "https://codepen.io", color: "#1e1f26", icon: "✏️" },
                    { name: "Twitch Clips", url: "https://clips.twitch.tv", color: "#9146FF", icon: "📹" },
                    { name: "Kick", url: "https://kick.com", color: "#53fc18", icon: "🎙️" },
                    { name: "Rumble", url: "https://rumble.com", color: "#85c742", icon: "🎥" },
                    { name: "Dropbox", url: "https://dropbox.com", color: "#0061ff", icon: "📦" },
                    { name: "iCloud", url: "https://icloud.com", color: "#157efb", icon: "☁️" },
                    { name: "Outlook", url: "https://outlook.live.com", color: "#0078d4", icon: "📬" },
                ];

                apps.forEach(app => {
                    const card = document.createElement('div');
                    card.className = 'rift-hub-card';
                    card.dataset.name = app.name.toLowerCase();
                    card.innerHTML = `<div class="hub-icon" style="background:${app.color};color:${app.textColor || '#fff'};">${app.icon}</div><span>${app.name}</span>`;
                    card.onclick = () => go(app.url);
                    grid.appendChild(card);
                });
            }
"""

# Inject this js right after the function hideNewTab block
hub_js_marker = "            function hideNewTab() {"
html = html.replace(hub_js_marker, hub_js + "\n            function hideNewTab() {")
print("  Hub JS injected")

print("Step 6: Fix dock buttons to use go() instead of createTab() for rift:// URLs...")
html = html.replace(
    '''<button class="nt-dock-btn" onclick="createTab('rift://newtab')" title="Home">''',
    '''<button class="nt-dock-btn" onclick="go('rift://newtab')" title="Home">'''
)
html = html.replace(
    '''<button class="nt-dock-btn" onclick="createTab('rift://games')" title="Games">''',
    '''<button class="nt-dock-btn" onclick="go('rift://games')" title="Games">'''
)
html = html.replace(
    '''<button class="nt-dock-btn" onclick="createTab('rift://apps')" title="Apps">''',
    '''<button class="nt-dock-btn" onclick="go('rift://apps')" title="Apps">'''
)
html = html.replace(
    '''<button class="nt-dock-btn" onclick="createTab('https://discord.com')" title="Chat">''',
    '''<button class="nt-dock-btn" onclick="go('https://discord.com')" title="Chat">'''
)
print("  Dock buttons fixed")

# Fix home button too
html = html.replace(
    '''<button class="nt-dock-btn" onclick="document.getElementById('ntSearchInput').focus()" title="Web">''',
    '''<button class="nt-dock-btn" onclick="(function(){const i=document.getElementById('ntSearchInput'); if(i){i.focus();}else{const b=document.querySelector('.nt-search-input'); if(b) b.focus();}})()" title="Web">'''
)

print("Step 7: Fix tabCloakBtn reference in dock...")
html = html.replace(
    '''<button class="nt-dock-btn" onclick="document.getElementById('tabCloakBtn').click()" title="Tab Cloaking">''',
    '''<button class="nt-dock-btn" onclick="(function(){const b=document.getElementById('tabCloakBtn')||document.querySelector('[data-section=tabcloaking]'); if(b) b.click();})()" title="Tab Cloaking">'''
)
print("  Done")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("\nAll done!")
