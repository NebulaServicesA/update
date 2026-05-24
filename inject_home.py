import sys

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update .nt-bg and add the blue glow pseudo element, plus styling for the favorites grid
old_bg_css = """        .nt-bg {
            background: url('images/backround.jpg') center/cover no-repeat !important;
            animation: none !important;
        }"""
new_bg_css = """        .nt-bg {
            background: #000 !important;
            animation: none !important;
            position: absolute;
            inset: 0;
            overflow: hidden;
            z-index: 0;
        }
        /* Blue glow at the bottom center */
        .nt-bg::after {
            content: "";
            position: absolute;
            bottom: -20vh;
            left: 50%;
            transform: translateX(-50%);
            width: 80vw;
            height: 60vh;
            background: radial-gradient(ellipse at center, rgba(80, 0, 255, 0.4) 0%, rgba(130, 0, 255, 0.2) 30%, transparent 70%);
            pointer-events: none;
            z-index: 1;
        }
        /* Stars canvas */
        #starsCanvas {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
            pointer-events: none;
        }"""
html = html.replace(old_bg_css, new_bg_css)

# Inject the canvas HTML into .nt-bg
html = html.replace('<div class="nt-bg" id="ntBg"></div>', '<div class="nt-bg" id="ntBg"><canvas id="starsCanvas"></canvas></div>')

# 2. Add the JS for the moving particles (stars)
stars_js = """
// --- Stars Canvas Animation ---
(function initStars() {
    const canvas = document.getElementById('starsCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let width, height;
    let stars = [];
    
    function resize() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();
    
    for (let i = 0; i < 150; i++) {
        stars.push({
            x: Math.random() * width,
            y: Math.random() * height,
            radius: Math.random() * 1.5,
            vx: Math.floor(Math.random() * 50) - 25,
            vy: Math.floor(Math.random() * 50) - 25
        });
    }
    
    function draw() {
        ctx.clearRect(0, 0, width, height);
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.beginPath();
        for (let i = 0; i < stars.length; i++) {
            let s = stars[i];
            ctx.moveTo(s.x, s.y);
            ctx.arc(s.x, s.y, s.radius, 0, Math.PI * 2, true);
            
            // Move
            s.x += s.vx / 100;
            s.y += s.vy / 100;
            
            // Wrap around
            if (s.x < 0) s.x = width;
            if (s.x > width) s.x = 0;
            if (s.y < 0) s.y = height;
            if (s.y > height) s.y = 0;
        }
        ctx.fill();
        requestAnimationFrame(draw);
    }
    draw();
})();
"""
# inject right before `let _gustAnimLocked = false;` or at the end of the script
js_insert_point = "let _gustAnimLocked = false;"
html = html.replace(js_insert_point, stars_js + "\n            " + js_insert_point)

# 3. Completely replace renderFavorites with the new pill design
start_idx = html.find("function renderFavorites() {")
end_idx = html.find("let _gustAnimLocked = false;") # Since it's right before it
if start_idx != -1 and end_idx != -1:
    # Safely find the end of the function block
    brace_count = 0
    curr_idx = start_idx
    while curr_idx < len(html):
        if html[curr_idx] == '{':
            brace_count += 1
        elif html[curr_idx] == '}':
            brace_count -= 1
            if brace_count == 0:
                curr_idx += 1
                break
        curr_idx += 1
    
    new_renderFavorites = """function renderFavorites() {
    if (!ntFavorites) return;
    ntFavorites.innerHTML = "";

    ntFavorites.style.cssText = "display:flex;flex-wrap:wrap;justify-content:center;max-width:850px;margin:40px auto 0;gap:12px;padding:0 20px;z-index:2;position:relative;";

    const apps = [
        { name: "Google", url: "https://google.com/", bg: "#ffffff", color: "#4285F4", icon: '<i class="fab fa-google"></i> <span style="color:#EA4335">o</span><span style="color:#FBBC05">o</span><span style="color:#4285F4">g</span><span style="color:#34A853">l</span><span style="color:#EA4335">e</span>' },
        { name: "YouTube", url: "https://youtube.com/", bg: "#ffffff", color: "#000", icon: '<i class="fab fa-youtube" style="color:#FF0000;font-size:18px;"></i> <span style="font-weight:700;letter-spacing:-0.5px;">YouTube</span>' },
        { name: "Spotify", url: "https://open.spotify.com/", bg: "#1DB954", color: "#fff", icon: '<i class="fab fa-spotify" style="font-size:18px;"></i> <span style="font-weight:700;letter-spacing:-0.5px;">Spotify</span>' },
        { name: "Discord", url: "https://discord.com/", bg: "#5865F2", color: "#fff", icon: '<i class="fab fa-discord" style="font-size:18px;"></i> <span style="font-weight:800;">Discord</span>' },
        { name: "ChatGPT", url: "https://chat.openai.com/", bg: "#10A37F", color: "#fff", icon: '<i class="fas fa-robot" style="font-size:18px;"></i> <span style="font-weight:600;">ChatGPT</span>' },
        { name: "GeForce Now", url: "https://play.geforcenow.com/", bg: "#76B900", color: "#000", icon: '<span style="font-weight:900;font-style:italic;letter-spacing:-0.5px;">GEFORCE NOW</span>' },
        { name: "GitHub", url: "https://github.com/", bg: "#000000", color: "#fff", icon: '<i class="fab fa-github" style="font-size:18px;"></i> <span style="font-weight:700;">GitHub</span>' },
        { name: "Twitch", url: "https://twitch.tv/", bg: "#9146FF", color: "#fff", icon: '<i class="fab fa-twitch" style="font-size:18px;"></i> <span style="font-weight:800;">twitch</span>' },
        { name: "ESPN", url: "https://espn.com/", bg: "#CC0000", color: "#fff", icon: '<span style="font-weight:900;font-style:italic;font-size:18px;letter-spacing:-1px;">ESPN</span>' },
        { name: "TikTok", url: "https://tiktok.com/", bg: "#000000", color: "#fff", icon: '<i class="fab fa-tiktok" style="font-size:16px;"></i> <span style="font-weight:700;">TikTok</span>' }
    ];

    apps.forEach(app => {
        const div = document.createElement("div");
        div.style.cssText = `display:flex;align-items:center;justify-content:center;gap:8px;cursor:pointer;padding:0 24px;height:52px;border-radius:12px;background:${app.bg};color:${app.color};transition:transform 0.2s cubic-bezier(0.34,1.56,0.64,1), filter 0.2s;min-width:140px;box-shadow:0 4px 15px rgba(0,0,0,0.4);font-family:'Inter',sans-serif;`;
        
        div.onmouseenter = () => {
            div.style.transform = "translateY(-4px)";
            div.style.filter = "brightness(1.1)";
        };
        div.onmouseleave = () => {
            div.style.transform = "translateY(0)";
            div.style.filter = "brightness(1)";
        };
        div.onclick = () => createTab(app.url);
        
        // Fix for games URL intercept logic
        if (app.name === "GeForce Now") {
            // Keep games URL intercept for GeForce Now so it routes through proxy smoothly if needed
        }

        div.innerHTML = app.icon;
        ntFavorites.appendChild(div);
    });
}"""
    html = html[:start_idx] + new_renderFavorites + html[curr_idx:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done with Homepage Redesign!")
