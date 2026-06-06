#!/usr/bin/env python3
"""Study 10 — Korea memory cycle + leverage: deep rebuild.

Question. Korean memory (Samsung 005930, SK Hynix 000660) is held on record retail
margin debt (~38tn won, 2026). If price collapses, is there a self-reinforcing
*death spiral* — worse forward returns and deeper drawdowns AFTER a sharp drop —
versus less-levered US memory, and is anything about it Korea-specific?

The clean Korean single-name tape is data-blocked (005930 / 000660 carry ~40 bars in
the warehouse; no long Samsung ADR). The Korea limb runs on EWY, the only liquid,
full-history (2016-05..2026-06) Korea-equity proxy. This rebuild ADDS the apples-to-apples
control the prior pass lacked: like-vol diversified US semis ETFs (SMH/SOXX/XSD) alongside
the US single names (MU/WDC/STX), so we can separate "Korea-specific" from "diversification".

Everything reads from the warehouse (split-adjusted close, 2016-present). $0 internal.
"""
from __future__ import annotations
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
DATA = HERE / "_data"; DATA.mkdir(exist_ok=True)


# ---- public reproducibility: prices ship in _data/prices.csv (split-adjusted close
#      from a private warehouse). The two helpers below are self-contained so this
#      script runs with nothing but numpy/pandas/matplotlib. -----------------------
def load_prices(tickers, start, end):
    px = pd.read_csv(DATA / "prices.csv", parse_dates=["date"]).set_index("date")
    return px.loc[(px.index >= pd.Timestamp(start)) & (px.index <= pd.Timestamp(end)), list(tickers)]


def block_bootstrap_ci(x, stat=np.mean, block=21, n_boot=5000, ci=0.95, seed=7):
    """Circular block bootstrap CI — respects autocorrelation / vol-clustering."""
    x = np.asarray(x, dtype=float); x = x[~np.isnan(x)]
    if len(x) == 0:
        return (np.nan, np.nan, np.nan)
    n = len(x); block = max(1, min(block, n)); nb = int(np.ceil(n / block))
    rng = np.random.default_rng(seed); stats = np.empty(n_boot)
    for i in range(n_boot):
        starts = rng.integers(0, n, nb)
        samp = np.concatenate([x[(s + np.arange(block)) % n] for s in starts])[:n]
        stats[i] = stat(samp)
    lo, hi = np.percentile(stats, [(1 - ci) / 2 * 100, (1 + ci) / 2 * 100])
    return (float(stat(x)), float(lo), float(hi))


def walk_forward(dates, train_frac=0.6):
    """Time-ordered (train, test) split — the out-of-sample guard."""
    uniq = sorted(pd.to_datetime(pd.Index(list(dates))).unique())
    k = int(len(uniq) * train_frac)
    return uniq[:k], uniq[k:]

# ---- house palette ----
BG, INK, ACCENT, SUPPLY = "#faf8f3", "#1c1a17", "#9c3d2e", "#7a8a78"
GREY = "#b9b3a7"
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "figure.dpi": 130, "savefig.dpi": 150, "font.size": 9, "font.family": "sans-serif",
    "axes.edgecolor": INK, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": INK, "ytick.color": INK,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": "#e6e0d4", "grid.linewidth": 0.6, "grid.alpha": 1.0,
})

START, END = "2016-01-01", "2026-06-03"
KOREA = "EWY"
US_SINGLE = ["MU", "WDC", "STX"]          # levered-ish single-name US memory/storage
US_DIVERSE = ["SMH", "SOXX", "XSD"]       # like-vol diversified US semis ETFs (the new control)
ALL = [KOREA] + US_SINGLE + US_DIVERSE
HORIZONS = (5, 10, 21, 63)
SHOCK_PCT = 10
N_BOOT = 5000


def daily_ret(s):
    return s.pct_change().dropna().clip(-0.5, 0.5)


def fwd_ret(s, i, k):
    if i + k >= len(s):
        return np.nan
    p0, p1 = s.iloc[i], s.iloc[i + k]
    return float(p1 / p0 - 1.0) if p0 > 0 else np.nan


def fwd_maxdd(s, i, k):
    if i + 1 >= len(s):
        return np.nan
    w = s.iloc[i:i + k + 1].values
    if len(w) < 2:
        return np.nan
    peak = w[0]; mdd = 0.0
    for v in w[1:]:
        peak = max(peak, v); mdd = min(mdd, v / peak - 1.0)
    return float(mdd)


def conditional(s, r, shock_thr=None, horizons=HORIZONS):
    thr = shock_thr if shock_thr is not None else np.percentile(r.values, SHOCK_PCT)
    shock_dates = r.index[r.values <= thr]
    s_idx = {d: i for i, d in enumerate(s.index)}
    arr, rows = {}, []
    for h in horizons:
        sh_r = np.array([fwd_ret(s, s_idx[d], h) for d in shock_dates if d in s_idx])
        sh_r = sh_r[~np.isnan(sh_r)]
        sh_d = np.array([fwd_maxdd(s, s_idx[d], h) for d in shock_dates if d in s_idx])
        sh_d = sh_d[~np.isnan(sh_d)]
        ba_r = np.array([fwd_ret(s, i, h) for i in range(len(s) - h - 1)]); ba_r = ba_r[~np.isnan(ba_r)]
        ba_d = np.array([fwd_maxdd(s, i, h) for i in range(len(s) - h - 1)]); ba_d = ba_d[~np.isnan(ba_d)]
        arr[(h, "shock", "ret")] = sh_r; arr[(h, "base", "ret")] = ba_r
        arr[(h, "shock", "dd")] = sh_d; arr[(h, "base", "dd")] = ba_d
        rows.append(dict(
            horizon=f"{h}d", n_shock=len(sh_r),
            shock_mean=round(100 * sh_r.mean(), 2), base_mean=round(100 * ba_r.mean(), 2),
            spread=round(100 * (sh_r.mean() - ba_r.mean()), 2),
            shock_win=round(100 * float(np.mean(sh_r > 0)), 1),
            base_win=round(100 * float(np.mean(ba_r > 0)), 1),
            shock_mdd=round(100 * sh_d.mean(), 2), base_mdd=round(100 * ba_d.mean(), 2),
        ))
    return pd.DataFrame(rows), arr, thr, len(shock_dates)


def boot_spread(sh, ba, block=21):
    if len(sh) < 5:
        return (np.nan, np.nan, np.nan)
    bm = float(np.mean(ba))
    pt, lo, hi = block_bootstrap_ci(sh, stat=np.mean, block=block, n_boot=N_BOOT)
    return (pt - bm, lo - bm, hi - bm)


def main():
    px = load_prices(ALL, START, END)
    print(f"loaded {list(px.columns)}  {px.index.min().date()}..{px.index.max().date()} rows={len(px)}\n")

    # annualized realized vol per name (to quantify the diversification artifact)
    vol = {}
    for tk in ALL:
        r = daily_ret(px[tk].dropna())
        vol[tk] = round(100 * r.std() * np.sqrt(252), 1)
    print("annualized realized vol:", vol)
    pd.Series(vol, name="ann_vol_pct").to_csv(DATA / "vol.csv")

    # per-name conditional tables + arrays
    arrs, thr_by, nshock_by, cond_tbls = {}, {}, {}, {}
    for tk in ALL:
        s = px[tk].dropna(); r = daily_ret(s)
        tbl, arr, thr, nsh = conditional(s, r)
        arrs[tk] = arr; thr_by[tk] = thr; nshock_by[tk] = nsh; cond_tbls[tk] = tbl
        tbl.insert(0, "ticker", tk)
    cond_df = pd.concat(cond_tbls.values(), ignore_index=True)
    cond_df.to_csv(DATA / "conditional.csv", index=False)
    print("\n=== Korea proxy (EWY) conditional table ===")
    print(cond_tbls[KOREA].to_string(index=False))

    # bootstrap CI on conditional-return spread, all names
    print("\n=== bootstrap CI on conditional fwd-return spread (shock - base) ===")
    boot_rows = []
    for tk in ALL:
        for h in HORIZONS:
            pt, lo, hi = boot_spread(arrs[tk][(h, "shock", "ret")], arrs[tk][(h, "base", "ret")])
            sig = "SIG" if (lo == lo and (lo > 0 or hi < 0)) else "ns"
            boot_rows.append(dict(ticker=tk, horizon=h, spread=round(100 * pt, 2),
                                  ci_lo=round(100 * lo, 2), ci_hi=round(100 * hi, 2), sig=sig))
            if tk == KOREA:
                print(f"  EWY {h:>2d}d  spread={pt*100:+.2f}%  CI[{lo*100:+.2f},{hi*100:+.2f}]  {sig}")
    boot_df = pd.DataFrame(boot_rows); boot_df.to_csv(DATA / "bootstrap_ci.csv", index=False)

    # deep tail: worst-5% and worst-2.5%, all names, 21d/63d, with CI
    print("\n=== deep-tail spreads (worst-5%, worst-2.5%) ===")
    deep_rows = []
    n_tail_tests = 0
    for pct in (5.0, 2.5):
        for tk in ALL:
            s = px[tk].dropna(); r = daily_ret(s)
            thr = np.percentile(r.values, pct)
            s_idx = {d: i for i, d in enumerate(s.index)}
            for h in (21, 63):
                n_tail_tests += 1
                sh = np.array([fwd_ret(s, s_idx[d], h) for d in r.index[r.values <= thr] if d in s_idx])
                sh = sh[~np.isnan(sh)]
                ba = np.array([fwd_ret(s, i, h) for i in range(len(s) - h - 1)]); ba = ba[~np.isnan(ba)]
                _, lo, hi = block_bootstrap_ci(sh, block=21, n_boot=N_BOOT)
                lo2, hi2 = (lo - ba.mean()) * 100, (hi - ba.mean()) * 100
                spread = (sh.mean() - ba.mean()) * 100
                sig = "SIG" if (lo2 > 0 or hi2 < 0) else "ns"
                deep_rows.append(dict(ticker=tk, tail=pct, horizon=h, n=len(sh),
                                      spread=round(spread, 2), ci_lo=round(lo2, 2),
                                      ci_hi=round(hi2, 2), sig=sig))
                if tk == KOREA:
                    print(f"  EWY {h:>2d}d worst{pct}% n={len(sh):3d} spread={spread:+.2f}% CI[{lo2:+.1f},{hi2:+.1f}] {sig}")
    deep_df = pd.DataFrame(deep_rows); deep_df.to_csv(DATA / "deep_tail.csv", index=False)
    print(f"  [multiple testing] {n_tail_tests} tail cells tested; "
          f"{(deep_df.sig=='SIG').sum()} cleared zero")

    # OOS with bootstrap CI (not just a point) — train threshold on first 60%, test on rest
    print("\n=== OOS (threshold from train half, 21d spread on test half) with CI ===")
    oos_rows = []
    for tk in ALL:
        s = px[tk].dropna(); r = daily_ret(s)
        tr, te = walk_forward(r.index, train_frac=0.6)
        thr = np.percentile(r.loc[r.index.isin(tr)].values, SHOCK_PCT)
        s_idx = {d: i for i, d in enumerate(s.index)}
        r_te = r.loc[r.index.isin(te)]
        h = 21
        sh = np.array([fwd_ret(s, s_idx[d], h) for d in r_te.index[r_te.values <= thr] if d in s_idx])
        sh = sh[~np.isnan(sh)]
        ba = np.array([fwd_ret(s, s_idx[d], h) for d in te if d in s_idx]); ba = ba[~np.isnan(ba)]
        _, lo, hi = block_bootstrap_ci(sh, block=21, n_boot=N_BOOT)
        lo2, hi2 = (lo - ba.mean()) * 100, (hi - ba.mean()) * 100
        spread = (sh.mean() - ba.mean()) * 100
        sig = "SIG" if (lo2 > 0 or hi2 < 0) else "ns"
        oos_rows.append(dict(ticker=tk, n_shock_test=len(sh), spread=round(spread, 2),
                             ci_lo=round(lo2, 2), ci_hi=round(hi2, 2), sig=sig,
                             train_end=str(tr[-1].date()), test_start=str(te[0].date())))
        if tk == KOREA:
            print(f"  EWY OOS 21d n={len(sh)} spread={spread:+.2f}% CI[{lo2:+.1f},{hi2:+.1f}] {sig} "
                  f"(train .. {tr[-1].date()}, test {te[0].date()} ..)")
    oos_df = pd.DataFrame(oos_rows); oos_df.to_csv(DATA / "oos.csv", index=False)

    # Korea vs the two US comparator groups (single-name AND diversified) — the artifact test
    print("\n=== Korea (EWY) vs US single-name AND US diversified groups ===")
    cmp_rows = []
    for h in HORIZONS:
        def grp_spread(names):
            return np.mean([arrs[t][(h, "shock", "ret")].mean() - arrs[t][(h, "base", "ret")].mean()
                            for t in names]) * 100
        def grp_mdd(names):
            return np.mean([arrs[t][(h, "shock", "dd")].mean() for t in names]) * 100
        row = dict(horizon=h,
                   ewy_spread=round(arrs[KOREA][(h, "shock", "ret")].mean() * 100 -
                                    arrs[KOREA][(h, "base", "ret")].mean() * 100, 2),
                   us_single_spread=round(grp_spread(US_SINGLE), 2),
                   us_diverse_spread=round(grp_spread(US_DIVERSE), 2),
                   ewy_mdd=round(arrs[KOREA][(h, "shock", "dd")].mean() * 100, 2),
                   us_single_mdd=round(grp_mdd(US_SINGLE), 2),
                   us_diverse_mdd=round(grp_mdd(US_DIVERSE), 2))
        cmp_rows.append(row)
        print(f"  {h:>2d}d  EWY sp={row['ewy_spread']:+.2f}  US-single={row['us_single_spread']:+.2f}  "
              f"US-diverse={row['us_diverse_spread']:+.2f} | "
              f"mdd EWY={row['ewy_mdd']:.2f} single={row['us_single_mdd']:.2f} diverse={row['us_diverse_mdd']:.2f}")
    cmp_df = pd.DataFrame(cmp_rows); cmp_df.to_csv(DATA / "korea_vs_us.csv", index=False)

    figs(px, arrs, vol, deep_df, cmp_df, boot_df)
    print("\nDONE — figures + _data/ written")
    return cond_df, deep_df, cmp_df, boot_df, oos_df, vol


def figs(px, arrs, vol, deep_df, cmp_df, boot_df):
    # FIG 1: conditional vs unconditional fwd return, EWY (rebound, not spiral)
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    hs = list(HORIZONS); x = np.arange(len(hs))
    ba = [arrs[KOREA][(h, "base", "ret")].mean() * 100 for h in hs]
    sh = [arrs[KOREA][(h, "shock", "ret")].mean() * 100 for h in hs]
    ax.bar(x - 0.2, ba, 0.4, color=GREY, label="any day (baseline)")
    ax.bar(x + 0.2, sh, 0.4, color=ACCENT, label="after a worst-decile drop")
    for xi, (b, s) in enumerate(zip(ba, sh)):
        ax.annotate(f"{b:+.1f}", (xi - 0.2, b), xytext=(0, 3), textcoords="offset points", ha="center", fontsize=7, color=INK)
        ax.annotate(f"{s:+.1f}", (xi + 0.2, s), xytext=(0, 3), textcoords="offset points", ha="center", fontsize=7, color=ACCENT)
    ax.axhline(0, color=INK, lw=0.7); ax.set_xticks(x); ax.set_xticklabels([f"{h}d" for h in hs])
    ax.set_ylabel("mean forward return, %")
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    ax.set_title("After a sharp drop the Korea proxy bounces — it does not keep falling",
                 loc="left", fontweight="bold", fontsize=10)
    fig.tight_layout(); fig.savefig(HERE / "fig1_rebound.png"); plt.close(fig)

    # FIG 2: deep-tail spreads with CI whiskers, EWY (only worst-2.5% clears zero)
    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    d = deep_df[deep_df.ticker == KOREA].reset_index(drop=True)
    tails = list(d["tail"]); hzns = list(d["horizon"])
    labels = [f"worst-{int(t) if t==int(t) else t}%\n{h}d" for t, h in zip(tails, hzns)]
    x = np.arange(len(d))
    cols = [ACCENT if s == "SIG" else GREY for s in d["sig"]]
    ax.bar(x, list(d["spread"]), 0.55, color=cols)
    for xi in x:
        lo, hi, sp = d["ci_lo"][xi], d["ci_hi"][xi], d["spread"][xi]
        ax.plot([xi, xi], [lo, hi], color=INK, lw=1.1)
        ax.plot([xi - 0.08, xi + 0.08], [lo, lo], color=INK, lw=1.1)
        ax.plot([xi - 0.08, xi + 0.08], [hi, hi], color=INK, lw=1.1)
        ax.annotate(f"{sp:+.1f}", (xi, hi), xytext=(0, 4), textcoords="offset points", ha="center", fontsize=7.5)
    ax.axhline(0, color=INK, lw=0.8); ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("spread vs baseline, %  (with 95% block-bootstrap CI)")
    ax.set_title("The deeper the drop, the bigger the bounce — only worst-2.5% clears zero",
                 loc="left", fontweight="bold", fontsize=9.8)
    fig.tight_layout(); fig.savefig(HERE / "fig2_deep_tail.png"); plt.close(fig)

    # FIG 3: vol bars — the diversification artifact, in one chart
    fig, ax = plt.subplots(figsize=(7.4, 3.2))
    order = [KOREA] + US_DIVERSE + US_SINGLE
    vals = [vol[t] for t in order]
    cols = [ACCENT] + [SUPPLY] * len(US_DIVERSE) + [INK] * len(US_SINGLE)
    ax.bar(np.arange(len(order)), vals, 0.6, color=cols)
    for i, v in enumerate(vals):
        ax.annotate(f"{v:.0f}", (i, v), xytext=(0, 3), textcoords="offset points", ha="center", fontsize=8)
    ax.set_xticks(np.arange(len(order))); ax.set_xticklabels(order)
    ax.set_ylabel("annualized realized vol, %")
    ax.set_title("Why Korea's drawdowns look milder: it is a calmer instrument by build",
                 loc="left", fontweight="bold", fontsize=9.8)
    # legend by color group
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=ACCENT, label="Korea proxy (diversified ETF)"),
                       Patch(color=SUPPLY, label="US diversified semis ETFs"),
                       Patch(color=INK, label="US single-name memory")],
              fontsize=7.5, frameon=False, loc="upper left")
    fig.tight_layout(); fig.savefig(HERE / "fig3_vol_artifact.png"); plt.close(fig)

    # FIG 4: Korea vs US-single vs US-diverse, 21d spread + subsequent drawdown
    fig, axes = plt.subplots(1, 2, figsize=(8.8, 3.5))
    h21 = cmp_df[cmp_df.horizon == 21].iloc[0]
    # left: 21d conditional spread
    grp = ["Korea\nproxy", "US single\nname", "US diversified\nETF"]
    spv = [h21.ewy_spread, h21.us_single_spread, h21.us_diverse_spread]
    axes[0].bar(np.arange(3), spv, 0.6, color=[ACCENT, INK, SUPPLY])
    for i, v in enumerate(spv):
        axes[0].annotate(f"{v:+.2f}", (i, v), xytext=(0, 3 if v >= 0 else -10), textcoords="offset points", ha="center", fontsize=8)
    axes[0].axhline(0, color=INK, lw=0.7); axes[0].set_xticks(range(3)); axes[0].set_xticklabels(grp, fontsize=8)
    axes[0].set_ylabel("21d conditional spread, %")
    axes[0].set_title("Bounce after a shock (21d)", loc="left", fontweight="bold", fontsize=9.3)
    # right: 21d subsequent drawdown
    mdv = [h21.ewy_mdd, h21.us_single_mdd, h21.us_diverse_mdd]
    axes[1].bar(np.arange(3), mdv, 0.6, color=[ACCENT, INK, SUPPLY])
    for i, v in enumerate(mdv):
        axes[1].annotate(f"{v:.1f}", (i, v), xytext=(0, -11), textcoords="offset points", ha="center", fontsize=8)
    axes[1].set_xticks(range(3)); axes[1].set_xticklabels(grp, fontsize=8)
    axes[1].set_ylabel("subsequent 21d drawdown, %")
    axes[1].set_title("Subsequent drawdown after a shock (21d)", loc="left", fontweight="bold", fontsize=9.3)
    fig.suptitle("Against a like-vol diversified US ETF, Korea's edge nearly vanishes",
                 fontsize=10, fontweight="bold", x=0.01, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.94]); fig.savefig(HERE / "fig4_korea_vs_us.png"); plt.close(fig)


if __name__ == "__main__":
    main()
