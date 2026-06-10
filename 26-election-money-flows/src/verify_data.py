"""Data-layer verification: spot checks against externally documented facts.

Checks (sources in lit_map.md):
 1. EEM saw heavy outflows in the weeks around the Nov 2016 election (EPFR notes).
 2. US equity funds saw inflows in the weeks after the 2016 result (reflation trade).
 3. Spring 2025: Europe equity inflows positive while US flows weak/negative (Sell America).
 4. Iraq 2003: SPX fell during the buildup, rallied after the outbreak (war puzzle).
 5. VIX fell from election day to the day after in 2016, 2020, 2024 (St. Louis Fed).
 6. Weekly flow magnitudes are sane (median abs < 2 pct of AUM).
 7. Latest EEM AUM in a plausible range (10-60 bn USD).
"""
import numpy as np
import pandas as pd

import event_study as ES
from config import DATA_DIR

PASS, FAIL = "PASS", "FAIL"
results = []


def check(name, ok, detail=""):
    results.append((PASS if ok else FAIL, name, detail))


def main():
    prices = ES.load_prices()
    funds = ES.load_fund_histories()
    spx = prices["idx_spx"]
    vix_f = DATA_DIR / "macro" / "vix_cboe.parquet"
    vix = pd.read_parquet(vix_f)["vix"] if vix_f.exists() else prices["idx_vix"]

    # 1. EEM flows around 2016 election
    eem = ES.weekly_flow_pct(funds["EEM"])
    w = eem.loc["2016-10-21":"2016-12-02"]
    check("EEM net outflow around Nov 2016 election", w.sum() < 0, f"sum={w.sum():.2f}% of AUM over {len(w)}w")

    # 2. US equity inflows after 2016 result
    us = ES.group_weekly_flow_pct(funds, {"US", "US_smallcap"})
    w2 = us.loc["2016-11-11":"2016-12-30"]
    check("US equity inflows post-2016 election", w2.sum() > 0, f"sum={w2.sum():.2f}%")

    # 3. 2025 rotation: Europe inflows Feb-Apr (German fiscal pivot), US outflows
    #    Apr-May after Liberation Day tariffs (Sell America).
    eu = ES.group_weekly_flow_pct(funds, {"Europe"})
    eu_rot = eu.loc["2025-02-01":"2025-04-30"].sum()
    us_tar = us.loc["2025-04-01":"2025-05-31"].sum()
    check("2025 rotation: Europe in (Feb-Apr), US out (Apr-May)", eu_rot > 0 and us_tar < 0,
          f"europe_feb_apr={eu_rot:.2f}% us_apr_may={us_tar:.2f}%")

    # 4. Iraq 2003 war puzzle on SPX
    pre = np.log(spx.asof("2003-03-11") / spx.asof("2002-09-12")) * 100
    post = np.log(spx.asof("2003-06-20") / spx.asof("2003-03-19")) * 100
    check("Iraq 2003: buildup down, outbreak up", pre < 0 and post > 0,
          f"buildup={pre:.1f}% post-outbreak={post:.1f}%")

    # 5. VIX drop day after recent elections
    drops = {}
    for d_el, d_after in [("2016-11-08", "2016-11-09"), ("2020-11-03", "2020-11-04"), ("2024-11-05", "2024-11-06")]:
        drops[d_el] = float(vix.asof(d_after) - vix.asof(d_el))
    check("VIX fell day after 2016/2020/2024 elections", all(v < 0 for v in drops.values()),
          " ".join(f"{k[:4]}:{v:+.1f}" for k, v in drops.items()))

    # 6. flow magnitude sanity
    med_abs = eem.abs().median()
    check("EEM weekly |flow| median < 2% AUM", med_abs < 2, f"median={med_abs:.2f}%")

    # 7. AUM sanity
    f = funds["EEM"].iloc[-1]
    aum_bn = f["nav"] * f["shares"] / 1e9
    check("EEM AUM plausible (10-60bn)", 10 < aum_bn < 60, f"aum={aum_bn:.1f}bn")

    width = max(len(n) for _, n, _ in results)
    nfail = 0
    for status, name, detail in results:
        print(f"{status}  {name:<{width}}  {detail}", flush=True)
        nfail += status == FAIL
    print(f"{len(results) - nfail}/{len(results)} checks passed", flush=True)
    raise SystemExit(1 if nfail else 0)


if __name__ == "__main__":
    main()
