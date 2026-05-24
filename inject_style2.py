import sys
import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# ============================================================
# 1. Find and replace the renderFavorites function
# ============================================================
start_idx = html.find("function renderFavorites() {")
if start_idx == -1:
    print("ERROR: renderFavorites not found!")
    sys.exit(1)

brace_count = 0
end_idx = start_idx
while end_idx < len(html):
    if html[end_idx] == "{":
        brace_count += 1
    elif html[end_idx] == "}":
        brace_count -= 1
        if brace_count == 0:
            end_idx += 1
            break
    end_idx += 1

old_func = html[start_idx:end_idx]

new_func = r"""function renderFavorites() {
    if (!ntFavorites) return;
    ntFavorites.innerHTML = "";

    ntFavorites.style.cssText = "display:flex;flex-wrap:wrap;justify-content:center;max-width:800px;margin:40px auto 0;gap:8px;padding:0 16px;";

    const apps = [
        { name: "Games",       url: "rift://games",              img: "https://play-lh.googleusercontent.com/r8BVvJL1St5IL8r0ZEMDjz8xKUEVOg9qOeuKpB9bw49Raoq9A1GAF6jaUcEL1XvsPi83=w480-h960-rw" },
        { name: "Snapchat",    url: "https://snapchat.com/",     img: "images/Snapchat.webp" },
        { name: "GeForce Now", url: "https://play.geforcenow.com/", img: "images/Geforce_NOW.webp" },
        { name: "Discord",     url: "https://discord.com/",      img: "images/Discord.webp" },
        { name: "Amazon",      url: "https://amazon.ca/",        img: "images/Amazon.webp" },
        { name: "Y8",          url: "https://y8.com/",           img: "images/Y8_Games.webp" },
        { name: "TikTok",      url: "https://tiktok.com/",       img: "images/TikTok.webp" },
        { name: "X",           url: "https://x.com/",            img: "images/Twitter_X.webp" },
        { name: "Poki",        url: "https://poki.com/",         img: "images/Poki.webp" }
    ];

    apps.forEach(app => {
        const div = document.createElement("div");
        div.style.cssText = "display:flex;flex-direction:column;align-items:center;gap:10px;cursor:pointer;padding:14px 12px;border-radius:16px;transition:background 0.2s ease,transform 0.2s cubic-bezier(0.34,1.56,0.64,1);min-width:90px;";
        div.onmouseenter = () => {
            div.style.background = "rgba(255,255,255,0.08)";
            div.style.transform = "translateY(-3px)";
        };
        div.onmouseleave = () => {
            div.style.background = "transparent";
            div.style.transform = "translateY(0)";
        };
        div.onclick = () => createTab(app.url);

        const img = document.createElement("img");
        img.src = app.img;
        img.style.cssText = "width:52px;height:52px;border-radius:14px;object-fit:cover;";
        img.onerror = () => { img.style.display = "none"; };

        const span = document.createElement("span");
        span.textContent = app.name;
        span.style.cssText = "font-size:13px;color:rgba(255,255,255,0.75);font-weight:400;font-family:'Inter',sans-serif;letter-spacing:0.02em;text-align:center;";

        div.appendChild(img);
        div.appendChild(span);
        ntFavorites.appendChild(div);
    });
}"""

html = html[:start_idx] + new_func + html[end_idx:]

# ============================================================
# 2. Style the nt-search-engine (engine dropdown button) cleaner
# ============================================================
# Find the nt-search-engine CSS block and make it more subtle
old_engine = """        .nt-search-engine {
            position: relative;
            height: 44px;
            margin-right: -3px;
            padding: 0 14px 0 18px;
            border-radius: 22px;
            border: 1px solid rgba(255, 255, 255, .2);
            background: rgba(20, 24, 30, .85);
            color: var(--tx);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 13px;
            font-weight: 500;
            transition: all .2s;
            white-space: nowrap;
        }"""
new_engine = """        .nt-search-engine {
            position: relative;
            height: 50px;
            margin-right: -3px;
            padding: 0 14px 0 18px;
            border-radius: 30px 0 0 30px;
            border: 1px solid rgba(255,255,255,0.18);
            border-right: none;
            background: rgba(255,255,255,0.07);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            color: rgba(255,255,255,0.65);
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 13px;
            font-weight: 400;
            font-family: 'Inter', sans-serif;
            transition: all .2s;
            white-space: nowrap;
        }"""
html = html.replace(old_engine, new_engine)

# ============================================================
# 3. Fix the search button (arrow button) styling
# ============================================================
old_search_btn = """        .nt-search button {"""
idx_btn = html.find(old_search_btn)
if idx_btn != -1:
    end_btn = html.find("}", idx_btn)
    old_block = html[idx_btn:end_btn+1]
    new_block = """        .nt-search button {
            height: 50px;
            width: 50px;
            border-radius: 0 30px 30px 0;
            border: 1px solid rgba(255,255,255,0.18);
            border-left: none;
            background: rgba(255,255,255,0.07);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            color: rgba(255,255,255,0.65);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            transition: all .2s;
            flex-shrink: 0;
        }"""
    html = html[:idx_btn] + new_block + html[end_btn+1:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done!")
