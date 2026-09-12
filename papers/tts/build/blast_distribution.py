"""Compute the blast-radius distribution over every claim in both deployments.

Reads the live ledgers via pe_lint's own parsers. Emits JSON + a figure.
No number in the paper is typed by hand; all come from this script's output.
"""
import json, os, sys, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "tools"))
import pe_lint

LEDGERS = {
    "brownfield": (r"C:\source\geometric-ethics\ledger", "native"),
    "greenfield": (r"C:\source\geometric-observation", "markdown"),
}

def load(root, kind):
    if kind == "native":
        return pe_lint.parse_native_ledger(root)
    claims, _registry, _notes = pe_lint.parse_markdown_ledger(root)
    return claims

out = {}
for name, (root, kind) in LEDGERS.items():
    claims = load(root, kind)
    radii = {}
    for cid in claims:
        br = pe_lint.blast_radius(claims, cid)
        radii[cid] = len(br.get("suspended", []))
    vals = sorted(radii.values())
    n = len(vals)
    indeg = collections.Counter()
    for c in claims.values():
        for d in c.uses:
            if d in claims:
                indeg[d] += 1
    out[name] = {
        "root": root,
        "n_claims": n,
        "radii": radii,
        "values": vals,
        "zero": sum(1 for v in vals if v == 0),
        "le2": sum(1 for v in vals if v <= 2),
        "max": max(vals) if vals else 0,
        "mean": round(sum(vals) / n, 3) if n else 0,
        "median": vals[n // 2] if n else 0,
        "frac_zero": round(sum(1 for v in vals if v == 0) / n, 4) if n else 0,
        "frac_le2": round(sum(1 for v in vals if v <= 2) / n, 4) if n else 0,
        "top10": sorted(radii.items(), key=lambda kv: -kv[1])[:10],
        "n_edges": sum(len([d for d in c.uses if d in claims]) for c in claims.values()),
        "max_indegree": max(indeg.values()) if indeg else 0,
    }

here = os.path.dirname(__file__)
with open(os.path.join(here, "blast_distribution.json"), "w") as fh:
    json.dump(out, fh, indent=2)

for name, d in out.items():
    print(f"[{name}] n={d['n_claims']} edges={d['n_edges']} "
          f"mean={d['mean']} median={d['median']} max={d['max']} "
          f"zero={d['zero']} ({d['frac_zero']:.1%}) le2={d['le2']} ({d['frac_le2']:.1%}) "
          f"max_indeg={d['max_indegree']}")
    print(f"   top: {[(k, v) for k, v in d['top10'][:5]]}")
