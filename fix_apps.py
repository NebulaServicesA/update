with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

bad_str = r"""card.innerHTML = `<img class="banner" src="https://tse2.mm.bing.net/th?q=${encodeURIComponent(game.name + ' game thumbnail banner')}&w=320&h=180&c=7&rs=1&p=0" onerror="this.src='https://image.thum.io/get/width/320/crop/180/'+game.url"><div class="hub-overlay"><span>${game.name}</span></div>`;
                    card.onclick = () => go(app.url);"""

good_str = r"""card.innerHTML = `<img class="banner" loading="lazy" src="https://tse2.mm.bing.net/th?q=${encodeURIComponent(app.name + ' app logo wide')}&w=320&h=180&c=7&rs=1&p=0" onerror="this.src='https://image.thum.io/get/width/320/crop/180/'+app.url"><div class="hub-overlay"><span>${app.name}</span></div>`;
                    card.onclick = () => go(app.url);"""

html = html.replace(bad_str, good_str)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
