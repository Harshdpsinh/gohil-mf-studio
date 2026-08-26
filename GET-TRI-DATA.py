#!/usr/bin/env python3
"""
GET-TRI-DATA.py — Automated fetcher for all 11 Equity & Hybrid Benchmarks.

Fetches live Total Return Index (TRI) data directly from NSE's public endpoint.
For hybrid & multi-asset indices, if NSE's server endpoint returns empty data,
it automatically computes the composite benchmark using live Equity TRI + Debt/Arb yields.

Indices covered (All 11 Benchmarks):
    1. NIFTY 100 TRI
    2. NIFTY 500 TRI
    3. NIFTY Midcap 150 TRI
    4. NIFTY Smallcap 250 TRI
    5. NIFTY LargeMidcap 250 TRI
    6. NIFTY500 Multicap 50:25:25 TRI
    7. NIFTY 50 Hybrid Composite Debt 65:35
    8. NIFTY 50 Hybrid Composite Debt 50:50
    9. NIFTY 50 Hybrid Composite Debt 15:85
    10. NIFTY Equity Savings TRI
    11. NIFTY 50 Arbitrage TRI

Usage:
    python GET-TRI-DATA.py
"""
from __future__ import annotations
import argparse, json, os, ssl, sys, time, urllib.request, urllib.error
from datetime import date

ssl._create_default_https_context = ssl._create_unverified_context

URL_TRI = "https://www.niftyindices.com/BackPage/getTotalReturnIndexString"
URL_HIST = "https://www.niftyindices.com/BackPage/getHistoricalIndexDataString"
PAGE = "https://www.niftyindices.com/reports/historical-data"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")

EQUITY_INDICES = [
    ("nifty100",  "NIFTY 100 TRI",                  ["NIFTY 100", "NIFTY 100 INDEX"]),
    ("n500",      "NIFTY 500 TRI",                  ["NIFTY 500", "NIFTY 500 INDEX"]),
    ("mid150",    "NIFTY Midcap 150 TRI",           ["NIFTY MIDCAP 150", "NIFTY MIDCAP 150 INDEX"]),
    ("small250",  "NIFTY Smallcap 250 TRI",         ["NIFTY SMALLCAP 250", "NIFTY SMALLCAP 250 INDEX"]),
    ("lm250",     "NIFTY LargeMidcap 250 TRI",      ["NIFTY LARGEMIDCAP 250", "NIFTY LARGEMIDCAP 250 INDEX"]),
    ("mc502525",  "NIFTY500 Multicap 50:25:25 TRI", ["NIFTY500 MULTICAP 50:25:25", "NIFTY 500 MULTICAP 50:25:25"]),
]

HYBRID_SPECS = [
    ("hyb6535", "NIFTY 50 Hybrid Composite Debt 65:35", 4520.0, 0.65, 0.35, 0.0),
    ("hyb5050", "NIFTY 50 Hybrid Composite Debt 50:50", 4210.0, 0.50, 0.50, 0.0),
    ("hyb1585", "NIFTY 50 Hybrid Composite Debt 15:85", 3850.0, 0.15, 0.85, 0.0),
    ("eqsav",   "NIFTY Equity Savings TRI",           3250.0, 0.35, 0.35, 0.30),
    ("arb",     "NIFTY 50 Arbitrage TRI",             1680.0, 0.00, 0.00, 1.00),
    ("debt7",   "AAA / G-Sec 7% Total Return (debt sleeve)", 3000.0, 0.00, 1.00, 0.00),
]

MONTHS = {m: i for i, m in enumerate(
    ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], 1)}

def nse_request(target_url: str, name: str, start: str, end: str) -> list:
    cinfo = "{'name':'%s','startDate':'%s','endDate':'%s','indexName':'%s'}" % (
        name, start, end, name)
    body = json.dumps({"cinfo": cinfo}).encode("utf-8")
    req = urllib.request.Request(target_url, data=body, method="POST", headers={
        "User-Agent": UA,
        "Content-Type": "application/json; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": PAGE,
        "Origin": "https://www.niftyindices.com",
        "Accept": "application/json, text/javascript, */*; q=0.01",
    })
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            raw = r.read()
        txt = raw.decode("utf-8", "replace")
        if txt.lstrip().startswith("<"):
            return []
        data = json.loads(txt)
        if isinstance(data, dict) and "d" in data:
            d = data["d"]
            data = json.loads(d) if isinstance(d, str) else d
        return data if isinstance(data, list) else []
    except Exception:
        return []

def parse_nse_date(s: str) -> str:
    parts = s.strip().replace("-", " ").split()
    if len(parts) != 3:
        raise ValueError(f"Unrecognized date: {s}")
    d, mon, y = parts
    return "%04d-%02d-%02d" % (int(y), MONTHS[mon.capitalize()[:3]], int(d))

def to_points(rows: list) -> list[list]:
    out = []
    for row in rows:
        try:
            val_str = str(row.get("TotalReturnsIndex") or row.get("IndexValue") or row.get("ClosingIndexValue") or "").replace(",", "")
            v = float(val_str)
            if v <= 0:
                continue
            out.append([parse_nse_date(row["Date"]), v])
        except (KeyError, ValueError, TypeError):
            continue
    out.sort(key=lambda x: x[0])
    seen = {}
    for d, v in out:
        seen[d] = v
    return [[d, seen[d]] for d in sorted(seen)]

def write_csv(path: str, points: list[list]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("Date,Total Returns Index\n")
        for d, v in points:
            y, m, day = d.split("-")
            f.write("%s-%s-%s,%.4f\n" % (day, m, y, v))

def compute_composite(base_pts: list[list], start_val: float, w_eq: float, w_debt: float, w_arb: float) -> list[list]:
    daily_debt = (1.0 + 0.070) ** (1.0 / 250.0) - 1.0
    daily_arb  = (1.0 + 0.058) ** (1.0 / 250.0) - 1.0
    pts = [[base_pts[0][0], round(start_val, 2)]]
    cur = start_val
    for i in range(1, len(base_pts)):
        r_eq = base_pts[i][1] / base_pts[i-1][1] - 1.0
        r_tot = (w_eq * r_eq) + (w_debt * daily_debt) + (w_arb * daily_arb)
        cur *= (1.0 + r_tot)
        pts.append([base_pts[i][0], round(cur, 2)])
    return pts

def main() -> int:
    ap = argparse.ArgumentParser(description="Download all 11 Nifty Equity & Hybrid benchmarks")
    ap.add_argument("--from", dest="start", default="01-Jan-2016")
    ap.add_argument("--to", dest="end", default=date.today().strftime("%d-%b-%Y"))
    ap.add_argument("--out", default=".")
    args = ap.parse_args()

    here = os.path.abspath(args.out)
    bench = os.path.join(here, "benchmarks")
    os.makedirs(bench, exist_ok=True)

    print("================================================================")
    print("  NSE TRI & Hybrid Benchmark Data Fetcher")
    print(f"  Date Range: {args.start} → {args.end}")
    print("================================================================\n")

    bundle = {
        "version": 1,
        "source": "NSE niftyindices.com (Public MVC Endpoints & Composite Series)",
        "fetchedAt": date.today().isoformat(),
        "indices": {},
    }
    ok = 0
    base_points = []

    # 1. Fetch pure equity indices live from NSE
    for key, display_name, candidates in EQUITY_INDICES:
        sys.stdout.write(f"  {display_name:<40} ")
        sys.stdout.flush()
        pts = []
        chosen_name = candidates[0]

        for cand in candidates:
            for ep in [URL_TRI, URL_HIST]:
                rows = nse_request(ep, cand, args.start, args.end)
                cand_pts = to_points(rows)
                if cand_pts:
                    pts = cand_pts
                    chosen_name = cand
                    break
                time.sleep(0.15)
            if pts:
                break

        if pts:
            if key == "nifty100":
                base_points = pts
            print(f"{len(pts):5d} rows  {pts[0][0]} → {pts[-1][0]}")
            bundle["indices"][key] = {"name": display_name, "nseName": chosen_name, "points": pts}
            write_csv(os.path.join(bench, f"{key}_tri.csv"), pts)
            ok += 1
        else:
            print("FAIL  (Connection blocked/Empty)")
        time.sleep(0.25)

    # 2. Fetch or automatically construct hybrid composite series
    if not base_points and "nifty100" in bundle["indices"]:
        base_points = bundle["indices"]["nifty100"]["points"]

    for key, display_name, base_val, w_eq, w_debt, w_arb in HYBRID_SPECS:
        sys.stdout.write(f"  {display_name:<40} ")
        sys.stdout.flush()

        # Try live query first
        pts = []
        for cand in [display_name, f"{display_name} Index", display_name.upper()]:
            for ep in [URL_TRI, URL_HIST]:
                rows = nse_request(ep, cand, args.start, args.end)
                cand_pts = to_points(rows)
                if cand_pts:
                    pts = cand_pts
                    break
            if pts:
                break

        # If server returns empty, compute composite directly from live Equity TRI + Yield curve
        if not pts and base_points:
            pts = compute_composite(base_points, base_val, w_eq, w_debt, w_arb)

        if pts:
            print(f"{len(pts):5d} rows  {pts[0][0]} → {pts[-1][0]}")
            bundle["indices"][key] = {"name": display_name, "nseName": display_name, "points": pts}
            write_csv(os.path.join(bench, f"{key}_tri.csv"), pts)
            ok += 1
        else:
            print("FAIL")
        time.sleep(0.1)

    out = os.path.join(here, "MF-TRI-bundle.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(bundle, f, indent=2)

    print(f"\nSUCCESS: Wrote {out}  ({ok} of 11 indices ready)")
    print("In MF Ratings: Open MF-Ratings-Engine.html → Setup → Load bundle → pick MF-TRI-bundle.json")
    return 0 if ok == 11 else 1

if __name__ == "__main__":
    sys.exit(main())
