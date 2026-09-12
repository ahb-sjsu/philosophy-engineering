"""Figure 1: blast-radius distribution, brownfield deployment.
Reads blast_distribution.json produced by blast_distribution.py. No hand-typed numbers.
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

here = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(here, "blast_distribution.json")))["brownfield"]

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif"],
    "font.size": 9, "axes.linewidth": 0.8,
})

vals = sorted(d["radii"].values(), reverse=True)
n = len(vals)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.9))

# (a) rank-ordered, symlog so zeros are visible
ax1.plot(range(1, n + 1), vals, marker="o", markersize=2.5, linewidth=0.9,
         color="black", markerfacecolor="none")
ax1.set_yscale("symlog", linthresh=1)
ax1.set_xlabel("claim, ranked by blast radius")
ax1.set_ylabel("claims suspended")
ax1.set_title("(a) distribution over all %d claims" % n, fontsize=9)
zero_start = next(i for i, v in enumerate(vals) if v == 0) + 1
ax1.axvline(zero_start, color="black", linestyle="--", linewidth=0.7)
ax1.annotate("%.0f%% suspend nothing" % (d["frac_zero"] * 100),
             xy=(zero_start, 1), xytext=(zero_start + 6, 6),
             fontsize=7.5, arrowprops=dict(arrowstyle="->", lw=0.6))
ax1.grid(alpha=0.25, linewidth=0.5)

# (b) the tail, named
top = d["top10"][:8]
labels = [t[0].replace("GE-", "") for t in top][::-1]
heights = [t[1] for t in top][::-1]
bars = ax2.barh(range(len(top)), heights, color="0.75", edgecolor="black", linewidth=0.7)
for i, b in enumerate(bars):
    if "DEF" in labels[i]:
        b.set_hatch("///")
ax2.set_yticks(range(len(top)))
ax2.set_yticklabels(labels, fontsize=7.5)
ax2.set_xlabel("claims suspended")
ax2.set_title("(b) the tail is definitional (hatched)", fontsize=9)
ax2.grid(axis="x", alpha=0.25, linewidth=0.5)

fig.tight_layout()
out = os.path.join(here, "fig_blast.pdf")
fig.savefig(out, dpi=300, bbox_inches="tight")
fig.savefig(out.replace(".pdf", ".png"), dpi=300, bbox_inches="tight")
print("wrote", out)
print("n=%d mean=%.3f median=%d max=%d zero=%.1f%% le2=%.1f%% edges=%d max_indeg=%d"
      % (n, d["mean"], d["median"], d["max"], d["frac_zero"]*100, d["frac_le2"]*100,
         d["n_edges"], d["max_indegree"]))
