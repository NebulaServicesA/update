
import sys
import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Fix the missing backtick for div.style.cssText
html = html.replace("div.style.cssText = \n            display: flex;", "div.style.cssText = `\n            display: flex;")
# Fix the missing backtick at the end of cssText
html = html.replace("box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);\n        ;\n        \n        div.onmouseenter", "box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);\n        `;\n        \n        div.onmouseenter")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

