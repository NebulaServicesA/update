import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

new_css = """.rift-hub-card {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 0;
            background: var(--surface2);
            border: 2px solid transparent;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
            color: var(--tx);
            position: relative;
            overflow: hidden;
            aspect-ratio: 16 / 10;
            box-shadow: 0 4px 10px rgba(0,0,0,0.4);
            font-family: 'Inter', sans-serif;
            font-size: 13px;
        }
        .rift-hub-card:hover {
            border-color: rgba(140, 60, 255, 0.6);
            transform: scale(1.05) translateY(-4px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.6);
            z-index: 10;
        }
        .rift-hub-card img.banner {
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s;
        }
        .rift-hub-card:hover img.banner {
            transform: scale(1.08);
        }
        .rift-hub-card .hub-overlay {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.6) 50%, transparent 100%);
            padding: 24px 10px 8px;
            text-align: center;
            opacity: 0;
            transition: opacity 0.2s;
            pointer-events: none;
        }
        .rift-hub-card:hover .hub-overlay {
            opacity: 1;
        }
        .rift-hub-card span {
            font-weight: 800;
            color: #fff;
            text-shadow: 0 2px 4px rgba(0,0,0,0.9);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            display: block;
        }
        .rift-hub-card .hub-icon {
            display: none !important;
        }"""

# Replace the block from .rift-hub-card { to the end of .rift-hub-card:hover { ... }
# We will use regex to find it
pattern = re.compile(r'\.rift-hub-card\s*\{.*?\.rift-hub-card:hover\s*\{.*?\}', re.DOTALL)
html = pattern.sub(new_css, html, count=1)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("CSS updated!")
