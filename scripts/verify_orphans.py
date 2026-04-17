"""Grep-verify suspected orphans against the actual codebase using git grep, with split bands.

Improvements vs v1:

- **Restricted oracle paths** — only search ``backend/{app,scripts,tests}/`` for
  backend orphans, ``frontend/{src,tests,e2e}/`` for frontend orphans. Excludes
  ``.superpowers/``, ``.claude/``, archived dirs that previously caused noise.
- **Code-only file types** — ignore matches in ``.md/.html/.json/.yaml/Makefile``
  (dropped name-collision noise like ``main()`` matching ``Makefile``).
- **Generic-name skip** — names that collide with everything (``__init__``,
  ``main``, ``config``, ``handler``, …) bypass grep entirely; they're tagged
  ``skip-generic`` and excluded from the FP-rate denominator.
- **File-stem inference** — for orphans whose label IS the file stem (e.g.
  ``datasets_api.py``), check whether ANY node from the same file has inbound
  edges in the augmented graph; if yes, the file is imported and we skip
  (``skip-file-imported``).
- **Split reporting** — backend and frontend FP rates printed separately, then
  a combined line.
"""
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GRAPH = REPO / "graphify" / "graph.json"

g = json.loads(GRAPH.read_text())
AUG = REPO / "graphify" / "graph.augmented.json"
if AUG.exists():
    aug = json.loads(AUG.read_text())
    g["nodes"].extend(aug["nodes"])
    g["links"].extend(aug["links"])
nodes = {n["id"]: n for n in g["nodes"]}
links = g["links"]

USE_RELATIONS = {
    "imports_from", "calls", "implements", "extends", "instantiates",
    "uses", "references", "decorated_by", "raises", "returns",
}
inbound: dict[str, set[str]] = defaultdict(set)
for e in links:
    if e.get("confidence") != "EXTRACTED":
        continue
    if e.get("relation") not in USE_RELATIONS:
        continue
    inbound[e["target"]].add(e["source"])


def _stem(src: str) -> str:
    return src.rsplit("/", 1)[-1].rsplit(".", 1)[0].lower()


# A file is considered imported if ANY node from it has an inbound EXTRACTED edge.
file_stem_used: set[str] = set()
for nid, n in nodes.items():
    src = n.get("source_file") or ""
    if not (src.endswith(".py") or src.endswith((".ts", ".tsx", ".js", ".jsx"))):
        continue
    if inbound.get(nid):
        file_stem_used.add(_stem(src))

ENTRY_PREFIXES = (
    "main_", "app_main", "conftest", "cli_", "settings",
    "__init__", "vite_config", "tailwind_config", "pyproject", "package_json",
)


def is_entry_or_skip(node: dict) -> bool:
    src = node.get("source_file", "") or ""
    nid = node["id"]
    if "/tests/" in src or src.endswith("_test.py") or ".test." in src:
        return True
    if "__tests__" in src or "/e2e/" in src:
        return True
    if any(nid.startswith(p) for p in ENTRY_PREFIXES):
        return True
    if src.endswith("/main.py") or src.endswith("/__init__.py"):
        return True
    if "/migrations/" in src or src.endswith((".md", ".json", ".yaml", ".yml", ".html", ".css", ".svg")):
        return True
    return False


orphan_symbols: list[dict] = []
for nid, n in nodes.items():
    if n.get("file_type") != "code":
        continue
    if is_entry_or_skip(n):
        continue
    if inbound[nid]:
        continue
    if "_" not in nid:
        continue
    label = n.get("label", "")
    if len(label) < 5 or label.lower() in {"main", "init", "test", "name"}:
        continue
    orphan_symbols.append(n)

import random
random.seed(42)
backend_orphans = [n for n in orphan_symbols if (n.get("source_file") or "").startswith("backend/")]
frontend_orphans = [n for n in orphan_symbols if (n.get("source_file") or "").startswith("frontend/")]
backend_sample = random.sample(backend_orphans, min(60, len(backend_orphans)))
frontend_sample = random.sample(frontend_orphans, min(40, len(frontend_orphans)))

print(f"Total orphan symbols: {len(orphan_symbols)} "
      f"({len(backend_orphans)} backend, {len(frontend_orphans)} frontend)")
print(f"Backend sample: {len(backend_sample)}, Frontend sample: {len(frontend_sample)}\n")


def clean_label(lab: str) -> str:
    """Strip leading method-marker dot and trailing ``()``; return bare identifier."""
    s = lab.strip()
    if s.startswith("."):
        s = s[1:]
    if s.endswith("()"):
        s = s[:-2]
    m = re.match(r"[A-Za-z_][A-Za-z0-9_]*", s)
    return m.group(0) if m else s


# Names too generic for grep to be a useful oracle — would name-collide with everything.
GENERIC_NAMES = {
    "__init__", "main", "init", "config", "setup", "run", "test", "name", "id",
    "app", "router", "handler", "client", "server", "build", "create",
    "get", "set", "load", "save", "open", "close", "start", "stop",
    "execute", "process", "send", "receive", "parse", "format", "data",
    "result", "response", "request", "value", "type", "state", "status",
    "model", "view", "controller", "service", "manager", "store",
}

BACKEND_PATHS = ("backend/app/", "backend/scripts/", "backend/tests/")
FRONTEND_PATHS = ("frontend/src/", "frontend/tests/", "frontend/e2e/")
PROD_EXTS = (".py", ".ts", ".tsx", ".js", ".jsx")


def search_refs(label: str, src_path: str, side: str) -> list[str]:
    paths = BACKEND_PATHS if side == "backend" else FRONTEND_PATHS
    res = subprocess.run(
        ["git", "grep", "-lw", label, "--", *paths],
        capture_output=True, text=True, cwd=str(REPO),
    )
    src_basename = src_path.split("/")[-1]
    out = []
    for f in res.stdout.splitlines():
        if f == src_path or f.endswith(f"/{src_basename}"):
            continue
        if not any(f.endswith(ext) for ext in PROD_EXTS):
            continue
        out.append(f)
    return out


def classify(node: dict, side: str) -> tuple[str, list[str]]:
    raw_label = node["label"]
    label = clean_label(raw_label)
    src = node["source_file"] or ""
    if not label or len(label) < 4:
        return "skip-short", []
    stem = _stem(src)
    # File-level orphan whose label matches its file stem AND the file is imported elsewhere
    if label.lower() == stem and stem in file_stem_used:
        return "skip-file-imported", []
    if label.lower() in GENERIC_NAMES:
        return "skip-generic", []
    files = search_refs(label, src, side)
    prod = [f for f in files if "/tests/" not in f and "__tests__" not in f]
    if prod:
        return "live", prod[:2]
    return "dead", files[:2]


def report(title: str, sample: list[dict], side: str) -> tuple[float, int, int]:
    counts: dict[str, list] = defaultdict(list)
    for n in sample:
        status, refs = classify(n, side)
        counts[status].append((n, refs))
    measured = len(counts["dead"]) + len(counts["live"])
    fp = len(counts["live"])
    rate = (fp / measured * 100) if measured else 0.0
    print(f"=== {title} (measured n={measured}, raw sample={len(sample)}) ===")
    print(f"  truly_dead:  {len(counts['dead'])}  ({100-rate:.1f}% of measured)")
    print(f"  false_pos:   {fp}  ({rate:.1f}% of measured)  ← graph missed these")
    for tag in ("skip-generic", "skip-file-imported", "skip-short"):
        if counts[tag]:
            print(f"  {tag}: {len(counts[tag])} (excluded from FP denominator)")
    if counts["live"]:
        print(f"  -- false-positive examples --")
        for n, refs in counts["live"][:8]:
            print(f"    {n['label']:40s}  {n['source_file']}")
            for r in refs:
                print(f"      used in: {r}")
    print()
    return rate, measured, fp


print("===== Per-side false-positive rates =====\n")
b_rate, b_n, b_fp = report("BACKEND", backend_sample, "backend")
f_rate, f_n, f_fp = report("FRONTEND", frontend_sample, "frontend")

print("===== Summary =====")
print(f"  Backend FP:  {b_fp}/{b_n}  ({b_rate:.1f}%)")
print(f"  Frontend FP: {f_fp}/{f_n}  ({f_rate:.1f}%)")
total_n = b_n + f_n
total_fp = b_fp + f_fp
total_rate = (total_fp / total_n * 100) if total_n else 0.0
print(f"  Combined:    {total_fp}/{total_n}  ({total_rate:.1f}%)")
