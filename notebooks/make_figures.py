import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, Normalize

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
OUT = os.path.join(HERE, "figures")
os.makedirs(OUT, exist_ok=True)

INK, INK2, MUTED, GRID = "#0b0b0b", "#52514e", "#898781", "#e1e0d9"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
HEAT = LinearSegmentedColormap.from_list(
    "heat", ["#fde3d5", "#f8a983", "#eb6834", "#a84119", "#6b280f"])

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 10,
    "axes.edgecolor": MUTED,
    "axes.labelcolor": INK2,
    "axes.titlecolor": INK,
    "axes.titlesize": 12,
    "axes.titleweight": "bold",
    "axes.titlelocation": "left",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "xtick.labelcolor": INK2,
    "ytick.labelcolor": INK2,
    "grid.color": GRID,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "savefig.bbox": "tight",
    "savefig.dpi": 200,
})

d = pd.read_csv(os.path.join(DATA, "city_temps.csv"))
cities = d.groupby("city").agg(country=("country", "first"),
                               lat=("lat", "first"), lon=("lon", "first")).reset_index()

mean = d.groupby(["city", "scenario", "year"]).warming_c.mean().rename("w").reset_index()
glob = mean.groupby(["scenario", "year"]).w.mean().rename("w").reset_index()

end = (mean[(mean.scenario == "ssp585") & mean.year.between(2090, 2100)]
       .groupby("city").w.mean().sort_values())
end126 = (mean[(mean.scenario == "ssp126") & mean.year.between(2090, 2100)]
          .groupby("city").w.mean())
VMAX = float(end.max())


def series(city, scen, model=None):
    src = d if model is None else d[d.model == model]
    g = (src[src.city == city] if city else src)
    hist = g[g.scenario == "historical"].groupby("year").warming_c.mean()
    fut = g[g.scenario == scen].groupby("year").warming_c.mean()
    s = pd.concat([hist, fut]).sort_index()
    return s.index.values, s.values


def spread(ys, gap):
    order = sorted(range(len(ys)), key=lambda i: ys[i])
    out = list(ys)
    for k in range(1, len(order)):
        a, b = order[k - 1], order[k]
        if out[b] - out[a] < gap:
            out[b] = out[a] + gap
    return out


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p)
    plt.close(fig)
    print("wrote", os.path.relpath(p, HERE))


# 1 ranked dot chart
fig, ax = plt.subplots(figsize=(7.5, 8.2))
y = np.arange(len(end))
ax.hlines(y, 0, end.values, color=GRID, lw=2.2, zorder=1)
ax.scatter(end.values, y, c=end.values, cmap=HEAT, norm=Normalize(0, VMAX),
           s=70, zorder=3, edgecolor="white", linewidth=1.2)
for yi, (c, v) in enumerate(end.items()):
    ax.text(v + 0.12, yi, f"{v:.1f}", va="center", fontsize=8.5, color=INK2)
ax.set_yticks(y, end.index, fontsize=9)
ax.set_xlim(0, VMAX + 0.8)
ax.set_xlabel("Warming in 2090 to 2100 vs each city's 1981 to 2010 mean (C)")
ax.set_title("Our 30-city average hides a 2.4 times spread")
ax.tick_params(left=False)
ax.grid(axis="x", lw=0.6)
ax.set_axisbelow(True)
save(fig, "fig1_city_ranking.png")

# 2 two pathways
fig, ax = plt.subplots(figsize=(8.5, 4.8))
for scen, color, lab in [("ssp585", SERIES[1], "SSP5-8.5 high emissions"),
                         ("ssp126", SERIES[0], "SSP1-2.6 low emissions")]:
    xs, ys = series(None, scen)
    ax.plot(xs, ys, color=color, lw=2, label=lab)
    ax.text(xs[-1] + 1.5, ys[-1], f"{ys[-1]:.1f}C", color=color, va="center", fontsize=9.5)
ax.axvline(2014, color=MUTED, lw=0.8, ls=":")
ax.text(2012, ax.get_ylim()[1] * 0.96, "history", ha="right", fontsize=8.5, color=MUTED)
ax.set_xlim(1950, 2112)
ax.set_xlabel("Year")
ax.set_ylabel("Mean warming across 30 cities (C)")
ax.set_title("Everyone agrees on the direction")
ax.legend(frameon=False, loc="upper left", fontsize=9)
ax.grid(lw=0.6)
ax.set_axisbelow(True)
save(fig, "fig2_pathways.png")

# 3 world map
world = json.load(open(os.path.join(DATA, "world_countries.json")))
fig, ax = plt.subplots(figsize=(11, 5.6))
for f in world["features"]:
    geom = f["geometry"]
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    for poly in polys:
        ring = np.array(poly[0])
        if ring[:, 0].max() - ring[:, 0].min() > 180:
            continue
        ax.fill(ring[:, 0], ring[:, 1], facecolor=GRID, edgecolor="white", lw=0.3, zorder=1)
cw = cities.assign(w=cities.city.map(
    mean[(mean.scenario == "ssp585") & (mean.year == 2095)].set_index("city").w))
sc = ax.scatter(cw.lon, cw.lat, c=cw.w, cmap=HEAT, norm=Normalize(0, VMAX),
                s=95, zorder=3, edgecolor="white", linewidth=1.4)
for _, r in cw.iterrows():
    off = {"San Diego": (-12, -16), "Anchorage": (10, 8), "Tehran": (10, 7),
           "Cape Town": (10, -14), "Singapore": (12, 6)}
    if r.city in off:
        ha = "right" if off[r.city][0] < 0 else "left"
        ax.annotate(f"{r.city} {r.w:.1f}", (r.lon, r.lat), textcoords="offset points",
                    xytext=off[r.city], ha=ha, fontsize=8.5, color=INK)
ax.set_xlim(-180, 180)
ax.set_ylim(-60, 85)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("Warming in 2095 under SSP5-8.5, by city")
cb = fig.colorbar(sc, ax=ax, shrink=0.6, pad=0.01)
cb.set_label("Warming (C)", color=INK2, fontsize=9)
cb.outline.set_visible(False)
save(fig, "fig3_world_map.png")

# 4 model disagreement
CITY = "San Diego"
fig, ax = plt.subplots(figsize=(8.5, 4.8))
models = sorted(d.model.unique())
ends = []
for i, m in enumerate(models):
    xs, ys = series(CITY, "ssp585", m)
    sm = pd.Series(ys).rolling(11, center=True, min_periods=3).mean().values
    ax.plot(xs, ys, color=SERIES[i], lw=0.8, alpha=0.22)
    ax.plot(xs, sm, color=SERIES[i], lw=2.2, label=m)
    ends.append(sm[-1])
for i, (m, y) in enumerate(zip(models, spread(ends, 0.42))):
    ax.text(xs[-1] + 3, y, m, color=SERIES[i], va="center", fontsize=9)
ax.set_xlim(1950, 2150)
ax.set_xlabel("Year")
ax.set_ylabel(f"{CITY} warming (C)")
ax.set_title(f"The models do not agree on how much: {CITY}, SSP5-8.5", pad=26)
ax.text(0, 1.012, "thin lines are annual values, thick lines are an 11 year mean",
        transform=ax.transAxes, fontsize=8.5, color=MUTED)
ax.legend(frameon=False, loc="upper left", fontsize=9)
ax.grid(lw=0.6)
ax.set_axisbelow(True)
save(fig, "fig4_model_spread.png")

# 5 pathway choice per city
gap = (end - end126.reindex(end.index)).sort_values()
fig, ax = plt.subplots(figsize=(7.5, 8.2))
y = np.arange(len(gap))
lo = end126.reindex(gap.index).values
hi = end.reindex(gap.index).values
ax.hlines(y, lo, hi, color=GRID, lw=2.2, zorder=1)
ax.scatter(lo, y, s=62, color=SERIES[0], zorder=3, edgecolor="white", linewidth=1.2,
           label="SSP1-2.6 low emissions")
ax.scatter(hi, y, s=62, color=SERIES[1], zorder=3, edgecolor="white", linewidth=1.2,
           label="SSP5-8.5 high emissions")
for yi, g in enumerate(gap.values):
    ax.text(hi[yi] + 0.15, yi, f"{g:.1f} avoided", va="center", fontsize=8, color=INK2)
ax.set_yticks(y, gap.index, fontsize=9)
ax.set_xlim(0, VMAX + 1.9)
ax.set_xlabel("Warming in 2090 to 2100 (C)")
ax.set_title("Cutting emissions helps every city, but not equally")
ax.tick_params(left=False)
ax.legend(frameon=False, loc="lower right", fontsize=9)
ax.grid(axis="x", lw=0.6)
ax.set_axisbelow(True)
save(fig, "fig5_pathway_choice.png")

# 6 small multiples
PICK = ["Tehran", "Anchorage", "Moscow", "San Diego", "Singapore", "Cape Town"]
fig, axes = plt.subplots(2, 3, figsize=(11, 5.6), sharex=True, sharey=True)
for ax, c in zip(axes.flat, PICK):
    for scen, color in [("ssp585", SERIES[1]), ("ssp126", SERIES[0])]:
        xs, ys = series(c, scen)
        ax.plot(xs, ys, color=color, lw=1.6)
    ax.set_title(f"{c}  {end[c]:.1f}C", fontsize=10.5)
    ax.grid(lw=0.6)
    ax.set_axisbelow(True)
for ax in axes[1]:
    ax.set_xlabel("Year")
for ax in axes[:, 0]:
    ax.set_ylabel("Warming (C)")
fig.suptitle("Same two pathways, six very different outcomes", x=0.005, ha="left",
             fontsize=12, fontweight="bold", color=INK)
handles = [plt.Line2D([], [], color=SERIES[1], lw=2, label="SSP5-8.5 high emissions"),
           plt.Line2D([], [], color=SERIES[0], lw=2, label="SSP1-2.6 low emissions")]
fig.legend(handles=handles, frameon=False, fontsize=9.5, ncol=2,
           loc="upper right", bbox_to_anchor=(0.995, 1.02))
fig.tight_layout(rect=[0, 0, 1, 0.95])
save(fig, "fig6_small_multiples.png")

print("\nnumbers used in the writeup")
print("  spread ratio:", round(end.max() / end.min(), 2))
print("  global ssp585:", round(glob[(glob.scenario == 'ssp585') & glob.year.between(2090, 2100)].w.mean(), 2))
print("  global ssp126:", round(glob[(glob.scenario == 'ssp126') & glob.year.between(2090, 2100)].w.mean(), 2))
