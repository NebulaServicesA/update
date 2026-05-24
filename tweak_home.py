import sys
import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update the glow
old_glow = "background: radial-gradient(ellipse at center, rgba(80, 0, 255, 0.4) 0%, rgba(130, 0, 255, 0.2) 30%, transparent 70%);"
new_glow = "background: radial-gradient(ellipse at bottom, rgba(140, 60, 255, 0.6) 0%, rgba(60, 0, 255, 0.4) 40%, transparent 70%);"
html = html.replace(old_glow, new_glow)

# 2. Make stars more visible and add a check
old_stars_fill = "ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';"
new_stars_fill = "ctx.fillStyle = 'rgba(255, 255, 255, 1)';"
html = html.replace(old_stars_fill, new_stars_fill)
html = html.replace("radius: Math.random() * 1.5", "radius: Math.random() * 2.5")

# 3. Search Bar Styling & Placeholder
old_placeholder = 'placeholder="Search the web or type a URL..."'
new_placeholder = 'placeholder="Search RIFT..."'
html = html.replace(old_placeholder, new_placeholder)

search_engine_css = """        .nt-search-engine {
            position: relative;
            height: 50px;
            margin-right: -3px;
            padding: 0 14px 0 18px;
            border-radius: 30px 0 0 30px;
            border: 1px solid rgba(255,255,255,0.18);
            border-right: none;
            background: rgba(255,255,255,0.07);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);"""
search_engine_css_new = """        .nt-search-engine {
            position: relative;
            height: 50px;
            margin-right: -3px;
            padding: 0 14px 0 18px;
            border-radius: 30px 0 0 30px;
            border: 1px solid rgba(255,255,255,0.08);
            border-right: none;
            background: rgba(15, 15, 20, 0.6);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);"""
html = html.replace(search_engine_css, search_engine_css_new)

search_input_css = """        .nt-search-input {
            flex: 1;
            height: 50px;
            padding: 0 10px;
            border: 1px solid rgba(255,255,255,0.18);
            border-left: none;
            border-right: none;
            background: rgba(255,255,255,0.07);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);"""
search_input_css_new = """        .nt-search-input {
            flex: 1;
            height: 50px;
            padding: 0 10px;
            border: 1px solid rgba(255,255,255,0.08);
            border-left: none;
            border-right: none;
            background: rgba(15, 15, 20, 0.6);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);"""
html = html.replace(search_input_css, search_input_css_new)

search_btn_css = """        .nt-search-btn {
            height: 50px;
            padding: 0 20px 0 14px;
            border-radius: 0 30px 30px 0;
            border: 1px solid rgba(255,255,255,0.18);
            border-left: none;
            background: rgba(255,255,255,0.07);
            backdrop-filter: blur(12px);"""
search_btn_css_new = """        .nt-search-btn {
            height: 50px;
            padding: 0 20px 0 14px;
            border-radius: 0 30px 30px 0;
            border: 1px solid rgba(255,255,255,0.08);
            border-left: none;
            background: rgba(15, 15, 20, 0.6);
            backdrop-filter: blur(12px);"""
html = html.replace(search_btn_css, search_btn_css_new)

search_hover_css = """        .nt-search-engine:hover, .nt-search-input:focus, .nt-search-btn:hover {
            border-color: rgba(157, 229, 255, .4);
            background: rgba(20, 24, 30, .95);
        }"""
search_hover_css_new = """        .nt-search-engine:hover, .nt-search-input:focus, .nt-search-btn:hover {
            border-color: rgba(140, 60, 255, 0.6);
            background: rgba(20, 20, 25, 0.95);
        }"""
html = html.replace(search_hover_css, search_hover_css_new)

# 4. Modify renderFavorites to include Games and increase height to 64px
render_fav_old = 'height:52px;'
render_fav_new = 'height:64px;'
html = html.replace(render_fav_old, render_fav_new)

games_app = '{ name: "Games", url: "rift://games", bg: "#1a1a1a", color: "#fff", icon: \'<i class="fas fa-gamepad" style="font-size:18px;color:#a040ff;"></i> <span style="font-weight:700;">Games</span>\' },'
google_app = '{ name: "Google"'
html = html.replace(google_app, games_app + '\n        ' + google_app)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done!")
