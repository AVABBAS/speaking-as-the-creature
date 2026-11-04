"""Descriptive recomputation for the When Utility Dissolves reframe (route a).

Reads only the archived materials deposited for this study:
  - the three conversation histories (JSON)
  - the three coding codebooks (JSON)
  - the pipeline trial table df_trials_final.csv (99 responses)
Produces descriptive counts and means only. No inferential statistics.
Canonical trial numbering follows the codebooks / pipeline (grouped by
pathway); the histories use a different internal numbering for Claude and
Gemini, resolved here by verbatim content matching (see trial_map).
"""
import json, re, pathlib, itertools, math
from collections import Counter as _Counter
import pandas as pd

HOME = pathlib.Path.home()
U = HOME / "workspace/user/files"
PKG = HOME / "workspace/submissions-prep-2026-10-30/when-utility-dissolves-jetai"
PIPE = PKG / "hidden_files/verification-outputs-2026-11-02/csv_files"

HIST = {"ChatGPT-5.4": "History_GPT-5.4.json",
        "Claude 4.6 Sonnet": "Claude_4.6_Sonnet_History.json",
        "Gemini 3.1 Pro": "History_Gemini_3.1_Pro.json"}
BOOK = {"ChatGPT-5.4": "CODEBOOK_ChatGPT.json",
        "Claude 4.6 Sonnet": "CODEBOOK_Claude_4.6_Sonnet.json",
        "Gemini 3.1 Pro": "CODEBOOK_Gemini_3.1_Pro.json"}
SCEN = {"Gas Giant": "Gas Giant", "Whale": "Ocean Organism", "Floating City": "Floating City"}

def norm(s):
    return re.sub(r"\s+", " ", str(s)).strip().lower()

tf = pd.read_csv(PIPE / "df_trials_final.csv")
tf["key"] = tf["response"].map(lambda x: norm(x)[:300])

# ---------- 1. Canonical trial table by verbatim content matching ----------
trial_map = []  # canonical trial_id, model, scenario, pathway, history experiment_id
for model, fn in HIST.items():
    d = json.loads((U / fn).read_text())
    for e in d["experiments"]:
        last = norm(e["phases"][-1]["response"])[:300]
        hits = tf[tf["key"] == last]
        cands = sorted(hits["trial_id"].unique())
        # disambiguate identical short final texts via the defocusing-phase response
        if len(cands) != 1:
            mid = norm(e["phases"][2]["response"])[:300]
            hits2 = tf[(tf["key"] == mid)]
            cands = sorted(hits2["trial_id"].unique())
        assert len(cands) == 1, (model, e["experiment_id"], cands)
        row = tf[tf["trial_id"] == cands[0]].iloc[0]
        trial_map.append({"trial": int(cands[0]), "model": model,
                          "scenario": SCEN[row["scenario"]], "pathway": row["pathway"],
                          "history_experiment": int(e["experiment_id"]),
                          "n_responses": len(e["phases"])})
trial_map.sort(key=lambda r: r["trial"])
assert [r["trial"] for r in trial_map] == list(range(1, 19))

# ---------- 2. Tier 1 primary codes per phase from the codebook matrices ----------
matrices = {}
for model, fn in BOOK.items():
    d = json.loads((U / fn).read_text())
    part = [v for k, v in d.items() if k.startswith("part_v_coding_matrix")][0]
    for key, tv in part.items():
        if not isinstance(tv, dict) or "phases" not in tv:
            continue
        m = re.search(r"trial_(\d+)_", key)
        matrices[int(m.group(1))] = {p["phase"]: p.get("tier_1_primary") for p in tv["phases"]}

from collections import Counter
# Codebook matrices number phases inconsistently across pathways, so group
# by position: first two entries = problem-solving + impasse; last two =
# return + confrontation.
tier1 = {"early": Counter(), "late": Counter()}
for tid, phases in matrices.items():
    items = [(ph, c) for ph, c in phases.items() if c]
    for ph, code in items[:2]: tier1["early"][code] += 1
    for ph, code in items[-2:]: tier1["late"][code] += 1
n_early = sum(tier1["early"].values()); n_late = sum(tier1["late"].values())

# ---------- 3. Tier 2 counts by pathway, pooled across the three codebooks ----------
tier2 = {}
for model, fn in BOOK.items():
    d = json.loads((U / fn).read_text())
    part = [v for k, v in d.items() if k.startswith("part_vi_code_frequency")][0]
    sec = [v for k, v in part.items() if "tier_2" in k][0]
    for row in sec["table"]:
        t = tier2.setdefault(row["code"], {"A": 0, "B": 0})
        t["A"] += int(row["path_a_count"]); t["B"] += int(row["path_b_count"])

# ---------- 4. Tier 3 presence counts per model ----------
tier3 = {}
for model, fn in BOOK.items():
    d = json.loads((U / fn).read_text())
    part = [v for k, v in d.items() if k.startswith("part_vi_code_frequency")][0]
    sec = [v for k, v in part.items() if "tier_3" in k][0]
    tier3[model] = {row["code"]: row["count"] for row in sec["table"]}

# ---------- 5-6. Transcript descriptives + metaphor baseline, from the histories ----------
# (df_trials_final phase labels are unreliable for the return phase, so both
# computations run on the primary transcripts via the canonical trial map.)
hist_by_trial = {}
for r in trial_map:
    d = json.loads((U / HIST[r["model"]]).read_text())
    e = [x for x in d["experiments"] if int(x["experiment_id"]) == r["history_experiment"]][0]
    hist_by_trial[r["trial"]] = (r, e["phases"])

def wcount(s): return len(str(s).split())
def fprate(s):
    w = wcount(s)
    return len(re.findall(r"\b(?:I|me|my|mine|myself)\b", str(s))) / w * 100 if w else 0.0

desc = {}
for path in ("A", "B"):
    for grp, idx in (("early", lambda n: [0, 1]), ("late", lambda n: [n - 2, n - 1])):
        rows = []
        for tid, (r, phases) in hist_by_trial.items():
            if r["pathway"] != path: continue
            sel = [phases[i] for i in idx(len(phases))
                   if not phases[i]["response"].startswith("[Note:")]  # Trial 18 confrontation is absent from the archive
            txt = " ".join(p["response"] for p in sel)
            rows.append((wcount(txt) / len(sel), fprate(txt)))
        desc[f"{path}_{grp}"] = {"n_responses": int(sum(len(idx(len(hist_by_trial[t][1]))) for t in hist_by_trial if hist_by_trial[t][0]["pathway"] == path)),
                                 "mean_words_per_response": round(sum(x[0] for x in rows) / len(rows), 1),
                                 "mean_first_person_per_100w": round(sum(x[1] for x in rows) / len(rows), 2)}

A = [tid for tid, (r, _) in hist_by_trial.items() if r["pathway"] == "A"]
src = {}; tgt = {}
for tid in A:
    phases = hist_by_trial[tid][1]
    src[tid] = phases[2]["response"] + " " + phases[3]["response"]          # the two artistic tasks
    tgt[tid] = phases[4]["response"] + " " + phases[5]["response"]          # return + confrontation
STOP = set("the a an and or of to in is are was were it its this that with as for on by be not no do does you he she we they them his her their our your".split())
def toks(s):
    w = [x for x in re.findall(r"[a-z']+", str(s).lower()) if x not in STOP and len(x) > 2]
    return w + [w[i] + " " + w[i + 1] for i in range(len(w) - 1)]
docs = [src[t] for t in A] + [tgt[t] for t in A]
counts = [_Counter(toks(d)) for d in docs]
dfreq = _Counter()
for c in counts:
    for term in c: dfreq[term] += 1
N = len(docs)
def vec_of(c):
    return {t_: (1 + math.log(n)) * (math.log((1 + N) / (1 + dfreq[t_])) + 1) for t_, n in c.items()}
vecs = [vec_of(c) for c in counts]
def cos(a, b):
    dot = sum(v * b.get(t_, 0.0) for t_, v in a.items())
    na = math.sqrt(sum(v * v for v in a.values())); nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0
k = len(A)
sim = [[cos(vecs[i], vecs[k + j]) for j in range(k)] for i in range(k)]
within = [float(sim[i][i]) for i in range(k)]
shuffled = [float(sim[i][j]) for i, j in itertools.permutations(range(k), 2)]
mirror = {"within_mean": round(sum(within) / len(within), 3),
          "shuffled_mean": round(sum(shuffled) / len(shuffled), 3),
          "within_values": [round(v, 3) for v in within],
          "n_shuffled_pairs": len(shuffled),
          "note": "TF-IDF (1-2 grams, English stop words) cosine between a Path A trial's own artistic-phase text and its late-phase text, vs all cross-trial pairings. Lexical overlap measure, not semantic embedding similarity."}

out = {"trial_map": trial_map,
       "tier1_primary_by_phase_group": {"early": dict(tier1["early"]), "late": dict(tier1["late"]),
                                        "n_early": n_early, "n_late": n_late},
       "tier2_by_pathway": tier2, "tier3_presence": tier3,
       "transcript_descriptives": desc, "metaphor_lexical_baseline": mirror}
dest = PKG / "hidden_files/build-2026-11-02/analysis-output.json"
dest.write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(json.dumps(out, indent=1, ensure_ascii=False))
