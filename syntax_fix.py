import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

bad_code = """                const hubApps = document.getElementById("hubApps");
                if (hubGames) hubGames.classList.remove("active");
                if (hubApps) hubApps.classList.remove("active");
                const ntContent = document.querySelector(".nt-content");
                if (ntContent) ntContent.style.display = "";"""

good_code = """                const hubApps = document.getElementById("hubApps");
                if (hubGames) hubGames.classList.remove("active");
                if (hubApps) hubApps.classList.remove("active");
                if (ntContent) ntContent.style.display = "";"""

html = html.replace(bad_code, good_code)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done!")
