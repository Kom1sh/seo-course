"""Снимок живых данных (Метрика, Вебмастер, GSC) для сборки деки.
Читает выгрузки из $CLAUDE_JOB_DIR/tmp/seo/*.json и пишет src/data.json — сборка не требует секретов."""
import json, pathlib, collections, os
SRC = pathlib.Path(os.environ.get("SEO_DUMP", "/Users/egor/.claude/jobs/dc65153a/tmp/seo"))
y = json.load(open(SRC / "yandex.json")); g = json.load(open(SRC / "gsc.json")); m = json.load(open(SRC / "metrika.json"))
SITES = {"techkio": ("https:techkio.ru:443", "sc-domain:techkio.ru", "techkio.ru"),
         "mapka": ("https:xn--80aa3agq.xn--p1ai:443", "sc-domain:xn--80aa3agq.xn--p1ai", "мапка.рф")}
out = {"snapshot_date": "2026-09-05"}
for key, (yh, gh, ms) in SITES.items():
    Y = y[yh]; G = g[gh]; M = next(v for v in m.values() if v["site"] == ms)
    d = {}
    s = Y["summary"]; d["yandex_summary"] = {"sqi": s.get("sqi"), "in_search": s.get("searchable_pages_count"), "excluded": s.get("excluded_pages_count"),
                                              "sitemap_urls": sum(x.get("urls_count", 0) for x in Y["sitemaps"].get("sitemaps", []))}
    d["yandex_in_search_history"] = [(x["date"][:10], x["value"]) for x in Y["insearch_hist"]["history"]]
    ms_, mc_ = collections.OrderedDict(), collections.OrderedDict()
    for x in Y["history"]["indicators"]["TOTAL_SHOWS"]: ms_[x["date"][:7]] = ms_.get(x["date"][:7], 0) + x["value"]
    for x in Y["history"]["indicators"]["TOTAL_CLICKS"]: mc_[x["date"][:7]] = mc_.get(x["date"][:7], 0) + x["value"]
    d["yandex_monthly"] = [(k, int(ms_[k]), int(mc_.get(k, 0))) for k in ms_ if k >= "2025-12"]
    qs = {q["query_text"]: q["indicators"] for q in Y["popular_shows30"].get("queries", [])}
    qs.update({q["query_text"]: q["indicators"] for q in Y["popular30"].get("queries", [])})
    b = collections.OrderedDict([("1", [0, 0, 0]), ("2–3", [0, 0, 0]), ("4–10", [0, 0, 0]), ("11+", [0, 0, 0])])
    for q, i in qs.items():
        p = i.get("AVG_SHOW_POSITION") or 99
        k = "1" if p < 1.5 else "2–3" if p < 3.5 else "4–10" if p < 10.5 else "11+"
        b[k][0] += i.get("TOTAL_SHOWS", 0); b[k][1] += i.get("TOTAL_CLICKS", 0); b[k][2] += 1
    d["yandex_ctr_buckets"] = [(k, int(v[0]), int(v[1]), v[2], round(100 * v[1] / v[0], 1) if v[0] else 0) for k, v in b.items()]
    d["yandex_ctr_queries_n"] = len(qs)
    d["yandex_top_queries"] = [(q["query_text"], int(q["indicators"]["TOTAL_SHOWS"]), int(q["indicators"]["TOTAL_CLICKS"]), round(q["indicators"]["AVG_SHOW_POSITION"], 1))
                               for q in Y["popular30"].get("queries", [])[:12]]
    t = G["total30"]["rows"][0]; d["gsc_30d"] = {"clicks": t["clicks"], "impressions": t["impressions"], "ctr": round(100 * t["ctr"], 1), "position": round(t["position"], 1)}
    d["gsc_devices30"] = [(r["keys"][0], r["clicks"], r["impressions"]) for r in G["devices30"].get("rows", [])]
    mm = collections.OrderedDict()
    for r in G["daily"]["rows"]: k = r["keys"][0][:7]; mm.setdefault(k, [0, 0]); mm[k][0] += r["clicks"]; mm[k][1] += r["impressions"]
    d["gsc_monthly"] = [(k, v[0], v[1]) for k, v in mm.items()]
    d["gsc_top_queries"] = [(r["keys"][0], r["impressions"], r["clicks"], round(r["position"], 1)) for r in G["queries30"]["rows"][:12]]
    d["gsc_top_pages"] = [(r["keys"][0].replace("https://xn--80aa3agq.xn--p1ai", "мапка.рф").replace("https://techkio.ru", "techkio.ru"), r["clicks"], r["impressions"]) for r in G["pages30"]["rows"][:10]]
    ow = M["organic_weekly"]; d["metrika_organic_weekly"] = [(t[0], int(v)) for t, v in zip(ow["time_intervals"], ow["data"][0]["metrics"][0])]
    aw = M["all_weekly"]; d["metrika_all_weekly"] = [(t[0], int(v)) for t, v in zip(aw["time_intervals"], aw["data"][0]["metrics"][0])]
    rows = lambda k: M[k].get("data", [])
    d["metrika_sources30"] = [(r["dimensions"][0]["name"], int(r["metrics"][0]), int(r["metrics"][1])) for r in rows("sources30")]
    d["metrika_engines30"] = [(r["dimensions"][0]["name"], int(r["metrics"][0])) for r in rows("engines30")]
    d["metrika_devices30"] = [(r["dimensions"][0]["name"], int(r["metrics"][0])) for r in rows("devices30")]
    d["metrika_geo30"] = [(r["dimensions"][0]["name"], int(r["metrics"][0])) for r in rows("geo30")]
    d["metrika_entry_organic30"] = [(r["dimensions"][0]["name"], int(r["metrics"][0])) for r in rows("entry_organic30")][:10]
    d["metrika_phrases30"] = [(r["dimensions"][0]["name"], int(r["metrics"][0])) for r in rows("phrases30")][:12]
    d["metrika_counter_created"] = str(M.get("create_time", ""))[:10]
    out[key] = d
pathlib.Path(__file__).with_name("data.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for k in SITES: print(k, {kk: (vv if not isinstance(vv, list) else f"list[{len(vv)}]") for kk, vv in out[k].items() if kk in ("yandex_summary", "gsc_30d", "yandex_ctr_buckets", "metrika_engines30", "metrika_devices30", "gsc_devices30")})
