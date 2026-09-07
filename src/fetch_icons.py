"""Собирает SVG-спрайт из Simple Icons (CC0) и словарь фирменных цветов."""
import json, urllib.request, pathlib, re
SLUGS = """google googlesearchconsole googleanalytics googlegemini googlechrome googlemaps googleads anthropic claude
perplexity duckduckgo brave semrush lighthouse cloudflare wordpress tildapublishing nextdotjs telegram vk reddit wikipedia
youtube github mistralai deepseek habr maildotru figma notion python react vercel nginx letsencrypt shopify webflow framer
cursor ollama huggingface discord steam curseforge modrinth tripadvisor medium stackoverflow docker x tiktok instagram meta
apple pinterest twitch quora substack trustpilot yelp javascript html5 css safari firefox githubcopilot googletagmanager
matomo hotjar spotify""".split()
data = json.load(open("/Users/egor/.claude/jobs/dc65153a/tmp/si.json"))
icons = data["icons"] if isinstance(data, dict) else data
hexmap = {}
for i in icons:
    slug = i.get("slug") or re.sub(r"[^a-z0-9]", "", i["title"].lower())
    hexmap[slug] = i["hex"]
sym, brands, miss = [], {}, []
for s in SLUGS:
    try:
        svg = urllib.request.urlopen(f"https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/{s}.svg").read().decode()
    except Exception as e:
        miss.append(s); continue
    d = re.search(r'<path d="([^"]+)"', svg).group(1)
    sym.append(f'<symbol id="i-{s}" viewBox="0 0 24 24"><path d="{d}"/></symbol>')
    brands[s] = "#" + hexmap.get(s, "000000")
here = pathlib.Path(__file__).parent
(here / "sprite.html").write_text('<svg id="sprite" aria-hidden="true" style="position:absolute;width:0;height:0;overflow:hidden"><defs>' + "".join(sym) + "</defs></svg>", encoding="utf-8")
json.dump(brands, open(here / "brands.json", "w"), indent=1)
print("icons:", len(sym), "missing:", miss)
