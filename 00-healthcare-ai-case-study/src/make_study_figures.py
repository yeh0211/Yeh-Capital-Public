"""Render the study-level findings figures. Data from the study briefs (Ch1, spotlight).
Numbers are sourced/estimated as noted in the study text; charts carry the argument."""
import os
import matplotlib.pyplot as plt
import numpy as np
from house import style, finish, save, place_labels, INK, ACCENT, SUPPLY, MUTE, GOOD, COND, BAD, CREAM

style()
FIG = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(FIG, exist_ok=True)


# Fig 1 — FDA AI/ML clearance velocity (annual authorizations; the 2023 inflection)
def fig_fda_velocity():
    yrs = ["2015", "2019", "2022", "2023", "2024", "2025"]
    vals = [6, 79, 91, 221, 253, 295]  # annual; selected years, FDA list / public tallies
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    colors = [MUTE] * 3 + [ACCENT] * 3
    ax.bar(yrs, vals, color=colors, width=0.62)
    for x, v in zip(yrs, vals):
        ax.annotate(str(v), (x, v), textcoords="offset points", xytext=(0, 4),
                    ha="center", fontsize=9, color=INK)
    ax.set_ylim(0, 330)
    ax.set_ylabel("New AI/ML device authorizations")
    ax.annotate("inflects at 2023", xy=(3, 221), xytext=(1.4, 265),
                fontsize=9.5, color=ACCENT,
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1))
    finish(ax, "The regulatory gate is wide open",
           "US FDA AI/ML-enabled device authorizations per year — cumulative 1,451 by end-2025",
           "Source: FDA AI-enabled device list and public tallies. Selected years.")
    save(fig, os.path.join(FIG, "01_fda_velocity.png"))


# Fig 2 — the reimbursement wall (cleared vs paid)
def fig_reimbursement_wall():
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    bars = ["FDA-cleared\nAI devices", "with a permanent\nnational payment code"]
    vals = [1451, 3]
    ax.bar(bars, vals, color=[MUTE, ACCENT], width=0.5)
    ax.annotate("1,451", (0, 1451), textcoords="offset points", xytext=(0, 5),
                ha="center", fontsize=11, color=INK, fontweight="bold")
    ax.annotate("3", (1, 3), textcoords="offset points", xytext=(0, 5),
                ha="center", fontsize=11, color=ACCENT, fontweight="bold")
    ax.set_ylim(0, 1600)
    ax.set_ylabel("Count")
    finish(ax, "The payment gate is nearly shut",
           "Clearance is a commodity; a durable reimbursement code is not (end-2025)",
           "Source: FDA list; public reimbursement policy review, Jan 2026.")
    save(fig, os.path.join(FIG, "02_reimbursement_wall.png"))


# Fig 3 — Phase I vs Phase II PoS: AI molecules vs historic (the wrong-phase edge)
def fig_pos_split():
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    groups = ["Phase I\n(safety / chemistry)", "Phase II\n(efficacy / biology)"]
    hist = [52, 29]
    ai = [85, 40]
    x = np.arange(len(groups)); w = 0.36
    ax.bar(x - w/2, hist, w, label="Historic base rate", color=MUTE)
    ax.bar(x + w/2, ai, w, label="AI-discovered molecules", color=ACCENT)
    for xi, h, a in zip(x, hist, ai):
        ax.annotate(f"{h}%", (xi - w/2, h), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=9, color=INK)
        ax.annotate(f"~{a}%", (xi + w/2, a), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=9, color=ACCENT)
    ax.set_xticks(x); ax.set_xticklabels(groups)
    ax.set_ylabel("Phase transition success (%)")
    ax.set_ylim(0, 100)
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    ax.annotate("the AI edge collapses\nback to baseline", xy=(1.18, 40), xytext=(1.05, 68),
                fontsize=9, color=INK, alpha=0.8, ha="left")
    finish(ax, "AI wins the cheap phase, not the expensive one",
           "AI solved chemistry (Phase I); the biology wall (Phase II) is unmoved",
           "Source: published AI-drug clinical analysis; industry base rates. Estimates.")
    save(fig, os.path.join(FIG, "03_pos_split.png"))


# Fig 4 — TAM vs measured spend (the 20-25x gap)
def fig_tam_gap():
    fig, ax = plt.subplots(figsize=(6.8, 4.2))
    labels = ["Top-down\n'healthcare AI market'\n(2025)", "Bottom-up\nmeasured software\nspend (2025)"]
    vals = [32, 1.4]
    ax.bar(labels, vals, color=[MUTE, ACCENT], width=0.5)
    ax.annotate("~$27-37bn", (0, 32), textcoords="offset points", xytext=(0, 5), ha="center", fontsize=10, color=INK, fontweight="bold")
    ax.annotate("~$1.4bn", (1, 1.4), textcoords="offset points", xytext=(0, 5), ha="center", fontsize=10, color=ACCENT, fontweight="bold")
    ax.set_ylabel("US$ bn")
    ax.set_ylim(0, 40)
    ax.annotate("~20-25x gap\nsignal is rate-of-change,\nnot the TAM point", xy=(1, 1.4), xytext=(0.55, 20),
                fontsize=9.5, color=INK, alpha=0.85, ha="left")
    finish(ax, "The headline TAM is not the number that matters",
           "What the market quotes vs what was actually invoiced",
           "Source: market-sizing houses vs venture-tracked software spend, 2025.")
    save(fig, os.path.join(FIG, "04_tam_gap.png"))


# Fig 5 — archetype value-capture grid (growth quality x moat duration)
def fig_archetype_grid():
    fig, ax = plt.subplots(figsize=(7.6, 5.2))
    # (name, growth_quality 0-5, moat_duration_yrs, pass/cond/fail)
    data = [
        ("Data-licensing /\ndata-attach", 4.3, 7.5, "pass"),
        ("Payment-rail /\ncode ownership", 3.8, 6.5, "pass"),
        ("Workflow\nownership", 3.5, 5.0, "cond"),
        ("Pharma-dist /\nown-pipeline", 2.6, 2.5, "cond"),
        ("Regulated SaMD\non bare clearance", 2.2, 0.4, "fail"),
        ("Bare model /\nraw-data flywheel", 1.8, 0.8, "fail"),
    ]
    cmap = {"pass": GOOD, "cond": COND, "fail": MUTE}
    for name, gq, md, v in data:
        ax.scatter(md, gq, s=200, color=cmap[v], edgecolor=INK, linewidth=0.6, zorder=3)
    ax.set_xlabel("Moat duration (years it plausibly compounds)")
    ax.set_ylabel("Growth quality (incremental ROIC, cash conversion)")
    ax.set_xlim(-0.8, 10.2); ax.set_ylim(0.8, 5.4)
    place_labels(ax, [d[2] for d in data], [d[1] for d in data], [d[0].replace("\n", " ") for d in data], fontsize=8.5)
    # legend proxies
    for lab, c in [("passes", GOOD), ("conditional", COND), ("fails as a moat", MUTE)]:
        ax.scatter([], [], color=c, edgecolor=INK, linewidth=0.6, label=lab, s=120)
    ax.legend(frameon=False, fontsize=8.5, loc="lower right")
    finish(ax, "Value accrues by archetype, not by sub-sector",
           "The six revenue archetypes on growth quality vs how long the moat lasts",
           "Source: study Ch4 (taxonomy) x Ch5 (moat audit).")
    save(fig, os.path.join(FIG, "05_archetype_grid.png"))


# Fig 6 — sub-sector: measured spend vs top-down TAM
def fig_subsector():
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    subs = ["Drug\ndiscovery", "Diagnostics\n/ imaging", "Clinical\ndocumentation", "RCM /\nadmin", "Monitoring"]
    measured = [0.0, 0.4, 0.6, 0.45, 0.0]   # 2025 measured, $bn (n/a shown as ~0)
    tam = [11, 20, 19.6, 25.7, 8.4]          # top-down $bn (2030-ish / TAM)
    x = np.arange(len(subs)); w = 0.36
    ax.bar(x - w/2, tam, w, label="Top-down TAM", color=MUTE)
    ax.bar(x + w/2, measured, w, label="2025 measured spend", color=ACCENT)
    ax.set_xticks(x); ax.set_xticklabels(subs, fontsize=9)
    ax.set_ylabel("US$ bn")
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    finish(ax, "Every sub-sector shows the same gap",
           "The runway is real; the realized spend is a fraction of the TAM quote",
           "Source: study Ch1. Drug-discovery/monitoring measured spend not separately invoiced.")
    save(fig, os.path.join(FIG, "06_subsector_gap.png"))


for f in (fig_fda_velocity, fig_reimbursement_wall, fig_pos_split, fig_tam_gap, fig_archetype_grid, fig_subsector):
    f()
print("rendered:", sorted(os.listdir(FIG)))
