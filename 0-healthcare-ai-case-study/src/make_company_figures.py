"""Master positioning map + one per-company highlight chart each.
Two-pillar read: moat duration (x) vs market expectation (y), colored by business quality.
Green = good business (house preference). Labels de-overlapped with leader lines."""
import os, json, hashlib, re
import matplotlib.pyplot as plt
from house import style, finish, save, place_labels, INK, GOOD, COND, BAD, CREAM

style()
HERE = os.path.dirname(__file__)
FIG = os.path.join(HERE, "..", "figures")
pos = json.load(open(os.path.join(HERE, "..", "data", "positioning.json")))

COL = {"yes": GOOD, "conditional": COND, "no": BAD}


def jit(key, scale):
    h = int(hashlib.md5(key.encode()).hexdigest(), 16)
    return ((h % 1000) / 1000.0 - 0.5) * scale


def ascii_name(x):
    return re.sub(r"\s+", " ", re.sub(r"[^\x00-\x7F]+", " ", x)).strip(" (,")


def coords(p):
    return (p["moat_years"] + jit(p["key"], 0.7), p["expectation"] + jit(p["key"] + "y", 0.6))


def base(ax, highlight=None):
    ax.axvline(4.5, color=INK, lw=0.5, alpha=0.12)
    ax.axhline(1, color=INK, lw=0.5, alpha=0.12)
    for p in pos:
        x, y = coords(p)
        hl = highlight is not None and p["key"] == highlight
        if hl:
            ax.scatter(x, y, s=250, color=COL[p["good_business"]], edgecolor=INK, linewidth=1.8, zorder=6)
            ax.annotate(p["key"], (x, y), textcoords="offset points", xytext=(10, 6),
                        fontsize=10.5, fontweight="bold", color=INK, zorder=7)
        else:
            a = 0.22 if highlight else 0.92
            s = 24 if highlight else 66
            ax.scatter(x, y, s=s, color=COL[p["good_business"]], edgecolor=INK,
                       linewidth=0.4, alpha=a, zorder=3)
    ax.set_xlim(-0.8, 10.2)
    ax.set_ylim(-1.9, 2.9)
    ax.set_xlabel("Moat duration  (years it plausibly compounds)  →")
    ax.set_yticks([-1, 0, 1, 2])
    ax.set_yticklabels(["fair-cheap", "fair", "full", "rich"])
    ax.set_ylabel("Market expectation")
    ax.annotate("durable + cheap\n= own with eyes open", (9.9, -1.5), fontsize=8, color=INK,
                alpha=0.4, ha="right", va="bottom")
    ax.annotate("commoditizing + rich\n= a demo at a franchise price", (-0.5, 2.6), fontsize=8,
                color=INK, alpha=0.4, ha="left", va="top")


def legend(ax):
    for lab, c in [("good business", GOOD), ("conditional", COND), ("not a good business", BAD)]:
        ax.scatter([], [], color=c, edgecolor=INK, linewidth=0.4, label=lab, s=70)
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")


# master — all labeled, de-overlapped
fig, ax = plt.subplots(figsize=(14.5, 9.6))
base(ax)
legend(ax)
xs = [coords(p)[0] for p in pos]
ys = [coords(p)[1] for p in pos]
place_labels(ax, xs, ys, [p["key"] for p in pos], fontsize=7.5)
finish(ax, "The whole universe on two axes",
       "Business quality (color) vs moat duration (x) vs what the market is paying (y)",
       "Source: this study's 94 company profiles. Positions are the author's read, not advice.")
save(fig, os.path.join(FIG, "00_positioning_master.png"))

# per-company — only the highlighted name is labeled, so no overlap
n = 0
for p in pos:
    fig, ax = plt.subplots(figsize=(6.8, 4.8))
    base(ax, highlight=p["key"])
    legend(ax)
    finish(ax, f"{ascii_name(p['name']) or p['key']} on the map",
           "Where this name sits vs the other 93 players",
           "Source: this study. Position is the author's read, not advice.")
    save(fig, os.path.join(FIG, f"co_{p['key']}.png"))
    n += 1
print(f"rendered master + {n} per-company figures")
