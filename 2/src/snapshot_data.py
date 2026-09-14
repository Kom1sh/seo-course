#!/usr/bin/env python3
"""Снимок данных для встречи 2. Читает выгрузки из $SEO_DUMP (Вебмастер, Search Console,
Метрика, подсказки Яндекса, sitemap Мапки) и пишет src/data.json.

    SEO_DUMP=/путь/к/выгрузкам python3 src/snapshot_data.py
"""
import json, os, pathlib, collections

SRC = pathlib.Path(os.environ.get("SEO_DUMP", "/Users/egor/.claude/jobs/dc65153a/tmp/seo2"))
p2 = json.load(open(SRC / "pull2.json"))
mt = json.load(open(SRC / "metrika.json"))
sek = json.load(open(SRC / "mapka_sektsii.json"))
TK, MP = "https://techkio.ru", "https://xn--80aa3agq.xn--p1ai"
out = {"period": p2["period"], "snapshot": "2026-09-14"}

# длинный хвост: доли показов по корзинам ранга запроса
def tail(key):
    sh = sorted([q["indicators"]["TOTAL_SHOWS"] for q in p2[key]["queries"]], reverse=True); t = sum(sh)
    b = [sum(sh[:10]), sum(sh[10:100]), sum(sh[100:1000]), sum(sh[1000:])]
    return {"queries": len(sh), "shows": int(t), "buckets": [round(100 * x / t) for x in b],
            "le5": round(100 * sum(1 for v in sh if v <= 5) / len(sh))}
out["tail"] = {"techkio": tail("wm:https:techkio.ru:443"), "mapka": tail("wm:https:xn--80aa3agq.xn--p1ai:443")}

# кластеры, которые Google сам собрал на одну страницу
def page_queries(site, prefix):
    pq = collections.defaultdict(list)
    for r in p2[site]["rows"]:
        pq[r["keys"][1].replace(prefix, "")].append((r["keys"][0], r["impressions"], r["clicks"]))
    return pq
tkq, mpq = page_queries("sc-domain:techkio.ru", TK), page_queries("sc-domain:xn--80aa3agq.xn--p1ai", MP)
def cl(pq, path, n=10):
    qs = sorted(pq[path], key=lambda x: -x[1]); return {"n": len(qs), "top": [q for q, _, _ in qs[:n]]}
out["clusters"] = {"press": cl(tkq, "/guide/create-press"), "verstak": cl(tkq, "/guide/tacz-verstak"),
                   "korpus": cl(tkq, "/guide/create-andezitovyy-korpus"),
                   "futbol": cl(mpq, "/sektsii/futbol"), "edinoborstva": cl(mpq, "/sektsii/edinoborstva")}

# каннибализация: гайд и статья про верстак TaCZ
A, B = TK + "/guide/tacz-verstak", TK + "/blog/verstaki-tacz-kak-skraftit"
by = collections.defaultdict(dict)
for r in p2["sc-domain:techkio.ru"]["rows"]: by[r["keys"][0]][r["keys"][1]] = r
both = sorted([(q, p[A], p[B]) for q, p in by.items() if A in p and B in p], key=lambda x: -(x[1]["impressions"] + x[2]["impressions"]))
out["cannibal"] = {"shared": len(both),
    "guide": {"clicks": sum(x[1]["clicks"] for x in both), "impr": sum(x[1]["impressions"] for x in both)},
    "blog": {"clicks": sum(x[2]["clicks"] for x in both), "impr": sum(x[2]["impressions"] for x in both)},
    "rows": [(q, round(a["position"], 1), a["clicks"], round(b["position"], 1), b["clicks"]) for q, a, b in both[:6]]}

# запросы Вебмастера
def wm(key, n=12):
    qs = sorted(p2[key]["queries"], key=lambda q: -q["indicators"]["TOTAL_SHOWS"])
    return [(q["query_text"], int(q["indicators"]["TOTAL_SHOWS"]), int(q["indicators"]["TOTAL_CLICKS"]), round(q["indicators"]["AVG_SHOW_POSITION"], 1)) for q in qs[:n]]
out["wm_mapka"], out["wm_techkio"] = wm("wm:https:xn--80aa3agq.xn--p1ai:443"), wm("wm:https:techkio.ru:443")
tkwm = {q["query_text"]: q["indicators"] for q in p2["wm:https:techkio.ru:443"]["queries"]}
out["andesite"] = {q: (int(tkwm[q]["TOTAL_SHOWS"]), int(tkwm[q]["TOTAL_CLICKS"]), round(tkwm[q]["AVG_SHOW_POSITION"], 1))
                   for q in ["андезит майнкрафт", "андезитовый корпус create крафт"]}

# районы в запросах Мапки
# «центр» не считаем: в запросах это чаще «детский центр», а не район
D = {"северн": "Северный", "левенцов": "Левенцовка", "западн": "Западный", "сельмаш": "Сельмаш", "нахичеван": "Нахичевань",
     "александровк": "Александровка", "военвед": "Военвед", "чкаловск": "Чкаловский", "суворовск": "Суворовский"}
mq = p2["wm:https:xn--80aa3agq.xn--p1ai:443"]["queries"]; cnt = collections.Counter(); sh = collections.Counter(); hitq = 0; hits = 0
for q in mq:
    t, s, f = q["query_text"], q["indicators"]["TOTAL_SHOWS"], False
    for k, v in D.items():
        if k in t: cnt[v] += 1; sh[v] += s; f = True
    if f: hitq += 1; hits += s
tot = sum(q["indicators"]["TOTAL_SHOWS"] for q in mq)
out["districts"] = {"queries": hitq, "total": len(mq), "shows_share": round(100 * hits / tot),
                    "top": [(v, cnt[v], int(sh[v])) for v, _ in cnt.most_common(6)]}
bq = [q for q in mq if "бесплатн" in q["query_text"]]
M = next(v for v in mt.values() if v["site"] == "мапка.рф"); T = next(v for v in mt.values() if v["site"] == "techkio.ru")
ent_m = dict((r["dimensions"][0]["name"], int(r["metrics"][0])) for r in M["entry_organic30"]["data"])
ent_t = [(r["dimensions"][0]["name"], int(r["metrics"][0])) for r in T["entry_organic30"]["data"]][:8]
out["besplatno"] = {"queries": len(bq), "shows": int(sum(q["indicators"]["TOTAL_SHOWS"] for q in bq)),
                    "clicks": int(sum(q["indicators"]["TOTAL_CLICKS"] for q in bq)), "entries": ent_m.get("/sektsii/besplatnye", 0)}
out["entries_techkio"] = ent_t

# устройство Мапки по sitemap и Вебмастеру
y1 = json.load(open(SRC / "yandex.json"))["https:xn--80aa3agq.xn--p1ai:443"]["summary"]
dirs = ["angliyskiy", "edinoborstva", "futbol", "gimnastika", "muzyka", "plavanie", "risovanie", "tancy"]
dist9 = ["v-centre", "na-zapadnom", "na-severnom", "na-selmashe", "na-chkalovskom", "v-levencovke", "v-nahichevani", "v-aleksandrovke", "na-voenvede"]
districts = [s for s in sek["направление или другое"] if s.startswith(("v-", "na-", "u-"))] + sek["район"]
picks = [s for s in sek["направление или другое"] if s in ("besplatnye", "nedorogie", "s-probnym-zanyatiem", "dlya-malyshey")] + sek.get("особые", [])
combos = sek["направление × район"] + sek.get("направление × возраст", []) + [s for s in sek["направление или другое"] if s == "plavanie-u-gorizonta"]
allsek = sum(len(v) for v in sek.values())
out["mapka"] = {"sitemap": 417, "in_search": y1["searchable_pages_count"], "excluded": y1["excluded_pages_count"],
    "landings": allsek, "cats": len(sek["категория"]), "dirs": len(dirs), "districts": len(set(districts)),
    "ages": len(sek["возраст"]), "picks": len(set(picks)), "combos": len(combos), "blog": 9, "cards": 301,
    "matrix": {d: [f"{d}-{x}" in sek["направление × район"] for x in dist9] for d in dirs + ["doshkolniki"]},
    "matrix_cols": dist9, "angliyskiy_all": 85, "angliyskiy_severny": 17}

# подсказки Яндекса под учебный пример
sug = {}
for line in open(SRC / "suggest_demo.tsv", encoding="utf-8"):
    if "\t" in line:
        k, v = line.rstrip("\n").split("\t", 1); sug[k] = [x.strip() for x in v.split("|")]
out["suggest"] = sug
sn = {}
for line in open(SRC / "suggest_niches.tsv", encoding="utf-8"):
    if "\t" in line:
        k, v = line.rstrip("\n").split("\t", 1); sn[k] = [x.strip() for x in v.split("|")]
out["suggest_niches"] = sn
pathlib.Path(__file__).with_name("data.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps({k: out[k] for k in ["tail", "cannibal", "districts", "besplatno", "andesite"]}, ensure_ascii=False))
print("мапка:", {k: v for k, v in out["mapka"].items() if k not in ("matrix", "matrix_cols")})
print("кластеры:", {k: v["n"] for k, v in out["clusters"].items()})
