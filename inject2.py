import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the old injected games square
old_games_square = '''<div style="text-align: center; margin-top: 30px; cursor: pointer; display: inline-block;" onclick="createTab('https://playhop.com/')">
    <img src="https://play-lh.googleusercontent.com/r8BVvJL1St5IL8r0ZEMDjz8xKUEVOg9qOeuKpB9bw49Raoq9A1GAF6jaUcEL1XvsPi83=w480-h960-rw" style="width: 60px; height: 60px; border-radius: 15px; object-fit: cover;">
    <div style="margin-top: 8px; color: var(--fg); font-size: 13px; font-weight: 500;">Games</div>
</div>'''
html = html.replace(old_games_square, '')

# Now replace renderFavorites
start_idx = html.find('function renderFavorites() {')
if start_idx != -1:
    brace_count = 0
    end_idx = start_idx
    while end_idx < len(html):
        if html[end_idx] == '{':
            brace_count += 1
        elif html[end_idx] == '}':
            brace_count -= 1
            if brace_count == 0:
                end_idx += 1
                break
        end_idx += 1
        
    old_func = html[start_idx:end_idx]
    
    new_func = '''function renderFavorites() {
    if (!ntFavorites) return;
    ntFavorites.innerHTML = "";

    ntFavorites.style.display = 'flex';
    ntFavorites.style.flexWrap = 'wrap';
    ntFavorites.style.justifyContent = 'center';
    ntFavorites.style.maxWidth = '750px';
    ntFavorites.style.margin = '30px auto 0';
    ntFavorites.style.gap = '15px';

    const apps = [
        { name: "Games", url: "https://playhop.com/", img: "https://play-lh.googleusercontent.com/r8BVvJL1St5IL8r0ZEMDjz8xKUEVOg9qOeuKpB9bw49Raoq9A1GAF6jaUcEL1XvsPi83=w480-h960-rw" },
        { name: "Snapchat", url: "https://snapchat.com/", img: "images/Snapchat.webp" },
        { name: "GeForce Now", url: "https://play.geforcenow.com/", img: "images/Geforce_NOW.webp" },
        { name: "Discord", url: "https://discord.com/", img: "images/Discord.webp" },
        { name: "Amazon", url: "https://amazon.ca/", img: "images/Amazon.webp" },
        { name: "Y8", url: "https://y8.com/", img: "images/Y8_Games.webp" },
        { name: "TikTok", url: "https://tiktok.com/", img: "images/TikTok.webp" },
        { name: "X", url: "https://x.com/", img: "images/Twitter_X.webp" },
        { name: "Poki", url: "https://poki.com/", img: "images/Poki.webp" }
    ];

    apps.forEach(app => {
        const div = document.createElement("div");
        div.style.cssText = 
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 100px;
            cursor: pointer;
            transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.2s ease, box-shadow 0.2s ease;
            border-radius: 18px;
            padding: 15px 10px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        ;
        
        div.onmouseenter = () => {
            div.style.transform = 'translateY(-6px) scale(1.05)';
            div.style.background = 'rgba(255, 255, 255, 0.15)';
            div.style.boxShadow = '0 10px 25px rgba(0, 0, 0, 0.3)';
            div.style.borderColor = 'rgba(255, 255, 255, 0.2)';
        };
        div.onmouseleave = () => {
            div.style.transform = 'translateY(0) scale(1)';
            div.style.background = 'rgba(255, 255, 255, 0.05)';
            div.style.boxShadow = '0 4px 15px rgba(0, 0, 0, 0.1)';
            div.style.borderColor = 'rgba(255, 255, 255, 0.08)';
        };
        
        div.onclick = () => {
            createTab(app.url);
        };

        const img = document.createElement("img");
        img.src = app.img;
        img.style.cssText = "width: 60px; height: 60px; border-radius: 14px; object-fit: cover; margin-bottom: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.2);";
        
        const span = document.createElement("span");
        span.textContent = app.name;
        span.style.cssText = "font-size: 14px; color: var(--fg); text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 100%; font-weight: 500; text-shadow: 0 1px 3px rgba(0,0,0,0.5);";
        
        div.appendChild(img);
        div.appendChild(span);
        ntFavorites.appendChild(div);
    });
}'''
    html = html.replace(old_func, new_func)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
