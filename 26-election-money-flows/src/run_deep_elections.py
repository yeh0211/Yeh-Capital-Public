"""Chapter 7: every president and every election since 1928, normalized.

Outputs
  derived/president_regimes.csv     name, party, dates, cum TR, ann TR, ann vol,
                                    Sharpe, max drawdown, worst day, days
  derived/president_paths.parquet   indexed-to-100 total-return path per president
                                    (x = trading days in office)
  derived/deep_election_paths.parquet  SPX +/-120td around 25 presidential + 24 midterms
  derived/deep_election_summary.csv    per-event stats incl. realized-vol change
  derived/deep_cohort_summary.csv      medians + hit rates by party / flip / era
  output/figures/president_*.png, deep_*.png
  output/deep/presidents.md, elections_1928.md

Metric note: president comparison uses the French total-return market series
(dividends included) in excess of T-bills - price-only series understate the
high-dividend pre-1960 era. Sharpe = mean daily excess return x 252 divided by
daily std x sqrt(252). Election event windows use the S&P 500 price index
(dividends negligible at +/-120 trading days).
"""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import event_study as ES
import events as EV
import figures as FG
from config import DATA_DIR, DERIVED_DIR, OUTPUT_DIR

DEEP_DIR = OUTPUT_DIR / "deep"
DEEP_DIR.mkdir(parents=True, exist_ok=True)


def load_market():
    ff = pd.read_parquet(DATA_DIR / "macro" / "ff_factors_daily.parquet")
    spx = ES.load_prices()["idx_spx"].dropna()
    spx_ret = spx.pct_change().dropna()
    # splice the FF publication lag (last ~weeks) with SPX price returns
    tail = spx_ret[spx_ret.index > ff.index.max()]
    if len(tail):
        add = pd.DataFrame({"mkt_tr": tail, "rf": ff["rf"].iloc[-1]})
        ff = pd.concat([ff[["mkt_tr", "rf"]], add])
    return ff[["mkt_tr", "rf"]].sort_index(), spx


def president_stats(ff: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows, paths = [], []
    for _, p in EV.presidents_full_df().iterrows():
        end = p["end"] if pd.notna(p["end"]) else ff.index.max()
        seg = ff.loc[p["start"]: end]
        if len(seg) < 60:
            continue
        r, rf = seg["mkt_tr"], seg["rf"]
        idx = (1 + r).cumprod()
        cum = idx.iloc[-1] - 1
        n = len(r)
        ann_tr = (1 + cum) ** (252 / n) - 1
        ann_vol = r.std() * np.sqrt(252)
        sharpe = ((r - rf).mean() * 252) / (r.std() * np.sqrt(252))
        dd = (idx / idx.cummax() - 1).min()
        rows.append(dict(
            president=p["admin"], party=p["party"],
            term=f"{p['start'].date()} - {end.date() if pd.notna(p['end']) else 'present'}",
            years=round(n / 252, 1),
            cum_return_pct=round(cum * 100, 1),
            ann_return_pct=round(ann_tr * 100, 1),
            ann_vol_pct=round(ann_vol * 100, 1),
            sharpe=round(sharpe, 2),
            max_drawdown_pct=round(dd * 100, 1),
            worst_day_pct=round(r.min() * 100, 1),
            days=n,
            note=p["partial"] or "",
        ))
        norm = idx / idx.iloc[0] * 100
        for t, v in enumerate(norm.values):
            paths.append((p["admin"], p["party"], t, float(v)))
    stats = pd.DataFrame(rows)
    paths = pd.DataFrame(paths, columns=["president", "party", "tday", "value"])
    return stats, paths


def realized_vol_series(spx: pd.Series) -> pd.Series:
    return np.log(spx / spx.shift(1)).rolling(21).std() * np.sqrt(252) * 100


def deep_event_study(spx: pd.Series):
    rv = realized_vol_series(spx)
    pres = EV.presidential_df(deep=True)
    mids = EV.midterms_df(deep=True)
    jobs = ([("presidential", f"{e['date'].year} {e['winner']}", e["date"], e) for _, e in pres.iterrows()]
            + [("midterm", f"{e['date'].year} midterm", e["date"], e) for _, e in mids.iterrows()])
    path_rows, summ_rows = [], []
    for cls, label, date, meta in jobs:
        p = ES.daily_path(spx, date, 120, 120)
        if p is None:
            continue
        for rd, v in p.items():
            path_rows.append((cls, label, int(rd), float(v)))
        rvp = ES.level_path(rv, date, 120, 120)
        def rv_at(h):
            return float(rvp.loc[h]) if rvp is not None and h in rvp.index else np.nan
        def at(h):
            return float(p.loc[h]) if h in p.index else np.nan
        idxw = np.exp(p / 100.0)
        maxdd = float((idxw / idxw.cummax() - 1).min() * 100)
        summ_rows.append(dict(
            event_class=cls, event=label,
            party=meta.get("party", meta.get("pres_party")),
            flip=bool(meta.get("flip", meta.get("any_flip", False))),
            pre60=-at(-60), pre20=-at(-20), post20=at(20), post60=at(60), post120=at(120),
            window_maxdd=maxdd, rv_pre=rv_at(-1), rv_change_20d=rv_at(20) - rv_at(-1),
        ))
    paths = pd.DataFrame(path_rows, columns=["event_class", "event", "rel_day", "value"])
    summ = pd.DataFrame(summ_rows).round(2)

    def era(label):
        y = int(label.split()[0])
        if y <= 1948: return "1928-1948"
        if y <= 1990: return "1952-1990"
        return "1992-2024"
    summ["era"] = summ["event"].map(era)

    coh_rows = []
    cohorts = {
        "all_presidential": summ[summ.event_class == "presidential"],
        "pres_D_win": summ[(summ.event_class == "presidential") & (summ.party == "D")],
        "pres_R_win": summ[(summ.event_class == "presidential") & (summ.party == "R")],
        "pres_flip": summ[(summ.event_class == "presidential") & summ.flip],
        "pres_hold": summ[(summ.event_class == "presidential") & ~summ.flip],
        "all_midterm": summ[summ.event_class == "midterm"],
    }
    for _, sub in summ.groupby("era"):
        cohorts[f"pres_{sub.era.iloc[0]}"] = sub[sub.event_class == "presidential"]
    for name, sub in cohorts.items():
        if sub.empty:
            continue
        for col in ("pre60", "post20", "post60", "post120", "rv_change_20d"):
            vals = sub[col].dropna()
            if len(vals):
                coh_rows.append(dict(cohort=name, metric=col, median=round(vals.median(), 2),
                                     hit_rate_pos=round((vals > 0).mean(), 2), n=len(vals)))
    coh = pd.DataFrame(coh_rows)
    return paths, summ, coh


# ---------------------------------------------------------------- figures

def fig_president_sharpe(stats: pd.DataFrame):
    s = stats.sort_values("sharpe")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 5.6))
    colors = [FG.INK if p == "D" else FG.GRAY for p in s["party"]]
    ax1.barh(s["president"], s["sharpe"], color=colors, height=0.62)
    for y, (v, nm) in enumerate(zip(s["sharpe"], s["president"])):
        ax1.text(v + (0.015 if v >= 0 else -0.015), y, f"{v:+.2f}",
                 va="center", ha="left" if v >= 0 else "right", fontsize=7.5)
    ax1.axvline(0, color=FG.INK, lw=0.8)
    ax1.set_title("Sharpe ratio by president (total return over T-bills)", loc="left")
    ax1.set_xlabel("Sharpe")
    for _, r in stats.iterrows():
        filled = r["party"] == "D"
        ax2.scatter(r["ann_vol_pct"], r["ann_return_pct"],
                    s=46, facecolor=FG.INK if filled else FG.CREAM,
                    edgecolor=FG.INK, linewidth=1.1, zorder=3)
        ax2.annotate(r["president"], (r["ann_vol_pct"], r["ann_return_pct"]),
                     xytext=(4, 4), textcoords="offset points", fontsize=7.5)
    ax2.axhline(0, color=FG.INK, lw=0.6, alpha=0.5)
    ax2.set_title("Annualized return vs volatility (filled = Democrat)", loc="left")
    ax2.set_xlabel("annualized volatility, %")
    ax2.set_ylabel("annualized total return, %")
    fig.tight_layout()
    out = FG.FIG_DIR / "president_sharpe.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def fig_president_paths(paths: pd.DataFrame, stats: pd.DataFrame):
    order = list(stats["president"])
    fig, axes = plt.subplots(3, 6, figsize=(13.5, 7.2), sharey=False)
    axes = list(axes.flat)
    cum = stats.set_index("president")["cum_return_pct"]
    for ax, name in zip(axes, order):
        sub = paths[paths.president == name]
        ax.plot(sub["tday"] / 252, sub["value"], color=FG.INK, lw=1.1)
        ax.axhline(100, color=FG.GRAY, lw=0.6)
        ax.set_yscale("log")
        ax.set_yticks([50, 100, 200, 400])
        ax.set_yticklabels(["50", "100", "200", "400"], fontsize=6.5)
        ax.set_title(f"{name} ({sub['party'].iloc[0]})  {cum[name]:+.0f}%", loc="left", fontsize=8)
        ax.tick_params(labelsize=6.5)
    for ax in axes[len(order):]:
        ax.axis("off")
    fig.suptitle("Total-return market path under each president, indexed to 100 at inauguration (log scale, x = years in office)",
                 x=0.01, ha="left", fontsize=11, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    out = FG.FIG_DIR / "president_paths.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def fig_event_grid(paths: pd.DataFrame, cls: str, fname: str, title: str):
    evs = sorted(paths[paths.event_class == cls]["event"].unique(),
                 key=lambda s: int(s.split()[0]))
    n = len(evs)
    ncols, nrows = 5, (n + 4) // 5
    fig, axes = plt.subplots(nrows, ncols, figsize=(12.5, 2.1 * nrows), sharex=True, sharey=True)
    axes = list(axes.flat)
    for ax, ev in zip(axes, evs):
        sub = paths[(paths.event_class == cls) & (paths.event == ev)]
        ax.plot(sub["rel_day"], sub["value"], color=FG.INK, lw=1.0)
        ax.axvline(0, color=FG.ACCENT, lw=0.8, alpha=0.9)
        ax.axhline(0, color=FG.GRAY, lw=0.5)
        ax.set_title(ev, loc="left", fontsize=7.5)
        ax.tick_params(labelsize=6.5)
    for ax in axes[n:]:
        ax.axis("off")
    fig.suptitle(title, x=0.01, ha="left", fontsize=11, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out = FG.FIG_DIR / f"{fname}.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def fig_overlay(paths: pd.DataFrame, summ: pd.DataFrame):
    sub = paths[paths.event_class == "presidential"]
    stack = sub.pivot_table(index="rel_day", columns="event", values="value")
    d_ev = summ[(summ.event_class == "presidential") & (summ.party == "D")]["event"]
    r_ev = summ[(summ.event_class == "presidential") & (summ.party == "R")]["event"]
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    for c in stack.columns:
        ax.plot(stack.index, stack[c], color=FG.GRAY, lw=0.55, alpha=0.65)
    ax.plot(stack.index, stack.median(axis=1), color=FG.INK, lw=2.0, label="median, all 25")
    ax.plot(stack.index, stack[[c for c in d_ev if c in stack]].median(axis=1),
            color=FG.INK, lw=1.3, ls="--", label="median, D wins")
    ax.plot(stack.index, stack[[c for c in r_ev if c in stack]].median(axis=1),
            color=FG.ACCENT, lw=1.3, ls="--", label="median, R wins")
    ax.axvline(0, color=FG.ACCENT, lw=0.9)
    ax.axhline(0, color=FG.INK, lw=0.6, alpha=0.5)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    ax.set_title("S&P 500 around all 25 presidential elections, 1928-2024 (%, 0 = election day)", loc="left")
    ax.set_xlabel("trading days from election")
    fig.tight_layout()
    out = FG.FIG_DIR / "deep_elections_overlay.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


# ---------------------------------------------------------------- markdown

def md_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(str(c) for c in cols) + " |",
             "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join("--" if pd.isna(v) else str(v) for v in r) + " |")
    return "\n".join(lines)


def write_md(stats: pd.DataFrame, summ: pd.DataFrame, coh: pd.DataFrame):
    ranked = stats.sort_values("sharpe", ascending=False).reset_index(drop=True)
    pres_md = [
        "# The market under every president, 1926-2026", "",
        "*Total-return market series (dividends included) in excess of T-bills; every president of the daily-data era, normalized to 100 at inauguration so terms of any length compare. Sharpe = annualized excess return / annualized volatility.*", "",
        "![](../figures/president_sharpe.png)", "",
        "![](../figures/president_paths.png)", "",
        "## The full table, ranked by Sharpe", "",
        md_table(ranked), "",
        "Notes: returns include dividends (price-only series understate the pre-1960 high-dividend era). "
        "Truman, Johnson and Ford start at succession, not election. Coolidge covers 1926-07 onward "
        "(data start); Trump II is in progress. Sharpe compares risk-adjusted results across eras, "
        "but eras differ structurally - the components matter as much as the ratio.", "",
    ]
    (DEEP_DIR / "presidents.md").write_text("\n".join(pres_md))

    p = summ[summ.event_class == "presidential"].copy().sort_values("event", key=lambda s: s.str.slice(0, 4))
    m = summ[summ.event_class == "midterm"].copy().sort_values("event", key=lambda s: s.str.slice(0, 4))
    show_cols = ["event", "party", "flip", "pre60", "post20", "post60", "post120", "window_maxdd", "rv_pre", "rv_change_20d"]
    elec_md = [
        "# Every election since 1928: the deep sample", "",
        "*S&P 500 price index around 25 presidential elections and 24 midterms; realized volatility (21-day, annualized) as the century-long volatility measure. All paths normalized to 0 at election day.*", "",
        "![](../figures/deep_elections_overlay.png)", "",
        "![](../figures/deep_elections_grid.png)", "",
        "## Per-election detail (presidential)", "",
        md_table(p[show_cols]), "",
        "![](../figures/deep_midterms_grid.png)", "",
        "## Per-election detail (midterms)", "",
        md_table(m[show_cols]), "",
        "## Cohort medians and hit rates", "",
        md_table(coh), "",
        "Columns: pre60/post20/post60/post120 = cumulative % move in the named window; window_maxdd = worst "
        "drawdown inside the +/-120-day window; rv_pre = realized vol level the day before; rv_change_20d = "
        "vol change 20 days after vs the day before (negative = uncertainty resolved).", "",
    ]
    (DEEP_DIR / "elections_1928.md").write_text("\n".join(elec_md))


def main():
    ff, spx = load_market()
    stats, paths = president_stats(ff)
    stats.to_csv(DERIVED_DIR / "president_regimes.csv", index=False)
    paths.to_parquet(DERIVED_DIR / "president_paths.parquet", index=False)

    epaths, summ, coh = deep_event_study(spx)
    epaths.to_parquet(DERIVED_DIR / "deep_election_paths.parquet", index=False)
    summ.to_csv(DERIVED_DIR / "deep_election_summary.csv", index=False)
    coh.to_csv(DERIVED_DIR / "deep_cohort_summary.csv", index=False)

    fig_president_sharpe(stats)
    fig_president_paths(paths, stats)
    fig_event_grid(epaths, "presidential", "deep_elections_grid",
                   "Each presidential election, S&P 500 +/-120 trading days (%, 0 = election day)")
    fig_event_grid(epaths, "midterm", "deep_midterms_grid",
                   "Each midterm, S&P 500 +/-120 trading days (%, 0 = election day)")
    fig_overlay(epaths, summ)
    write_md(stats, summ, coh)

    # verification prints
    s = stats.set_index("president")
    print("VERIFY Hoover ann return negative:", s.loc["Hoover", "ann_return_pct"], flush=True)
    print("VERIFY Roosevelt cum positive:", s.loc["Roosevelt", "cum_return_pct"], flush=True)
    p1948 = summ[(summ.event == "1948 Truman")]["post20"].iloc[0]
    print("VERIFY 1948 surprise post20 negative:", p1948, flush=True)
    print("counts:", summ.groupby("event_class").size().to_dict(), "| presidents:", len(stats), flush=True)
    print("presidents:", ", ".join(stats["president"]), flush=True)


if __name__ == "__main__":
    main()
