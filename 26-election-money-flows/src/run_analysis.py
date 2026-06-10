"""Compute all derived datasets for the election money-flow study.

Outputs (derived/):
  returns_paths.parquet   event_class, anchor, event, series, rel_day, value (cum log ret, pct)
  flows_caf_paths.parquet event_class, event, bucket, rel_week, value (cum flow, pct of AUM)
  vix_paths.parquet       event_class, event, rel_day, value (VIX level)
  event_summary.csv       per event x series horizons
  cohort_summary.csv      cohort x series x horizon medians + hit rates
  admin_regimes.csv       per administration return/vol stats
  cycle_seasonal.csv      presidential-cycle-year average SPX path (since 1950)
  rotation_paths.parquet  US-minus-ROW weekly flow differential CAF around events
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from config import BUCKETS, DATA_DIR, DERIVED_DIR, ETF_PANEL
import events as EV
import event_study as ES

PRE_D, POST_D = 120, 120
PRE_W, POST_W = 26, 26

BUCKET_SHOW = ["US", "EM", "China", "Taiwan", "Korea", "Japan", "AsiaExJapan",
               "India", "Europe", "Bonds", "Gold", "Cash", "Credit", "US_smallcap"]


def bucket_members(bucket: str) -> list[str]:
    return [e["ticker"] for e in ETF_PANEL if e["bucket"] == bucket]


def composite_return_path(prices: pd.DataFrame, tickers: list[str], date,
                          pre=PRE_D, post=POST_D) -> pd.Series | None:
    paths = []
    for t in tickers:
        if t in prices.columns:
            p = ES.daily_path(prices[t], date, pre, post)
            if p is not None:
                paths.append(p)
    if not paths:
        return None
    return pd.concat(paths, axis=1).mean(axis=1)


def main():
    prices = ES.load_prices()
    funds = ES.load_fund_histories()
    vix_file = DATA_DIR / "macro" / "vix_cboe.parquet"
    if vix_file.exists():
        vix = pd.read_parquet(vix_file)["vix"]
    else:
        vix = prices["idx_vix"]
    spx = prices["idx_spx"]

    # weekly flow pct per bucket
    bucket_flow_pct = {}
    for b in BUCKET_SHOW:
        s = ES.group_weekly_flow_pct(funds, {b})
        if len(s):
            bucket_flow_pct[b] = s
    rotation = ES.us_minus_row_weekly(funds)

    # ---------------- event registry ----------------
    pres = EV.presidential_df()
    mids = EV.midterms_df()
    wars = EV.wars_df()
    tars = EV.tariffs_df()

    jobs = []  # (event_class, anchor, label, date, meta)
    for _, e in pres.iterrows():
        y = e["date"].year
        jobs.append(("presidential", "vote", f"{y} {e['winner']}", e["date"], e))
        jobs.append(("presidential", "known", f"{y} {e['winner']}", e["result_known"], e))
    for _, e in mids.iterrows():
        jobs.append(("midterm", "vote", f"{e['date'].year} midterm", e["date"], e))
    for _, e in wars.iterrows():
        jobs.append(("war", "outbreak", f"{e['t0'].year} {e['name']}", e["t0"], e))
        if pd.notna(e["buildup"]):
            jobs.append(("war", "buildup", f"{e['t0'].year} {e['name']}", e["buildup"], e))
    for _, e in tars.iterrows():
        jobs.append(("tariff", "announce", f"{e['t0'].date()} {e['name']}", e["t0"], e))

    # ---------------- returns + vix paths ----------------
    ret_rows, vix_rows, flow_rows, rot_rows, summary_rows = [], [], [], [], []
    for cls, anchor, label, date, meta in jobs:
        series_map = {"SPX": ES.daily_path(spx, date, PRE_D, POST_D)}
        for b in BUCKET_SHOW:
            series_map[b] = composite_return_path(prices, bucket_members(b), date)
        us = series_map.get("US")
        for name, path in series_map.items():
            if path is None:
                continue
            for rd, v in path.items():
                ret_rows.append((cls, anchor, label, name, int(rd), float(v)))
            # relative-to-US rotation in return space
            if name not in ("SPX", "US") and us is not None:
                rel = (path - us).dropna()
                for rd, v in rel.items():
                    ret_rows.append((cls, anchor, label, f"{name}_minus_US", int(rd), float(v)))
        vp = ES.level_path(vix, date, PRE_D, POST_D)
        if vp is not None:
            for rd, v in vp.items():
                vix_rows.append((cls, anchor, label, int(rd), float(v)))

        if anchor in ("vote", "outbreak", "announce"):
            for b, s in bucket_flow_pct.items():
                cp = ES.weekly_caf_path(s, date, PRE_W, POST_W)
                if cp is None:
                    continue
                for rw, v in cp.items():
                    flow_rows.append((cls, label, b, int(rw), float(v)))
            rp = ES.weekly_caf_path(rotation, date, PRE_W, POST_W)
            if rp is not None:
                for rw, v in rp.items():
                    rot_rows.append((cls, label, int(rw), float(v)))

        # summary stats
        for name, path in series_map.items():
            if path is None:
                continue
            def at(h):
                return float(path.loc[h]) if h in path.index else np.nan
            summary_rows.append(dict(
                event_class=cls, anchor=anchor, event=label, series=name,
                pre60=-at(-60), pre20=-at(-20), post20=at(20), post60=at(60), post120=at(120),
            ))
        if vp is not None and 1 in vp.index and -1 in vp.index:
            summary_rows.append(dict(
                event_class=cls, anchor=anchor, event=label, series="VIX",
                pre60=float(vp.loc[-60]) if -60 in vp.index else np.nan,
                pre20=float(vp.loc[-20]) if -20 in vp.index else np.nan,
                post20=float(vp.loc[1] - vp.loc[-1]),   # 1-day resolution change
                post60=float(vp.loc[20] - vp.loc[-1]) if 20 in vp.index else np.nan,
                post120=np.nan,
            ))

    ret = pd.DataFrame(ret_rows, columns=["event_class", "anchor", "event", "series", "rel_day", "value"])
    ret.to_parquet(DERIVED_DIR / "returns_paths.parquet", index=False)
    pd.DataFrame(vix_rows, columns=["event_class", "anchor", "event", "rel_day", "value"]).to_parquet(
        DERIVED_DIR / "vix_paths.parquet", index=False)
    pd.DataFrame(flow_rows, columns=["event_class", "event", "bucket", "rel_week", "value"]).to_parquet(
        DERIVED_DIR / "flows_caf_paths.parquet", index=False)
    pd.DataFrame(rot_rows, columns=["event_class", "event", "rel_week", "value"]).to_parquet(
        DERIVED_DIR / "rotation_paths.parquet", index=False)
    pd.DataFrame(summary_rows).to_csv(DERIVED_DIR / "event_summary.csv", index=False)

    # ---------------- cohorts ----------------
    pres_events = {f"{e['date'].year} {e['winner']}": e for _, e in pres.iterrows()}
    cohorts = {
        "pres_all": list(pres_events),
        "pres_flip": [k for k, e in pres_events.items() if e["flip"]],
        "pres_hold": [k for k, e in pres_events.items() if not e["flip"]],
        "pres_R_win": [k for k, e in pres_events.items() if e["party"] == "R"],
        "pres_D_win": [k for k, e in pres_events.items() if e["party"] == "D"],
        "pres_surprise": [k for k, e in pres_events.items() if e["surprise"]],
        "pres_trump": [k for k in pres_events if "Trump" in k],
        "midterm_all": [f"{e['date'].year} midterm" for _, e in mids.iterrows()],
        "midterm_flip": [f"{e['date'].year} midterm" for _, e in mids.iterrows() if e["any_flip"]],
        "war_telegraphed": [f"{e['t0'].year} {e['name']}" for _, e in wars.iterrows() if e["telegraphed"]],
        "war_surprise": [f"{e['t0'].year} {e['name']}" for _, e in wars.iterrows() if not e["telegraphed"]],
    }
    coh_rows = []
    for coh, evlist in cohorts.items():
        cls = "presidential" if coh.startswith("pres") else ("midterm" if coh.startswith("mid") else "war")
        anchor = "vote" if cls in ("presidential", "midterm") else "outbreak"
        for series in ["SPX", "US", "EM", "China", "Europe", "Japan", "Taiwan", "Bonds", "Gold",
                       "EM_minus_US", "China_minus_US", "Europe_minus_US"]:
            sub = ret[(ret.event_class == cls) & (ret.anchor == anchor) &
                      (ret.series == series) & (ret.event.isin(evlist))]
            if sub.empty:
                continue
            stacked = sub.pivot_table(index="rel_day", columns="event", values="value")
            summ = ES.cohort_summary(stacked)
            for _, r in summ.iterrows():
                coh_rows.append(dict(cohort=coh, series=series, **r.to_dict()))
        # flows cohorts
        for b in ["US", "EM", "China", "Europe", "Bonds", "Gold", "Cash"]:
            subf = pd.DataFrame(flow_rows, columns=["event_class", "event", "bucket", "rel_week", "value"])
            subf = subf[(subf.event_class == cls) & (subf.bucket == b) & (subf.event.isin(evlist))]
            if subf.empty:
                continue
            stacked = subf.pivot_table(index="rel_week", columns="event", values="value")
            summ = ES.cohort_summary(stacked, horizons=(4, 13, 26))
            for _, r in summ.iterrows():
                coh_rows.append(dict(cohort=coh, series=f"flow_{b}", **r.to_dict()))
    pd.DataFrame(coh_rows).to_csv(DERIVED_DIR / "cohort_summary.csv", index=False)

    # ---------------- regimes + seasonality ----------------
    admins = EV.admins_df()
    ES.admin_regime_table(spx, vix, admins).to_csv(DERIVED_DIR / "admin_regimes.csv", index=False)

    r = np.log(spx / spx.shift(1)).dropna()
    r = r[r.index >= "1950-01-01"]
    election_years = set(range(1952, 2028, 4))
    def term_year(y):
        for ey in election_years:
            if y in (ey + 1, ey + 2, ey + 3, ey + 4):
                return {ey + 1: 1, ey + 2: 2, ey + 3: 3, ey + 4: 4}[y]
        return np.nan
    df = pd.DataFrame({"ret": r})
    df["year"] = df.index.year
    df["tyear"] = df["year"].map(term_year)
    df["doy_rank"] = df.groupby("year").cumcount()
    seas = (df.groupby(["tyear", "doy_rank"])["ret"].mean().groupby(level=0).cumsum() * 100)
    seas = seas.reset_index().rename(columns={"ret": "cum_ret_pct"})
    seas.to_csv(DERIVED_DIR / "cycle_seasonal.csv", index=False)

    print("derived datasets written:", flush=True)
    for p in sorted(DERIVED_DIR.iterdir()):
        print("  ", p.name, f"{p.stat().st_size/1e3:.0f}KB", flush=True)


if __name__ == "__main__":
    main()
