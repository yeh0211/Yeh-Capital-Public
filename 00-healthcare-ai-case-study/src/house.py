"""House chart style for the Yeh Capital public studies.

Cream background, near-black ink, one restrained accent, a supply gray-green.
Monochrome-first, zero chartjunk, institutional restraint (WSJ/FT/Economist).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CREAM = "#faf8f3"
INK = "#1c1a17"
ACCENT = "#9c3d2e"   # restrained brick red (emphasis series in findings charts)
SUPPLY = "#7a8a78"   # gray-green
MUTE = "#b8b2a7"     # muted tan-gray for secondary

# Business-quality semantics (green = good, per house preference)
GOOD = "#3f7a52"     # restrained hunter green
COND = "#c0913f"     # muted amber/gold
BAD = "#9c3d2e"      # clay red = not a good business


def style():
    plt.rcParams.update({
        "figure.facecolor": CREAM,
        "axes.facecolor": CREAM,
        "savefig.facecolor": CREAM,
        "font.family": "DejaVu Sans",
        "font.size": 11,
        "axes.edgecolor": INK,
        "axes.linewidth": 0.8,
        "axes.labelcolor": INK,
        "axes.titlecolor": INK,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.color": INK,
        "ytick.color": INK,
        "text.color": INK,
        "axes.grid": False,
    })


def finish(ax, title=None, subtitle=None, source=None):
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", loc="left", pad=14)
    if subtitle:
        ax.annotate(subtitle, xy=(0, 1.015), xycoords="axes fraction",
                    fontsize=9.5, color=INK, alpha=0.75, ha="left", va="bottom")
    if source:
        ax.annotate(source, xy=(0, -0.16), xycoords="axes fraction",
                    fontsize=8, color=INK, alpha=0.55, ha="left", va="top")
    ax.tick_params(length=3)


def save(fig, path):
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=CREAM)
    plt.close(fig)


def _overlap(a, b, pad=2.0):
    return not (a[2] + pad < b[0] or b[2] + pad < a[0] or a[3] + pad < b[1] or b[3] + pad < a[1])


def place_labels(ax, xs, ys, texts, fontsize=7, color=INK, marker_px=7):
    """Greedy non-overlapping label placement in display space, with leader lines.
    Places each label at the first candidate offset that collides with neither an
    already-placed label nor any point marker. No external dependency."""
    fig = ax.figure
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    dpi = fig.dpi
    pts = ax.transData.transform(list(zip(xs, ys)))
    inv = ax.transData.inverted()

    def wh(t):
        tmp = ax.text(0, 0, t, fontsize=fontsize)
        bb = tmp.get_window_extent(r)
        tmp.remove()
        return bb.width, bb.height

    cand = [(7, 0), (7, 7), (0, 9), (-7, 7), (-7, 0), (7, -7), (0, -9), (-7, -7),
            (15, 0), (15, 10), (0, 15), (-15, 10), (-15, 0), (15, -10), (0, -15), (-15, -10),
            (24, 6), (-24, 6), (24, -6), (-24, -6), (0, 22), (0, -22)]
    placed = [(px - marker_px, py - marker_px, px + marker_px, py + marker_px) for px, py in pts]
    order = sorted(range(len(texts)), key=lambda i: (-pts[i][1], pts[i][0]))
    for i in order:
        px, py = pts[i]
        w, h = wh(texts[i])
        chosen = cand[-1]
        box = None
        for dx, dy in cand:
            ox, oy = dx * dpi / 72.0, dy * dpi / 72.0
            x0 = px + ox if dx >= 0 else px + ox - w
            y0 = py + oy - h / 2
            b = (x0, y0, x0 + w, y0 + h)
            if not any(_overlap(b, pb) for pb in placed):
                chosen, box = (dx, dy), b
                break
        if box is None:
            dx, dy = chosen
            ox, oy = dx * dpi / 72.0, dy * dpi / 72.0
            x0 = px + ox if dx >= 0 else px + ox - w
            box = (x0, py + oy - h / 2, x0 + w, py + oy + h / 2)
        placed.append(box)
        dx, dy = chosen
        xd, yd = inv.transform((px, py))
        far = abs(dx) > 8 or abs(dy) > 8
        ax.annotate(texts[i], (xd, yd), textcoords="offset points", xytext=(dx, dy),
                    ha="left" if dx >= 0 else "right", va="center", fontsize=fontsize, color=color,
                    arrowprops=dict(arrowstyle="-", lw=0.4, color=color, alpha=0.35) if far else None,
                    zorder=8)
