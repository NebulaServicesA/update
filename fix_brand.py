with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# ---- 1. Replace the entire nt-brand HTML block ----
old_brand = '''                        <div class="nt-brand" style="position:relative;">
                            <span style="letter-spacing: 0.45em; display:inline-flex;">
                                <span class="gust-letter-G">R</span><span class="gust-letter-U">I</span><span class="gust-letter-S">F</span><span class="gust-letter-T">T</span>
                            </span>
                            <span class="gust-badge-anim" style="
                                font-size: 11px;
                                font-weight: 700;
                                letter-spacing: 0.05em;
                                color: var(--ac);
                                background: rgba(157,229,255,0.10);
                                border: 1px solid rgba(157,229,255,0.35);
                                border-radius: 6px;
                                padding: 2px 7px;
                                margin-left: 10px;
                                vertical-align: middle;
                                line-height: 1.4;
                                font-family: var(--mono);
                                position: relative;
                                top: -16px;
                                margin-left: -3px;
                            ">v1.0</span>
                        </div>'''

new_brand = '''                        <div class="nt-brand" style="position:relative;">
                            <span class="gust-letter-G">r</span><span class="gust-letter-U">i</span><span class="gust-letter-S">f</span><span class="gust-letter-T">t</span>
                        </div>'''

html = html.replace(old_brand, new_brand)

# ---- 2. Update nt-brand CSS to xylora-style ----
old_brand_css = """.nt-brand {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0;
            color: var(--ac);
            font-weight: 300;
            font-size: 5rem;
            letter-spacing: 0.45em;
            margin-bottom: 0;
            margin-top: 30px;
            line-height: 1;
            font-family: 'Inter', var(--ui), sans-serif;
            text-transform: lowercase;
            opacity: 0.92;
        }"""
new_brand_css = """.nt-brand {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0;
            color: var(--ac);
            font-weight: 200;
            font-size: 5.5rem;
            letter-spacing: 0.55em;
            margin-bottom: 0;
            margin-top: 30px;
            line-height: 1;
            font-family: 'Inter', var(--ui), sans-serif;
            text-transform: lowercase;
            opacity: 0.88;
            text-indent: 0.55em;
        }"""
html = html.replace(old_brand_css, new_brand_css)

# ---- 3. Remove the "Made with love by Nautilus Labs" credit text entirely ----
old_credit = '''<div id="gustCredit"
                        style="position:absolute; bottom:20px; right:24px; z-index:10; color:rgba(255,255,255,1); font-size:18px; font-weight:600; font-family:var(--ui); display:flex; align-items:center; gap:5px; pointer-events:none; user-select:none; text-shadow:0 1px 4px rgba(0,0,0,0.6); letter-spacing:0.02em;">
                        Made with <i class="fas fa-heart" style="color:#ff6b8a; font-size:15px;"></i> by Nautilus Labs
                    </div>'''
html = html.replace(old_credit, "<!-- credit removed -->")

# ---- 4. Hide the credit via the injected display:none version too ----
html = html.replace('<div id="gustCredit" style="display:none!important;"', '<div id="gustCredit" style="display:none!important;"')

# ---- 5. Polish nt-content gap/layout ----
old_content_css = """.nt-content {
            position: relative;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 20px;
            padding: 24px;
            text-align: center
        }"""
new_content_css = """.nt-content {
            position: relative;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 0;
            padding: 24px;
            text-align: center;
        }"""
html = html.replace(old_content_css, new_content_css)

# ---- 6. Make animated background gradient override live ----
old_ntbg_css = """.nt-bg {
            background: linear-gradient(-45deg, #0d121c, #1a1f33, #0f2027, #203a43) !important;
            background-size: 400% 400% !important;
            animation: gradientBG 15s ease infinite !important;
        }"""
# Already injected via <style> tag so just confirm it's there
if old_ntbg_css not in html:
    print("WARNING: nt-bg override not found - already handled via injected style block")

# ---- 7. Add search bar icon (magnifying glass) inside the input area ----
# Wrap ntSearch input to add a search icon
old_search_input_html = '''<input id="ntSearch" placeholder="Search or enter address" autocomplete="off">'''
new_search_input_html = '''<i class="fas fa-magnifying-glass" style="position:absolute;left:calc(100% - 100% + 20px + 120px);color:rgba(255,255,255,0.3);font-size:14px;pointer-events:none;z-index:2;top:50%;transform:translateY(-50%);"></i><input id="ntSearch" placeholder="Search or enter address" autocomplete="off" style="padding-left:40px;">'''
# Actually better to just style search wrapper with position:relative and add via CSS
# Let's add the icon differently - inject before the input
old_search_wrapper = '''<input id="ntSearch" placeholder="Search or enter address" autocomplete="off">'''
new_search_wrapper = '''<span style="position:relative;flex:1;display:flex;align-items:center;"><i class="fas fa-magnifying-glass" style="position:absolute;left:16px;color:rgba(255,255,255,0.3);font-size:14px;pointer-events:none;z-index:2;"></i><input id="ntSearch" placeholder="Search or enter address..." autocomplete="off" style="padding-left:44px;width:100%;"></span>'''
html = html.replace(old_search_wrapper, new_search_wrapper)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done!")
