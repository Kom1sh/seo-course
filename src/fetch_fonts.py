"""Качает вариативные шрифты с Google Fonts (latin + cyrillic) и вшивает base64 в src/fonts.css."""
import re, urllib.request, base64, pathlib
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}
FAMS = ["Unbounded:wght@200..900", "Golos+Text:wght@400..900", "JetBrains+Mono:wght@400..700"]
KEEP = ("latin", "cyrillic")
out = []
for fam in FAMS:
    css = urllib.request.urlopen(urllib.request.Request(f"https://fonts.googleapis.com/css2?family={fam}&display=block", headers=UA)).read().decode()
    for m in re.finditer(r"/\* (\S+) \*/\s*@font-face\s*{(.*?)}", css, re.S):
        subset, body = m.group(1), m.group(2)
        if subset not in KEEP: continue
        url = re.search(r"url\((\S+?)\)", body).group(1)
        data = base64.b64encode(urllib.request.urlopen(url).read()).decode()
        body = re.sub(r"src:\s*url\(\S+?\)\s*format\('woff2'\);", f"src:url(data:font/woff2;base64,{data}) format('woff2');", body)
        out.append("@font-face{" + re.sub(r"\s+", " ", body).strip() + "}")
        print(fam, subset, len(data) // 1024, "КБ")
pathlib.Path(__file__).with_name("fonts.css").write_text("\n".join(out), encoding="utf-8")
print("fonts.css:", sum(len(x) for x in out) // 1024, "КБ")
