#!/usr/bin/env python
"""K2 pilot coding (registration 7.4): model auditors code the blinded units.

Owner's decisions, 2026-10-18:
  - coders: two model families on the NRP ELLM gateway, each coding every unit
    twice. glm-5 was the first choice; in the smoke run it spent its whole
    16,000-token budget reasoning on all four attempts and returned no answer,
    and the owner swapped it out. deepseek-v4-flash replaced it and failed the
    same way in the full run; the owner stopped it (2026-10-19) and, after a
    smoke run of minimax-m2 and qwen3, chose minimax-m2 at 8,000 tokens.
    Hosted aliases, so no revision can be pinned, and the gateway's model
    field is recorded per call (4.3 rule 5)
  - the person's leak read (4.1) happens before any human coder sees a text;
    model coders get the texts now, and each records recognition first
  - the claim is given as the target study only (RP:P study number, Many Labs
    effect name), not as claim wording: a stated pilot deviation from RUBRIC-v0
    section 0. The v1 pilot (K2_RUBRIC=RUBRIC-v1.md) gives the claim
    statement from devset/claims_dev.csv instead, as section 0 specifies

The prompt is the rubric's (K2_RUBRIC, default RUBRIC-v0.md) sections 0 and
A1 to A4 verbatim (Adjudication, Changes and Known gaps are not coder
instructions), with the four checks in an order
shuffled per call (4.3 rule 7). Item scores come from the model; check and
gate scores are computed here by the rubric's rules, and an item scored 1
without evidence is recoded U (the adjudicator rule). No replication outcome
is read or written anywhere in this script (7.1 consequence 5).

The unit-vs-full-text comparison (4.1) codes a subset from the redacted whole
body as well, once per model; a body with any residual leak is skipped.

Raw responses hold article quotes and stay on Atlas (OUT/raw); only scores go
to the repository (k2_pilot_summary.py). Resumable: an existing output is
skipped.

    python3 k2_pilot_code.py /archive/experiments/k2/raw/fulltext /archive/experiments/k2/pilot

The recorded run: gpt-oss under the default model list, beside
deepseek-v4-flash, at 48,000 tokens; then minimax-m2 alone with

    K2_PILOT_MODELS=minimax-m2 K2_PILOT_MAX_TOKENS=8000
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATEWAY = "https://ellm.nrp-nautilus.io/v1/chat/completions"
# deepseek-v4-flash replaced glm-5, and failed the same way in the full run (all
# 8 attempts on its first article reasoned past 48,000 tokens); stopped
# 2026-10-19, owner. K2_PILOT_MODELS overrides the list for smoke runs.
MODELS = os.environ.get("K2_PILOT_MODELS", "deepseek-v4-flash,gpt-oss").split(",")
REPS = 2
FULLTEXT_SUBSET = 6
TEMPERATURE = 0.2
# 16000 cut deepseek-v4-flash off mid-reasoning, item by item, on all 4 smoke
# attempts. minimax-m2 runs at 8000 (owner, 2026-10-19): its answers in the
# smoke used 2,000-3,000 tokens, and 3 of its 5 tries ran on to 48,000.
MAX_TOKENS = int(os.environ.get("K2_PILOT_MAX_TOKENS", "48000"))
SEED = 20261018
LIMIT = int(os.environ.get("K2_PILOT_LIMIT", "0"))  # smoke runs: calls per model
# The v0 pilot ran RUBRIC-v0 with study-number targets. RUBRIC-v1 restores the
# claim statement its section 0 names (devset/claims_dev.csv, k2_dev_claims.py).
RUBRIC = os.environ.get("K2_RUBRIC", "RUBRIC-v0.md")
CLAIM_TARGETS = RUBRIC != "RUBRIC-v0.md"
CLAIMS = ({r["dev_id"]: r for r in csv.DictReader(open(HERE / "devset" / "claims_dev.csv", encoding="utf-8"))}
          if CLAIM_TARGETS else {})
ITEMS = {"A1": ["A1.1", "A1.2", "A1.3", "A1.4"],
         "A2": ["A2.1", "A2.2", "A2.3", "A2.4"],
         "A3": ["A3.1", "A3.2", "A3.3", "A3.4"],
         "A4": ["A4.1", "A4.2", "A4.3", "A4.4", "A4.5"]}

SYSTEM = ("You are a methods auditor. You code one study of a published empirical "
          "article with a fixed rubric, from the text given and nothing else. "
          "Reason briefly: at most two or three sentences per item before you "
          "answer. Answer with one JSON object and no other text.")
# brief reasoning and JSON mode: in the smoke runs glm-5 and deepseek-v4-flash
# deliberated item by item past 16,000 and 48,000 tokens without answering,
# and one finished deepseek answer was invalid JSON (owner's choice, 2026-10-19)

OUTPUT = """## Output

First, before coding, record recognition: whether you recognize the study (its
authors, title or source) from the text, your guess of its identity if so, and
whether you know if this study was later replicated successfully. Do not state
what the replication found.

Then code every item for the target study. Each score is "0", "1", "U", or
"na" (A3 items only, when the study has no manipulation). Every "1" needs
evidence: a verbatim quote from the text in double quotes, or a located
absence ("Method, Participants: no exclusion rule stated").

Return exactly this JSON shape:
{"recognition": {"recognizes_study": true|false, "identity_guess": "..."|null,
                 "knows_replication_outcome": true|false},
 "a3_applicable": true|false,
 "items": {"A1.1": {"score": "0|1|U|na", "evidence": "..."}, ... one entry for
           each of A1.1-A1.4, A2.1-A2.4, A3.1-A3.4, A4.1-A4.5}}
"""
if CLAIM_TARGETS:  # RUBRIC-v1 allows na on A3.2 and other items that say so
    OUTPUT = OUTPUT.replace('"na" (A3 items only, when the study has no manipulation)',
                            '"na" (only where the rubric allows it)')
    OUTPUT = OUTPUT.replace("code every item for the target study", "code every item for the target claim")


def rubric_sections() -> tuple[str, dict[str, str]]:
    text = (HERE / RUBRIC).read_text(encoding="utf-8")
    parts = re.split(r"(?m)^## ", text)
    sec0 = next(p for p in parts if p.startswith("0."))
    checks = {p[:2]: p for p in parts if re.match(r"A[1-4] ", p)}
    assert set(checks) == set(ITEMS), checks.keys()
    return "## " + sec0, {k: "## " + v for k, v in checks.items()}


def target(dev: str, rpp: dict, ml: dict) -> str:
    if CLAIM_TARGETS:
        c = CLAIMS[dev]
        where = (f"Study {c['study']} of this article (if the article reports a single "
                 f"study, that study)") if c["study"] else "the study in this article that tests it"
        test = f" The original focal test: {c['focal_test']}." if c["focal_test"] else ""
        return (f"The replication targeted this claim, in {where}: {c['claim']}{test} "
                f"Code that claim.")
    if dev in rpp:
        n = rpp[dev]["study_number"]
        return (f"The replication targeted Study {n} of this article (if the article "
                f"reports a single study, that study). Code that study.")
    effs = sorted({r["effect"] for r in ml[dev]})
    return (f"The replication targeted the study in this article that tests the effect "
            f"labelled \"{' / '.join(effs)}\". Code that study.")


def prompt(dev, model, rep, text, tgt, sec0, checks):
    order = sorted(checks)
    rnd = random.Random(int(hashlib.sha256(f"{SEED}|{dev}|{model}|{rep}".encode()).hexdigest()[:12], 16))
    rnd.shuffle(order)
    body = "\n\n".join([sec0] + [checks[k] for k in order] + [OUTPUT,
                       "## Target", tgt, "## Article text (blinded)", text])
    return body, order


def call(model, user, token):
    """Streamed, so a long reasoning phase is not cut by a whole-reply timeout
    (glm-5 ran past 900 s unstreamed in the smoke run); the socket timeout is
    on silence only. Returns the shape of a non-streamed reply."""
    data = json.dumps({"model": model, "temperature": TEMPERATURE, "max_tokens": MAX_TOKENS,
                       "stream": True, "stream_options": {"include_usage": True},
                       "response_format": {"type": "json_object"},
                       "messages": [{"role": "system", "content": SYSTEM},
                                    {"role": "user", "content": user}]}).encode()
    req = urllib.request.Request(GATEWAY, data=data, headers={
        "Authorization": "Bearer " + token, "Content-Type": "application/json"})
    content, reasoning, out = [], 0, {"choices": []}
    finish = None
    with urllib.request.urlopen(req, timeout=300) as r:
        for line in r:
            line = line.decode("utf-8", "replace").strip()
            if not line.startswith("data:") or line.endswith("[DONE]"):
                continue
            j = json.loads(line[5:])
            out["model"] = j.get("model", out.get("model"))
            out["system_fingerprint"] = j.get("system_fingerprint", out.get("system_fingerprint"))
            if j.get("usage"):
                out["usage"] = j["usage"]
            for ch in j.get("choices") or []:
                d = ch.get("delta") or {}
                content.append(d.get("content") or "")
                reasoning += len(d.get("reasoning_content") or d.get("reasoning") or "")
                finish = ch.get("finish_reason") or finish
    out["choices"] = [{"message": {"content": "".join(content)}, "finish_reason": finish}]
    out["reasoning_chars"] = reasoning
    return out


def parse(content: str):
    content = re.sub(r"^```(?:json)?|```$", "", content.strip(), flags=re.M).strip()
    a, b = content.find("{"), content.rfind("}")
    return json.loads(content[a:b + 1])


def score(parsed: dict) -> dict:
    """Check and gate scores by RUBRIC-v0 section 0."""
    items, out = parsed.get("items", {}), {"items": {}, "checks": {}}
    a3na = parsed.get("a3_applicable") is False
    for chk, ids in ITEMS.items():
        vals = []
        for i in ids:
            it = items.get(i) or {}
            s = str(it.get("score", "U")).strip().upper().replace("NA", "na")
            if s not in ("0", "1", "U", "na"):
                s = "U"
            if s == "1" and len(str(it.get("evidence") or "").strip()) < 10:
                s = "U"  # a 1 without evidence is recoded U
            if chk == "A3" and a3na:
                s = "na"
            out["items"][i] = s
            vals.append(s)
        if chk == "A3" and a3na:
            out["checks"][chk] = "na"
        elif "1" in vals:
            out["checks"][chk] = "1"
        elif "U" in vals:
            out["checks"][chk] = "U"
        else:
            out["checks"][chk] = "0"
    out["gate"] = sum(v == "1" for v in out["checks"].values())
    out["n_U"] = sum(v == "U" for v in out["checks"].values())
    return out


def job(args):
    dev, model, rep, kind, text, tgt, sec0, checks, token, dest = args
    if dest.exists():
        return dest.name, "skip"
    user, order = prompt(dev, model, rep, text, tgt, sec0, checks)
    rec = {"dev_id": dev, "model_requested": model, "rep": rep, "input": kind,
           "check_order": order, "temperature": TEMPERATURE, "max_tokens": MAX_TOKENS,
           "prompt_sha256": hashlib.sha256(user.encode()).hexdigest(),
           "rubric": RUBRIC,
           "rubric_sha256": hashlib.sha256((HERE / RUBRIC).read_bytes()).hexdigest(),
           "attempts": []}
    for attempt in range(4):
        t0 = time.time()
        try:
            r = call(model, user, token)
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
            rec["attempts"].append({"error": str(e)[:300], "seconds": round(time.time() - t0, 1)})
            time.sleep(30 * (attempt + 1))
            continue
        if not r.get("choices"):
            rec["attempts"].append({"error": json.dumps(r)[:300], "seconds": round(time.time() - t0, 1)})
            time.sleep(30 * (attempt + 1))
            continue
        msg = r["choices"][0]["message"]
        a = {"seconds": round(time.time() - t0, 1), "model_returned": r.get("model"),
             "system_fingerprint": r.get("system_fingerprint"), "usage": r.get("usage"),
             "reasoning_chars": r.get("reasoning_chars"),
             "finish_reason": r["choices"][0].get("finish_reason"),
             "content": msg.get("content")}
        rec["attempts"].append(a)
        try:
            rec["parsed"] = parse(msg.get("content") or "")
            rec["scored"] = score(rec["parsed"])
            break
        except (ValueError, AttributeError) as e:
            a["parse_error"] = str(e)[:200]
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(rec, indent=1), encoding="utf-8")
    return dest.name, "ok" if "scored" in rec else "FAILED"


def main() -> int:
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    sys.path.insert(0, str(HERE))
    from k2_blinding import leaks, redact
    from k2_intake import cut_references

    token = None
    for line in open(os.path.expanduser("~/.primer.env")):
        m = re.match(r"\s*(?:export\s+)?NRP_LLM_TOKEN\s*=\s*['\"]?([^'\"\n]*)", line)
        if m:
            token = m.group(1)
    assert token, "NRP_LLM_TOKEN not found"
    meta = json.loads((root / "meta.json").read_text(encoding="utf-8"))
    man = list(csv.DictReader(open(HERE / "devset" / "intake_manifest.csv", encoding="utf-8")))
    devs = [r["dev_id"] for r in man if r["status"] == "blinded"]
    rpp = {r["dev_id"]: r for r in csv.DictReader(open(HERE / "devset" / "devset_rpp.csv", encoding="utf-8"))}
    ml: dict[str, list] = {}
    for r in csv.DictReader(open(HERE / "devset" / "devset_ml.csv", encoding="utf-8")):
        ml.setdefault(r["dev_id"], []).append(r)
    sec0, checks = rubric_sections()

    jobs = []
    for dev in devs:
        text = (root / "blinded" / f"{dev}.txt").read_text(encoding="utf-8")
        for model in MODELS:
            for rep in range(1, REPS + 1):
                jobs.append((dev, model, rep, "unit", text, target(dev, rpp, ml), sec0, checks,
                             token, out / "raw" / model / f"{dev}_unit_r{rep}.json"))
    subset = sorted(random.Random(SEED).sample(devs, FULLTEXT_SUBSET))
    skipped = {}
    for dev in subset:
        raw = subprocess.run(["pdftotext", "-enc", "UTF-8", str(root / "pdf" / f"{dev}.pdf"), "-"],
                             capture_output=True, text=True, check=True).stdout
        body, _ = cut_references(raw)
        full = redact(body, meta[dev])
        res = leaks(full, meta[dev])
        if res:
            skipped[dev] = sorted({k for k, _ in res})
            continue
        for model in MODELS:
            jobs.append((dev, model, 1, "fulltext", full, target(dev, rpp, ml), sec0, checks,
                         token, out / "raw" / model / f"{dev}_fulltext_r1.json"))
    out.mkdir(parents=True, exist_ok=True)
    (out / f"plan_{'_'.join(MODELS)}.json").write_text(json.dumps(
        {"units": devs, "models": MODELS, "reps": REPS, "max_tokens": MAX_TOKENS, "rubric": RUBRIC,
         "fulltext_subset": subset,
         "fulltext_skipped_for_leaks": skipped, "calls": len(jobs)}, indent=1))
    print(f"{len(jobs)} calls; fulltext subset {subset}; skipped {skipped}", flush=True)
    # one worker per model: at most two calls in flight on the shared gateway
    by_model = {m: [j for j in jobs if j[1] == m] for m in MODELS}

    def run_model(m):
        for j in by_model[m][:LIMIT or None]:
            try:
                name, st = job(j)
            except Exception as e:  # one bad call must not stop the model's queue
                name, st = j[-1].name, f"ERROR {type(e).__name__}: {str(e)[:200]}"
            print(m, name, st, flush=True)

    with ThreadPoolExecutor(len(MODELS)) as ex:
        list(ex.map(run_model, MODELS))
    print("DONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
