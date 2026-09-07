#!/usr/bin/env python3
"""Генерирует src/slides.html из данных (data.json) и текстов ниже.
Правится этот файл, затем: python3 src/make_slides.py && python3 src/build.py && python3 src/qa.py
"""
import json, pathlib, math, html
HERE = pathlib.Path(__file__).resolve().parent
D = json.load(open(HERE / "data.json", encoding="utf-8"))
BR = json.load(open(HERE / "brands.json"))
INK = "#1C1C1E"
TK, MP = D["techkio"], D["mapka"]
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
        "frog": ("Screaming Frog", "#4E7E2E"), "wordstat": ("Wordstat", "#FC3F1D"), "neuro": ("Нейро", "#5B3DF0"), "metrika": ("Метрика", "#FC3F1D"),
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

# ── данные для слайдов ───────────────────────────────────────────────────────
def week_label(s): return f"{int(s[8:10])}.{s[5:7]}"
tk_weeks = [(week_label(d), v) for d, v in TK["metrika_organic_weekly"] if v > 0]
mp_weeks = [(week_label(d), v) for d, v in MP["metrika_organic_weekly"] if d >= "2026-01-05"]
mp_aug_idx = next(i for i, (d, v) in enumerate([(d, v) for d, v in MP["metrika_organic_weekly"] if d >= "2026-01-05"]) if d == "2026-08-03")
tk_search = next(v for n, v, u in TK["metrika_sources30"] if n.startswith("Search"))
mp_search = next(v for n, v, u in MP["metrika_sources30"] if n.startswith("Search"))
tk_eng = dict((n, v) for n, v in TK["metrika_engines30"]); mp_eng = dict((n, v) for n, v in MP["metrika_engines30"])
tk_ya_share = round(100 * tk_eng["Yandex"] / sum(tk_eng.values())); mp_ya_share = round(100 * mp_eng["Yandex"] / sum(mp_eng.values()))
mp_dev = dict(MP["metrika_devices30"]); mp_mob = round(100 * mp_dev["Smartphones"] / sum(mp_dev.values()))
tk_dev = dict(TK["metrika_devices30"]); tk_pc = round(100 * tk_dev["PC"] / sum(tk_dev.values()))
mp_ins = [(d, v) for d, v in MP["yandex_in_search_history"]]
mp_month = {k: (s, c) for k, s, c in MP["yandex_monthly"]}
ctr_tk = {k: r for k, s, c, n, r in TK["yandex_ctr_buckets"]}; ctr_mp = {k: r for k, s, c, n, r in MP["yandex_ctr_buckets"]}
tk_entry = TK["metrika_entry_organic30"][:6]

S = []
# 01 обложка
stack = "".join(f'<div class="tile big{" word" if s in WORD else ""}" style="left:{x}px;top:{y}px;transform:rotate({r}deg);{"color:"+WORD[s][1] if s in WORD else ""}">{WORD[s][0] if s in WORD else ico(s)}</div>'
                for s, x, y, r in [("yandex", 40, 30, -7), ("google", 300, 10, 5), ("chatgpt", 420, 130, -4), ("perplexity", 120, 170, 6), ("claude", 250, 300, -5),
                                   ("googlegemini", 60, 330, 4), ("bing", 470, 290, 7), ("duckduckgo", 380, 420, -6), ("neuro", 130, 470, 3)])
S.append(slide(top("Школа Икс, факультатив. Встреча 1 из 5") +
  '<div class="body cover"><div class="row fill" style="gap:40px"><div style="flex:1;display:flex;flex-direction:column;min-width:0">'
  '<h1>Поиск<br>и ИИ-выдача</h1><p class="sub">Как веб-проект находят люди: в Яндексе, в Google и в ответах ChatGPT. Первая встреча из пяти — карта местности на двух живых проектах.</p>'
  '<div class="who"><div><b>Егор Протасов<span class="mono" style="font-weight:500;font-size:19px;color:var(--blue);margin-left:14px">egorprotasov.ru</span></b><br><span>SEO-специалист и PM. Автор проектов мапка.рф, techkio.ru, mediachef.app</span></div><div><b>Суббота</b><br><span>90 минут, для 1–3 курсов</span></div></div></div>'
  f'<div class="stack" style="width:640px;flex:none">{stack}</div></div></div>', "Обложка", "cover"))

# 02 кто говорит
S.append(slide(top("Кто говорит") + '<h1>Весь материал сегодня — из двух моих проектов и трёх систем аналитики</h1>'
  '<div class="body"><div class="row fill" style="gap:28px">'
  f'<div style="width:420px;flex:none;display:grid;grid-template-rows:repeat(3,minmax(0,1fr));gap:14px">{stat(fmt(tk_search+mp_search), "визитов из поиска за 30 дней на двух проектах вместе", "sm")}'
  f'{stat(f"{tk_ya_share}%", "поискового трафика приносит Яндекс, остальное Google", "sm")}'
  f'{stat(fmt(TK["yandex_summary"]["in_search"]+MP["yandex_summary"]["in_search"]), "страниц двух сайтов знает поиск Яндекса", "sm")}</div>'
  f'<div style="flex:1;display:grid;grid-template-columns:1fr 1fr;gap:20px;align-items:center">{browser("techkio.ru", "techkio.webp")}{browser("мапка.рф", "mapka.webp")}</div></div>'
  '<p class="foot">Все цифры в деке — Яндекс Метрика, Яндекс Вебмастер и Google Search Console на 6 сентября 2026, если не указан другой источник.</p></div>', "Кто говорит"))

# 03 зачем
S.append(slide(top("Зачем это вам") + '<h1>Трафик — это люди, которые пришли сами. У проекта без трафика нет пользователей</h1>'
  '<div class="body"><div class="g3 fill">'
  + sticky("grey", "Реклама", "Платишь за каждый клик. Выключил бюджет — трафик кончился в ту же минуту. Цена клика растёт каждый год.", ui("megaphone", "lg"))
  + sticky("grey", "Соцсети", "Алгоритм решает, кому показать. Пост живёт день, потом его нет. Аудитория принадлежит платформе, не тебе.", ui("share", "lg"))
  + sticky("teal", "Поиск", "Спрос уже существует: люди сами вбивают запрос. Хорошая страница приносит визиты месяцами без доплаты.", ui("search", "lg"))
  + '</div><p class="foot">Дальше в деке: почему страница попадает в выдачу, что видит человек и как ИИ решает, кого цитировать.</p></div>', "Зачем это вам"))

# 04 techkio крюк
S.append(slide(top("Живой пример") + f'<h1>Сайту techkio.ru восемь недель. Поиск приносит {fmt(tk_search)} визитов в месяц</h1>'
  '<div class="body"><div class="row fill" style="gap:32px">'
  f'<div class="chart" style="flex:1.1">{line_chart(tk_weeks, w=800, h=470)}<div class="leg"><span><i style="background:#0FBCB0"></i>визиты из поисковых систем в неделю</span></div></div>'
  f'<div style="flex:1">{browser("techkio.ru", "techkio.webp")}</div></div>'
  '<p class="foot">Яндекс Метрика, недели с 13 июля по 6 сентября 2026. Сайт открыт 15 июля.</p></div>', "techkio.ru за восемь недель"))

# 05 мапка крюк
S.append(slide(top("Живой пример") + f'<h1>Мапка.рф полгода стояла на 10–30 визитах в неделю. В конце августа — {fmt(mp_weeks[-1][1])}</h1>'
  '<div class="body"><div class="row fill" style="gap:32px">'
  f'<div class="chart" style="flex:1.1">{line_chart(mp_weeks, w=800, h=470, every=5, vline=(mp_aug_idx, "2 августа"))}<div class="leg"><span><i style="background:#0FBCB0"></i>визиты из поисковых систем в неделю</span></div></div>'
  f'<div style="flex:1">{browser("мапка.рф", "mapka.webp")}</div></div>'
  '<p class="foot">Яндекс Метрика, недели 2026 года. Что случилось 2 августа — в четвёртом блоке.</p></div>', "мапка.рф до и после августа"))

# 06 серия
series = [("1", "Как устроен поиск и ИИ-выдача", "Сканирование, индекс, ранжирование. Что видит пользователь. Как отвечает ИИ. Два кейса.", "gold"),
          ("2", "Семантика", "Что люди ищут и как это узнать: Wordstat, Вебмастер, Search Console, кластеры и намерение.", "grey"),
          ("3", "Техничка", "Чтобы робот дошёл и понял: индексация, адреса, скорость, разметка.", "grey"),
          ("4", "Контент и авторитет", "Почему одну страницу цитируют, а другую нет. Ссылки, упоминания, E-E-A-T.", "grey"),
          ("5", "GEO-практикум", "Попасть в ответ ChatGPT и Perplexity: структура, свежесть, измерение.", "grey")]
S.append(slide(top("Серия встреч") + '<h1>Пять встреч. Сегодня — карта местности, остальное по одной теме за раз</h1>'
  '<div class="body"><div class="g5 fill">' + "".join(
  f'<div class="sticky {k}"><span class="num{" w" if k=="gold" else ""}">{n}</span><h4>{h}</h4><p>{p}</p>{"<span class=lab>сегодня</span>" if k=="gold" else ""}</div>' for n, h, p, k in series)
  + '</div><p class="foot">Даты остальных встреч согласуем в чате курса. Каждая — суббота, 90 минут, с практикумом на своём проекте.</p></div>', "Серия из пяти встреч"))

# 07 план встречи
plan = [("1", "Как работает поиск", "20 минут. Робот, индекс, ранжирование, намерение запроса.", "search"),
        ("2", "Что видит пользователь", "15 минут. Анатомия выдачи, сниппет, позиция и клики.", "eye"),
        ("3", "ИИ-выдача и GEO", "20 минут. Где теперь ищут, как ИИ отвечает и кого цитирует.", "chat"),
        ("4", "Два кейса", "20 минут. Мапка.рф и techkio.ru с цифрами.", "flag"),
        ("5", "Практикум", "15 минут. Проверяем ваш проект и берём домашку.", "check")]
S.append(slide(top("План на сегодня") + '<h1>Полтора часа: четыре блока и практикум</h1>'
  '<div class="body"><div class="pipe" style="margin:auto 0">' + arrow().join(step(n, h, p, "", ic, i) for i, (n, h, p, ic) in enumerate(plan))
  + '</div><p class="foot">Вопросы можно задавать по ходу. Ничего записывать не нужно — дека останется по ссылке.</p></div>', "План встречи"))

def divider(n, title, sub, items):
    return slide(top("Раздел " + n) + f'<div class="body"><div class="row fill" style="gap:60px;align-items:flex-end"><div style="flex:1.2;display:flex;flex-direction:column;height:100%">'
      f'<div class="divn">{n}</div><div style="margin-top:auto"><div class="divt">{title}</div><div class="divs">{sub}</div></div></div>'
      f'<div class="divlist" style="flex:1;padding-bottom:12px">{"".join(f"<span>{x}</span>" for x in items)}</div></div></div>', f"Раздел {n}: {title}", "dark")

S.append(divider("01", "Как работает поиск", "Что происходит между твоей страницей и строкой поиска.",
                 ["Шесть слов, без которых не разобраться", "Кто ищет где: Яндекс и Google", "Три шага поисковика", "Робот, индекс, ранжирование по отдельности", "Намерение запроса"]))

# 08 словарь
terms = [("SEO", "search engine optimization", "Делать так, чтобы страницу находили по запросам в Яндексе и Google без оплаты за клик."),
         ("GEO", "generative engine optimization", "Делать так, чтобы ИИ-ассистенты цитировали тебя в ответе. Новая дисциплина, 2024–2026."),
         ("Запрос", "«бассейн ростов западный»", "Слова, которые человек вбил в строку. За словами стоит намерение, и оно важнее слов."),
         ("Выдача", "SERP, search results page", "Страница результатов: реклама, ИИ-ответ, органика, карты, картинки, вопросы."),
         ("Органика", "organic results", "Результаты, за которые никто не платил поисковику. Наша территория на всех встречах."),
         ("Сниппет", "title, url, description", "Как выглядит ссылка на тебя в выдаче: заголовок, адрес, описание. Единственное, что видят до клика.")]
S.append(slide(top("Словарь") + '<h1>Шесть слов, без которых дальше не разобраться</h1>'
  '<div class="body"><div class="kv" style="margin:auto 0">' + "".join(
  f'<div class="it"><div class="k">{k}<small>{s}</small></div><div class="v">{v}</div></div>' for k, s, v in terms) + '</div></div>', "Словарь"))

# 09 рынок
mk = donut([("Яндекс", 72, "#FC3F1D"), ("Google", 26, "#4285F4"), ("Остальные", 2, "#E0E2E8")], size=320, center="72%")
tk_other = sum(tk_eng.values()) - tk_eng["Yandex"] - tk_eng["Google"]
S.append(slide(top("Рынок") + f'<h1>В России ищут в Яндексе. Мои проекты получают из него {min(tk_ya_share, mp_ya_share)}–{max(tk_ya_share, mp_ya_share)}% поискового трафика</h1>'
  '<div class="body"><div class="row fill" style="gap:48px;align-items:center">'
  f'<div style="flex:none;display:flex;gap:28px;align-items:center">{mk}<div class="leg" style="flex-direction:column;gap:14px;font-size:20px"><span><i style="background:#FC3F1D"></i>Яндекс 72%</span><span><i style="background:#4285F4"></i>Google 26%</span><span><i style="background:#E0E2E8"></i>Остальные 2%</span></div></div>'
  f'<div class="chart" style="flex:1"><div class="cap" style="font-weight:500;color:{INK}">Визиты из поисковых систем за 30 дней</div>'
  + hbars([(f"techkio.ru: Яндекс", tk_eng["Yandex"], "#FC3F1D"), ("techkio.ru: Google", tk_eng["Google"], "#4285F4"), ("techkio.ru: остальные", tk_other, "#E0E2E8"),
           ("мапка.рф: Яндекс", mp_eng["Yandex"], "#FC3F1D"), ("мапка.рф: Google", mp_eng["Google"], "#4285F4")], w=760, rowh=54, labw=260)
  + '</div></div><p class="foot">Доли рынка: Яндекс Радар и StatCounter, 2026. Свои цифры: Яндекс Метрика, 30 дней до 6 сентября 2026. На смартфонах доля Google выше, на компьютерах ниже.</p></div>', "Рынок поиска"))

# 10 три шага
S.append(slide(top("Три шага поисковика") + '<h1>Поисковик делает три вещи: находит страницы, запоминает их и сортирует под запрос</h1>'
  '<div class="body"><div class="pipe" style="margin:auto 0">'
  + step("1", "Сканирование", "Робот ходит по ссылкам и скачивает страницы. Ломается, если на страницу нет ссылок или робот закрыт в robots.txt.", "teal", "robot", 0) + arrow()
  + step("2", "Индексация", "Разбирает страницу и кладёт в базу: о чём она, какому адресу принадлежит. Ломается на дублях, noindex и чужом canonical.", "lav", "book", 1) + arrow()
  + step("3", "Ранжирование", "На каждый запрос сортирует подходящие страницы по сотням сигналов. Проигрывает слабый ответ и страница без авторитета.", "yel", "podium", 2)
  + '</div><p class="foot">Порядок важен: нельзя ранжироваться, не попав в индекс, и нельзя попасть в индекс, если робот не дошёл.</p></div>', "Три шага"))

# 11 сканирование
S.append(slide(top("Шаг 1. Сканирование") + '<h1>Робот идёт по ссылкам. Страница без входящих ссылок для него не существует</h1>'
  '<div class="body"><div class="row fill" style="gap:36px;align-items:center">'
  f'<div style="flex:none">{graph()}</div><div class="g2" style="flex:1;align-content:center">'
  + f'<div class="card"><h4><span class="mono">robots.txt</span></h4><p>Файл в корне сайта: что роботу можно обходить, а что нельзя. Одна ошибочная строка закрывает весь сайт.</p></div>'
  + f'<div class="card"><h4><span class="mono">sitemap.xml</span></h4><p>Список адресов, которые ты хочешь показать. Робот берёт его как маршрут, а не как приказ.</p></div>'
  + '<div class="card"><h4>Внутренние ссылки</h4><p>Путь робота и вес страниц: чем больше ссылок ведёт на страницу, тем чаще её обходят.</p></div>'
  + '<div class="card"><h4>Скорость ответа</h4><p>У робота бюджет времени на сайт. Медленный сервер отдаёт меньше страниц за визит.</p></div>'
  + f'</div></div><p class="foot">мапка.рф: в sitemap {MP["yandex_summary"]["sitemap_urls"]} адресов, в поиске Яндекса {MP["yandex_summary"]["in_search"]} страниц, {MP["yandex_summary"]["excluded"]} исключено. techkio.ru: {TK["yandex_summary"]["sitemap_urls"]} и {TK["yandex_summary"]["in_search"]}. Данные Вебмастера.</p></div>', "Сканирование"))

# 12 индексация
S.append(slide(top("Шаг 2. Индексация") + '<h1>Один адрес на одну страницу. Дубли и противоречия выбрасывают из индекса</h1>'
  '<div class="body"><div class="row fill" style="gap:26px">'
  '<div style="flex:1.3;display:flex;flex-direction:column;gap:16px">'
  f'<div class="sticky coral"><span class="lab">Как мапка.рф теряла страницы, июль 2026</span><h4>Ссылки вели на один адрес, canonical — на другой</h4>'
  f'<p>Меню и футер ссылались на <span class="mono">/sektsii/futbol</span>, а в коде страницы стояло «настоящий адрес — <span class="mono">/sektsii/sportivnye/futbol</span>». Google обходил первый, читал указание и исключал его как копию. Страницы просто не было в поиске.</p></div>'
  f'<div class="sticky teal"><span class="lab">Починка, 29 июля</span><h4>Canonical стал равен адресу из ссылок, старые адреса отдают 308</h4>'
  f'<p>Робот видит один адрес везде: в ссылках, в canonical, в sitemap. Через три недели страниц в поиске Яндекса стало {MP["yandex_in_search_history"][-1][1]} вместо 36.</p></div></div>'
  '<div style="flex:1;display:flex;flex-direction:column;gap:14px">'
  '<div class="card"><h4><span class="mono">noindex</span></h4><p>Метка «не клади в индекс». Нужна служебным и тонким страницам. Случайно поставленная на весь сайт — обнуляет трафик.</p></div>'
  '<div class="card"><h4><span class="mono">canonical</span></h4><p>Указание «главная версия этой страницы — вот по такому адресу». Должен совпадать с тем, куда ведут ссылки.</p></div>'
  '<div class="card"><h4><span class="mono">301 / 308</span></h4><p>Постоянный редирект: страница переехала. Переносит накопленный вес. 404 его теряет.</p></div>'
  '</div></div></div>', "Индексация"))

# 13 ранжирование
S.append(slide(top("Шаг 3. Ранжирование") + '<h1>Сотни сигналов, но все они отвечают на три вопроса</h1>'
  '<div class="body"><div class="g3 fill">'
  + sticky("yel", "Отвечает ли страница на запрос?", "Релевантность: слова, смысл, полнота ответа. Страница про «крафт верстака» должна показать крафт в первом экране, а не историю мода.", ui("target", "lg"))
  + sticky("grey", "Можно ли ей верить?", "Качество и опыт: кто автор, есть ли факты и цифры, удобно ли читать с телефона. Google называет это E-E-A-T: опыт, экспертность, авторитетность, доверие.", ui("shield", "lg"))
  + sticky("grey", "Кто за неё ручается?", "Авторитет: ссылаются ли на тебя другие сайты, упоминают ли бренд. Чужие голоса весят больше собственных заявлений.", ui("link", "lg"))
  + '</div><p class="foot">Яндекс добавляет четвёртый вопрос: как ведут себя люди. Вернулся ли человек в выдачу через пять секунд или остался читать.</p></div>', "Ранжирование"))

# 14 намерение
def qcard(kind, label, q, meta, page, win=None):
    tail = f'<span class="pill" style="margin-top:auto;align-self:flex-start">{win}</span>' if win else ""
    return f'<div class="sticky {kind}"><span class="lab">{label}</span><div class="qcard"><div class="q">{q}</div><div class="meta">{meta}</div></div><p>{page}</p>{tail}</div>'
S.append(slide(top("Намерение запроса") + '<h1>У запроса есть намерение. Страница должна совпасть с ним, а не со словами</h1>'
  '<div class="body"><div class="g4 fill">'
  + qcard("yel", "Информационный", "как записать мэ сеть", "54 показа, 21 клик, позиция 3", "Человек хочет инструкцию, а не знакомство с сервером.", "Побеждает: гайд с шагами")
  + qcard("grey", "Навигационный", "k.i.o сервер", "8 показов, 7 кликов, позиция 1–2", "Ищут конкретный сайт. Важно быть первым по своему имени, и только.", "Побеждает: главная")
  + qcard("grey", "Коммерческий", "бассейн ростов-на-дону западный", "52 показа, 5 кликов, позиция 6", "Выбирают между вариантами, хотят сравнить цены и адреса.", "Побеждает: список с картой")
  + qcard("yel", "Чужой бренд", "южный меридиан бассейн ростов", "154 показа, 20 кликов, позиция 5", "Ищут конкретный клуб. Агрегатор живёт на том, что его карточка полнее сайта клуба.", "Побеждает: карточка клуба")
  + '</div><p class="foot">Все четыре запроса реальные: Яндекс Вебмастер, techkio.ru и мапка.рф, 30 дней до 5 сентября 2026.</p></div>', "Намерение запроса"))

S.append(divider("02", "Что видит пользователь", "Выдача, сниппет и почему позиция решает почти всё.",
                 ["Анатомия современной выдачи", "Сниппет: три строки, которыми ты управляешь", "Позиция и клики на своих данных", "Запросы без клика и ИИ-ответ"]))

# 15 анатомия выдачи
serp = ('<div class="serp"><div class="q">' + ui("search") + 'детские секции ростов-на-дону</div>'
  '<div class="sr ad"><span class="m">1</span><div class="t">Детский центр «Умка» — запись на пробное занятие</div><div class="u">umka-rostov.example</div><div class="d">Скидка 20% на первый месяц. Танцы, английский, робототехника.</div></div>'
  '<div class="sr"><span class="m">2</span><div class="ai"><b>Быстрый ответ</b>В Ростове-на-Дону работает больше 200 детских секций: спортивные, творческие и языковые. Выбирать удобнее по району и возрасту ребёнка<sup>[1]</sup>, средняя цена от 2 400 ₽<sup>[2]</sup>.</div></div>'
  '<div class="sr"><span class="m">3</span><div class="t">Кружки и секции для детей в Ростове-на-Дону — Мапка</div><div class="u">мапка.рф</div><div class="d">205 клубов на карте: спорт, творчество, языки. Цены, отзывы, расписание, фильтр по району.</div></div>'
  '<div class="sr"><span class="m">4</span><div class="loc"><span>Южный Меридиан<br>бассейн, 4,7 ★</span><span>Кай Кидс<br>гимнастика, 4,9 ★</span><span>Лягушонок<br>плавание, 4,8 ★</span></div></div>'
  '<div class="sr"><span class="m">5</span><div class="paa"><span>Сколько стоят детские секции в Ростове?</span><span>Куда отдать ребёнка в 5 лет?</span></div></div></div>')
legend = [("1", "Реклама", "Первые строки куплены. Пометка мелкая, кликов много."),
          ("2", "ИИ-ответ", "Нейро у Яндекса, AI Overview у Google. Цитирует несколько сайтов — это уже GEO."),
          ("3", "Органика", "Бесплатные результаты. Наша территория: позиция зависит от страницы, не от бюджета."),
          ("4", "Карты и организации", "Локальный блок. Для офлайн-бизнеса забирает клики выше органики."),
          ("5", "Похожие вопросы", "Подсказка, что ещё спрашивают. Готовый план контента.")]
S.append(slide(top("Анатомия выдачи") + '<h1>Выдача давно не десять синих ссылок</h1>'
  '<div class="body"><div class="row fill" style="gap:40px">'
  f'<div style="flex:1.05">{serp}</div><div class="legend" style="flex:1;justify-content:center">'
  + "".join(f'<div class="li"><span class="m">{n}</span><div><h5>{h}</h5><p>{p}</p></div></div>' for n, h, p in legend)
  + '</div></div><p class="foot">Макет собран по реальной выдаче Яндекса, названия рекламодателя условные.</p></div>', "Анатомия выдачи"))

# 16 сниппет
S.append(slide(top("Сниппет") + '<h1>Сниппет — единственное, что человек видит до клика. И ты им управляешь</h1>'
  '<div class="body"><div class="anat" style="margin-bottom:26px">'
  '<div class="k">Заголовок, тег title</div><div class="box"><div class="t">Плавание для детей в Ростове-на-Дону — 20 секций, цены, отзывы | Мапка</div></div>'
  '<div class="k">Адрес страницы</div><div class="box"><div class="u">мапка.рф/sektsii/plavanie</div></div>'
  '<div class="k">Описание, meta description</div><div class="box"><div class="d">Бассейны и школы плавания для детей от 3 лет: 20 секций на карте с ценами от 500 ₽, отзывами и расписанием. Подбор по району.</div></div>'
  '</div><div class="g2 fill">'
  '<div class="sticky coral"><span class="lab">Было на карточках клубов до 2 августа</span><h4>Южный Меридиан - Мапка</h4><p>Ни города, ни сути. Человек ищет «бассейн южный меридиан ростов» и не видит совпадения.</p></div>'
  '<div class="sticky teal"><span class="lab">Стало</span><h4>Южный Меридиан в Ростове-на-Дону — цены, отзывы | Мапка</h4><p>Город, что внутри, чей это сайт. Клики на карточки клубов выросли вместе с позициями.</p></div>'
  '</div><p class="foot">Заголовок до 60 знаков, описание до 160, иначе поисковик обрежет или заменит своим текстом.</p></div>', "Сниппет"))

# 17 позиция и CTR
cats = ["позиции 2–3", "позиции 4–10", "позиции 11+"]
S.append(slide(top("Позиция и клики") + '<h1>Со второй-третьей строки кликают в шесть раз чаще, чем с четвёртой–десятой</h1>'
  '<div class="body"><div class="row fill" style="gap:40px">'
  f'<div class="chart" style="flex:1.2">{bars(cats, [("techkio.ru", "#0FBCB0", [ctr_tk["2–3"], ctr_tk["4–10"], ctr_tk["11+"]]), ("мапка.рф", "#FFD02F", [ctr_mp["2–3"], ctr_mp["4–10"], 0])], w=820, h=400, suffix="%", ymax=40)}'
  '<div class="leg"><span><i style="background:#0FBCB0"></i>techkio.ru</span><span><i style="background:#FFD02F"></i>мапка.рф</span><span>доля кликов от показов, CTR</span></div></div>'
  '<div style="flex:1;display:flex;flex-direction:column;gap:16px;justify-content:center">'
  + sticky("yel", "Главный рычаг — не новые страницы, а подъём существующих", "У techkio.ru 8 886 показов пришлись на позиции 4–10 и дали 278 кликов. Те же показы на позициях 2–3 дали бы около 1 700.")
  + sticky("grey", "С одиннадцатой строки не кликают вообще", "Вторая страница выдачи — это ноль. Быть «в топ-20» ничего не значит.")
  + f'</div></div><p class="foot">Яндекс Вебмастер, топ запросов за 30 дней до 5 сентября 2026: {TK["yandex_ctr_queries_n"]} запросов techkio.ru и {MP["yandex_ctr_queries_n"]} запросов мапка.рф. Позиция 1 не показана: слишком мало запросов.</p></div>', "Позиция и клики"))

# 18 zero-click
S.append(slide(top("Запросы без клика") + '<h1>Больше половины запросов заканчиваются без клика. ИИ-ответ забирает ещё</h1>'
  '<div class="body"><div class="g3" style="margin-bottom:26px">'
  + stat("68%", "запросов в Google США завершились без перехода на сайт, начало 2026")
  + stat('<span style="white-space:nowrap;font-size:68px">27% <small>→</small> 11%</span>', "CTR первой позиции, когда над выдачей стоит ИИ-ответ")
  + stat("20–48%", "запросов Google уже показывают AI Overview, по разным выборкам")
  + '</div><div class="g2 fill">'
  + sticky("rose", "Что это меняет", "Борьба идёт не только за клик, но за место в ответе. Если ИИ пересказывает твою страницу и ставит ссылку — это трафик и доверие. Если пересказывает конкурента — ты невидим.", ui("chat", "lg"))
  + sticky("grey", "Что не меняется", "ИИ-ответ собирается из тех же страниц, что и обычная выдача. Не попал в индекс — не попал в ответ. SEO остаётся фундаментом.", ui("layers", "lg"))
  + '</div><p class="foot">SparkToro и Datos, 2026; исследование немецкой выдачи с AI Overview, 2026; Semrush и Ahrefs по доле AI Overview. Ссылки на слайде с источниками.</p></div>', "Запросы без клика"))

S.append(divider("03", "ИИ-выдача и GEO", "Где теперь ищут, как ассистент собирает ответ и кого он цитирует.",
                 ["Ищут уже не только в поисковике", "Как ИИ строит ответ", "Четыре ответчика — четыре индекса", "Шесть вещей, повышающих шанс цитирования", "SEO против GEO",
                  "Что перестало работать, а что работает"]))

# 19 где ищут
S.append(slide(top("Где ищут") + '<h1>Ищут уже не только в поисковике</h1>'
  '<div class="body"><div class="row fill" style="gap:48px;align-items:center">'
  f'<div style="flex:none">{stat("900 <small>млн</small>", "человек пользуются ChatGPT каждую неделю. OpenAI, февраль 2026. Год назад было 400 миллионов.")}</div>'
  '<div class="tiles" style="flex:1;gap:22px">' + "".join(tile(s, l, "big") for s, l in [("chatgpt", "ChatGPT"), ("perplexity", "Perplexity"), ("claude", "Claude"), ("googlegemini", "Gemini и AI Mode"),
   ("neuro", "Нейро и Алиса"), ("deepseek", "DeepSeek"), ("copilot", "Copilot в Bing"), ("duckduckgo", "DuckDuckGo AI")])
  + '</div></div><p class="foot">Каждый из них отвечает текстом и ставит ссылки на источники. Вопрос встречи: как оказаться среди источников.</p></div>', "Где ищут"))

# 20 как ИИ отвечает
S.append(slide(top("Как ИИ отвечает") + '<h1>ИИ не читает интернет. Он ищет так же, как ты, и пересказывает найденное</h1>'
  '<div class="body"><div class="pipe" style="margin:auto 0">'
  + step("1", "Запрос", "«куда отдать ребёнка в 5 лет в Ростове»", "grey", "chat", 0) + arrow()
  + step("2", "Веер подзапросов", "Ассистент разбивает вопрос на 8–12 поисковых запросов: секции по возрасту, цены, районы, отзывы.", "rose", "share", 1) + arrow()
  + step("3", "Поиск по индексу", "Каждый подзапрос уходит в поисковый индекс. Свой или чужой — у каждого ассистента по-разному.", "rose", "search", 2) + arrow()
  + step("4", "Отбор источников", "Из десятков страниц остаются 5–8. Берут те, где ответ виден сразу и данные свежие.", "rose", "list", 3) + arrow()
  + step("5", "Ответ с цитатами", "Текст с пометками [1], [2]. Ссылка ведёт на источник — это и есть GEO-трафик.", "grey", "quote", 4)
  + '</div><p class="foot">Если страницы нет в индексе, шаг 3 её не найдёт. Поэтому GEO не заменяет SEO, а надстраивается над ним.</p></div>', "Как ИИ отвечает"))

# 21 четыре двери
S.append(slide(top("Четыре ответчика") + '<h1>Единого «индекса ИИ» нет. Четыре ответчика — четыре разных двери</h1>'
  '<div class="body"><div class="g4 fill">'
  + f'<div class="sticky rose">{tile("chatgpt")}<h4>ChatGPT</h4><p>Свой индекс плюс покупные результаты Google. JavaScript не исполняет: что не в HTML, того для него нет. Хранит копии страниц по 90 дней.</p></div>'
  + f'<div class="sticky grey">{tile("claude")}<h4>Claude</h4><p>Ищет через Brave. Единственная дверь с ручкой: адрес можно отправить напрямую в <span class="mono">search.brave.com/webmaster</span>.</p></div>'
  + f'<div class="sticky grey">{tile("googlegemini")}<h4>Google AI Mode</h4><p>Веер из 8–12 подзапросов. Лишь 14% источников совпадают с обычным топ-10 по исходному запросу.</p></div>'
  + f'<div class="sticky rose">{tile("perplexity")}<h4>Perplexity</h4><p>Свой краулер и индекс, около 8 источников на ответ. Любит свежее и обсуждения: треть цитат из соцсетей и Reddit.</p></div>'
  + '</div><p class="foot">Сводка исследований цитируемости 2025–2026, собрана в августе 2026. Цифры меняются каждый квартал, проверять перед использованием.</p></div>', "Четыре ответчика"))

# 22 что влияет
influ = [("Ответ в первых ста словах", "Девять из десяти цитируемых страниц отвечают на вопрос до первого скролла. Предисловия ИИ пропускает."),
         ("Свежесть", "Почти все цитаты моложе десяти месяцев. Страница, обновлённая за последние 30 дней, цитируется втрое чаще."),
         ("Структура списком или шагами", "Подборки «топ-N» и пошаговые инструкции собирают больше половины цитат. Абзацы без структуры проигрывают."),
         ("Свои цифры и факты", "Три и больше собственных чисел на странице — в четыре раза больше цитат. Пересказ чужого не цитируют."),
         ("Видимый автор", "Имя и роль автора на странице добавляют около 40%. Анонимный текст доверия не вызывает."),
         ("Упоминания бренда на чужих сайтах", "Связь упоминаний с цитируемостью втрое сильнее, чем у ссылок. Про тебя должны говорить.")]
S.append(slide(top("Что влияет на цитирование") + '<h1>Шесть вещей, которые измеримо повышают шанс попасть в ответ</h1>'
  '<div class="body"><div class="chk fill" style="grid-template-rows:repeat(3,minmax(0,1fr))">' + "".join(
  f'<div class="ck"><span class="num{" y" if i<3 else ""}">{i+1}</span><div><h5>{h}</h5><p>{p}</p></div></div>' for i, (h, p) in enumerate(influ))
  + '</div><p class="foot">Порядок по силе эффекта в исследованиях 2025–2026. Первые три — про страницу, последние три — про доверие к автору и бренду.</p></div>', "Что влияет на цитирование"))

# 23 SEO vs GEO
rows = [("Цель", "Клик на сайт из выдачи", "Цитата и ссылка внутри ответа"),
        ("Единица", "Страница целиком", "Абзац, который отвечает на подзапрос"),
        ("Главный сигнал", "Релевантность, ссылки, поведение", "Свежесть, структура, упоминания бренда"),
        ("Как измерять", "Позиция, показы, клики в Вебмастере и Search Console", "Доля ответов с твоей ссылкой, с повторами: ответы нестабильны"),
        ("Что общего", "Страница должна быть в индексе и быстро отдаваться", "Ровно то же самое. Без SEO нет GEO")]
S.append(slide(top("SEO и GEO") + '<h1>Две дисциплины с одним фундаментом</h1>'
  '<div class="body"><div class="tbl fill"><div class="h"></div><div class="h">SEO: поисковая выдача</div><div class="h geo">GEO: ответ ассистента</div>'
  + "".join(f'<div class="k">{k}</div><div>{a}</div><div class="geo">{b}</div>' for k, a, b in rows)
  + '</div><p class="foot">На встрече 5 разберём GEO руками: соберём страницу под цитирование и проверим её в четырёх ассистентах.</p></div>', "SEO и GEO"))

# 27 что работает и что нет
DEAD = [("Закупка ссылок пачками", "Яндекс фильтрует такие ссылки «Минусинском» с 2015 года, Google их просто не считает. Заработанное упоминание весит больше купленного."),
        ("Ключи ради ключей", "За переспам и текст «для робота» Яндекс наказывает «Баден-Баденом» с 2017 года. Точное вхождение запроса давно не нужно."),
        ("Страницы без спроса", "Пустые и тонкие страницы тянут вниз весь сайт. На Мапке поэтому порог: посадочная выходит в индекс от трёх клубов."),
        ("llms.txt как вход в ИИ", "Из 137 тысяч сайтов 97% файлов не прочитал ни один бот. Google говорит прямо, что файл не нужен."),
        ("Обман робота", "Подмена контента по агенту и подсказки ассистенту в разметке. С мая 2026 это прямо в спам-политиках Google.")]
ALIVE = [("Одна страница — одно намерение", "Совпасть с тем, зачем человек искал, важнее, чем совпасть со словами запроса."),
         ("Ответ в первом экране", "Начало страницы читают и человек, и ассистент. Предисловие пропускают оба."),
         ("Свои цифры и свой опыт", "Пересказ чужого не цитируют и не ранжируют. Собственные данные отличают страницу от сотни похожих."),
         ("Технически чистая страница", "Один адрес, есть в карте сайта, быстро отдаётся, открыта роботу. Без этого не работает ничего дальше."),
         ("Упоминания, а не только ссылки", "Про проект должны говорить там, где живёт его аудитория. Это влияет и на поиск, и на ответы ИИ.")]
def plist(items, icon):
    return '<ul class="plist">' + "".join(
        f'<li>{ui(icon, "xs")}<div><b>{h}</b><i>{p}</i></div></li>' for h, p in items) + '</ul>'
S.append(slide(top("Итог первых трёх блоков") + '<h1>Что в 2026-м перестало работать, а что работает</h1>'
  '<div class="body"><div class="g2 fill">'
  f'<div class="sticky coral tight"><span class="lab">Перестало работать</span>{plist(DEAD, "no")}</div>'
  f'<div class="sticky teal tight"><span class="lab">Работает</span>{plist(ALIVE, "check")}</div>'
  '</div><p class="foot">«Минусинск» и «Баден-Баден» — фильтры Яндекса за покупные ссылки и переоптимизацию. Данные по llms.txt: разбор Ahrefs на 137 тысячах сайтов, май 2026.</p></div>', "Что работает и что нет"))

S.append(divider("04", "Два кейса", "Мапка.рф и techkio.ru: что сделано, что выросло и какой урок общий.",
                 ["Мапка.рф: каталог секций Ростова", "Что случилось 2 августа", "Агрегатор ловит чужие бренды", "techkio.ru: гайды под запросы игроков", "Правило сироты", "Один цикл для обоих"]))

# 24 мапка интро
S.append(slide(top("Кейс 1. Мапка.рф") + f'<h1>Каталог детских секций Ростова: 205 клубов, {MP["yandex_summary"]["sitemap_urls"]} адресов в карте сайта</h1>'
  '<div class="body"><div class="row fill" style="gap:32px">'
  f'<div style="flex:1.25">{browser("мапка.рф/sektsii/futbol", "mapka_sekcii.webp")}</div>'
  '<div style="flex:1;display:flex;flex-direction:column;gap:14px">'
  + sticky("orange", "Страницы под спрос из данных", "8 направлений, 7 районов, 2 возраста: «плавание», «в Левенцовке», «для дошкольников». Каждая посадочная — своя карта и свой текст.")
  + sticky("grey", "Порог качества", "Посадочная выходит в индекс, если на ней три клуба и больше. Тонкие страницы получают noindex, чтобы не тянуть сайт вниз.")
  + sticky("grey", f"Родители ищут с телефона", f"{mp_mob}% визитов со смартфонов. Дизайн, скорость и сниппеты проверяются сначала на телефоне.")
  + '</div></div><p class="foot">Проект запущен в декабре 2025. Технически: Next.js, Postgres, FastAPI, один маленький сервер.</p></div>', "Мапка.рф"))

# 25 мапка август
ins_pts = [(d[5:10].replace("-", "."), v) for d, v in mp_ins if d >= "2026-02-01"]
def xl(s): return s[3:] + "." + s[:2] if False else s[3:5] + "." + s[0:2]
S.append(slide(top("Кейс 1. Что случилось 2 августа") + '<h1>Больше страниц, честные заголовки, редиректы. Страниц в поиске Яндекса: 36 → 454</h1>'
  '<div class="body"><div class="row fill" style="gap:36px">'
  f'<div class="chart" style="flex:1.25">{line_chart(ins_pts, w=860, h=420, color="#3F3A8F", fill="#EDEAFF", every=7, mark_peak=True, xfmt=lambda s: s[3:5]+"."+s[0:2])}<div class="leg"><span><i style="background:#3F3A8F"></i>страниц мапка.рф в поиске Яндекса, по данным Вебмастера</span></div></div>'
  f'<div style="flex:1;display:grid;grid-template-rows:repeat(3,minmax(0,1fr));gap:12px">'
  + stat(f'{fmt(mp_month["2026-07"][0])} <small>→</small> {fmt(mp_month["2026-08"][0])}', "показов в Яндексе за месяц, июль и август", "sm")
  + stat(f'{fmt(mp_month["2026-07"][1])} <small>→</small> {fmt(mp_month["2026-08"][1])}', "кликов из Яндекса за месяц", "sm")
  + stat(f'34 <small>→</small> {fmt(mp_weeks[-1][1])}', "визитов из поиска в неделю, конец июля и конец августа", "sm")
  + '</div></div><p class="foot">Ничего волшебного: больше страниц под реальный спрос, чистая индексация и сниппет с сутью. Всё остальное сделал поисковик.</p></div>', "Мапка.рф: 2 августа"))

# 26 мапка урок
pairs = [("южный меридиан бассейн ростов на дону", "/yuzhny-meridian", 300), ("бесплатные кружки и секции для детей в ростове", "/sektsii/besplatnye", 89),
         ("лягушонок бассейн ростов", "/lyagushonok", 66), ("кай кидс ростов", "/kaykids", 30), ("бассейн дгту", "/basseyn-dgtu", 21)]
S.append(slide(top("Кейс 1. Урок") + '<h1>Агрегатор ловит чужие бренды: ищут клуб, а находят его карточку на Мапке</h1>'
  '<div class="body"><div class="row fill" style="gap:36px">'
  '<div style="flex:1.3;display:flex;flex-direction:column;gap:10px">'
  '<div class="tbl" style="grid-template-columns:minmax(0,1.4fr) minmax(0,1fr) 150px"><div class="h">Что вбивают в Яндекс</div><div class="h">Куда попадают</div><div class="h">Входов за 30 дней</div>'
  + "".join(f'<div class="mono" style="font-size:19px">{q}</div><div class="mono" style="font-size:19px;color:var(--moss)">{p}</div><div class="k" style="text-align:right">{v}</div>' for q, p, v in pairs)
  + '</div></div><div style="flex:1;display:flex;flex-direction:column;gap:14px;justify-content:center">'
  + sticky("orange", "Делай страницы под сущности, которые уже ищут", "Клубы, адреса, районы, «бесплатные». Не под абстрактные «детские секции»: по ним конкурируют Яндекс Карты и 2ГИС.")
  + sticky("grey", "Карточка обгоняет сайт клуба", "У половины клубов сайта нет вовсе. Полная карточка с ценами, расписанием и отзывами становится их страницей в поиске.")
  + '</div></div><p class="foot">Яндекс Метрика, страницы входа из поиска, 30 дней до 6 сентября 2026.</p></div>', "Мапка.рф: урок"))

# 27 techkio интро
geo = TK["metrika_geo30"][:3]
S.append(slide(top("Кейс 2. techkio.ru") + f'<h1>Сайт Minecraft-сервера. Восемь недель, {TK["yandex_summary"]["in_search"]} страниц в поиске, {fmt(tk_search)} визитов из поиска за месяц</h1>'
  '<div class="body"><div class="row fill" style="gap:32px">'
  f'<div style="flex:1.25">{browser("techkio.ru", "techkio.webp")}</div>'
  '<div style="flex:1;display:grid;grid-template-rows:repeat(3,minmax(0,1fr));gap:12px">'
  + stat(f'{fmt(tk_eng["Yandex"])} <small>и</small> {fmt(tk_eng["Google"])}', "визитов из Яндекса и из Google за 30 дней", "sm")
  + stat(f"{tk_pc}%", "визитов с компьютера: игроки ищут гайды прямо во время игры", "sm")
  + stat(", ".join(g[0].replace("Saint Petersburg", "Петербург").replace("Moscow", "Москва").replace("Rostov-na-Donu", "Ростов") for g in geo), "три главных города аудитории", "sm")
  + '</div></div><p class="foot">Сайт открыт 15 июля 2026. Это не «сайт про сервер», а библиотека гайдов по модам, которые стоят на сервере.</p></div>', "techkio.ru"))

# 28 techkio гайды
S.append(slide(top("Кейс 2. Гайды под запросы") + '<h1>Гайды под запросы игроков: одна страница дала 1 306 входов за месяц</h1>'
  '<div class="body"><div class="row fill" style="gap:36px;align-items:center">'
  f'<div class="chart" style="flex:1.2"><div class="cap" style="font-weight:500;color:{INK}">Страницы входа из поиска за 30 дней, Метрика</div>{hbars([(p, v) for p, v in tk_entry], w=800, rowh=54, labw=330, mono=True)}</div>'
  '<div style="flex:1;display:flex;flex-direction:column;gap:12px">'
  + qcard("yel", "Запрос → гайд", "как записать мэ сеть", "54 показа, 21 клик, позиция 3: CTR 39%", "Ответ в первом абзаце, потом шаги с картинками. Разметка HowTo и FAQ.")
  + qcard("grey", "Запрос → гайд", "tacz крафты", "117 показов, 15 кликов, позиция 2,6", "Таблица крафтов сразу под заголовком. Игрок получает ответ за пять секунд и остаётся.")
  + '</div></div><p class="foot">Главная страница даёт 299 входов. Гайд про верстак — в четыре раза больше. Трафик приносит полезность, не бренд.</p></div>', "techkio.ru: гайды"))

# 29 правило сироты
S.append(slide(top("Кейс 2. Правило сироты") + '<h1>Новая страница получает входящие ссылки в день публикации. Иначе робот её не найдёт</h1>'
  '<div class="body"><div class="row fill" style="gap:36px;align-items:center">'
  f'<div style="flex:none">{graph()}</div><div style="flex:1;display:flex;flex-direction:column;gap:14px">'
  + '<div class="card"><h4>Карта сайта</h4><p>Первое, что обновляется. Робот увидит адрес, но не поймёт, насколько он важен.</p></div>'
  + '<div class="card"><h4>Меню или футер</h4><p>Ссылка с каждой страницы сайта. Так робот доходит за один визит и считает страницу важной.</p></div>'
  + '<div class="card"><h4>Тематически близкая страница</h4><p>Гайд для Steam Deck получил ссылку со страницы скачивания лаунчера: тот же читатель, тот же вопрос.</p></div>'
  + '</div></div><p class="foot">Запрос «майнкрафт стим дек» — 84 показа в месяц по Wordstat, конкурентов почти нет. Узкий спрос без конкуренции окупается быстрее широкого с конкуренцией.</p></div>', "Правило сироты"))

# 30 общий цикл
S.append(slide(top("Общий урок") + '<h1>Обе истории — один и тот же цикл. Он повторяется на любом проекте</h1>'
  '<div class="body"><div class="pipe" style="margin:auto 0">'
  + step("1", "Спрос уже есть", "Смотрим Вебмастер, Search Console, Wordstat: что люди вбивают и по чему нас уже показывают.", "orange", "search", 0) + arrow()
  + step("2", "Страница под спрос", "Гайд, карточка, посадочная. Одна страница — одно намерение. Ответ в первом экране.", "orange", "doc", 1) + arrow()
  + step("3", "Технически чистая", "Один адрес, есть в sitemap, быстро отдаётся, открыта роботу.", "grey", "shield", 2) + arrow()
  + step("4", "Сниппет продаёт клик", "Заголовок с сутью и гео, описание с цифрами. Проверяем CTR по позициям.", "grey", "eye", 3) + arrow()
  + step("5", "Ссылки внутри и снаружи", "Входящие ссылки в день публикации. Упоминания там, где живёт аудитория.", "grey", "link", 4)
  + '</div><p class="foot">Через месяц смотрим данные и возвращаемся к шагу 1. Остальные встречи серии — про каждый шаг по отдельности.</p></div>', "Общий цикл"))

S.append(divider("05", "Практикум", "Проверяем ваш проект, забираем инструменты и домашку.",
                 ["Десять минут на свой проект", "Инструменты: бесплатных хватает", "Домашка к встрече 2", "Что будет на встрече 2"]))

# 31 проверь проект
checks = [("Сколько страниц знает поиск", 'Вбей <span class="mono">site:твой-домен</span> в Яндексе и Google. Ноль — сайт не в индексе. Тысячи мусорных адресов — тоже проблема.'),
          ("Открыт ли сайт роботу", 'Открой <span class="mono">/robots.txt</span> и <span class="mono">/sitemap.xml</span>. Строка <span class="mono">Disallow: /</span> закрывает всё.'),
          ("Что написано в сниппете", "Посмотри title и description главной. Есть ли там суть проекта и город, если он важен."),
          ("Как быстро открывается с телефона", "PageSpeed Insights, вкладка «Мобильные». Ниже 50 — есть над чем работать."),
          ("Кого цитирует ИИ по твоей теме", "Спроси ChatGPT или Perplexity так, как спросил бы твой пользователь. Посмотри, чьи ссылки в ответе."),
          ("Подключены ли данные", "Яндекс Вебмастер и Google Search Console бесплатны и ставятся за десять минут. Без них всё остальное — гадание.")]
S.append(slide(top("Практикум") + '<h1>Проверь свой проект за десять минут</h1>'
  '<div class="body"><div class="chk fill" style="grid-template-rows:repeat(3,minmax(0,1fr))">' + "".join(
  f'<div class="ck"><span class="num y">{i+1}</span><div><h5>{h}</h5><p>{p}</p></div></div>' for i, (h, p) in enumerate(checks))
  + '</div><p class="foot">Нет своего проекта — возьми сайт друга, учебный проект или любимый локальный бизнес. Проверка одинаковая.</p></div>', "Практикум"))

# 32 инструменты
groups = [("Данные о поиске", [("webmaster", "Яндекс Вебмастер"), ("gsc", "Search Console")], "бесплатно"),
          ("Что делают посетители", [("metrika", "Яндекс Метрика"), ("googleanalytics", "Google Analytics")], "бесплатно"),
          ("Спрос и конкуренты", [("wordstat", "Wordstat"), ("ahrefs", "Ahrefs"), ("semrush", "Semrush")], "Wordstat бесплатно, остальное платно"),
          ("Техника", [("pagespeed", "PageSpeed"), ("frog", "Screaming Frog")], "бесплатно до 500 страниц"),
          ("ИИ-выдача", [("chatgpt", "ChatGPT"), ("perplexity", "Perplexity"), ("claude", "Claude")], "проверять руками, с повторами")]
S.append(slide(top("Инструменты") + '<h1 class="md">Инструменты: бесплатных хватает на первый год</h1>'
  '<div class="body"><div class="fill" style="display:flex;flex-direction:column;gap:6px;justify-content:center">' + "".join(
  f'<div class="row" style="align-items:center;gap:28px;padding:6px 0;border-bottom:1px solid var(--hair)"><div style="width:320px;flex:none"><div style="font:500 22px/1.2 var(--fd)">{g}</div><div style="font:400 17px/1.3 var(--ft);color:var(--slate);margin-top:5px">{note}</div></div>'
  f'<div class="tiles" style="gap:18px">{"".join(tile(s, l, "sm") for s, l in items)}</div></div>' for g, items, note in groups)
  + '</div><p class="foot">Логотипы Simple Icons и текстовые метки. Для домашки нужны только первые две строки.</p></div>', "Инструменты"))

# 33 домашка
S.append(slide(top("Домашнее задание") + '<h1>Домашка к встрече 2: три шага на час работы</h1>'
  '<div class="body"><div class="g3 fill">'
  + f'<div class="sticky yel"><span class="num">1</span><h4>Выбери проект</h4><p>Свой сайт, проект друга, учебный проект, страница на Tilda. Главное — чтобы он был открыт в интернете и ты мог менять его текст.</p></div>'
  + f'<div class="sticky grey"><span class="num">2</span><h4>Напиши десять запросов</h4><p>По каким словам проект должны находить. Проверь каждый руками в Яндексе и Google: на какой позиции ты, кто выше и почему.</p></div>'
  + f'<div class="sticky grey"><span class="num">3</span><h4>Подключи данные</h4><p>Яндекс Вебмастер и Google Search Console. Принеси скриншот: что уже показывается, по каким запросам. С этого начнём семантику.</p></div>'
  + '</div><p class="foot">Вопросы по домашке — в чат курса или мне в Telegram, отвечаю в течение дня.</p></div>', "Домашка"))

# 34 анонс
S.append(slide(top("Встреча 2") + '<h1>Встреча 2 — семантика: узнать, что люди ищут, до того как что-то писать</h1>'
  '<div class="body"><div class="g4 fill">'
  + sticky("grey", "Где брать запросы", "Wordstat, подсказки поиска, Вебмастер и Search Console: чужой спрос и свой уже существующий.", ui("search", "lg"))
  + sticky("grey", "Как группировать", "Кластеры: один смысл — одна страница. Почему «цена» и «купить» — разные страницы, а «стоимость» и «цена» — одна.", ui("layers", "lg"))
  + sticky("grey", "Как оценить спрос", "Частотность, сезонность, конкуренция. Узкий запрос без конкурентов против широкого с гигантами.", ui("gauge", "lg"))
  + sticky("yel", "Практикум", "Собираем ядро на 30–50 запросов для вашего проекта и раскладываем его по будущим страницам.", ui("pen", "lg"))
  + '</div><p class="foot">Дата — в чате курса. Приходите с домашкой: без списка запросов практикум не получится.</p></div>', "Анонс встречи 2"))

# 35 источники
srcs = [("Яндекс Метрика: визиты, источники, страницы входа", "metrika.yandex.ru", "мапка.рф и techkio.ru, 30 дней до 6 сентября 2026"),
        ("Яндекс Вебмастер: показы, клики, позиции, страниц в поиске", "webmaster.yandex.ru", "те же сайты, 30 дней и история с декабря 2025"),
        ("Google Search Console: клики, показы, устройства", "search.google.com/search-console", "sc-domain для обоих сайтов"),
        ("Доли поисковых систем в России, 2026", "radar.yandex.ru", "также StatCounter; сводки inclient.ru и botfaqtor.ru"),
        ("ChatGPT: 900 млн недельных пользователей", "techcrunch.com, 27.02.2026", "заявление OpenAI при раунде финансирования"),
        ("68% запросов без клика, Google США", "sparktoro.com, 2026", "исследование SparkToro и Datos"),
        ("CTR первой позиции при AI Overview: 27% → 11%", "seo-kreativ.de, 2026", "немецкая выдача; сходные оценки у Ahrefs и Semrush"),
        ("Доля запросов с AI Overview 20–48%", "cognizo.ai, thestacc.com", "зависит от выборки и типа запросов"),
        ("Механика цитирования в ИИ: четыре индекса, факторы", "сводка исследований, август 2026", "Seer Interactive, Profound, SparkToro, собственные проверки"),
        ("Спам-политики Google про ИИ-ответы, 15.05.2026", "searchengineland.com", "манипуляция генеративными ответами приравнена к спаму"),
        ("llms.txt: 97% файлов не читает ни один бот", "ahrefs.com/blog/llmstxt-study", "137 тысяч сайтов, май 2026; Google файл не поддерживает"),
        ("Каталог DESIGN.md, стиль деки", "github.com/VoltAgent/awesome-design-md", "донор токенов — Miro"),
        ("Логотипы", "simpleicons.org", "лицензия CC0; Яндекс, ChatGPT, Bing, Ahrefs — текстовые метки"),
        ("Дека и исходники", "github.com/Kom1sh/seo-course", "закрыто от индексации, правится в src/")]
S.append(slide(top("Источники") + '<h1 class="md">Источники и данные</h1>'
  '<div class="body"><div class="src fill">' + "".join(
  f'<div class="srow"><span class="num">{t}</span><span class="lnk">{l}</span><span class="whr">{w}</span></div>' for t, l, w in srcs)
  + '</div></div>', "Источники"))

# 36 контакты
S.append(slide(top("Вопросы") + '<div class="body"><div class="row fill" style="align-items:flex-end;gap:60px"><div style="flex:1.2;display:flex;flex-direction:column;height:100%">'
  '<div class="divt" style="font-size:96px;line-height:.98">Вопросы?</div>'
  '<div style="margin-top:auto;display:flex;flex-direction:column;gap:20px">'
  '<div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px">'
  '<div class="card"><h4>Telegram</h4><p class="mono" style="font-size:21px;color:#fff">@Kom1sh</p></div>'
  '<div class="card"><h4>Сайт</h4><p class="mono" style="font-size:19px;color:#fff;white-space:nowrap">egorprotasov.ru</p></div>'
  '<div class="card"><h4>Проекты</h4><p class="mono" style="font-size:19px;line-height:1.5;color:#fff">мапка.рф<br>techkio.ru<br>mediachef.app</p></div></div>'
  '<div class="card"><h4>Эта дека, слайды останутся</h4>'
  '<p class="mono" style="font-size:30px;color:var(--yel);white-space:nowrap">kom1sh.github.io/seo-course</p></div></div></div>'
  '<div class="divlist" style="flex:1;padding-bottom:12px"><span>Домашка: проект, десять запросов, Вебмастер и Search Console</span><span>Встреча 2 — семантика, дата в чате курса</span><span>Вопросы по ходу — в чат или лично</span></div></div></div>', "Вопросы", "dark"))

out = "\n".join(S)
(HERE / "slides.html").write_text(out, encoding="utf-8")
print("slides.html:", len(S), "слайдов,", len(out.encode()) // 1024, "КБ")
