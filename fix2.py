import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

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

# Remove ALL occurrences of css_inject
html = html.replace(css_inject, '')

# Now inject it back ONLY at the first occurrence
# We can find the first </head> by searching for it
idx = html.find('</head>')
if idx != -1:
    html = html[:idx] + css_inject + html[idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
