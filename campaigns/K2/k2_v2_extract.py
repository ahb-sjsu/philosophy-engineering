#!/usr/bin/env python
"""K2 rubric v2 coding: model coders answer RUBRIC-v2's factual questions; k2_v2_rules computes the checks.

DEVELOPMENT UNITS ONLY until RUBRIC-v2.md and k2_v2_rules.py are committed and hashed (RUBRIC-v2-PLAN
Section 3 step 5): the script refuses any text under raw/v2/ (the held-out set); held-out coding gets its
own entry point after the commit.

Runs on Atlas against the NRP ELLM gateway (token from ~/.primer.env, never printed). Coders, settings and
units are given on the command line and recorded in every output. One call in flight per model; the
caller runs at most two models at a time.

Units:
  psych   the 22 v0/v1 development units (raw/fulltext/blinded), target from devset/claims_dev.csv with
          the replication project's name removed (7.4.1 item 4)
  v2dev   v2 development papers (raw/v2dev/blinded; v2dev2: raw/v2dev2, k2_v2dev_draw.py), target from SCORE's claim fields claim3a, claim3b
          and claim4 (d9x6s, read on Atlas; author fields never read), redacted like the unit

    python3 k2_v2_extract.py --units psych,v2dev --models gpt-oss,gemma --reps 2 --out /archive/experiments/k2/v2dev_r1
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import random
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from k2_v2_rules import checks, clean

HERE = Path(__file__).resolve().parent
K2 = Path("/archive/experiments/k2")
GATEWAY = "https://ellm.nrp-nautilus.io/v1/chat/completions"
RUBRIC = "RUBRIC-v2.md"
RULES = "k2_v2_rules.py"
SEED = 20261026
TEMPERATURE = 0.2
CALL_DEADLINE_S = 900
CLAIMS_D9X6S = K2 / "raw/replicats_d9x6s/phase_one_singletrace_claims_anonymised.csv"
CLAIM_COLS = (("Hypothesis", "claim3a_concretehyp"), ("Test", "claim3b_testspec"), ("Reported result", "claim4_inftest"))
# a target must not point to the replication (7.4.1 item 4); checked on every prompt
FORBIDDEN = re.compile(r"(?i:many\s+labs|replicat|reproducibility\s+project)|RP:P|SCORE|repliCATS")

SYSTEM = ("You extract facts from one published empirical article about one claim, answering fixed questions "
          "from the text given and nothing else. Copy quotes exactly from the text. Reason briefly. Answer with "
          "one JSON object and no other text.")

OUTPUT = """## Output

Return exactly this JSON shape, one entry for every question Q1.1 to Q6.2, Q2.3 included (answer Q4.1 to Q4.3 with
"not_reported", "na" and "no" when Q1.1 is not researcher_assigned):
{"recognition": {"recognizes_study": true|false, "knows_replication_outcome": true|false},
 "answers": {"Q1.1": {"answer": "<one allowed answer>", "quote": "<exact quote, or empty for absences>"},
             ...,
             "Q6.2": {"answer": "...", "quote": "..."}}}
Numbers are given as numbers (130, 0.82). A quote is one passage copied exactly (short: under 40 words where possible), with no
ellipsis.
"""


def rubric_prompt() -> str:
    text = (HERE / RUBRIC).read_text(encoding="utf-8")
    parts = re.split(r"(?m)^## ", text)
    keep = [p for p in parts if p.startswith("0.") or p.startswith("1.")]
    assert len(keep) == 2, "RUBRIC-v2.md sections 0 and 1 not found"
    return "\n\n".join("## " + p.strip() for p in keep)


def psych_units() -> list[dict]:
    man = list(csv.DictReader(open(HERE / "devset" / "intake_manifest.csv", encoding="utf-8")))
    claims = {r["dev_id"]: r for r in csv.DictReader(open(HERE / "devset" / "claims_dev.csv", encoding="utf-8"))}
    out = []
    for r in man:
        if r["status"] != "blinded":
            continue
        c = claims[r["dev_id"]]
        claim = re.sub(r"Many Labs \d+ compared", "The original study compared", c["claim"])
        where = (f"Study {c['study']} of this article (if the article reports a single study, that study)"
                 if c["study"] else "the study in this article that tests it")
        test = f" The original test: {c['focal_test']}." if c["focal_test"] else ""
        out.append({"unit": r["dev_id"], "set": "psych", "path": K2 / "raw/fulltext/blinded" / f"{r['dev_id']}.txt",
                    "target": f"The claim, in {where}: {claim}{test}"})
    return out


def v2dev_units(sub: str = "v2dev") -> list[dict]:
    sys.path.insert(0, str(HERE))
    from k2_blinding import redact
    meta = json.loads((K2 / "raw" / sub / "meta.json").read_text(encoding="utf-8"))
    rows: dict[str, list] = {}
    with open(CLAIMS_D9X6S, encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            if r["paper_id"] in meta:
                rows.setdefault(r["paper_id"], []).append({k: r.get(k, "") for _, k in CLAIM_COLS})
    out = []
    for pid in sorted(meta):
        path = K2 / "raw" / sub / "blinded" / f"{pid}.txt"
        if not path.exists() or pid not in rows:
            continue
        r = rows[pid][0]
        parts = [f"{lab}: {r[col].strip()}" for lab, col in CLAIM_COLS if r[col].strip() and r[col].strip().lower() != "na"]
        out.append({"unit": pid, "set": sub, "path": path, "target": redact(" ".join(parts), meta[pid])})
    return out


def call(model, system, user, token, max_tokens, extra=None):
    body = {"model": model, "temperature": TEMPERATURE, "max_tokens": max_tokens, "stream": True,
            "stream_options": {"include_usage": True}, "response_format": {"type": "json_object"},
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    data = json.dumps({**body, **(extra or {})}).encode()
    req = urllib.request.Request(GATEWAY, data=data, headers={"Authorization": "Bearer " + token,
                                                             "Content-Type": "application/json"})
    content, reasoning, out, finish = [], 0, {}, None
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=300) as r:
        for line in r:
            # the socket timeout is on silence only, and the gateway can keep a dead stream alive (gemma,
            # 2026-10-27: one call open 50 min), so every call also has a wall-clock deadline
            if time.time() - t0 > CALL_DEADLINE_S:
                raise TimeoutError(f"call exceeded {CALL_DEADLINE_S} s")
            line = line.decode("utf-8", "replace").strip()
            if not line.startswith("data:") or line.endswith("[DONE]"):
                continue
            j = json.loads(line[5:])
            out["model"] = j.get("model", out.get("model"))
            if j.get("usage"):
                out["usage"] = j["usage"]
            for ch in j.get("choices") or []:
                d = ch.get("delta") or {}
                content.append(d.get("content") or "")
                reasoning += len(d.get("reasoning_content") or d.get("reasoning") or "")
                finish = ch.get("finish_reason") or finish
    out.update(content="".join(content), reasoning_chars=reasoning, finish_reason=finish)
    return out


def parse(content: str) -> dict:
    content = re.sub(r"^```(?:json)?|```$", "", content.strip(), flags=re.M).strip()
    a, b = content.find("{"), content.rfind("}")
    return json.loads(content[a:b + 1])


def job(u, model, rep, token, rubric, max_tokens, dest, meta, extra=None):
    if dest.exists():
        return "skip"
    text = Path(u["path"]).read_text(encoding="utf-8")
    assert not FORBIDDEN.search(u["target"]), f"{u['unit']}: target names the replication"
    user = "\n\n".join([rubric, OUTPUT, "## Claim", u["target"], "## Article text (blinded)", text])
    rec = {**meta, "unit": u["unit"], "set": u["set"], "model_requested": model, "rep": rep,
           "prompt_sha256": hashlib.sha256(user.encode()).hexdigest(), "attempts": []}
    for attempt in range(3):
        t0 = time.time()
        try:
            r = call(model, SYSTEM, user, token, max_tokens, extra)
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
            rec["attempts"].append({"error": str(e)[:300], "seconds": round(time.time() - t0, 1)})
            time.sleep(30 * (attempt + 1))
            continue
        a = {"seconds": round(time.time() - t0, 1), "model_returned": r.get("model"), "usage": r.get("usage"),
             "reasoning_chars": r["reasoning_chars"], "finish_reason": r["finish_reason"], "content": r["content"]}
        rec["attempts"].append(a)
        try:
            p = parse(r["content"])
        except (ValueError, AttributeError) as e:
            a["parse_error"] = str(e)[:200]
            continue
        rec["recognition"] = p.get("recognition")
        rec["answers_raw"] = p.get("answers") or {}
        ans, why = clean(rec["answers_raw"], text)
        rec["answers"], rec["voided"] = ans, why
        rec["scored"] = checks(ans)
        break
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(rec, indent=1), encoding="utf-8")
    return "ok" if "scored" in rec else "FAILED"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--units", required=True, help="comma list of: psych, v2dev")
    ap.add_argument("--models", required=True)
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--max-tokens", type=int, default=16000)
    ap.add_argument("--limit", type=int, default=0, help="units per set (smoke runs)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--extra", default="", help='JSON merged into the request, e.g. {"chat_template_kwargs": {"enable_thinking": false}}')
    a = ap.parse_args()
    units = []
    for s in a.units.split(","):
        units += {"psych": psych_units, "v2dev": v2dev_units,
                  "v2dev2": lambda: v2dev_units("v2dev2")}[s]()[:a.limit or None]
    for u in units:
        if "/raw/v2/" in str(u["path"]):
            sys.exit("REFUSED: held-out text; v2 is not committed")
    token = None
    for line in open(os.path.expanduser("~/.primer.env")):
        m = re.match(r"\s*(?:export\s+)?NRP_LLM_TOKEN\s*=\s*['\"]?([^'\"\n]*)", line)
        if m:
            token = m.group(1)
    assert token, "NRP_LLM_TOKEN not found"
    rubric = rubric_prompt()
    meta = {"rubric": RUBRIC, "rubric_sha256": hashlib.sha256((HERE / RUBRIC).read_bytes()).hexdigest(),
            "rules_sha256": hashlib.sha256((HERE / RULES).read_bytes()).hexdigest(),
            "temperature": TEMPERATURE, "max_tokens": a.max_tokens, "seed": SEED,
            "extra": json.loads(a.extra) if a.extra else None}
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    models = a.models.split(",")
    (out / f"plan_{'_'.join(models)}.json").write_text(json.dumps(
        {**meta, "models": models, "reps": a.reps, "units": [u["unit"] for u in units]}, indent=1))
    print(f"{len(units)} units x {len(models)} models x {a.reps} reps", flush=True)

    def run_model(m):
        order = [(u, rep) for rep in range(1, a.reps + 1) for u in units]
        random.Random(f"{SEED}|{m}").shuffle(order)
        for u, rep in order:
            try:
                st = job(u, m, rep, token, rubric, a.max_tokens, out / "raw" / m / f"{u['unit']}_r{rep}.json", meta,
                         meta["extra"])
            except Exception as e:  # one bad call must not stop the model's queue
                st = f"ERROR {type(e).__name__}: {str(e)[:200]}"
            print(m, u["unit"], rep, st, flush=True)

    with ThreadPoolExecutor(len(models)) as ex:
        list(ex.map(run_model, models))
    print("DONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
