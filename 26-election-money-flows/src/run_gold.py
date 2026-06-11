"""Chapter 8: gold around elections, administrations, and Trump shocks.

Outputs
  derived/gold_admin.csv          per-president gold return/vol/Sharpe (1971-, float era)
  derived/gold_elections.csv      gold around every election since 1972 (monthly +/-12m)
  derived/gold_trump_events.csv   daily gold vs SPX around Trump-era shocks
  derived/gold_correlations.csv   rolling/era correlations vs dollar, equities, GPR
  output/figures/gold_admin.png, gold_trump.png
  output/deep/gold.md

Honesty rule: Trump-era gold claims are tested against the post-2022 baseline
drift (central-bank buying era), not against zero.
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
FLOAT_ERA = "1971-08-15"  # Nixon closes the gold window


def load():
    gm = pd.read_parquet(DATA_DIR / "macro" / "gold_monthly.parquet")["gold"].dropna()
    gd = pd.read_parquet(DATA_DIR / "prices" / "idx_gold.parquet")["close"].dropna()
    spx = ES.load_prices()["idx_spx"].dropna()
    dxy = pd.read_parquet(DATA_DIR / "prices" / "idx_dxy.parquet")["close"].dropna()
    ff = pd.read_parquet(DATA_DIR / "macro" / "ff_factors_daily.parquet")
    gpr = pd.read_parquet(DATA_DIR / "macro" / "gpr_daily.parquet")
    gpr_col = [c for c in gpr.columns if str(c).upper().startswith("GPRD")][:1] or [gpr.columns[0]]
    gprd = pd.to_numeric(gpr[gpr_col[0]], errors="coerce").dropna()
    iau = ES.load_fund_histories().get("IAU")
    return gm, gd, spx, dxy, ff, gprd, iau


def admin_gold(gm: pd.Series, ff: pd.DataFrame) -> pd.DataFrame:
    rf_m = (1 + ff["rf"]).resample("MS").prod() - 1
    rows = []
    for _, p in EV.presidents_full_df().iterrows():
        start = max(p["start"], pd.Timestamp(FLOAT_ERA))
        end = p["end"] if pd.notna(p["end"]) else gm.index.max()
        if end <= pd.Timestamp(FLOAT_ERA):
            continue
        seg = gm.loc[start:end]
        if len(seg) < 12:
            continue
        r = seg.pct_change().dropna()
        rfseg = rf_m.reindex(r.index).ffill().fillna(0)
        cum = seg.iloc[-1] / seg.iloc[0] - 1
        n = len(r)
        rows.append(dict(
            president=p["admin"], party=p["party"],
            months=n,
            cum_gold_pct=round(cum * 100, 1),
            ann_gold_pct=round(((1 + cum) ** (12 / n) - 1) * 100, 1),
            ann_vol_pct=round(r.std() * np.sqrt(12) * 100, 1),
            sharpe=round(((r - rfseg).mean() * 12) / (r.std() * np.sqrt(12)), 2),
            max_dd_pct=round(((seg / seg.cummax()) - 1).min() * 100, 1),
            note=("from 1971-08" if p["admin"] == "Nixon" else (p["partial"] or "")),
        ))
    return pd.DataFrame(rows)


def gold_elections(gm: pd.Series) -> pd.DataFrame:
    pres = EV.presidential_df(deep=True)
    pres = pres[pres["date"] >= "1972-01-01"]
    rows = []
    for _, e in pres.iterrows():
        s = gm.dropna()
        i = s.index.searchsorted(e["date"])
        if i < 12 or i >= len(s):
            continue
        base = s.iloc[i]
        def at(k):
            j = i + k
            return (s.iloc[j] / base - 1) * 100 if 0 <= j < len(s) else np.nan
        rows.append(dict(
            event=f"{e['date'].year} {e['winner']}", party=e["party"], flip=e["flip"],
            pre_12m=round(-((s.iloc[i - 12] / base - 1) * 100) if i >= 12 else np.nan, 1),
            post_3m=round(at(3), 1), post_6m=round(at(6), 1), post_12m=round(at(12), 1),
        ))
    return pd.DataFrame(rows)


TRUMP_EVENTS = [
    ("2016 election", "2016-11-08"), ("2024 election", "2024-11-05"),
    ("2018 steel tariffs", "2018-03-01"), ("2019 escalation tweets", "2019-05-05"),
    ("2025 Feb tariff EOs", "2025-02-01"), ("2025 Liberation Day", "2025-04-02"),
    ("2025 pause", "2025-04-09"), ("2025 Geneva step-down", "2025-05-12"),
    ("2025 Israel-Iran war", "2025-06-13"), ("2025 US strikes Iran", "2025-06-22"),
]


def trump_events_table(gd: pd.Series, spx: pd.Series) -> pd.DataFrame:
    rows = []
    for name, d in TRUMP_EVENTS:
        gp = ES.daily_path(gd, d, 5, 60)
        sp = ES.daily_path(spx, d, 5, 60)
        def at(p, h):
            return round(float(p.loc[h]), 1) if p is not None and h in p.index else np.nan
        rows.append(dict(event=name, date=d,
                         gold_5d=at(gp, 5), gold_20d=at(gp, 20), gold_60d=at(gp, 60),
                         spx_5d=at(sp, 5), spx_20d=at(sp, 20), spx_60d=at(sp, 60)))
    return pd.DataFrame(rows)


def correlations(gd: pd.Series, spx: pd.Series, dxy: pd.Series, gprd: pd.Series):
    df = pd.DataFrame({
        "gold": gd.pct_change(), "spx": spx.pct_change(),
        "dxy": dxy.pct_change(), "gpr": gprd.diff().rolling(5).mean(),
    }).dropna()
    roll = pd.DataFrame({
        "gold_dxy": df["gold"].rolling(90).corr(df["dxy"]),
        "gold_spx": df["gold"].rolling(90).corr(df["spx"]),
        "gold_gpr": df["gold"].rolling(90).corr(df["gpr"]),
    })
    eras = {"2000-2016": ("2000-09-01", "2017-01-19"), "Trump I": ("2017-01-20", "2021-01-19"),
            "Biden": ("2021-01-20", "2025-01-19"), "Trump II": ("2025-01-20", None)}
    rows = []
    for era, (a, b) in eras.items():
        seg = df.loc[a:b]
        g = gd.loc[a:b]
        ann = ((g.iloc[-1] / g.iloc[0]) ** (252 / len(g)) - 1) * 100 if len(g) > 60 else np.nan
        rows.append(dict(era=era, gold_ann_ret_pct=round(ann, 1),
                         corr_dxy=round(seg["gold"].corr(seg["dxy"]), 2),
                         corr_spx=round(seg["gold"].corr(seg["spx"]), 2),
                         corr_gpr=round(seg["gold"].corr(seg["gpr"]), 2),
                         days=len(seg)))
    return roll, pd.DataFrame(rows)


def baseline_test(gd: pd.Series) -> dict:
    def ann(a, b):
        seg = gd.loc[a:b]
        return ((seg.iloc[-1] / seg.iloc[0]) ** (252 / len(seg)) - 1) * 100
    return {
        "2017-2021 (Trump I)": round(ann("2017-01-20", "2021-01-19"), 1),
        "2022-01 to 2024-10 (CB-buying era, pre-election)": round(ann("2022-01-01", "2024-10-31"), 1),
        "2024-11 to present (post-election, Trump II)": round(ann("2024-11-05", None), 1),
    }


def make_figures(gm, gd, iau, roll, admin):
    # fig 1: long gold + per-admin returns
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.8))
    g = gm.loc[FLOAT_ERA:]
    ax1.plot(g.index, g.values, color=FG.INK, lw=1.1)
    ax1.set_yscale("log")
    for _, p in EV.presidents_full_df().iterrows():
        if pd.notna(p["end"]) and p["end"] > pd.Timestamp(FLOAT_ERA):
            ax1.axvline(p["end"], color=FG.GRID, lw=0.7)
    ax1.set_title("Gold, monthly, 1971-2026 (log scale; gridlines = changes of president)", loc="left")
    s = admin.sort_values("ann_gold_pct")
    colors = [FG.INK if p == "D" else FG.GRAY for p in s["party"]]
    ax2.barh(s["president"], s["ann_gold_pct"], color=colors, height=0.62)
    for y, v in enumerate(s["ann_gold_pct"]):
        ax2.text(v + (0.4 if v >= 0 else -0.4), y, f"{v:+.0f}%", va="center",
                 ha="left" if v >= 0 else "right", fontsize=7.5)
    ax2.axvline(0, color=FG.INK, lw=0.8)
    ax2.set_title("Annualized gold return by president (black = Democrat)", loc="left")
    fig.tight_layout()
    fig.savefig(FG.FIG_DIR / "gold_admin.png", bbox_inches="tight")
    plt.close(fig)

    # fig 2: Trump windows + correlations + IAU flows
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 7.0))
    ax = axes[0, 0]
    for name, d, style in [("2016 election", "2016-11-08", "--"), ("2024 election", "2024-11-05", "-")]:
        p = ES.daily_path(gd, d, 60, 120)
        if p is not None:
            ax.plot(p.index, p.values, color=FG.INK, lw=1.3, ls=style, label=f"gold, {name}")
    ax.axvline(0, color=FG.ACCENT, lw=0.9)
    ax.axhline(0, color=FG.INK, lw=0.6, alpha=0.5)
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Gold around the two Trump elections, % (0 = election day)", loc="left")

    ax = axes[0, 1]
    p25 = ES.daily_path(gd, "2025-04-02", 40, 60)
    s25 = ES.daily_path(ES.load_prices()["idx_spx"], "2025-04-02", 40, 60)
    if p25 is not None:
        ax.plot(p25.index, p25.values, color=FG.ACCENT, lw=1.5, label="gold")
    if s25 is not None:
        ax.plot(s25.index, s25.values, color=FG.INK, lw=1.2, label="S&P 500")
    ax.axvline(0, color=FG.ACCENT, lw=0.9)
    ax.axhline(0, color=FG.INK, lw=0.6, alpha=0.5)
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Liberation Day 2025: gold vs equities, %", loc="left")

    ax = axes[1, 0]
    for col, style in [("gold_dxy", "-"), ("gold_spx", "--"), ("gold_gpr", ":")]:
        ax.plot(roll.index, roll[col], lw=1.0, ls=style, color=FG.INK, label=col.replace("gold_", "vs "))
    ax.axhline(0, color=FG.GRAY, lw=0.6)
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("Rolling 90-day correlation of daily gold returns", loc="left")

    ax = axes[1, 1]
    if iau is not None:
        pct = ES.weekly_flow_pct(iau)
        for name, d, style in [("2024 election", "2024-11-05", "-"), ("Liberation Day", "2025-04-02", "--")]:
            cp = ES.weekly_caf_path(pct, d, 26, 26)
            if cp is not None:
                ax.plot(cp.index, cp.values, color=FG.INK, lw=1.3, ls=style, label=name)
        ax.axvline(0, color=FG.ACCENT, lw=0.9)
        ax.axhline(0, color=FG.INK, lw=0.6, alpha=0.5)
        ax.legend(frameon=False, fontsize=8)
    ax.set_title("Gold ETF flows (IAU), cumulative % of AUM, weekly", loc="left")
    fig.tight_layout()
    fig.savefig(FG.FIG_DIR / "gold_trump.png", bbox_inches="tight")
    plt.close(fig)


def md_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(str(c) for c in cols) + " |",
             "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join("--" if pd.isna(v) else str(v) for v in r) + " |")
    return "\n".join(lines)


def main():
    gm, gd, spx, dxy, ff, gprd, iau = load()
    admin = admin_gold(gm, ff)
    admin.to_csv(DERIVED_DIR / "gold_admin.csv", index=False)
    elec = gold_elections(gm)
    elec.to_csv(DERIVED_DIR / "gold_elections.csv", index=False)
    tev = trump_events_table(gd, spx)
    tev.to_csv(DERIVED_DIR / "gold_trump_events.csv", index=False)
    roll, eras = correlations(gd, spx, dxy, gprd)
    eras.to_csv(DERIVED_DIR / "gold_correlations.csv", index=False)
    base = baseline_test(gd)
    make_figures(gm, gd, iau, roll, admin)

    md = [
        "# Gold: elections, presidents, and the Trump question", "",
        "*Monthly gold from the 1971 float; daily futures from 2000; gold-ETF (IAU) creation/redemption flows from 2005. The question: is the recent rise a Trump effect or a structural one?*", "",
        "![](../figures/gold_admin.png)", "",
        "## Gold by president (float era)", "", md_table(admin), "",
        "## Gold around every election since 1972 (monthly)", "", md_table(elec), "",
        "![](../figures/gold_trump.png)", "",
        "## Trump-era shock windows (daily, % moves)", "", md_table(tev), "",
        "## Era correlations and returns", "", md_table(eras), "",
        "## The baseline test", "",
        *[f"- {k}: {v:+.1f}% annualized" for k, v in base.items()], "",
    ]
    (DEEP_DIR / "gold.md").write_text("\n".join(md))

    a = admin.set_index("president")
    print("VERIFY Carter-era gold strongly positive:", a.loc["Carter", "ann_gold_pct"], flush=True)
    print("VERIFY Reagan-era gold weak:", a.loc["Reagan", "ann_gold_pct"], flush=True)
    print("VERIFY Trump II gold:", a.loc["Trump II", "ann_gold_pct"], flush=True)
    print("baseline:", base, flush=True)
    print("era corr table:\n", eras.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
