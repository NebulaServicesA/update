import sys

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add "adblocker" to VALID_SETTINGS_SECTIONS
html = html.replace(
    "'connection','search','privacy','cache','filesandmedia',",
    "'connection','search','privacy','cache','filesandmedia','adblocker',"
)

# 2. Inject the settings-nav-item for adblocker
tab_cloaking_nav = '<button class="settings-nav-item" data-section="tabcloaking"><i class="fas fa-mask"></i><span>Tab Cloaking</span></button>'
adblocker_nav = '<button class="settings-nav-item" data-section="adblocker"><i class="fas fa-shield-halved"></i><span>Adblocker</span></button>\n'
html = html.replace(tab_cloaking_nav, tab_cloaking_nav + '\n                                ' + adblocker_nav)

# 3. Create the actual adblocker settings section HTML
tab_cloaking_section = '<div class="settings-section" data-section="tabcloaking" style="display:none;">'
adblocker_section = """
                        <div class="settings-section" data-section="adblocker" style="display:none;">
                            <div class="settings-card">
                                <div class="settings-card-head">
                                    <div class="settings-card-title">Adblocker</div>
                                    <div class="settings-card-desc">Manage the built-in ad and tracker blocking functionality on RIFT.</div>
                                </div>
                                <div class="settings-item">
                                    <div class="settings-info">
                                        <div class="settings-label">Enable Adblocker</div>
                                        <div class="settings-hint">When enabled, the proxy will block known ad and tracker domains.</div>
                                    </div>
                                    <label class="switch">
                                        <input type="checkbox" id="adblockerToggleProxy" checked>
                                        <span class="slider"></span>
                                    </label>
                                </div>
                            </div>
                        </div>
"""
html = html.replace(tab_cloaking_section, adblocker_section + '\n' + tab_cloaking_section)

# 4. Inject JS to link the new toggle to the existing blockToggle functionality
js_injection = """
const adblockerToggleProxy = document.getElementById('adblockerToggleProxy');
if (adblockerToggleProxy) {
    const mainBlockToggle = document.getElementById('blockToggle');
    // Sync initial state
    if (mainBlockToggle) {
        adblockerToggleProxy.checked = mainBlockToggle.classList.contains('on');
        
        // When settings toggle is clicked, click the main block toggle
        adblockerToggleProxy.addEventListener('change', (e) => {
            if (mainBlockToggle.classList.contains('on') !== e.target.checked) {
                mainBlockToggle.click();
            }
        });

        // Ensure they stay synced if main block toggle is clicked
        mainBlockToggle.addEventListener('click', () => {
            setTimeout(() => {
                adblockerToggleProxy.checked = mainBlockToggle.classList.contains('on');
            }, 10);
        });
    }
}
"""
# Insert JS right before the end of the initCache function or near where other listeners are attached.
js_target = "panicClear.addEventListener('click', () => {"
html = html.replace(js_target, js_injection + '\n' + js_target)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done with Adblocker injection!")
