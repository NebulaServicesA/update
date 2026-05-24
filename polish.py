with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# ---- Find the injected <style> block and update/add missing styles ----
# Find our injected style block marker and update the nt-bg gradient
old_injected_style = """    <style>
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
    </style>"""

new_injected_style = """    <style>
        body, input, button, select, textarea {
            font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
        }

        /* === Omnibox (address bar) glassmorphism === */
        .omnibox {
            background: rgba(20,24,32,0.6) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
            border-radius: 12px !important;
            transition: all 0.25s ease !important;
        }
        .omnibox:focus-within {
            background: rgba(30,36,48,0.75) !important;
            border-color: rgba(255,255,255,0.22) !important;
            box-shadow: 0 4px 24px rgba(0,0,0,0.4), 0 0 0 2px rgba(255,255,255,0.05) !important;
        }

        /* === New tab background gradient === */
        .nt-bg {
            background: linear-gradient(135deg, #0d0f18 0%, #111827 40%, #0d1117 70%, #161c2a 100%) !important;
            animation: none !important;
        }
        @keyframes gradientBG {
            0%   { background-position: 0% 50%; }
            50%  { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* === Settings cards === */
        .settings-card {
            background: rgba(16,20,28,0.7) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            border: 1px solid rgba(255,255,255,0.07) !important;
            border-radius: 14px !important;
        }
        .settings-card-head {
            border-bottom: 1px solid rgba(255,255,255,0.06) !important;
        }

        /* === Tab strip === */
        .tab-strip {
            background: rgba(10,12,18,0.9) !important;
        }
        .tab {
            border-radius: 8px !important;
        }
        .tab.active {
            background: rgba(255,255,255,0.1) !important;
        }

        /* === Toolbar === */
        .toolbar {
            background: rgba(10,12,18,0.95) !important;
            border-bottom: 1px solid rgba(255,255,255,0.06) !important;
        }

        /* === ntSearch input override === */
        #ntSearch {
            background: transparent !important;
            border: none !important;
            outline: none !important;
            color: rgba(255,255,255,0.9) !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 300 !important;
            font-size: 15px !important;
            letter-spacing: 0.01em !important;
        }
        #ntSearch::placeholder {
            color: rgba(255,255,255,0.3) !important;
            font-weight: 300 !important;
        }

        /* === Animated entry for favorites icons === */
        #ntFavorites > div {
            animation: fadeUp 0.4s cubic-bezier(0.22,1,0.36,1) both;
        }
        #ntFavorites > div:nth-child(1) { animation-delay: 0.05s; }
        #ntFavorites > div:nth-child(2) { animation-delay: 0.10s; }
        #ntFavorites > div:nth-child(3) { animation-delay: 0.15s; }
        #ntFavorites > div:nth-child(4) { animation-delay: 0.20s; }
        #ntFavorites > div:nth-child(5) { animation-delay: 0.25s; }
        #ntFavorites > div:nth-child(6) { animation-delay: 0.30s; }
        #ntFavorites > div:nth-child(7) { animation-delay: 0.35s; }
        #ntFavorites > div:nth-child(8) { animation-delay: 0.40s; }
        #ntFavorites > div:nth-child(9) { animation-delay: 0.45s; }
        @keyframes fadeUp {
            0%   { opacity: 0; transform: translateY(16px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        /* === nt-brand fade-in === */
        .nt-brand {
            animation: brandFade 0.9s cubic-bezier(0.22,1,0.36,1) both !important;
        }
        @keyframes brandFade {
            0%   { opacity: 0; transform: translateY(-10px); }
            100% { opacity: 0.88; transform: translateY(0); }
        }

        /* === nt-search wrapper glass pill === */
        .nt-search {
            background: rgba(255,255,255,0.05) !important;
            border: 1px solid rgba(255,255,255,0.12) !important;
            border-radius: 40px !important;
            backdrop-filter: blur(14px) !important;
            -webkit-backdrop-filter: blur(14px) !important;
            padding: 0 6px 0 0 !important;
            box-shadow: 0 4px 24px rgba(0,0,0,0.25) !important;
            transition: all 0.25s ease !important;
            animation: searchFade 1.0s cubic-bezier(0.22,1,0.36,1) 0.2s both !important;
        }
        .nt-search:focus-within {
            border-color: rgba(255,255,255,0.22) !important;
            background: rgba(255,255,255,0.08) !important;
            box-shadow: 0 4px 30px rgba(0,0,0,0.35) !important;
        }
        @keyframes searchFade {
            0%   { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        /* Hide the separate engine + button borders (now unified in pill) */
        .nt-search-engine {
            border: none !important;
            background: transparent !important;
            backdrop-filter: none !important;
        }
        .nt-search button {
            border: none !important;
            background: transparent !important;
            backdrop-filter: none !important;
        }
        .nt-search button:hover {
            background: rgba(255,255,255,0.1) !important;
            border-radius: 50% !important;
        }
    </style>"""

html = html.replace(old_injected_style, new_injected_style)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done!")
