import sys
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject Tab Cloaking Nav Item
nav_inject_marker = '<button class=\"settings-nav-item\" data-section=\"homescreen\">'
nav_item = '<button class=\"settings-nav-item\" data-section=\"tabcloaking\"><i class=\"fas fa-mask\"></i><span>Tab Cloaking</span></button>\n                                '
html = html.replace(nav_inject_marker, nav_item + nav_inject_marker)

# 2. Inject Tab Cloaking Section Content
section_inject_marker = '<div class=\"settings-section\" data-section=\"language\" style=\"display:none;\">'
tab_cloaking_section = '''
<div class=\"settings-section\" data-section=\"tabcloaking\" style=\"display:none;\">
    <div class=\"settings-card\">
        <div class=\"settings-card-head\"><i class=\"fas fa-mask\"></i> Tab Cloaking</div>
        <div class=\"settings-card-body\">
            <div style=\"margin-bottom: 12px;\">
                <div class=\"settings-label\">Preset</div>
                <select id=\"tabCloakPreset\" class=\"settings-input\">
                    <option value=\"none\">None</option>
                    <option value=\"classroom\">Google Classroom</option>
                    <option value=\"google\">Google</option>
                </select>
                <div class=\"settings-hint\">Change the tab title and icon to hide the site.</div>
            </div>
            <div>
                <div class=\"settings-label\">Panic Key</div>
                <input type=\"text\" id=\"panicKeyInput\" class=\"settings-input\" placeholder=\"Press a key...\" readonly>
                <button class=\"settings-btn-icon\" id=\"panicKeyClear\" title=\"Clear panic key\"><i class=\"fas fa-times\"></i></button>
                <div class=\"settings-hint\">When pressed, the site will instantly redirect to google.ca. Default is none.</div>
            </div>
        </div>
    </div>
</div>
'''
html = html.replace(section_inject_marker, tab_cloaking_section + section_inject_marker)

# 3. Inject Games Square
search_container_end = '<div class=\"nt-favorites\" id=\"ntFavorites\"></div>'
games_square = '''
<div style=\"text-align: center; margin-top: 30px; cursor: pointer; display: inline-block;\" onclick=\"createTab('https://playhop.com/')\">
    <img src=\"https://play-lh.googleusercontent.com/r8BVvJL1St5IL8r0ZEMDjz8xKUEVOg9qOeuKpB9bw49Raoq9A1GAF6jaUcEL1XvsPi83=w480-h960-rw\" style=\"width: 60px; height: 60px; border-radius: 15px; object-fit: cover;\">
    <div style=\"margin-top: 8px; color: var(--fg); font-size: 13px; font-weight: 500;\">Games</div>
</div>
'''
html = html.replace(search_container_end, search_container_end + '\n' + games_square)

# 4. Inject JS logic for Panic Key and Tab Cloaking
js_inject_marker = 'const TUTORIAL_KEY'
js_logic = '''
// Tab Cloaking Logic
const panicInput = document.getElementById('panicKeyInput');
const panicClear = document.getElementById('panicKeyClear');
const tabCloakPreset = document.getElementById('tabCloakPreset');

let currentPanicKey = localStorage.getItem('rift:panickey') || '';
let currentCloak = localStorage.getItem('rift:tabcloak') || 'none';

if(currentPanicKey) panicInput.value = currentPanicKey;
tabCloakPreset.value = currentCloak;

function applyCloak() {
    const link = document.querySelector(\"link[rel~='icon']\") || document.createElement('link');
    link.rel = 'icon';
    if(currentCloak === 'classroom') {
        document.title = 'Google Classroom';
        link.href = 'https://upload.wikimedia.org/wikipedia/commons/1/19/Google_Classroom_Logo.svg';
    } else if(currentCloak === 'google') {
        document.title = 'Google';
        link.href = 'https://images.icon-icons.com/2699/PNG/512/google_logo_icon_169090.png';
    } else {
        document.title = 'RIFT Browser';
        link.href = 'svg/brand.svg'; // Default or reset
    }
    document.getElementsByTagName('head')[0].appendChild(link);
}
applyCloak();

tabCloakPreset.addEventListener('change', (e) => {
    currentCloak = e.target.value;
    localStorage.setItem('rift:tabcloak', currentCloak);
    applyCloak();
});

panicInput.addEventListener('keydown', (e) => {
    e.preventDefault();
    if(e.key === 'Escape' || e.key === 'Backspace') return;
    currentPanicKey = e.key;
    panicInput.value = currentPanicKey;
    localStorage.setItem('rift:panickey', currentPanicKey);
});

panicClear.addEventListener('click', () => {
    currentPanicKey = '';
    panicInput.value = '';
    localStorage.removeItem('rift:panickey');
});

document.addEventListener('keydown', (e) => {
    // Only redirect if a panic key is set, and we are not focused on the panic input itself
    if(currentPanicKey && e.key === currentPanicKey && document.activeElement !== panicInput) {
        window.location.href = 'https://google.ca/';
    }
});
'''
html = html.replace(js_inject_marker, js_logic + '\n' + js_inject_marker)

# 5. Disable Tour entirely
html = html.replace("if (ls.getItem(TUTORIAL_KEY) === 'done') return;", "return;")
html = html.replace("function startTour(force = false) {", "function startTour(force = false) { return;")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
