import sys
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Change G U S T to R I F T
content = content.replace('<span class=\"gust-letter-G\">G</span><span class=\"gust-letter-U\">U</span><span class=\"gust-letter-S\">S</span><span class=\"gust-letter-T\">T</span>', '<span class=\"gust-letter-G\">R</span><span class=\"gust-letter-U\">I</span><span class=\"gust-letter-S\">F</span><span class=\"gust-letter-T\">T</span>')

# 2. Change GUST Browser / Gust Browser to RIFT Browser
content = content.replace('GUST Browser', 'RIFT Browser')
content = content.replace('Gust Browser', 'RIFT Browser')

# 3. Remove github button and stuff at bottom logo
github_btn_regex = r'<button class=\"nt-wallpaper-btn\" id=\"ntGithubBtn\" title=\"View on GitHub\"[\s\S]*?</button>'
content = re.sub(github_btn_regex, '', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
