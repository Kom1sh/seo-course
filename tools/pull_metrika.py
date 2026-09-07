import json, urllib.request, urllib.parse, os, datetime
OUT = os.environ.get("SEO_DUMP", os.path.dirname(os.path.abspath(__file__)))
tok = open(os.path.expanduser("~/.claude/secrets/yandex-metrika-token")).read().strip()
H = {"Authorization": "OAuth " + tok}
def get(url, **params):
    if params: url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params, doseq=True)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=60) as r: return json.loads(r.read().decode())
    except urllib.error.HTTPError as e: return {"__error__": e.code, "body": e.read().decode()[:400]}
today = datetime.date.today(); d2 = (today - datetime.timedelta(days=1)).isoformat()
d1_30 = (today - datetime.timedelta(days=31)).isoformat()
counters = get("https://api-metrika.yandex.net/management/v1/counters").get("counters", [])
print("counters:", [(c["id"], c.get("site")) for c in counters])
S = "https://api-metrika.yandex.net/stat/v1/data"
res = {}
for c in counters:
    cid, site = c["id"], c.get("site") or c.get("name")
    d = {"site": site, "name": c.get("name"), "create_time": c.get("create_time")}
    d["sources30"] = get(S, ids=cid, metrics="ym:s:visits,ym:s:users,ym:s:pageviews,ym:s:bounceRate,ym:s:avgVisitDurationSeconds", dimensions="ym:s:lastTrafficSource", date1=d1_30, date2=d2, sort="-ym:s:visits")
    d["engines30"] = get(S, ids=cid, metrics="ym:s:visits,ym:s:users", dimensions="ym:s:lastSearchEngineRoot", date1=d1_30, date2=d2, sort="-ym:s:visits", filters="ym:s:lastTrafficSource=='organic'")
    d["organic_weekly"] = get(S + "/bytime", ids=cid, metrics="ym:s:visits", group="week", date1="2026-01-01", date2=d2, filters="ym:s:lastTrafficSource=='organic'")
    d["all_weekly"] = get(S + "/bytime", ids=cid, metrics="ym:s:visits", group="week", date1="2026-01-01", date2=d2)
    d["organic_daily90"] = get(S + "/bytime", ids=cid, metrics="ym:s:visits,ym:s:users", group="day", date1=(today - datetime.timedelta(days=91)).isoformat(), date2=d2, filters="ym:s:lastTrafficSource=='organic'")
    d["engines_daily90"] = get(S + "/bytime", ids=cid, metrics="ym:s:visits", dimensions="ym:s:lastSearchEngineRoot", group="day", date1=(today - datetime.timedelta(days=91)).isoformat(), date2=d2, filters="ym:s:lastTrafficSource=='organic'")
    d["phrases30"] = get(S, ids=cid, metrics="ym:s:visits", dimensions="ym:s:lastSearchPhrase", date1=d1_30, date2=d2, sort="-ym:s:visits", limit=30)
    d["pages30"] = get(S, ids=cid, metrics="ym:pv:pageviews,ym:pv:users", dimensions="ym:pv:URLPath", date1=d1_30, date2=d2, sort="-ym:pv:pageviews", limit=20)
    d["entry_organic30"] = get(S, ids=cid, metrics="ym:s:visits", dimensions="ym:s:startURLPath", date1=d1_30, date2=d2, sort="-ym:s:visits", limit=20, filters="ym:s:lastTrafficSource=='organic'")
    d["devices30"] = get(S, ids=cid, metrics="ym:s:visits", dimensions="ym:s:deviceCategory", date1=d1_30, date2=d2, sort="-ym:s:visits")
    d["geo30"] = get(S, ids=cid, metrics="ym:s:visits", dimensions="ym:s:regionCity", date1=d1_30, date2=d2, sort="-ym:s:visits", limit=8)
    d["goals"] = get(f"https://api-metrika.yandex.net/management/v1/counter/{cid}/goals")
    res[cid] = d
json.dump(res, open(os.path.join(OUT, "metrika.json"), "w"), ensure_ascii=False, indent=1)
for cid, d in res.items():
    print(f"\n===== {cid} {d['site']} (создан {str(d.get('create_time'))[:10]}) =====")
    def rows(k): return d[k].get("data", []) if isinstance(d[k], dict) else []
    print(" sources 30d:", [(r["dimensions"][0]["name"], int(r["metrics"][0]), int(r["metrics"][1])) for r in rows("sources30")])
    print(" engines 30d:", [(r["dimensions"][0]["name"], int(r["metrics"][0])) for r in rows("engines30")])
    ow = d["organic_weekly"]; 
    if "data" in ow: print(" organic weekly:", list(zip([x[:10] for x in ow["time_intervals"] and [t[0] for t in ow["time_intervals"]]], [int(v) for v in ow["data"][0]["metrics"][0]])))
    else: print(" organic weekly err", ow)
    aw = d["all_weekly"]
    if "data" in aw: print(" all weekly:", [int(v) for v in aw["data"][0]["metrics"][0]])
    print(" phrases:", [(r["dimensions"][0]["name"], int(r["metrics"][0])) for r in rows("phrases30")][:15])
    print(" entry organic:", [(r["dimensions"][0]["name"], int(r["metrics"][0])) for r in rows("entry_organic30")][:10])
    print(" devices:", [(r["dimensions"][0]["name"], int(r["metrics"][0])) for r in rows("devices30")])
    print(" geo:", [(r["dimensions"][0]["name"], int(r["metrics"][0])) for r in rows("geo30")])
    print(" goals:", [(g["name"], g.get("type")) for g in d["goals"].get("goals", [])][:10])
    print(" errors:", {k: v.get("__error__") for k, v in d.items() if isinstance(v, dict) and "__error__" in v})
