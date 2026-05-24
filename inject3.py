import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Aesthetics: Inject Font & Glassmorphism into <head>
css_inject = '''<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body, input, button, select, textarea {
            font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
        }
        .omnibox {
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
            transition: all 0.3s ease !important;
        }
        .omnibox:focus-within {
            background: rgba(255, 255, 255, 0.12) !important;
            border-color: rgba(255, 255, 255, 0.3) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4), 0 0 15px rgba(255,255,255,0.1) !important;
        }
        .nt-bg {
            background: linear-gradient(-45deg, #0d121c, #1a1f33, #0f2027, #203a43) !important;
            background-size: 400% 400% !important;
            animation: gradientBG 15s ease infinite !important;
        }
        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .custom-fav {
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            background: rgba(255, 255, 255, 0.06) !important;
            backdrop-filter: blur(8px) !important;
        }
        .settings-card {
            background: rgba(20, 24, 32, 0.6) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
        }
    </style>
'''
html = html.replace('</head>', css_inject + '</head>')

# 2. Add About Blank button to Tab Cloaking section
tab_cloaking_target = '<div class="settings-hint">When pressed, the site will instantly redirect to google.ca. Default is none.</div>\n            </div>'
about_blank_ui = '''
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);">
                <div class="settings-label">About:Blank Cloaking</div>
                <button id="aboutBlankBtn" style="padding: 8px 16px; border-radius: 8px; background: var(--ac); color: #fff; border: none; cursor: pointer; font-weight: 500; transition: opacity 0.2s;">Open in About:Blank</button>
                <div class="settings-hint">Opens this site in a disguised about:blank window and hides the current tab.</div>
            </div>
'''
html = html.replace(tab_cloaking_target, tab_cloaking_target + about_blank_ui)

# 3. Inject JS for About Blank
js_target = "panicClear.addEventListener('click', () => {"
about_blank_js = '''
const aboutBlankBtn = document.getElementById('aboutBlankBtn');
if (aboutBlankBtn) {
    aboutBlankBtn.addEventListener('click', () => {
        let win = window.open('about:blank', '_blank');
        if (!win) {
            alert("Pop-ups must be allowed to use About:Blank cloaking.");
            return;
        }
        let iframe = win.document.createElement('iframe');
        iframe.src = window.location.href;
        iframe.style.width = '100vw';
        iframe.style.height = '100vh';
        iframe.style.border = 'none';
        iframe.style.margin = '0';
        iframe.style.padding = '0';
        win.document.body.style.margin = '0';
        win.document.body.style.padding = '0';
        win.document.body.appendChild(iframe);
        win.document.title = 'Google Classroom'; // Default title for about:blank cloak
        let link = win.document.createElement('link');
        link.rel = 'icon';
        link.href = 'https://upload.wikimedia.org/wikipedia/commons/1/19/Google_Classroom_Logo.svg';
        win.document.head.appendChild(link);
        
        window.location.replace("https://google.ca/");
    });
}
'''
html = html.replace(js_target, about_blank_js + '\n' + js_target)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
