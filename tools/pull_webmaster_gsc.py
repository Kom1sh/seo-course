import json, urllib.request, urllib.parse, base64, time, subprocess, os, sys, datetime, tempfile
OUT = os.environ.get("SEO_DUMP", os.path.dirname(os.path.abspath(__file__)))
def req(url, headers=None, data=None, method=None):
    r = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"__error__": e.code, "body": e.read().decode()[:600]}

today = datetime.date.today()
d_to = (today - datetime.timedelta(days=2)).isoformat()
d_from90 = (today - datetime.timedelta(days=92)).isoformat()
d_from30 = (today - datetime.timedelta(days=32)).isoformat()
d_from400 = (today - datetime.timedelta(days=400)).isoformat()

# ---------------- YANDEX ----------------
tok = open(os.path.expanduser("~/.claude/secrets/yandex-webmaster-token")).read().strip()
YH = {"Authorization": "OAuth " + tok}
Y = "https://api.webmaster.yandex.net/v4"
u = req(Y + "/user", YH); uid = u.get("user_id"); print("yandex user", uid)
hosts = req(f"{Y}/user/{uid}/hosts", YH)
ys = {}
for h in hosts.get("hosts", []):
    hid = h["host_id"]; print("host", hid, h.get("verified"), h.get("main_mirror"))
    if not h.get("verified"): continue
    base = f"{Y}/user/{uid}/hosts/{urllib.parse.quote(hid, safe='')}"
    d = {"host": h}
    d["summary"] = req(base + "/summary", YH)
    d["sitemaps"] = req(base + "/sitemaps", YH)
    d["history"] = req(base + f"/search-queries/all/history?query_indicator=TOTAL_SHOWS&query_indicator=TOTAL_CLICKS&query_indicator=AVG_SHOW_POSITION&date_from={d_from400}&date_to={d_to}", YH)
    d["popular30"] = req(base + f"/search-queries/popular?order_by=TOTAL_CLICKS&query_indicator=TOTAL_SHOWS&query_indicator=TOTAL_CLICKS&query_indicator=AVG_SHOW_POSITION&query_indicator=AVG_CLICK_POSITION&date_from={d_from30}&date_to={d_to}&limit=100", YH)
    d["popular_shows30"] = req(base + f"/search-queries/popular?order_by=TOTAL_SHOWS&query_indicator=TOTAL_SHOWS&query_indicator=TOTAL_CLICKS&query_indicator=AVG_SHOW_POSITION&date_from={d_from30}&date_to={d_to}&limit=100", YH)
    d["insearch_hist"] = req(base + f"/search-urls/in-search/history?date_from={d_from400}&date_to={d_to}", YH)
    d["indexing_hist"] = req(base + f"/indexing/history?date_from={d_from400}&date_to={d_to}", YH)
    d["diagnostics"] = req(base + "/diagnostics", YH)
    ys[hid] = d
json.dump(ys, open(os.path.join(OUT, "yandex.json"), "w"), ensure_ascii=False, indent=1)

# ---------------- GSC ----------------
sa = json.load(open(os.path.expanduser("~/.claude/secrets/gsc-service-account.json")))
def b64(b): return base64.urlsafe_b64encode(b).rstrip(b"=").decode()
now = int(time.time())
hdr = b64(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
claims = b64(json.dumps({"iss": sa["client_email"], "scope": "https://www.googleapis.com/auth/webmasters.readonly",
                          "aud": "https://oauth2.googleapis.com/token", "iat": now, "exp": now + 3600}).encode())
signing = f"{hdr}.{claims}".encode()
with tempfile.NamedTemporaryFile("w", delete=False, suffix=".pem") as kf:
    kf.write(sa["private_key"]); kp = kf.name
sig = subprocess.run(["openssl", "dgst", "-sha256", "-sign", kp], input=signing, capture_output=True, check=True).stdout
os.unlink(kp)
jwt = f"{hdr}.{claims}.{b64(sig)}"
tokr = req("https://oauth2.googleapis.com/token", {"Content-Type": "application/x-www-form-urlencoded"},
           urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt}).encode())
at = tokr.get("access_token"); print("gsc token ok" if at else tokr)
GH = {"Authorization": "Bearer " + at, "Content-Type": "application/json"}
G = "https://www.googleapis.com/webmasters/v3"
sites = req(G + "/sites", GH); print("gsc sites", [s["siteUrl"] for s in sites.get("siteEntry", [])])
gs = {}
for s in sites.get("siteEntry", []):
    su = s["siteUrl"]; base = G + "/sites/" + urllib.parse.quote(su, safe="") + "/searchAnalytics/query"
    def q(body): return req(base, GH, json.dumps(body).encode(), "POST")
    d = {"permission": s.get("permissionLevel")}
    d["daily"] = q({"startDate": d_from400, "endDate": d_to, "dimensions": ["date"], "rowLimit": 500})
    d["queries30"] = q({"startDate": d_from30, "endDate": d_to, "dimensions": ["query"], "rowLimit": 100})
    d["pages30"] = q({"startDate": d_from30, "endDate": d_to, "dimensions": ["page"], "rowLimit": 50})
    d["total30"] = q({"startDate": d_from30, "endDate": d_to, "rowLimit": 1})
    d["devices30"] = q({"startDate": d_from30, "endDate": d_to, "dimensions": ["device"], "rowLimit": 5})
    d["countries30"] = q({"startDate": d_from30, "endDate": d_to, "dimensions": ["country"], "rowLimit": 5})
    gs[su] = d
json.dump(gs, open(os.path.join(OUT, "gsc.json"), "w"), ensure_ascii=False, indent=1)

# ---------------- SUMMARY ----------------
print("\n========== YANDEX ==========")
for hid, d in ys.items():
    s = d["summary"]; print(f"\n{hid}: ИКС={s.get('sqi')} в поиске={s.get('searchable_pages_count')} исключено={s.get('excluded_pages_count')} проблем={s.get('site_problems')}")
    hist = d["history"].get("indicators", {})
    for k, v in hist.items():
        vals = [(x["date"][:10], x["value"]) for x in v]
        print(f"  {k}: {len(vals)} days, first={vals[:1]}, last={vals[-1:]}, sum={sum(x[1] for x in vals):.0f}")
    print("  sitemaps:", [(m.get('sitemap_url'), m.get('urls_count'), m.get('errors_count')) for m in d["sitemaps"].get("sitemaps", [])][:5])
    print("  top queries 30d by clicks:")
    for qq in d["popular30"].get("queries", [])[:15]:
        ind = qq["indicators"]; print(f"    {qq['query_text'][:50]:50s} shows={ind.get('TOTAL_SHOWS'):>6.0f} clicks={ind.get('TOTAL_CLICKS'):>4.0f} pos={ind.get('AVG_SHOW_POSITION'):.1f}")
    ins = d["insearch_hist"]; print("  insearch keys:", list(ins.keys())[:5], str(ins)[:300])
print("\n========== GSC ==========")
for su, d in gs.items():
    t = d["total30"].get("rows", [{}])[0]; print(f"\n{su}: 30d clicks={t.get('clicks')} impr={t.get('impressions')} ctr={t.get('ctr')} pos={t.get('position')}")
    rows = d["daily"].get("rows", []); print(f"  daily rows={len(rows)} first={rows[:1]} last={rows[-1:]}")
    print("  top queries:")
    for r in d["queries30"].get("rows", [])[:15]:
        print(f"    {r['keys'][0][:50]:50s} impr={r['impressions']:>6} clicks={r['clicks']:>4} pos={r['position']:.1f}")
    print("  top pages:", [(r['keys'][0], r['clicks']) for r in d["pages30"].get("rows", [])[:8]])
    print("  err?", {k: v for k, v in d.items() if isinstance(v, dict) and "__error__" in v})
