#!/usr/bin/env python3
"""Study 29, Chapter 1 — peer crowding-out around sector-leader listings.

For each leader listing, measure the equal-weight peer basket's return net of
the S&P 500 in four windows around the leader's first trading day:
  W1 allocation window  [-30, -1]   investors raise cash / make room
  W2 listing window     [ 0, +5]
  W3 digestion          [+6, +60]
  W4 lockup band        [+121, +190]

Peer prices: macrotrends daily closes (split-adjusted). Benchmark: S&P 500.
Output: ch1_results.json, ch1_peer_windows.csv, fig1 heatmap.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).parent
DATA = HERE / "data"

CREAM, INK, GREY, ACCENT = "#faf8f3", "#1c1a17", "#7a8a78", "#9c3d2e"
plt.rcParams.update({
    "figure.facecolor": CREAM, "axes.facecolor": CREAM, "savefig.facecolor": CREAM,
    "text.color": INK, "axes.edgecolor": INK, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK, "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
})

EVENTS = [
    ("FB",   "Facebook",  "2012-05-18", ["GOOG", "GRPN", "YELP"]),
    ("BABA", "Alibaba",   "2014-09-19", ["AMZN", "EBAY", "JD"]),
    ("UBER", "Uber",      "2019-05-10", ["LYFT"]),
    ("SNOW", "Snowflake", "2020-09-16", ["DDOG", "MDB", "NET", "WDAY"]),
    ("DASH", "DoorDash",  "2020-12-09", ["UBER_pr", "LYFT"]),
    ("ABNB", "Airbnb",    "2020-12-10", ["BKNG", "EXPE", "MAR"]),
    ("COIN", "Coinbase",  "2021-04-14", ["MSTR", "MARA", "RIOT"]),
    ("RIVN", "Rivian",    "2021-11-10", ["TSLA", "LCID", "F", "GM", "NIO", "XPEV"]),
    ("ARM",  "ARM",       "2023-09-14", ["NVDA", "AMD", "INTC", "QCOM", "AVGO", "TXN"]),
    ("SPCX", "SpaceX",    "2026-06-12", ["RKLB", "ASTS", "IRDM", "LUNR", "RDW", "PL", "SPCE", "TSLA"]),
]
WINDOWS = {"W1_alloc_-30_-1": (-30, -1), "W2_listing_0_+5": (0, 5),
           "W3_digest_+6_+60": (6, 60), "W4_lockup_+121_+190": (121, 190)}


def load(name: str, folder: str = "peers") -> pd.Series:
    f = DATA / folder / f"{name}.csv" if folder else DATA / f"{name}.csv"
    df = pd.read_csv(f, parse_dates=["date"])
    s = df.set_index("date")["close"].astype(float).sort_index()
    return s[~s.index.duplicated()]


def window_return(s: pd.Series, anchor_i: int, lo: int, hi: int) -> float:
    i0, i1 = anchor_i + lo, anchor_i + hi
    if i0 - 1 < 0 or i1 >= len(s):
        return np.nan
    return s.iloc[i1] / s.iloc[i0 - 1] - 1


def main() -> None:
    spx = load("sp500", folder=None)
    # UBER appears both as a leader and as a DASH peer
    peer_cache = {}

    rows = []
    for lead, name, date_s, peers in EVENTS:
        d = pd.Timestamp(date_s)
        for p in peers:
            fname = p.replace("_pr", "")
            if fname not in peer_cache:
                src = DATA / "peers" / f"{fname}.csv"
                if not src.exists():
                    src2 = Path(__file__).parent.parent / "28-spacex-vs-trump-coin" / "data" / "megastocks" / f"{fname}.csv"
                    peer_cache[fname] = pd.read_csv(src2, parse_dates=["date"]).set_index("date")["close"].astype(float).sort_index()
                else:
                    peer_cache[fname] = load(fname)
            s = peer_cache[fname]
            i = s.index.searchsorted(d, side="right") - 1
            ispx = spx.index.searchsorted(d, side="right") - 1
            # peers with short pre-listing history (e.g. LYFT before Uber)
            # contribute only the windows their data covers
            if i < 0:
                continue
            row = {"event": name, "leader": lead, "peer": fname}
            for wname, (lo, hi) in WINDOWS.items():
                pr = window_return(s, i, lo, hi)
                br = window_return(spx, ispx, lo, hi)
                row[wname] = round((pr - br) * 100, 2) if np.isfinite(pr) and np.isfinite(br) else np.nan
            rows.append(row)

    t = pd.DataFrame(rows)
    t.to_csv(HERE / "ch1_peer_windows.csv", index=False)

    # per-event basket = mean across peers; summary = median across events
    basket = t.groupby("event")[list(WINDOWS)].mean().round(2)
    # keep event order
    basket = basket.reindex([e[1] for e in EVENTS])
    summary = {}
    hist = basket.drop(index="SpaceX", errors="ignore")
    for w in WINDOWS:
        v = hist[w].dropna()
        summary[w] = {
            "median_pct": round(float(v.median()), 2),
            "mean_pct": round(float(v.mean()), 2),
            "pct_negative": round(float((v < 0).mean()) * 100, 1),
            "n_events": int(len(v)),
        }
    out = {"per_event_basket_excess_pct": json.loads(basket.to_json(orient="index")),
           "summary_across_events_ex_spacex": summary}

    # BTC during the Coinbase windows (the crypto host-asset read)
    btc = load("BTC_2020_2021", folder=None)
    i = btc.index.searchsorted(pd.Timestamp("2021-04-14"), side="right") - 1
    out["btc_around_coinbase"] = {
        w: round(window_return(btc, i, lo, hi) * 100, 2) for w, (lo, hi) in WINDOWS.items() if i + hi < len(btc)}

    (HERE / "ch1_results.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=2))

    # Fig — heatmap of per-event basket excess by window
    fig, ax = plt.subplots(figsize=(9, 5.2))
    M = basket[list(WINDOWS)].values.astype(float)
    vmax = np.nanmax(np.abs(M))
    im = ax.imshow(M, cmap="RdGy_r", vmin=-vmax, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(WINDOWS)))
    ax.set_xticklabels(["allocation\n[-30,-1]", "listing\n[0,+5]", "digestion\n[+6,+60]", "lockup band\n[+121,+190]"], fontsize=8.5)
    ax.set_yticks(range(len(basket)))
    ax.set_yticklabels([f"{n} ({d[:4]})" for _, n, d, _ in EVENTS], fontsize=9)
    for yi in range(M.shape[0]):
        for xi in range(M.shape[1]):
            if np.isfinite(M[yi, xi]):
                ax.text(xi, yi, f"{M[yi, xi]:+.1f}", ha="center", va="center", fontsize=8,
                        color="white" if abs(M[yi, xi]) > vmax * 0.5 else INK)
    ax.set_title("Peer-basket return net of S&P 500 around sector-leader listings (%)",
                 loc="left", fontsize=11.5)
    fig.colorbar(im, ax=ax, shrink=0.8, label="excess %")
    fig.tight_layout()
    fig.savefig(HERE / "fig1_peer_crowding_heatmap.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    main()
