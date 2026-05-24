import sys

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the incorrect fetchAndRender games block with a proper implementation
# The trick: we load the real URL into the frame directly, but keep the UI showing rift://games
old_games = """if (url === GAMES_INTERNAL) {
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
                }"""

new_games = """if (url === GAMES_INTERNAL) {
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

html = html.replace(old_games, new_games)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done!")
