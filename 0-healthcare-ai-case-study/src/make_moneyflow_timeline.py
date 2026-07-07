"""Money-flow figure (upfront vs headline) + the 2010-now timeline figure."""
import os, csv
import matplotlib.pyplot as plt
import numpy as np
from house import style, finish, save, INK, GOOD, COND, BAD, MUTE, ACCENT, SUPPLY, CREAM

style()
HERE = os.path.dirname(__file__)
FIG = os.path.join(HERE, "..", "figures")
DATA = os.path.join(HERE, "..", "data")


def load_csv(name):
    with open(os.path.join(DATA, name)) as f:
        return list(csv.DictReader(f))


# Figure: upfront vs headline (the cheap-optionality point)
def fig_moneyflow():
    rows = load_csv("deals.csv")
    ds = []
    for r in rows:
        try:
            up = float(r["upfront_musd"]); tot = float(r["total_musd"])
        except (ValueError, KeyError):
            continue
        if up > 0 and tot > 0 and r.get("kind") == "discovery-partnership":
            ds.append((f"{r['funder'].split('/')[0]} -> {r['recipient']}", up, tot))
    ds.sort(key=lambda x: x[2], reverse=True)
    ds = ds[:10]
    labels = [d[0] for d in ds]
    ups = [d[1] for d in ds]
    tots = [d[2] for d in ds]
    y = np.arange(len(ds))
    fig, ax = plt.subplots(figsize=(9.4, 6.0))
    ax.barh(y, tots, color=MUTE, height=0.6, label="Headline 'deal value' (mostly contingent milestones)")
    ax.barh(y, ups, color=GOOD, height=0.6, label="Cash actually paid up front")
    for i, (u, t) in enumerate(zip(ups, tots)):
        ax.annotate(f"\\${u:.0f}m of \\${t/1000:.1f}bn  ({u/t*100:.1f}%)", (t, i),
                    textcoords="offset points", xytext=(6, 0), va="center", fontsize=8, color=INK)
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=8.5)
    ax.invert_yaxis()
    ax.set_xlabel("US$ million")
    ax.set_xlim(0, max(tots) * 1.28)
    ax.legend(frameon=False, fontsize=8.5, loc="lower right")
    finish(ax, "The headline number is not the money that changes hands",
           "AI drug-discovery deals: the up-front cash is 1-3% of the 'deal value'",
           "Source: this study's deal tape (data/deals.csv), company announcements.")
    save(fig, os.path.join(FIG, "07_money_flow.png"))


# Figure: the 2010-now timeline
def fig_timeline():
    rows = load_csv("timeline.csv")
    ev = []
    catcol = {"model": ACCENT, "regulation": SUPPLY, "reimbursement": SUPPLY,
              "deal": GOOD, "ipo": COND, "product": INK, "failure": BAD, "policy": SUPPLY}
    for r in rows:
        d = r["date"][:4]
        try:
            yr = int(d)
        except ValueError:
            continue
        ev.append((yr, r["title"], r.get("category", "product")))
    ev.sort()
    fig, ax = plt.subplots(figsize=(11.5, 6.6))
    ax.axhline(0, color=INK, lw=1)
    # stagger labels above/below, and within a year
    from collections import defaultdict
    byyr = defaultdict(list)
    for yr, t, c in ev:
        byyr[yr].append((t, c))
    for yr, items in byyr.items():
        n = len(items)
        for j, (t, c) in enumerate(items):
            side = 1 if (j % 2 == 0) else -1
            level = (j // 2) + 1
            yv = side * level * 1.05
            ax.plot([yr, yr], [0, yv], color=catcol.get(c, INK), lw=0.7, alpha=0.6)
            ax.scatter([yr], [0], s=26, color=catcol.get(c, INK), zorder=5, edgecolor=CREAM, linewidth=0.5)
            ax.annotate(f"{t}", (yr, yv), fontsize=7, color=INK, ha="center",
                        va="bottom" if side > 0 else "top",
                        bbox=dict(boxstyle="round,pad=0.15", fc=CREAM, ec="none", alpha=0.85))
    yrs = sorted(byyr)
    ax.set_xlim(min(yrs) - 0.6, max(yrs) + 0.6)
    ax.set_ylim(-max(len(v) for v in byyr.values()) * 0.62 - 1.4, max(len(v) for v in byyr.values()) * 0.62 + 1.4)
    ax.set_xticks(range(min(yrs), max(yrs) + 1, 2))
    ax.get_yaxis().set_visible(False)
    ax.spines["left"].set_visible(False)
    # legend
    for lab, c in [("model", ACCENT), ("deal", GOOD), ("regulation/pay", SUPPLY), ("IPO", COND), ("failure", BAD)]:
        ax.scatter([], [], color=c, label=lab, s=30)
    ax.legend(frameon=False, fontsize=8, loc="lower center", ncol=5, bbox_to_anchor=(0.5, -0.12))
    finish(ax, "How we got here: healthcare AI, 2010 to now",
           "From Watson to AlphaFold to the reimbursement wall to the big pharma deals",
           "Source: this study's timeline (data/timeline.csv).")
    save(fig, os.path.join(FIG, "08_timeline.png"))


fig_moneyflow()
fig_timeline()
print("rendered:", [f for f in sorted(os.listdir(FIG)) if f.startswith(("07", "08"))])
