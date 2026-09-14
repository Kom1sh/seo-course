#!/usr/bin/env python3
"""Генерирует src/slides.html из данных (data.json) и текстов ниже.
Встреча 2: семантика и структура. Правится этот файл, затем: python3 src/make_slides.py && python3 src/build.py && python3 src/qa.py
"""
import json, pathlib, math, html
HERE = pathlib.Path(__file__).resolve().parent
D = json.load(open(HERE / "data.json", encoding="utf-8"))
BR = json.load(open(HERE / "brands.json"))
INK = "#1C1C1E"
# белые и чёрные фирменные цвета на белой плитке заменяем чернилами
for k, v in list(BR.items()):
    if v.upper() in ("#000000", "#FFFFFF", "#181717", "#191919"): BR[k] = INK
NAME = {"google": "Google", "googlesearchconsole": "Search Console", "googleanalytics": "Google Analytics", "googlegemini": "Gemini",
        "googlechrome": "Chrome", "googlemaps": "Google Maps", "googleads": "Google Ads", "anthropic": "Anthropic", "claude": "Claude",
        "perplexity": "Perplexity", "duckduckgo": "DuckDuckGo", "brave": "Brave", "semrush": "Semrush", "lighthouse": "Lighthouse",
        "cloudflare": "Cloudflare", "wordpress": "WordPress", "tildapublishing": "Tilda", "nextdotjs": "Next.js", "telegram": "Telegram",
        "vk": "VK", "reddit": "Reddit", "wikipedia": "Wikipedia", "youtube": "YouTube", "github": "GitHub", "mistralai": "Mistral",
        "deepseek": "DeepSeek", "habr": "Хабр", "maildotru": "Mail.ru", "figma": "Figma", "notion": "Notion", "githubcopilot": "Copilot",
        "googletagmanager": "Tag Manager", "matomo": "Matomo", "hotjar": "Hotjar"}

# ── штриховые иконки (свои, смысловые) ─────────────────────────────────────
UI = {
 "search": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/>',
 "robot": '<rect x="4.5" y="8.5" width="15" height="11" rx="2.5"/><path d="M12 8.5V4.5"/><circle cx="12" cy="3.5" r="1.2"/><circle cx="9" cy="14" r="1.3"/><circle cx="15" cy="14" r="1.3"/><path d="M2 13v3M22 13v3"/>',
 "book": '<path d="M3.5 5h6.5a2 2 0 0 1 2 2v13a2 2 0 0 0-2-2H3.5z"/><path d="M20.5 5H14a2 2 0 0 0-2 2v13a2 2 0 0 1 2-2h6.5z"/>',
 "podium": '<rect x="2.5" y="12.5" width="5.5" height="8.5" rx="1"/><rect x="9.25" y="5.5" width="5.5" height="15.5" rx="1"/><rect x="16" y="9.5" width="5.5" height="11.5" rx="1"/>',
 "link": '<path d="M10 14a4.5 4.5 0 0 0 6.4 0l2.6-2.6a4.5 4.5 0 0 0-6.4-6.4L11.2 6.4"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0L5 12.6a4.5 4.5 0 0 0 6.4 6.4l1.4-1.4"/>',
 "sitemap": '<rect x="9" y="2.5" width="6" height="4.5" rx="1"/><rect x="2.5" y="17" width="6" height="4.5" rx="1"/><rect x="15.5" y="17" width="6" height="4.5" rx="1"/><path d="M12 7v4.5M5.5 17v-5.5h13V17"/>',
 "gauge": '<path d="M4 16a8 8 0 0 1 16 0"/><path d="M12 16l4.5-5.5"/><circle cx="12" cy="16" r="1.3"/><path d="M3 20h18"/>',
 "shield": '<path d="M12 2.5 4 6v6c0 5 3.4 8.4 8 9.5 4.6-1.1 8-4.5 8-9.5V6z"/><path d="M9 12l2 2 4-4"/>',
 "check": '<circle cx="12" cy="12" r="9"/><path d="M8 12.5l2.6 2.6L16.5 9"/>',
 "no": '<circle cx="12" cy="12" r="9"/><path d="M6 6l12 12"/>',
 "phone": '<rect x="7" y="2.5" width="10" height="19" rx="2.2"/><path d="M11 18.5h2"/>',
 "list": '<path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1.2"/><circle cx="4.5" cy="12" r="1.2"/><circle cx="4.5" cy="18" r="1.2"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 "quote": '<path d="M4 15V9a3 3 0 0 1 3-3h2v5H6v4H4z"/><path d="M14 15V9a3 3 0 0 1 3-3h2v5h-3v4h-2z"/>',
 "chat": '<path d="M4 5.5h16v10H10l-5 4v-4H4z"/>',
 "doc": '<path d="M6 2.5h8l4 4v15H6z"/><path d="M14 2.5v4h4"/><path d="M9 12h6M9 16h6"/>',
 "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a14 14 0 0 1 0 18a14 14 0 0 1 0-18z"/>',
 "megaphone": '<path d="M3 10v4l11 4V6z"/><path d="M14 6v12"/><path d="M17.5 9.5a3 3 0 0 1 0 5"/><path d="M6 14l1.5 5"/>',
 "pin": '<path d="M12 21.5s-7-6.2-7-11.3a7 7 0 0 1 14 0c0 5.1-7 11.3-7 11.3z"/><circle cx="12" cy="10" r="2.5"/>',
 "refresh": '<path d="M20 12a8 8 0 1 1-2.3-5.7"/><path d="M20 3.5v4.5h-4.5"/>',
 "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
 "zap": '<path d="M13 2.5 5 13.5h6l-1 8 8-11h-6z"/>',
 "eye": '<path d="M1.5 12S5.5 5 12 5s10.5 7 10.5 7-4 7-10.5 7S1.5 12 1.5 12z"/><circle cx="12" cy="12" r="3"/>',
 "pen": '<path d="M4 20l3.2-.7L20 6.5a2.1 2.1 0 0 0-3-3L4.2 16.3z"/><path d="M15.5 5.5l3 3"/>',
 "arrow": '<path d="M4 12h16"/><path d="M13 5l7 7-7 7"/>',
 "coins": '<circle cx="9" cy="9" r="6"/><path d="M15.5 8.2A6 6 0 1 1 8.2 15.5"/>',
 "share": '<circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="M8.2 10.8l7.6-4.6M8.2 13.2l7.6 4.6"/>',
 "star": '<path d="M12 3l2.8 5.8 6.2.9-4.5 4.4 1.1 6.3L12 17.4l-5.6 3 1.1-6.3L3 9.7l6.2-.9z"/>',
 "flag": '<path d="M5 21V4"/><path d="M5 4h12l-2 4 2 4H5"/>',
 "home": '<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v10h13V10"/>',
 "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.3"/>',
 "layers": '<path d="M12 3 2.5 8 12 13l9.5-5z"/><path d="M2.5 12.5 12 17.5l9.5-5"/><path d="M2.5 17 12 22l9.5-5"/>',
}
def ui(name, cls=""): return f'<svg class="ui {cls}" viewBox="0 0 24 24" aria-hidden="true">{UI[name]}</svg>'

WORD = {"yandex": ("Яндекс", "#FC3F1D"), "chatgpt": ("ChatGPT", INK), "bing": ("Bing", "#008373"), "ahrefs": ("Ahrefs", "#FF8800"),
        "frog": ("Screaming Frog", "#4E7E2E"), "wordstat": ("Вордстат", "#FC3F1D"), "neuro": ("Нейро", "#5B3DF0"), "metrika": ("Метрика", "#FC3F1D"),
        "webmaster": ("Вебмастер", "#FC3F1D"), "pagespeed": ("PageSpeed", "#4285F4"), "tilda": ("Tilda", INK), "copilot": ("Copilot", INK),
        "alice": ("Алиса", "#5B3DF0"), "gsc": ("Search Console", "#458CF5")}
def ico(slug):
    return f'<svg class="ic" style="color:{BR.get(slug, INK)}"><use href="#i-{slug}"/></svg>'
def tile(slug, label=None, size="", extra=""):
    if slug in WORD:
        t, c = WORD[slug]; inner = f'<div class="tile word {size}" style="color:{c};{extra}">{t}</div>'
    else:
        inner = f'<div class="tile {size}" style="{extra}">{ico(slug)}</div>'
    if label is None or (slug in WORD and label == WORD[slug][0]): return inner
    return f'<div class="tl{" w" if slug in WORD else ""}">{inner}<span>{label}</span></div>'

def top(pill): return f'<div class="top"><span class="pill">{pill}</span><span class="cnt"></span></div>'
def slide(inner, title, cls=""): return f'<section class="s {cls}" data-t="{html.escape(title)}">{inner}</section>'
def sticky(kind, h, p, extra=""): return f'<div class="sticky {kind}">{extra}<h4>{h}</h4><p>{p}</p></div>'
def stat(n, l, cls=""): return f'<div class="stat {cls}"><div class="n">{n}</div><div class="l">{l}</div></div>'
def browser(url, img, w=None):
    """Окно браузера. Высота выводится из пропорций снимка, поэтому страница видна целиком."""
    st = f' style="max-width:{w}px"' if w else ""
    return f'<div class="browser"{st}><div class="bar"><i></i><i></i><i></i><span class="url">{url}</span></div><div class="shot"><img src="assets/{img}" alt=""></div></div>'
def arrow(): return '<div class="arr"><svg viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div>'
def step(n, h, p, kind="", icon=None, i=0):
    ic = ui(icon, "sm") if icon else ""
    return f'<div class="step {kind} r" style="--i:{i}"><div class="hd"><span class="num">{n}</span>{ic}</div><h4>{h}</h4><p>{p}</p></div>'
def fmt(n): return f"{int(round(n)):,}".replace(",", " ")

# ── графики: SVG фиксированного размера ─────────────────────────────────────
def nice(v):
    """Округляет потолок оси до «красивого» числа: 1621 → 2000, 537 → 600, 38 → 40."""
    if v <= 0: return 1
    import math as _m
    mag = 10 ** _m.floor(_m.log10(v)); f = v / mag
    for step in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if f <= step: return step * mag
    return 10 * mag

def line_chart(points, w=760, h=330, color="#0FBCB0", fill="#C3FAF5", every=1, vline=None, ymax=None, mark_last=True, mark_peak=False, xfmt=None, dot_r=5):
    L, R, T, B = 74, 24, 28, 44
    vals = [v for _, v in points]; ymax = ymax or nice(max(vals) * 1.12) or 1
    n = len(points); xs = [L + (w - L - R) * i / max(1, n - 1) for i in range(n)]
    ys = [T + (h - T - B) * (1 - v / ymax) for v in vals]
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">']
    ticks = 4
    for k in range(ticks + 1):
        yy = T + (h - T - B) * k / ticks; vv = ymax * (1 - k / ticks)
        out.append(f'<line x1="{L}" x2="{w-R}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="#E0E2E8" stroke-width="1"/>')
        out.append(f'<text class="ax" x="{L-10}" y="{yy+5:.1f}" text-anchor="end">{fmt(vv)}</text>')
    area = f"M{xs[0]:.1f},{h-B} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in zip(xs, ys)) + f" L{xs[-1]:.1f},{h-B} Z"
    line = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    out.append(f'<path d="{area}" fill="{fill}"/>'); out.append(f'<path d="{line}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>')
    for i, (lab, v) in enumerate(points):
        if i == n - 1 or (i % every == 0 and n - 1 - i >= max(2, every // 2)):
            out.append(f'<text class="ax" x="{xs[i]:.1f}" y="{h-14}" text-anchor="middle">{xfmt(lab) if xfmt else lab}</text>')
    if vline is not None:
        i, txt = vline; out.append(f'<line x1="{xs[i]:.1f}" x2="{xs[i]:.1f}" y1="{T-8}" y2="{h-B}" stroke="{INK}" stroke-width="2" stroke-dasharray="6 6"/>')
        out.append(f'<text class="val" x="{xs[i]+10:.1f}" y="{T+8}" text-anchor="start">{txt}</text>')
    if mark_last:
        out.append(f'<circle cx="{xs[-1]:.1f}" cy="{ys[-1]:.1f}" r="{dot_r+2}" fill="#fff" stroke="{color}" stroke-width="4"/>')
        out.append(f'<text class="val" x="{xs[-1]-14:.1f}" y="{ys[-1]-16:.1f}" text-anchor="end" style="font-size:22px">{fmt(vals[-1])}</text>')
    if mark_peak and n > 1:
        out.append(f'<circle cx="{xs[0]:.1f}" cy="{ys[0]:.1f}" r="{dot_r}" fill="#fff" stroke="{color}" stroke-width="3"/>')
        out.append(f'<text class="val" x="{xs[0]+12:.1f}" y="{ys[0]-14:.1f}" text-anchor="start">{fmt(vals[0])}</text>')
    out.append("</svg>"); return "".join(out)

def bars(cats, series, w=760, h=330, suffix="", ymax=None):
    L, R, T, B = 60, 16, 30, 44
    allv = [v for _, _, vals in series for v in vals]; ymax = ymax or nice(max(allv) * 1.15) or 1
    n, m = len(cats), len(series); gw = (w - L - R) / n; bw = min(78, gw * 0.7 / m); gap = 8
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">']
    for k in range(5):
        yy = T + (h - T - B) * k / 4; out.append(f'<line x1="{L}" x2="{w-R}" y1="{yy:.1f}" y2="{yy:.1f}" stroke="#E0E2E8"/>')
        out.append(f'<text class="ax" x="{L-10}" y="{yy+5:.1f}" text-anchor="end">{ymax*(1-k/4):.0f}{suffix}</text>')
    for ci, c in enumerate(cats):
        cx = L + gw * ci + gw / 2; total = m * bw + (m - 1) * gap; x0 = cx - total / 2
        for si, (name, color, vals) in enumerate(series):
            v = vals[ci]; x = x0 + si * (bw + gap); hh = (h - T - B) * v / ymax; y = h - B - hh
            out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{max(hh,2):.1f}" rx="8" fill="{color}"/>')
            lab = ("—" if v is None else f"{v:g}{suffix}")
            out.append(f'<text class="val" x="{x+bw/2:.1f}" y="{y-10:.1f}" text-anchor="middle">{lab}</text>')
        out.append(f'<text class="ax" x="{cx:.1f}" y="{h-14}" text-anchor="middle" style="font-size:17px;fill:{INK};font-weight:500">{c}</text>')
    out.append("</svg>"); return "".join(out)

def hbars(items, w=700, rowh=52, maxv=None, labw=300, color="#0FBCB0", fmtv=fmt, mono=False):
    maxv = maxv or max(v for _, v, *_ in items)
    h = rowh * len(items); out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">']
    for i, it in enumerate(items):
        lab, v = it[0], it[1]; col = it[2] if len(it) > 2 else color
        y = i * rowh; bw = (w - labw - 110) * v / maxv
        fam = "font-family:var(--fm);font-weight:500;font-size:16px" if mono else "font-size:18px;font-weight:500"
        out.append(f'<text x="{labw-14}" y="{y+rowh/2+6}" text-anchor="end" style="{fam};fill:{INK}">{html.escape(lab)}</text>')
        out.append(f'<rect x="{labw}" y="{y+rowh/2-14}" width="{max(bw,3):.1f}" height="28" rx="8" fill="{col}"/>')
        out.append(f'<text class="val" x="{labw+bw+12:.1f}" y="{y+rowh/2+6}">{fmtv(v)}</text>')
    out.append("</svg>"); return "".join(out)

def donut(parts, size=300, thick=46, center=""):
    r = (size - thick) / 2; c = math.pi * 2 * r; tot = sum(v for _, v, _ in parts); off = 0
    out = [f'<svg viewBox="0 0 {size} {size}" width="{size}" height="{size}" aria-hidden="true"><g transform="rotate(-90 {size/2} {size/2})">']
    for lab, v, col in parts:
        seg = c * v / tot
        out.append(f'<circle cx="{size/2}" cy="{size/2}" r="{r}" fill="none" stroke="{col}" stroke-width="{thick}" stroke-dasharray="{seg:.2f} {c-seg:.2f}" stroke-dashoffset="{-off:.2f}"/>')
        off += seg
    out.append("</g>")
    if center: out.append(f'<text x="{size/2}" y="{size/2+12}" text-anchor="middle" class="val" style="font-size:34px">{center}</text>')
    out.append("</svg>"); return "".join(out)

def graph(orphan=True, w=640, h=420):
    """Схема ссылок: узлы-страницы и связи; одна страница-сирота."""
    nodes = {"home": (110, 92, "Главная"), "a": (330, 74, "/guide"), "b": (500, 90, "/create"), "c": (200, 230, "/tacz"),
             "d": (400, 220, "/guide/verstak"), "e": (560, 250, "/download"), "f": (300, 360, "/blog"), "o": (100, 360, "/steam-deck")}
    edges = [("home", "a"), ("home", "b"), ("home", "c"), ("a", "d"), ("b", "d"), ("b", "e"), ("c", "f"), ("d", "f"), ("a", "c")]
    out = [f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true">']
    for a, b in edges:
        x1, y1, _ = nodes[a]; x2, y2, _ = nodes[b]; out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#C9CCD4" stroke-width="3"/>')
    for k, (x, y, lab) in nodes.items():
        iso = (k == "o")
        fill = "#FFC6C6" if iso else ("#C3FAF5" if k == "home" else "#F7F8FA"); stroke = "#600000" if iso else "#0FBCB0" if k == "home" else "#C9CCD4"
        out.append(f'<rect x="{x-52}" y="{y-26}" width="104" height="52" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        out.append(f'<text x="{x}" y="{y+5}" text-anchor="middle" style="font-family:var(--fm);font-weight:500;font-size:13px;fill:{INK}">{lab}</text>')
    hx, hy, _ = nodes["home"]
    out.append(f'<circle cx="{hx-36}" cy="{hy-62}" r="16" fill="{INK}"/><circle cx="{hx-41}" cy="{hy-65}" r="2.5" fill="#fff"/><circle cx="{hx-31}" cy="{hy-65}" r="2.5" fill="#fff"/><path d="M{hx-42} {hy-56} q6 5 12 0" stroke="#fff" stroke-width="2" fill="none"/>')
    out.append(f'<text x="{hx-12}" y="{hy-57}" style="font-size:16px;font-weight:500;fill:{INK}">робот идёт по ссылкам</text>')
    ox, oy, _ = nodes["o"]
    out.append(f'<text x="{ox}" y="{oy+52}" text-anchor="middle" style="font-size:16px;font-weight:500;fill:#600000">ни одной входящей ссылки</text>')
    out.append("</svg>"); return "".join(out)


def qcard(kind, label, q, meta, page, win=None):
    tail = f'<span class="pill" style="margin-top:auto;align-self:flex-start">{win}</span>' if win else ""
    return f'<div class="sticky {kind}"><span class="lab">{label}</span><div class="qcard"><div class="q">{q}</div><div class="meta">{meta}</div></div><p>{page}</p>{tail}</div>'

def plist(items, icon):
    return '<ul class="plist">' + "".join(
        f'<li>{ui(icon, "xs")}<div><b>{h}</b><i>{p}</i></div></li>' for h, p in items) + '</ul>'

def divider(n, title, sub, items):
    return slide(top("Раздел " + n) + f'<div class="body"><div class="row fill" style="gap:60px;align-items:flex-end"><div style="flex:1.2;display:flex;flex-direction:column;height:100%">'
      f'<div class="divn">{n}</div><div style="margin-top:auto"><div class="divt">{title}</div><div class="divs">{sub}</div></div></div>'
      f'<div class="divlist" style="flex:1;padding-bottom:12px">{"".join(f"<span>{x}</span>" for x in items)}</div></div></div>', f"Раздел {n}: {title}", "dark")


# ═══════════════════════════════════════════════════════════════════════════
#  ВСТРЕЧА 2 · СЕМАНТИКА И СТРУКТУРА
# ═══════════════════════════════════════════════════════════════════════════
WORD.update({"keysso": ("Keys.so", "#E8473C"), "topvisor": ("Топвизор", "#2F6BFF"), "rush": ("Rush Analytics", "#1B1F3B"),
             "kc": ("Key Collector", "#3C7A3C"), "bukvarix": ("Букварикс", "#E08A00")})
PER = "13 августа — 12 сентября 2026"
SUG = D["suggest"]; TL = D["tail"]; CLU = D["clusters"]; CAN = D["cannibal"]; MPK = D["mapka"]
ARR = '<svg viewBox="0 0 24 24"><path d="M4 12h16M13 5l7 7-7 7"/></svg>'

def chips(items, cls=""):
    return '<div class="chips">' + "".join(f'<span class="chip {cls}">{html.escape(x)}</span>' for x in items) + '</div>'

def flow(items, url, n, label, cls="t"):
    return (f'<div class="flow">{chips(items, cls)}<div class="to">{ARR}</div>'
            f'<div class="page"><span class="u">{url}</span><span class="n">{n}</span><span class="l">{label}</span></div></div>')

def suggest_box(typed, items, n=8):
    lis = ""
    for it in items[:n]:
        if it.startswith(typed) and it != typed:
            lis += f'<li>{ui("search")}<span>{html.escape(typed)}<b>{html.escape(it[len(typed):])}</b></span></li>'
        else:
            lis += f'<li>{ui("search")}<span><b>{html.escape(it)}</b></span></li>'
    return f'<div class="sugg"><div class="in">{ui("search")}<span>{html.escape(typed)}</span><i></i></div><ul>{lis}</ul></div>'

def diagram(w, h, nodes, edges, nh=58, badges=()):
    """Дерево: узлы HTML на абсолютных координатах центра, линии уступом на svg под ними."""
    svg = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" aria-hidden="true">']
    for a, b in edges:
        ax, ay = nodes[a][0], nodes[a][1] + nh / 2
        bx, by = nodes[b][0], nodes[b][1] - nh / 2
        my = (ay + by) / 2
        svg.append(f'<path d="M{ax},{ay} V{my} H{bx} V{by}" fill="none" stroke="#C9CCD4" stroke-width="2"/>')
    svg.append("</svg>")
    divs = []
    for k, (x, y, nw, t, sub, cls) in nodes.items():
        s = f'<small>{sub}</small>' if sub else ""
        divs.append(f'<div class="node {cls}" style="left:{x}px;top:{y}px;width:{nw}px;height:{nh}px"><b>{t}</b>{s}</div>')
    bd = "".join(f'<span class="cnt2" style="left:{x}px;top:{y}px">{t}</span>' for x, y, t in badges)
    return f'<div class="dg" style="width:{w}px;height:{h}px">' + "".join(svg) + "".join(divs) + bd + '</div>'

def matrix(rows, cols, data, rowlab, collab):
    out = [f'<div class="mx" style="grid-template-columns:170px repeat({len(cols)},minmax(0,1fr))"><div></div>']
    out += [f'<div class="h">{collab[c]}</div>' for c in cols]
    for r in rows:
        out.append(f'<div class="rh">{rowlab[r]}</div>')
        out += [f'<div class="c{" on" if on else ""}"></div>' for on in data[r]]
    return "".join(out) + '</div>'

S = []

# 01 обложка
cover_groups = [
    ("t", ["курсы английского языка ростов на дону", "школа английского языка в ростове на дону", "английский для взрослых ростов на дону"], "/kursy-dlya-vzroslyh"),
    ("l", ["английский для детей ростов-на-дону", "английский язык для детей ростов на дону"], "/dlya-detey"),
    ("y", ["подготовка к егэ по английскому 2026", "подготовка к егэ по английскому с нуля"], "/ege"),
]
cover_right = "".join(
    f'<div class="sticky {"teal" if k == "t" else "lav" if k == "l" else "yel"} tight" style="gap:10px">{chips(q, k)}'
    f'<div style="display:flex;align-items:center;gap:10px;font:500 19px/1 var(--fm);color:var(--ink)">'
    f'<svg class="ui xs" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h16"/><path d="M13 5l7 7-7 7"/></svg>{u}</div></div>'
    for k, q, u in cover_groups)
S.append(slide(top("Школа Икс, факультатив. Встреча 2 из 5") +
  '<div class="body cover"><div class="row fill" style="gap:44px">'
  '<div style="flex:1;display:flex;flex-direction:column;min-width:0">'
  '<h1>Семантика<br>и структура</h1>'
  '<p class="sub">Как узнать, что люди ищут, и разложить это по страницам сайта. На живых данных Мапки и techkio.</p>'
  '<div class="who"><div><b>Егор Протасов<span class="mono" style="font-weight:500;font-size:19px;color:var(--blue);margin-left:14px">egorprotasov.ru</span></b>'
  '<br><span>SEO-специалист и PM. Автор проектов мапка.рф, techkio.ru, mediachef.app</span></div>'
  '<div><b>Суббота</b><br><span>90 минут, для 1–3 курсов</span></div></div></div>'
  f'<div style="width:640px;flex:none;display:flex;flex-direction:column;gap:14px;justify-content:center">{cover_right}</div>'
  '</div></div>', "Обложка", "cover"))

# 02 где мы
S.append(slide(top("В прошлый раз") + '<h1>Поиск находит, запоминает и сортирует страницы. Сегодня разбираем, какие страницы ему дать</h1>'
  '<div class="body"><div class="pipe" style="margin:auto 0 22px">'
  + step("1", "Сканирование", "Робот идёт по ссылкам и скачивает страницы.", "grey", "robot", 0) + arrow()
  + step("2", "Индексация", "Кладёт страницу в базу под одним адресом.", "grey", "book", 1) + arrow()
  + step("3", "Ранжирование", "Сортирует под запрос: кто лучше ответил на намерение.", "grey", "podium", 2)
  + '</div><div class="sticky gold" style="flex-direction:row;align-items:center;gap:22px;margin-bottom:auto">'
  + ui("target", "lg") + '<div><h4>Сегодня: что именно люди ищут и какими страницами на это ответить</h4>'
  '<p>Без этого поисковику нечего находить: хорошая техника не спасёт сайт, на котором нет страницы под запрос.</p></div></div></div>', "Где мы"))

# 03 план
S.append(slide(top("План на сегодня") + '<h1>От запросов к карте сайта: пять шагов за полтора часа</h1>'
  '<div class="body"><div class="pipe" style="margin:auto 0">'
  + step("1", "Спрос", "15 минут. Частотность, намерение, время в запросах.", "", "gauge", 0) + arrow()
  + step("2", "Где брать", "15 минут. Подсказки, Вордстат, свой Вебмастер, сервисы.", "", "search", 1) + arrow()
  + step("3", "Чистка и кластеры", "15 минут. Что выкинуть и как понять, одна страница или две.", "", "layers", 2) + arrow()
  + step("4", "Структура", "20 минут. Дерево, фасеты, адреса, перелинковка.", "", "sitemap", 3) + arrow()
  + step("5", "Практикум", "25 минут. Ядро и дерево для ниши, которую выберем.", "", "pen", 4)
  + '</div><p class="foot">Слайды остаются по ссылке, записывать не нужно. Вопросы задавайте по ходу.</p></div>', "План"))

# 04 длинный хвост
tk, mp = TL["techkio"], TL["mapka"]
S.append(slide(top("С чего начать") + f'<h1>За месяц у techkio {fmt(tk["queries"])} разных запроса. Десять самых частых дают {tk["buckets"][0]}% показов</h1>'
  '<div class="body"><div class="row fill" style="gap:36px;align-items:center">'
  f'<div class="chart" style="flex:1.2">{bars(["топ-10", "11–100", "101–1000", "1001 и дальше"], [("techkio.ru", "#0FBCB0", tk["buckets"]), ("мапка.рф", "#FFD02F", mp["buckets"])], w=840, h=420, suffix="%", ymax=50)}'
  '<div class="leg"><span><i style="background:#0FBCB0"></i>techkio.ru</span><span><i style="background:#FFD02F"></i>мапка.рф</span><span>доля всех показов в Яндексе</span></div></div>'
  '<div style="flex:1;display:flex;flex-direction:column;gap:16px">'
  + sticky("yel", "Сайт растёт на хвосте, а не на пяти главных словах", "Почти половина показов приходится на запросы с сотого места по тысячное. Угадать их заранее нельзя, их собирают.")
  + f'<div class="card"><div class="stat sm"><div class="n">{mp["le5"]}%</div><div class="l">запросов Мапки показаны за месяц пять раз или меньше. По одному они ничего не весят, вместе дают трафик.</div></div></div>'
  + f'</div></div><p class="foot">Яндекс Вебмастер, все запросы за {PER}: techkio.ru — {fmt(tk["queries"])}, мапка.рф — {fmt(mp["queries"])}.</p></div>', "Длинный хвост"))

# 05 голосование за нишу
SN = D["suggest_niches"]
NICHES = [("1", "Школа английского", "Много намерений: дети, взрослые, ЕГЭ, онлайн.", [SN["школа английского ростов"][5], SN["школа английского ростов"][2]]),
          ("2", "Кофейня", "Почти весь спрос локальный: рядом, в центре, открыто.", [SN["кофейня ростов"][2], SN["кофейня ростов"][5]]),
          ("3", "Барбершоп", "Услуги, цены, мастера и районы города.", [SN["барбершоп ростов"][2], SN["барбершоп ростов"][5]]),
          ("4", "Секция единоборств", "Вид спорта, возраст и район, как на Мапке.", [SN["секция единоборств для детей ростов"][0]]),
          ("5", "Ремонт телефонов", "Модели, поломки и районы: сотни узких страниц.", [SN["ремонт телефонов ростов"][2], SN["ремонт телефонов ростов"][3]]),
          ("6", "Доставка цветов", "Повод, срочность, цена и сезонность.", [SN["доставка цветов ростов"][4], SN["доставка цветов ростов"][5]])]
S.append(slide(top("Учебный кейс") + '<h1>Выбираем нишу на всю серию</h1>'
  '<div class="body"><div class="vote" style="margin:auto 0">'
  + "".join(f'<div class="sticky tight {"gold" if n == "1" else "grey"}"><span class="num{" w" if n == "1" else ""}">{n}</span><div style="display:flex;flex-direction:column;gap:10px"><h4>{h}</h4><p>{p}</p>{chips(q)}</div></div>' for n, h, p, q in NICHES)
  + '</div><p class="foot">Голосуем руками. Ход показываю на школе английского, вы повторяете на победившей нише. Под каждой нишей — настоящие подсказки Яндекса для Ростова, 14.09.2026.</p></div>', "Выбор ниши"))

S.append(divider("01", "Что люди ищут", "Как устроен спрос: частотность, намерение и время в запросах.",
                 ["Словарь на шесть слов", "Чем длиннее запрос, тем точнее желание", "Намерение и город", "Время в запросах"]))

# 07 словарь
T7 = [("Запрос", "«английский для детей ростов»", "Что человек набрал в строке поиска, дословно и со всеми ошибками."),
      ("Маркер", "«английский», «репетитор»", "Короткое слово, от которого разворачивают сбор. Смысл ниши в одном слове."),
      ("Семантическое ядро", "таблица запросов", "Все запросы, по которым сайт хочет находиться, с частотой и намерением."),
      ("Кластер", "группа запросов", "Запросы с одним намерением. Отвечает на них одна страница."),
      ("Частотность", "показы в месяц", "Сколько раз запрос ввели за месяц. Берётся из Вордстата."),
      ("Посадочная", "страница под кластер", "Куда человек попадает из поиска по запросам этого кластера.")]
S.append(slide(top("Словарь") + '<h1>Шесть слов, без которых сегодня не разобраться</h1>'
  '<div class="body"><div class="kv" style="margin:auto 0">' + "".join(
  f'<div class="it"><div class="k">{k}<small>{s}</small></div><div class="v">{v}</div></div>' for k, s, v in T7) + '</div></div>', "Словарь"))

# 08 лестница конкретики
ST = [("ВЧ", "английский", "Учить, перевести слово, купить курс? Непонятно, чего человек хочет."),
      ("СЧ", "курсы английского языка", "Хочет учиться. Где, для кого и в каком формате, пока неясно."),
      ("НЧ", "курсы английского языка ростов на дону", "Город известен. Человек выбирает школу."),
      ("НЧ", "курсы английского языка в ростове на дону для взрослых", "Знает, чего хочет. Осталось найти страницу, которая это обещает.")]
S.append(slide(top("Частотность") + '<h1>Чем длиннее запрос, тем точнее человек знает, чего хочет</h1>'
  '<div class="body"><div class="stairs" style="margin:auto 0">' + "".join(
  f'<div class="stair" style="margin-left:{i * 56}px"><span class="tag">{t}</span><span class="q">{q}</span><span class="d">{d}</span></div>' for i, (t, q, d) in enumerate(ST))
  + '</div><p class="foot">ВЧ, СЧ, НЧ — высоко-, средне- и низкочастотные. Границы зависят от ниши и города. Все четыре запроса — настоящие подсказки Яндекса для Ростова, 14 сентября 2026.</p></div>', "От общего к конкретному"))

# 09 намерение и город
geo = [x.replace("английский для взрослых ", "") for x in SUG["английский для взрослых"][1:6]]
S.append(slide(top("Намерение") + '<h1>Один маркер — разные намерения. Яндекс ещё и учитывает город</h1>'
  '<div class="body"><div class="g4 fill">'
  + qcard("lav", "Информационный", "как выучить английский язык самостоятельно дома", "подсказка Яндекса", "Человек хочет разобраться сам. Отвечает статья или гайд, а не страница курсов.", "Нужна: статья")
  + qcard("teal", "Коммерческий", "курсы английского языка в ростове на дону для взрослых", "подсказка Яндекса", "Готов платить и выбирает. Отвечает страница услуги с ценами и адресом.", "Нужна: услуга")
  + qcard("grey", "Навигационный", "макси кидс ростов", "мапка.рф в Вебмастере", "Ищет конкретную организацию. Отвечает её сайт или карточка в каталоге.", "Нужна: карточка")
  + qcard("yel", "Зависит от города", "английский для взрослых", "подсказки Яндекса", "Яндекс сам достроил: " + ", ".join(geo) + ". Без города на странице она не для этого запроса.", "Нужен: город")
  + '</div><p class="foot">Подсказки Яндекса, 14 сентября 2026. Намерение определяет тип страницы: одна и та же тема на услуге и в статье — две разные страницы.</p></div>', "Намерение и город"))

# 10 время в запросах
ege = [x for x in SUG["подготовка к егэ по английскому"] if "2026" in x][:3]
S.append(slide(top("Сезонность") + '<h1>В запросах живёт время: год, сезон, праздник</h1>'
  '<div class="body"><div class="g3" style="margin:auto 0">'
  + f'<div class="sticky yel"><span class="lab">Год прямо в запросе</span>{chips(ege, "y")}<p>Страницу с «2026» в заголовке придётся обновить в следующем сезоне, иначе она устареет вместе с годом.</p></div>'
  + sticky("teal", "Сезон виден в Вордстате", "Вкладка «Динамика» показывает спрос помесячно с 2018 года и подневно за последние два месяца. Пик и спад видны сразу.", ui("gauge", "lg"))
  + sticky("grey", "Страницу готовят до пика", "Роботу нужно время дойти и проиндексировать. Страница к сентябрю пишется летом, к 8 марта — в январе.", ui("clock", "lg"))
  + '</div><p class="foot">Подсказки Яндекса, 14 сентября 2026. Данные вкладки «Динамика» — гайд по Вордстату 2026, wehaveidea.ru.</p></div>', "Время в запросах"))

S.append(divider("02", "Где брать запросы", "Шесть источников, из них четыре бесплатные.",
                 ["Откуда вообще берутся запросы", "Подсказки поиска", "Вордстат в 2026 году и его операторы", "Свой Вебмастер", "Сервисы и ИИ"]))

# 12 шесть источников
SRC6 = [("teal", "user", "Голова и клиенты", "Как люди сами называют проблему: отзывы, переписки, звонки. Отсюда маркеры."),
        ("teal", "search", "Подсказки поиска", "Что уже набирают люди. Бесплатно, живьём, с учётом города."),
        ("teal", "gauge", "Вордстат", "Частотность, динамика по месяцам и спрос по регионам. Главный источник цифр по Яндексу."),
        ("yel", "eye", "Свой Вебмастер", "По каким запросам сайт уже показывают. Самые честные данные, но нужен свой сайт."),
        ("grey", "target", "Конкуренты", "По каким запросам видны другие сайты ниши. Платные сервисы вроде Keys.so."),
        ("grey", "chat", "ИИ-ассистент", "Синонимы, жаргон, вопросы клиентов. Цифры не даёт, только слова.")]
S.append(slide(top("Источники") + '<h1>Запросы берут из шести мест, и четыре из них бесплатные</h1>'
  '<div class="body"><div class="g3 fill" style="grid-template-rows:repeat(2,minmax(0,1fr))">'
  + "".join(sticky(k, h, p, ui(i, "lg")) for k, i, h, p in SRC6)
  + '</div></div>', "Источники запросов"))

# 13 подсказки
S.append(slide(top("Подсказки поиска") + '<h1>Подсказки — бесплатный список того, что уже набирают люди</h1>'
  '<div class="body"><div class="row fill" style="gap:26px;align-items:center">'
  f'<div style="flex:1.05">{suggest_box("курсы английского языка", SUG["курсы английского языка"], 8)}</div>'
  f'<div style="flex:1;display:flex;flex-direction:column;gap:18px">{suggest_box("школа английского ростов", SUG["школа английского ростов"], 5)}'
  + '<div class="card"><h4>Как выжать больше</h4><p>Добавляйте к маркеру буквы по алфавиту: «курсы английского а», «…б», «…в». И проверяйте в режиме инкогнито, чтобы история не подмешивала своё.</p></div></div>'
  + '</div><p class="foot">Настоящие подсказки Яндекса для Ростова-на-Дону, сняты 14 сентября 2026. Среди них уже есть «онлайн», «для взрослых», «таганрог» и «бесплатно» — к ним вернёмся на чистке.</p></div>', "Подсказки"))

# 14 Вордстат 2026
S.append(slide(top("Вордстат") + '<h1>Вордстат — главный источник цифр по Яндексу. С 2025 года он выглядит иначе</h1>'
  '<div class="body"><div class="row fill" style="gap:26px">'
  '<div style="flex:1;display:flex;flex-direction:column;gap:14px;justify-content:center">'
  '<div class="card"><span class="lab mono" style="color:var(--slate);font-size:16px">июнь 2025</span><h4>Бесплатный API по заявке</h4><p>Те же данные можно забирать программой, без ручного копирования.</p></div>'
  '<div class="card"><span class="lab mono" style="color:var(--slate);font-size:16px">11 августа 2025</span><h4>Старую версию отключили</h4><p>Все инструкции со скриншотами старого Вордстата устарели.</p></div>'
  '<div class="card"><span class="lab mono" style="color:var(--slate);font-size:16px">25 августа 2026</span><h4>Меню слева и поле минус-слов</h4><p>Разделы собраны в вертикальное меню, для минус-слов отдельное поле, появился помощник.</p></div></div>'
  '<div style="flex:1.2;display:grid;grid-template-rows:repeat(3,minmax(0,1fr));gap:14px">'
  + sticky("teal", "Топ запросов", "Что искали вместе с маркером за последние 30 дней, отдельно с телефонов и компьютеров.", ui("list", "lg")).replace('class="sticky teal"', 'class="sticky teal tight" style="flex-direction:row;gap:18px;align-items:center"')
  + sticky("yel", "Динамика", "Спрос помесячно с 2018 года и подневно за последние два месяца. Отсюда сезонность.", ui("gauge", "lg")).replace('class="sticky yel"', 'class="sticky yel tight" style="flex-direction:row;gap:18px;align-items:center"')
  + sticky("lav", "Регионы", "Где спрос выше среднего: по городам и областям. Отсюда решение про города на сайте.", ui("pin", "lg")).replace('class="sticky lav"', 'class="sticky lav tight" style="flex-direction:row;gap:18px;align-items:center"')
  + '</div></div><p class="foot">Хабр и ppc.world — API, 2025; lucky-seo.com — отключение старой версии; Топвизор Журнал — обновление 25.08.2026; wehaveidea.ru — вкладки.</p></div>', "Вордстат 2026"))

# 15 операторы
OPS = [('" "', "Только эти слова, без добавок, в любой форме", '"курсы английского"'),
       ("!", "Точная форма слова", "!курсы !английского"),
       ("[ ]", "Точный порядок слов", "[английский для детей]"),
       ("+", "Учесть предлог. Работает только в «Динамике»", "английский +для детей"),
       ("( | )", "Перебрать варианты одним запросом", "(курсы|школа) английского"),
       ("−", "Выкинуть запросы с этим словом", "курсы английского -бесплатно")]
S.append(slide(top("Операторы Вордстата") + '<h1>Шесть операторов превращают Вордстат из счётчика в инструмент</h1>'
  '<div class="body"><div class="tbl fill" style="grid-template-columns:150px minmax(0,1.1fr) minmax(0,1fr)">'
  '<div class="h">Оператор</div><div class="h">Что делает</div><div class="h">Пример на нашей нише</div>'
  + "".join(f'<div class="k mono" style="font-size:26px">{html.escape(o)}</div><div>{d}</div><div class="mono" style="font-size:20px;color:var(--ink)">{html.escape(e)}</div>' for o, d, e in OPS)
  + '</div><p class="foot">Операторы интерфейса 2026 года: wehaveidea.ru, pr-cy.ru. Минус-слова с августа 2026 можно вписать в отдельное поле.</p></div>', "Операторы"))

# 16 частота без кавычек обманывает
S.append(slide(top("Три частоты") + '<h1>Без кавычек Вордстат считает всё подряд. Сравнивают точную частоту</h1>'
  '<div class="body"><div class="nest teal" style="margin:auto 0">'
  '<span class="k">Базовая частота</span><span class="q">английский</span>'
  '<span class="d">Все запросы, где встречается слово: «английский алфавит», «перевод с английского», «английский для детей». Для решения бесполезна.</span>'
  '<div class="nest" style="background:#fff;margin-top:6px"><span class="k">Фразовая</span><span class="q">"курсы английского"</span>'
  '<span class="d">Только запросы ровно из этих слов, в любой форме и порядке.</span>'
  '<div class="nest yel" style="margin-top:6px"><span class="k">Точная</span><span class="q">"!курсы !английского"</span>'
  '<span class="d">Ровно эта фраза в этой форме. Именно её пишут в таблицу ядра.</span></div></div></div>'
  '<p class="foot">На практикуме вбиваем все три варианта одного запроса и сравниваем цифры сами.</p></div>', "Три частоты"))

# 17 свой Вебмастер
WANT = ["услуги секций и кружков", "алекс фитнес ростов-на-дону левенцовка", "бассейн дгту", "киндер спейс", "макси кидс ростов-на-дону", "южный меридиан"]
wmrows = [r for r in D["wm_mapka"] if r[0] in WANT]
S.append(slide(top("Свой спрос") + '<h1>Самые честные запросы — те, по которым вас уже показывают</h1>'
  '<div class="body"><div class="row fill" style="gap:32px;align-items:center">'
  '<div style="flex:1.35"><div class="tbl" style="grid-template-columns:minmax(0,1fr) 120px 110px 120px">'
  '<div class="h">Запрос к мапка.рф в Яндексе</div><div class="h" style="text-align:right">Показы</div><div class="h" style="text-align:right">Клики</div><div class="h" style="text-align:right">Позиция</div>'
  + "".join(f'<div class="mono" style="font-size:19px;color:var(--ink)">{q}</div><div style="text-align:right">{fmt(s)}</div>'
            f'<div style="text-align:right;{"color:var(--coral-d);font-weight:600" if c == 0 else ""}">{c}</div><div style="text-align:right">{str(p).replace(".", ",")}</div>' for q, s, c, p in wmrows)
  + '</div></div><div style="flex:1;display:flex;flex-direction:column;gap:16px">'
  + sticky("coral", "Показы без кликов — готовая задача", "Сотни показов и ноль кликов: страница есть, но стоит низко или сниппет не обещает то, что ищут.")
  + sticky("grey", "И заодно чистка", "Что ищут на самом деле: расписание сети фитнес-клубов или детскую секцию? От ответа зависит, работать со страницей или отпустить запрос.")
  + f'</div></div><p class="foot">Яндекс Вебмастер, мапка.рф, {PER}. Раздел «Поисковые запросы» → «Популярные запросы».</p></div>', "Свой Вебмастер"))

# 18 сервисы в РФ
TOOLS = [("Бесплатно", [("wordstat", "Вордстат"), ("webmaster", "Вебмастер"), ("bukvarix", "Букварикс")], "база Букварикса — больше 2 млрд фраз"),
         ("Запросы конкурентов", [("keysso", "Keys.so")], "по каким запросам видны другие сайты"),
         ("Кластеризация по выдаче", [("topvisor", "Топвизор"), ("rush", "Rush Analytics")], "база Топвизора — больше 3 млрд запросов"),
         ("Большие ядра на компьютере", [("kc", "Key Collector")], "программа, платная лицензия")]
S.append(slide(top("Сервисы") + '<h1>Чем собирать в России: для учёбы хватает трёх бесплатных</h1>'
  '<div class="body"><div class="fill" style="display:flex;flex-direction:column;gap:8px;justify-content:center">' + "".join(
  f'<div class="row" style="align-items:center;gap:28px;padding:12px 0;border-bottom:1px solid var(--hair)"><div style="width:360px;flex:none"><div style="font:500 23px/1.2 var(--fd)">{g}</div>'
  f'<div style="font:400 18px/1.3 var(--ft);color:var(--slate);margin-top:6px">{note}</div></div><div class="tiles" style="gap:16px">{"".join(tile(s, None, "") for s, l in items)}</div></div>'
  for g, items, note in TOOLS)
  + '</div><p class="foot">Состав рынка и объёмы баз: key-core.ru и kokoc.com, обзоры сервисов 2026; toolfox.ru — Букварикс. Для практикума нужны только Вордстат и подсказки.</p></div>', "Сервисы в России"))

# 19 ИИ
AI_OK = [("Придумать маркеры и синонимы", "Как ещё называют «курсы»: школа, занятия, уроки, репетитор."),
         ("Вспомнить жаргон клиентов", "Как говорят родители, студенты, айтишники о своей задаче."),
         ("Сформулировать вопросы", "Что спрашивают перед покупкой: цена, уровень, пробное занятие."),
         ("Разложить черновик", "Первичная группировка сотни запросов по смыслу.")]
AI_NO = [("Называть частотность", "Цифры он выдумывает правдоподобно. Частота — только из Вордстата."),
         ("Знать спрос в конкретном городе", "Ростов и Москва ищут по-разному, модель этого не видит."),
         ("Видеть свежие тренды", "Новые моды, законы и сервисы последних месяцев ему неизвестны."),
         ("Решать, одна страница или две", "Это видно только по реальной выдаче, об этом следующий раздел.")]
S.append(slide(top("ИИ в сборе") + '<h1>ИИ хорошо придумывает слова и плохо знает цифры</h1>'
  '<div class="body"><div class="g2" style="margin:auto 0">'
  f'<div class="sticky teal tight"><span class="lab">Поручать</span>{plist(AI_OK, "check")}</div>'
  f'<div class="sticky coral tight"><span class="lab">Не поручать</span>{plist(AI_NO, "no")}</div>'
  '</div><p class="foot">Рабочая формулировка: <span class="mono">«Придумай 30 способов, которыми родители в Ростове ищут английский для ребёнка. Без цифр.»</span></p></div>', "ИИ в сборе"))

S.append(divider("03", "Чистка и кластеры", "Что выкинуть и как понять, одна страница или две.",
                 ["Половина собранного — мусор", "Минус-слово или страница", "Кластер равен странице", "Кластеризация по выдаче", "Похожие слова, разные намерения", "Каннибализация"]))

# 21 чистка
BUCKETS = [("coral", "Убрать", "x", ["курсы английского языка таганрог", "английский для взрослых минск", "онлайн школа ростов на дону официальный сайт"], "Другой город или чужой сайт"),
           ("lav", "В статью", "l", ["разговорный английский это какой уровень", "как выучить английский с нуля самостоятельно дома"], "Вопрос, а не покупка"),
           ("yel", "Решает бизнес", "y", ["курсы английского языка бесплатно", "курсы английского языка онлайн"], "Подходит, если это в модели школы"),
           ("teal", "На услугу", "t", ["курсы английского языка в ростове на дону для взрослых", "английский для детей ростов-на-дону"], "Наш город, наша услуга")]
S.append(slide(top("Чистка") + '<h1>Половину собранного выкидывают или откладывают до кластеризации</h1>'
  '<div class="body"><div class="g4" style="margin:auto 0;align-items:start">' + "".join(
  f'<div class="sticky {k}"><span class="lab">{h}</span><h4>{p}</h4>{chips(q, c)}</div>'
  for k, h, c, q, p in BUCKETS) + '</div><p class="foot">Все запросы — подсказки Яндекса по нашей нише из предыдущих слайдов, 14 сентября 2026. Ни один не выдуман.</p></div>', "Чистка"))

# 22 бесплатно
BP = D["besplatno"]
S.append(slide(top("Минус-слова") + '<h1>Минус-слово для одного сайта — целая страница для другого</h1>'
  '<div class="body"><div class="g2" style="margin:auto 0">'
  '<div class="sticky coral"><span class="lab">Платная школа английского</span><h4>В минус-слова</h4>'
  + chips(["бесплатно", "скачать", "вакансии", "своими руками", "pdf", "реферат"], "x")
  + '<p style="margin-top:8px">Человек с таким запросом не купит курс. Эти слова вписывают в поле минус-слов Вордстата, и хвост сразу чище.</p></div>'
  '<div class="sticky teal"><span class="lab">Мапка, каталог секций</span><h4>Отдельная посадочная /sektsii/besplatnye</h4>'
  f'<div class="g2" style="gap:14px;margin:6px 0">{stat(fmt(BP["entries"]), "входов из поиска за месяц на эту страницу", "sm")}{stat(str(BP["clicks"]), "кликов из " + str(BP["shows"]) + " показов по запросам со словом «бесплатные»", "sm")}</div>'
  '<p style="margin-top:8px">Родители ищут бесплатные секции, и каталог на этом выигрывает. То же слово, противоположное решение.</p></div>'
  f'</div><p class="foot">Яндекс Метрика и Вебмастер, мапка.рф, {PER}.</p></div>', "Минус-слово или страница"))

# 23 кластер = страница
S.append(slide(top("Кластер") + f'<h1>Google сам собрал {CLU["press"]["n"]} разных запросов на одну страницу про пресс</h1>'
  '<div class="body"><div style="display:flex;flex-direction:column;gap:22px;margin:auto 0">'
  + flow(CLU["press"]["top"][:7], "/guide/create-press", f'{CLU["press"]["n"]} запросов', "techkio: гайд про пресс", "l")
  + flow(CLU["verstak"]["top"][:5], "/guide/tacz-verstak", f'{CLU["verstak"]["n"]} запроса', "techkio: гайд про верстак", "y")
  + flow(CLU["futbol"]["top"][:7], "/sektsii/futbol", f'{CLU["futbol"]["n"]} запросов', "Мапка: секции футбола", "t")
  + f'</div><p class="foot">Google Search Console, {PER}: все запросы, по которым показывалась страница. Разные слова, одно намерение — поэтому одна страница.</p></div>', "Кластер = страница"))

# 24 кластеризация по выдаче
A10 = ["сайт А", "сайт Б", "сайт В", "сайт Г", "сайт Д", "сайт Е", "сайт Ж"]
B10 = ["сайт В", "сайт К", "сайт А", "сайт Л", "сайт Д", "сайт М", "сайт Ж"]
common = set(A10) & set(B10)
def olist(q, lst):
    return f'<div class="col"><div class="qh">{q}</div>' + "".join(f'<div class="oi{" m" if x in common else ""}"><b>{i + 1}</b>{x}</div>' for i, x in enumerate(lst)) + '</div>'
S.append(slide(top("Кластеризация") + '<h1>Одна страница или две — решает выдача, а не похожесть слов</h1>'
  '<div class="body"><div class="row fill" style="gap:34px;align-items:center">'
  f'<div class="ovx" style="flex:1.25">{olist("курсы английского ростов", A10)}<div class="mid"><div class="n">{len(common)}</div><div class="l">общих<br>сайта в топе</div></div>{olist("школа английского языка в ростове", B10)}</div>'
  '<div style="flex:1;display:flex;flex-direction:column;gap:14px">'
  + sticky("lav", "Правило", "Вбиваем оба запроса и сравниваем первую десятку. Совпало 3–5 адресов — поиск считает намерение одним, делаем одну страницу. Меньше — две.")
  + '<div class="g2" style="gap:14px"><div class="card"><h4>Hard</h4><p>Все запросы группы связаны общими адресами. Кластеры узкие и чистые.</p></div>'
  '<div class="card"><h4>Soft</h4><p>Каждый связан только с главным запросом. Шире, но может смешать намерения.</p></div></div>'
  + '</div></div><p class="foot">Схема, сайты условные. Порог 3–5 общих адресов и методы hard и soft — практика сервисов кластеризации: xmlriver.com, seo.ru, 2026. Вручную так проверяют спорные пары, сервисы — тысячи запросов.</p></div>', "Кластеризация по выдаче"))

# 25 андезит
AN = D["andesite"]; a1, a2 = AN["андезитовый корпус create крафт"], AN["андезит майнкрафт"]
S.append(slide(top("Спорный случай") + '<h1>Похожие слова — не одно намерение: андезит и андезитовый корпус</h1>'
  '<div class="body"><div style="margin:auto 0;display:flex;flex-direction:column;gap:22px"><div class="g2">'
  f'<div class="sticky teal"><span class="lab">есть своя страница</span><div class="qcard"><div class="q">андезитовый корпус create крафт</div><div class="meta">{a1[0]} показов, позиция {str(a1[2]).replace(".", ",")}</div></div>'
  f'<p>Деталь из мода Create. На неё ведёт гайд /guide/create-andezitovyy-korpus: Google собрал на него {CLU["korpus"]["n"]} запроса.</p></div>'
  f'<div class="sticky coral"><span class="lab">своей страницы нет</span><div class="qcard"><div class="q">андезит майнкрафт</div><div class="meta">{a2[0]} показов, позиция {str(a2[2]).replace(".", ",")}, {a2[1]} клика</div></div>'
  '<p>Ищут сам камень: где найти, зачем нужен. Страницы про камень на сайте нет, и запрос висит низко при вдвое большем спросе.</p></div></div>'
  + '<div class="sticky gold" style="flex-direction:row;align-items:center;gap:22px">' + ui("layers", "lg")
  + '<div><h4>Вывод: у запроса про камень свой кластер</h4><p>Ему нужна своя страница. Упоминание в гайде про корпус его не закроет, сколько ни дописывай слово «андезит».</p></div></div></div>'
  + f'<p class="foot">Яндекс Вебмастер и Google Search Console, techkio.ru, {PER}; карта сайта techkio.ru, 14 сентября 2026.</p></div>', "Андезит"))

# 26 каннибализация
g, b = CAN["guide"], CAN["blog"]
S.append(slide(top("Каннибализация") + '<h1>Две страницы под одно намерение делят трафик: гайд и статья про верстак</h1>'
  '<div class="body"><div class="row fill" style="gap:30px">'
  '<div style="flex:1.45"><div class="tbl" style="grid-template-columns:minmax(0,1fr) 130px 130px">'
  '<div class="h">Запрос</div><div class="h" style="text-align:right">Гайд</div><div class="h" style="text-align:right">Статья</div>'
  + "".join(f'<div class="mono" style="font-size:18px;color:var(--ink)">{q}</div><div style="text-align:right">поз {str(pa).replace(".", ",")}</div><div style="text-align:right">поз {str(pb).replace(".", ",")}</div>' for q, pa, ca, pb, cb in CAN["rows"][:6])
  + '</div></div><div style="flex:1;display:flex;flex-direction:column;gap:14px">'
  + f'<div class="card"><div class="stat sm"><div class="n">{CAN["shared"]}</div><div class="l">запроса, по которым Google показывает обе страницы</div></div></div>'
  + f'<div class="g2" style="gap:14px"><div class="card">{stat(str(g["clicks"]), "кликов у гайда", "sm")}</div><div class="card">{stat(str(b["clicks"]), "кликов у статьи", "sm")}</div></div>'
  + sticky("yel", "Что делать", "Склеить в одну страницу и поставить 301 со второй. Или развести намерения: гайд про крафт, статья про выбор верстака.")
  + f'</div></div><p class="foot">Google Search Console, techkio.ru, {PER}: /guide/tacz-verstak и /blog/verstaki-tacz-kak-skraftit.</p></div>', "Каннибализация"))

S.append(divider("04", "Структура сайта", "Как разложить кластеры в дерево, которое понятно и человеку, и роботу.",
                 ["Структура — это дерево кластеров", "Типы страниц", "Мапка: дерево из спроса", "Фасеты и районы", "Адреса, глубина, перелинковка"]))

# 28 дерево учебного кейса
W, H = 1432, 470
N = {"home": (716, 40, 210, "Главная", "бренд и общий запрос", "home"),
     "kursy": (230, 185, 190, "Курсы", "/kursy", "t"), "ceny": (520, 185, 170, "Цены", "/ceny", "t"),
     "prep": (790, 185, 210, "Преподаватели", "/prepodavateli", "g"), "otz": (1050, 185, 160, "Отзывы", "/otzyvy", "g"),
     "blog": (1280, 185, 160, "Блог", "/blog", "l"),
     "deti": (80, 330, 150, "Для детей", "/kursy/deti", "t"), "vzr": (245, 330, 160, "Для взрослых", "/kursy/vzroslye", "t"),
     "ege": (400, 330, 130, "ЕГЭ", "/kursy/ege", "t"), "razg": (555, 330, 160, "Разговорный", "/kursy/razgovor", "t"),
     "onl": (715, 330, 140, "Онлайн", "/kursy/online", "t"),
     "b1": (1095, 330, 260, "Как выучить самому", "/blog/samostoyatelno", "l"), "b2": (1345, 330, 160, "Уровни", "/blog/urovni", "l"),
     "lead": (716, 440, 520, "Каждая страница ведёт к заявке на пробное", None, "y")}
E = [("home", k) for k in ("kursy", "ceny", "prep", "otz", "blog")] + [("kursy", k) for k in ("deti", "vzr", "ege", "razg", "onl")] + [("blog", "b1"), ("blog", "b2")]
S.append(slide(top("Структура") + '<h1>Структура — это кластеры, разложенные в дерево</h1>'
  f'<div class="body"><div style="margin:auto 0">{diagram(W, H, N, E, nh=62)}</div>'
  '<div class="leg" style="margin-top:14px"><span><i style="background:#C3FAF5"></i>коммерческие: услуги и цены</span><span><i style="background:#EDEAFF"></i>информационные: статьи</span>'
  '<span><i style="background:#F7F8FA;border:1px solid #E0E2E8"></i>доверие: люди и отзывы</span><span><i style="background:#FFF4C4"></i>цель каждой страницы</span></div>'
  '<p class="foot">Учебный пример на школе английского. Каждая страница второго ряда — отдельный кластер из подсказок, которые мы уже собрали.</p></div>', "Дерево кластеров"))

# 29 типы страниц
PT = [("Главная", "Бренд и самый общий запрос", "мапка.рф", "techkio.ru"),
      ("Категория, хаб", "Широкий запрос: вся тема сразу", "/sektsii/sportivnye", "/guide"),
      ("Посадочная", "Узкий коммерческий: направление, район, возраст", "/sektsii/angliyskiy-na-severnom", "/create"),
      ("Карточка", "Навигационный: название организации", "/yuzhny-meridian", "—"),
      ("Статья, гайд", "Информационный: как, что, почему", "/blog/kak-vybrat-sekciyu-dlya-rebenka", "/guide/create-press")]
S.append(slide(top("Типы страниц") + '<h1>У каждого типа страницы своё намерение</h1>'
  '<div class="body"><div class="tbl fill" style="grid-template-columns:230px minmax(0,1fr) minmax(0,1.05fr) minmax(0,.75fr)">'
  '<div class="h">Тип</div><div class="h">Какое намерение закрывает</div><div class="h">Мапка</div><div class="h">techkio</div>'
  + "".join(f'<div class="k">{t}</div><div>{i}</div><div class="mono" style="font-size:18px;color:var(--moss)">{a}</div><div class="mono" style="font-size:18px;color:var(--moss)">{b}</div>' for t, i, a, b in PT)
  + '</div><p class="foot">Все адреса настоящие и открываются. Ошибка новичка — вести коммерческий запрос в статью или информационный на страницу услуги.</p></div>', "Типы страниц"))

# 30 дерево Мапки
W2, H2 = 1432, 430
N2 = {"home": (716, 40, 200, "Главная", "мапка.рф", "home"),
      "cat": (716, 150, 360, "Категории", "спорт, творчество, языки", "g"),
      "dir": (190, 280, 230, "Направления", "футбол, плавание…", "t"), "dist": (500, 280, 230, "Районы", "Северный, Западный…", "t"),
      "age": (800, 280, 260, "Возраст", "дошкольники, подростки", "t"), "pick": (1100, 280, 250, "Подборки", "бесплатные, недорогие…", "t"),
      "blog": (1320, 150, 170, "Блог", "статьи", "l"),
      "combo": (345, 390, 380, "Направление × район", "английский на Северном", "y"),
      "card": (1000, 390, 330, "Карточки секций", "/yuzhny-meridian", "o")}
E2 = [("home", "cat"), ("home", "blog"), ("cat", "dir"), ("cat", "dist"), ("cat", "age"), ("cat", "pick"), ("dir", "combo"), ("dist", "combo"), ("age", "card"), ("pick", "card")]
BD = [(716, 118, str(MPK["cats"])), (190, 248, str(MPK["dirs"])), (500, 248, str(MPK["districts"])), (800, 248, str(MPK["ages"])),
      (1100, 248, str(MPK["picks"])), (1320, 118, str(MPK["blog"])), (345, 358, str(MPK["combos"])), (1000, 358, "≈300")]
S.append(slide(top("Кейс: Мапка") + f'<h1>Дерево Мапки выросло из спроса: {MPK["landings"]} посадочных</h1>'
  f'<div class="body"><div style="margin:auto 0">{diagram(W2, H2, N2, E2, nh=62, badges=BD)}</div>'
  f'<p class="foot">Карта сайта мапка.рф, 14 сентября 2026: {MPK["sitemap"]} адресов, из них {MPK["landings"]} посадочных, {MPK["blog"]} статей, остальное — карточки секций и служебные страницы. Жёлтые цифры — сколько страниц такого типа.</p></div>', "Дерево Мапки"))

# 31 фасеты
COLS = MPK["matrix_cols"]
COLLAB = {"v-centre": "Центр", "na-zapadnom": "Западный", "na-severnom": "Северный", "na-selmashe": "Сельмаш", "na-chkalovskom": "Чкаловский",
          "v-levencovke": "Левенцовка", "v-nahichevani": "Нахичевань", "v-aleksandrovke": "Александровка", "na-voenvede": "Военвед"}
ROWS = ["angliyskiy", "edinoborstva", "futbol", "gimnastika", "muzyka", "plavanie", "risovanie", "tancy", "doshkolniki"]
ROWLAB = {"angliyskiy": "Английский", "edinoborstva": "Единоборства", "futbol": "Футбол", "gimnastika": "Гимнастика", "muzyka": "Музыка",
          "plavanie": "Плавание", "risovanie": "Рисование", "tancy": "Танцы", "doshkolniki": "Дошкольники"}
ncells = sum(sum(1 for v in MPK["matrix"][r] if v) for r in ROWS)
S.append(slide(top("Фасеты") + '<h1>Направление и район — отдельная страница, если есть спрос и секции</h1>'
  '<div class="body"><div class="row fill" style="gap:30px;align-items:center">'
  f'<div style="flex:1.3"><div style="font:500 19px/1.3 var(--ft);color:var(--slate);margin-bottom:12px">Какие сочетания у Мапки стали страницами: {ncells} из {len(ROWS) * len(COLS)}</div>'
  f'{matrix(ROWS, COLS, MPK["matrix"], ROWLAB, COLLAB)}</div>'
  '<div style="flex:1;display:flex;flex-direction:column;gap:14px">'
  f'<div class="card"><div class="stat sm"><div class="n">{MPK["angliyskiy_severny"]} <small>из</small> {MPK["angliyskiy_all"]}</div><div class="l">секций английского приходится на Северный. Этого хватает на отдельную страницу с картой и списком.</div></div></div>'
  + sticky("yel", "Порог: от трёх секций", "Где секций меньше трёх, страница закрыта от индексации. Пустая посадочная ничего не даёт человеку и тянет вниз весь сайт.")
  + '</div></div><p class="foot">Карта сайта и страницы мапка.рф, 14 сентября 2026. Пустые клетки — сочетаний пока нет: мало секций или нет спроса.</p></div>', "Фасеты"))

# 32 районы в запросах
DS = D["districts"]
S.append(slide(top("Спрос на районы") + f'<h1>Каждый шестой запрос к Мапке содержит район: {fmt(DS["queries"])} из {fmt(DS["total"])}</h1>'
  '<div class="body"><div class="row fill" style="gap:36px;align-items:center">'
  f'<div class="chart" style="flex:1.25"><div class="cap" style="font-weight:500;color:{INK}">Запросов с названием района за месяц</div>'
  f'{hbars([(n, q, "#FFD02F") for n, q, s in DS["top"]], w=820, rowh=58, labw=220)}</div>'
  '<div style="flex:1;display:flex;flex-direction:column;gap:16px">'
  + sticky("teal", "Поэтому районы стали страницами", "Спрос на «секции на Северном» и «бассейн на Западном» реальный. Под него и сделаны посадочные с районом в адресе и заголовке.")
  + sticky("grey", "Слово «центр» мы не считали", "В запросах оно чаще значит «детский центр», чем район города. Это и есть чистка: слово одно, смысла два.")
  + f'</div></div><p class="foot">Яндекс Вебмастер, мапка.рф, {PER}. Показано шесть районов с наибольшим числом запросов.</p></div>', "Районы в запросах"))

# 33 адрес страницы
S.append(slide(top("Адреса") + '<h1>Адрес страницы читается как её краткое описание</h1>'
  '<div class="body"><div class="anat" style="margin-bottom:24px">'
  '<div class="k">Домен</div><div class="box"><div class="u">мапка.рф</div><div class="d" style="font-size:19px;margin-top:4px">кириллический; для роботов он записан как xn--80aa3agq.xn--p1ai</div></div>'
  '<div class="k">Раздел</div><div class="box"><div class="u">/sektsii/</div><div class="d" style="font-size:19px;margin-top:4px">сразу видно, что это каталог секций</div></div>'
  '<div class="k">Страница</div><div class="box good"><div class="u">angliyskiy-na-severnom</div><div class="d" style="font-size:19px;margin-top:4px">направление и район транслитом, без цифр и мусора</div></div>'
  '</div><div class="g2" style="margin-bottom:auto">'
  + sticky("teal", "Как делать", "Коротко, читаемо, один адрес на страницу. Транслит надёжнее кириллицы в пути: скопированная ссылка с кириллицей превращается в %D0%B0%D0%BD…")
  + sticky("coral", "Чего не делать: менять адрес без редиректа", "Летом Мапка сократила адреса 26 карточек и не поставила 301. Яндекс держал старые и новые адреса как дубли, пока не добавили редиректы.")
  + '</div></div>', "Адреса"))

# 34 глубина
S.append(slide(top("Вложенность") + '<h1>Важные страницы — в двух-трёх кликах от главной</h1>'
  '<div class="body"><div class="pipe" style="margin:auto 0">'
  + step("0", "Главная", "мапка.рф", "grey", None, 0) + arrow()
  + step("1", "Языковые секции", "/sektsii/yazykovye", "grey", None, 1) + arrow()
  + step("2", "Английский", f'/sektsii/angliyskiy<br>{MPK["angliyskiy_all"]} секций', "teal", None, 2) + arrow()
  + step("3", "На Северном", f'/sektsii/angliyskiy-na-severnom<br>{MPK["angliyskiy_severny"]} секций', "yel", None, 3) + arrow()
  + step("4", "Карточка школы", "одна секция: цены, адрес, отзывы", "orange", None, 4)
  + '</div><p class="foot">Номер в кружке — сколько кликов от главной. Практики отмечают, что страницы глубже третьего-четвёртого уровня индексируются хуже; структуру по уровням показывает Вебмастер. Разбор Вебмастера — kokoc.com, 2026.</p></div>', "Глубина"))

# 35 перелинковка
LINKS = [("Меню и хабы", "С главной и категорий в каждый раздел, робот доходит за один визит."),
         ("Хлебные крошки", "Главная / Языковые секции / Английский на Северном — путь назад по дереву."),
         ("Соседние страницы", "С «английского на Северном» — на «английский на Западном»."),
         ("Из статьи в каталог", "Читатель статьи о выборе секции уходит к секциям своего района."),
         ("Футер", "Все направления на каждой странице: ни одной сироты.")]
S.append(slide(top("Перелинковка") + '<h1>Ссылки внутри сайта ведут по дереву и человека, и робота</h1>'
  '<div class="body"><div class="row fill" style="gap:28px;align-items:center">'
  f'<div style="flex:1.1">{browser("мапка.рф/sektsii/angliyskiy-na-severnom", "mapka_combo.webp")}</div>'
  f'<div class="sticky teal tight" style="flex:1"><span class="lab">Пять видов ссылок на Мапке</span>{plist(LINKS, "link")}</div>'
  '</div><p class="foot">Хлебные крошки видны на снимке под меню. Правило с первой встречи: новая страница получает входящие ссылки в день публикации.</p></div>', "Перелинковка"))

# 36 techkio хаб
ET = D["entries_techkio"]; e1 = dict(ET)
S.append(slide(top("Кейс: techkio") + '<h1>Хаб собирает широкий спрос, гайды — узкий</h1>'
  '<div class="body"><div class="g2" style="gap:24px;margin:auto 0">'
  f'<div style="display:flex;flex-direction:column;gap:12px">{browser("techkio.ru/guide", "techkio_guide.webp")}<p style="font:400 20px/1.35 var(--ft);color:var(--charcoal)"><b>Хаб /guide</b> — база знаний на 34 разбора. Ведёт на каждый гайд и ловит «гайд по серверу».</p></div>'
  f'<div style="display:flex;flex-direction:column;gap:12px">{browser("techkio.ru/guide/create-press", "techkio_press.webp")}<p style="font:400 20px/1.35 var(--ft);color:var(--charcoal)"><b>Гайд под кластер</b> — один механизм, один ответ. Самый сильный гайд дал {fmt(e1.get("/guide/tacz-verstak", 0))} входов из поиска за месяц.</p></div>'
  f'</div><p class="foot">Яндекс Метрика, techkio.ru, входы из поисковых систем, {PER}. Главная за тот же месяц — {fmt(e1.get("/", 0))} входов.</p></div>', "Хаб и гайды"))

S.append(divider("05", "Практикум", "Собираем ядро и дерево для ниши, которую выбрали в начале.",
                 ["Шаг 1: тридцать запросов", "Шаг 2: таблица ядра", "Шаг 3: дерево страниц", "Разбор на экране"]))

# 38 шаг 1
S.append(slide(top("Практикум, шаг 1") + '<h1>Шаг 1. Тридцать запросов за десять минут</h1>'
  '<div class="body"><div class="pipe" style="margin:auto 0 22px">'
  + step("1", "Маркеры", "Пять-семь слов о нише: как её называют клиенты. Можно спросить ИИ.", "teal", "pen", 0) + arrow()
  + step("2", "Подсказки", "Каждый маркер в поиск, плюс буквы по алфавиту. Всё выписываем.", "teal", "search", 1) + arrow()
  + step("3", "Вордстат", "Маркер во вкладку «Топ запросов», регион — Ростов. Добираем до тридцати.", "teal", "gauge", 2)
  + '</div><div class="card" style="margin-bottom:auto"><h4>Так это выглядит на школе английского</h4>'
  + chips(["курсы английского языка", "английский для детей ростов-на-дону", "подготовка к егэ по английскому 2026", "разговорный английский для начинающих", "репетитор английского онлайн для детей", "курсы английского языка онлайн"], "t")
  + '</div><p class="foot">Работаем в парах. У кого свой проект — делает на нём, остальные на победившей нише.</p></div>', "Шаг 1"))

# 39 шаг 2
CORE = [("курсы английского языка в ростове на дону для взрослых", "Коммерческий", "Взрослые", "/kursy/vzroslye"),
        ("английский для детей ростов-на-дону", "Коммерческий", "Дети", "/kursy/deti"),
        ("подготовка к егэ по английскому 2026", "Коммерческий", "ЕГЭ", "/kursy/ege"),
        ("как выучить английский с нуля самостоятельно дома", "Информационный", "Самостоятельно", "/blog/samostoyatelno"),
        ("разговорный английский это какой уровень", "Информационный", "Уровни", "/blog/urovni")]
S.append(slide(top("Практикум, шаг 2") + '<h1>Шаг 2. Раскладываем запросы в таблицу ядра</h1>'
  '<div class="body"><div class="tbl fill" style="grid-template-columns:minmax(0,1fr) 160px 230px 240px 270px">'
  '<div class="h">Запрос</div><div class="h">Точная частота</div><div class="h">Намерение</div><div class="h">Кластер</div><div class="h">Страница</div>'
  + "".join(f'<div class="mono" style="font-size:18px;color:var(--ink)">{q}</div><div style="color:var(--steel)">Вордстат</div><div>{i}</div><div class="k" style="font-size:19px">{c}</div><div class="mono" style="font-size:18px;color:var(--moss)">{p}</div>' for q, i, c, p in CORE)
  + '</div><p class="foot">Точную частоту вписываем на паре, с кавычками и восклицательными знаками. Запросы — подсказки Яндекса, 14 сентября 2026.</p></div>', "Шаг 2"))

# 40 шаг 3
W3, H3 = 780, 400
N3 = {"home": (390, 40, 200, "Главная", None, "home"),
      "a": (120, 170, 170, "Раздел", None, "e"), "b": (390, 170, 170, "Раздел", None, "e"), "c": (660, 170, 170, "Раздел", None, "e"),
      "a1": (60, 310, 110, "?", None, "e"), "a2": (180, 310, 110, "?", None, "e"), "b1": (330, 310, 110, "?", None, "e"),
      "b2": (450, 310, 110, "?", None, "e"), "c1": (660, 310, 170, "Статья", None, "e")}
E3 = [("home", "a"), ("home", "b"), ("home", "c"), ("a", "a1"), ("a", "a2"), ("b", "b1"), ("b", "b2"), ("c", "c1")]
CHECK = [("Одному кластеру — одна страница", "Нет двух страниц под одно намерение."),
         ("Информационное — в статьи", "Коммерческое — на услуги и посадочные."),
         ("Важное в трёх кликах", "От главной до любой услуги."),
         ("Адреса читаемые", "Транслит, коротко, без цифр."),
         ("У каждой страницы есть вход", "Меню, крошки или ссылка из статьи.")]
S.append(slide(top("Практикум, шаг 3") + '<h1>Шаг 3. Рисуем дерево и проверяем его по чек-листу</h1>'
  '<div class="body"><div class="row fill" style="gap:34px;align-items:center">'
  f'<div style="flex:none">{diagram(W3, H3, N3, E3, nh=58)}</div>'
  f'<div class="sticky yel tight" style="flex:1"><span class="lab">Проверка дерева</span>{plist(CHECK, "check")}</div>'
  '</div><p class="foot">Рисуем на бумаге или в Miro. В конце две-три пары показывают своё дерево на проекторе, разбираем вместе.</p></div>', "Шаг 3"))

# 41 работает и нет
DEAD = [("Ядро на тысячи ключей без кластеров", "Таблица есть, а какую страницу под что делать, непонятно."),
        ("Страница под каждую словоформу", "«курсы английского» и «курсы по английскому» — одно намерение."),
        ("Частота без кавычек", "Базовое число считает всё подряд и обманывает."),
        ("Цифры спроса от ИИ", "Правдоподобные и выдуманные."),
        ("Пустые посадочные ради ключа", "Сочетание без содержимого тянет вниз весь сайт.")]
ALIVE = [("Кластеризация по выдаче", "Одна страница или две — решает первая десятка."),
         ("Свой спрос из Вебмастера", "Самые честные запросы, и там видны показы без кликов."),
         ("Одна страница — одно намерение", "Коммерческое на услуги, информационное в статьи."),
         ("Фасеты с порогом", "Страница-сочетание есть, только если есть что показать."),
         ("Год и сезон в запросах", "Обновлять к сезону и готовить заранее.")]
S.append(slide(top("Итог") + '<h1>Что в семантике и структуре в 2026-м не работает, а что работает</h1>'
  '<div class="body"><div class="g2" style="margin:auto 0">'
  f'<div class="sticky coral tight"><span class="lab">Не работает</span>{plist(DEAD, "no")}</div>'
  f'<div class="sticky teal tight"><span class="lab">Работает</span>{plist(ALIVE, "check")}</div>'
  '</div></div>', "Работает и не работает"))

# 42 домашка
S.append(slide(top("Домашнее задание") + '<h1>Домашка к встрече 3: доделать ядро и выбрать одну страницу</h1>'
  '<div class="body"><div class="g3" style="margin:auto 0">'
  + '<div class="sticky yel"><span class="num">1</span><h4>Добрать ядро до 50 запросов</h4><p>С точной частотой из Вордстата, намерением и кластером. Для учебной ниши или своего проекта.</p></div>'
  + '<div class="sticky grey"><span class="num">2</span><h4>Дорисовать дерево</h4><p>Каждый кластер на своём месте, проверка по чек-листу из практикума. Фото или скриншот — в чат курса.</p></div>'
  + '<div class="sticky grey"><span class="num">3</span><h4>Выбрать одну посадочную</h4><p>Самую важную для бизнеса. На встрече 3 пишем для неё заголовок, описание и первый экран.</p></div>'
  + '</div><p class="foot">Домашка по желанию. Вопросы — в чат курса или мне в Telegram.</p></div>', "Домашка"))

# 43 анонс
S.append(slide(top("Встреча 3") + '<h1>Встреча 3 — страница и контент: как написать то, что выиграет выдачу</h1>'
  '<div class="body"><div class="g4" style="margin:auto 0">'
  + sticky("grey", "Заголовок и описание", "Как собрать сниппет из кластера, чтобы по нему кликали.", ui("eye", "lg"))
  + sticky("grey", "Первый экран", "Ответ на намерение до скролла: для человека и для ИИ-ответа.", ui("zap", "lg"))
  + sticky("grey", "Текст под кластер", "Какие слова нужны, а какие — переспам. Структура, списки, таблицы.", ui("doc", "lg"))
  + sticky("yel", "Практикум", "Пишем страницу под посадочную из домашки и сравниваем с топом выдачи.", ui("pen", "lg"))
  + '</div><p class="foot">Дата — в чате курса. Приносите ядро и выбранную страницу: без них практикум не соберётся.</p></div>', "Анонс встречи 3"))

# 44 источники
SRCS = [("Яндекс Вебмастер: запросы, показы, клики", "webmaster.yandex.ru", "мапка.рф и techkio.ru, 13.08–12.09.2026"),
        ("Google Search Console: запросы по страницам", "search.google.com/search-console", "кластеры и каннибализация, тот же период"),
        ("Яндекс Метрика: входы из поиска", "metrika.yandex.ru", "те же сайты и период"),
        ("Подсказки Яндекса, регион Ростов-на-Дону", "suggest.yandex.ru", "сняты 14.09.2026"),
        ("Карты сайта мапка.рф и techkio.ru", "/sitemap.xml", "устройство сайтов, 14.09.2026"),
        ("API Вордстата, бесплатно по заявке", "habr.com, ppc.world", "июнь 2025"),
        ("Отключение старого Вордстата 11.08.2025", "lucky-seo.com, adlook.me", "обзоры 2026"),
        ("Обновление интерфейса Вордстата", "journal.topvisor.com", "25.08.2026"),
        ("Операторы и вкладки Вордстата", "wehaveidea.ru, pr-cy.ru", "гайды 2026"),
        ("Кластеризация: hard, soft, порог 3–5", "xmlriver.com, seo.ru", "2026"),
        ("Сервисы сбора семантики в России", "key-core.ru, kokoc.com", "обзоры 2026"),
        ("Букварикс: база и бесплатный режим", "toolfox.ru, bukvarix.com", "2026"),
        ("Вебмастер: структура и вложенность", "kokoc.com", "руководство 2026"),
        ("Дека и исходники", "github.com/Kom1sh/seo-course", "папка 2, закрыто от индексации")]
S.append(slide(top("Источники") + '<h1 class="md">Источники и данные</h1>'
  '<div class="body"><div class="src fill">' + "".join(
  f'<div class="srow"><span class="num">{t}</span><span class="lnk">{l}</span><span class="whr">{w}</span></div>' for t, l, w in SRCS)
  + '</div></div>', "Источники"))

# 45 вопросы
S.append(slide(top("Вопросы") + '<div class="body"><div class="row fill" style="align-items:flex-end;gap:60px"><div style="flex:1.2;display:flex;flex-direction:column;height:100%">'
  '<div class="divt" style="font-size:96px;line-height:.98">Вопросы?</div>'
  '<div style="margin-top:auto;display:flex;flex-direction:column;gap:20px">'
  '<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px">'
  '<div class="card"><h4>Telegram</h4><p class="mono" style="font-size:21px;color:#fff">@Kom1sh</p></div>'
  '<div class="card"><h4>Сайт</h4><p class="mono" style="font-size:19px;color:#fff;white-space:nowrap">egorprotasov.ru</p></div>'
  '<div class="card"><h4>Проекты</h4><p class="mono" style="font-size:19px;line-height:1.5;color:#fff">мапка.рф<br>techkio.ru<br>mediachef.app</p></div></div>'
  '<div class="card"><h4>Слайды этой встречи</h4>'
  '<p class="mono" style="font-size:30px;color:var(--yel);white-space:nowrap">kom1sh.github.io/seo-course/2</p></div></div></div>'
  '<div class="divlist" style="flex:1;padding-bottom:12px"><span>Домашка: ядро на 50 запросов, дерево, одна посадочная</span><span>Встреча 3 — страница и контент</span><span>Первая встреча: <span style="white-space:nowrap">kom1sh.github.io/seo-course</span></span></div></div></div>', "Вопросы", "dark"))

out = "\n".join(S)
(HERE / "slides.html").write_text(out, encoding="utf-8")
print("slides.html:", len(S), "слайдов,", len(out.encode()) // 1024, "КБ")
