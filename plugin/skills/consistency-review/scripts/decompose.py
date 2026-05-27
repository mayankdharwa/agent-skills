#!/usr/bin/env python3
"""Markdown decomposer -> cross-file similarity graph.

Splits every ``.md`` file under a directory into heading-scoped chunks, then
builds a similarity graph so a reviewing agent can do *pointed* comparisons
(open only the suspicious pairs) instead of reading the whole corpus.

Engine is deterministic and dependency-free:

  - chunk = a heading plus its body, down to the next same-or-higher heading
  - TF-IDF vector per chunk over normalized tokens
  - cosine similarity between cross-file chunk pairs (kept above a threshold)
  - "defined terms" per chunk (bold, backtick spans, IDs, callout labels)
  - edge score = cosine + a boost for shared *rare* terms, since a rare term
    shared across two chunks is strong evidence they discuss the same rule

A high-scoring edge means: "these two sections probably describe the same thing
-- compare them for contradiction or differing levels of detail."

Usage:
    python3 decompose.py <dir> [--json] [--threshold 0.25] [--top 20] [--min-tokens 10]

Stdout: the JSON similarity graph (with --json, pretty-printed).
Stderr: a human-readable ranked list of candidate pairs to inspect.

Pure standard library; no third-party dependencies.
"""

import argparse
import json
import math
import os
import re
import sys
from collections import defaultdict


FENCE_RE = re.compile(r"^\s*(```|~~~)")
ATX_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")

# Defined-term extractors (run on raw chunk text).
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*|__([^_]+)__")
CODE_SPAN_RE = re.compile(r"`([^`]+)`")
ID_RE = re.compile(r"\b([A-Z]{2,}(?:-?\d+)?|[A-Z]\d+|Q<?N?>?\d*|#\d+)\b")

STOPWORDS = set("""
a an and are as at be been being but by for from has have if in into is it its
of on or that the their then there these this to was were will with not no can
do does done you your we our they them he she his her i me my us if else when
which who whom what where why how than too very just only also been about over
under more most some any each every both either neither such own same so up out
""".split())

TOKEN_RE = re.compile(r"[a-z][a-z0-9_-]+")


def iter_md_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for name in sorted(filenames):
            if name.endswith(".md"):
                yield os.path.join(dirpath, name)


def chunk_file(path, rel):
    """Split a file into heading-scoped chunks.

    Returns list of dicts: {file, heading, heading_path, level, start, end, text}.
    Content before the first heading becomes a synthetic "(preamble)" chunk.
    """
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()

    chunks = []
    stack = []  # (level, text) breadcrumb for heading_path

    def push_path(level, text):
        while stack and stack[-1][0] >= level:
            stack.pop()
        stack.append((level, text))
        return " > ".join(t for (_, t) in stack)

    current = {"file": rel, "heading": "(preamble)", "heading_path": "(preamble)",
               "level": 0, "start": 1, "lines": []}
    in_fence = False

    for i, line in enumerate(lines, start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            current["lines"].append(line)
            continue
        m = ATX_HEADING_RE.match(line) if not in_fence else None
        if m:
            # Close the current chunk.
            current["end"] = i - 1
            current["text"] = "\n".join(current["lines"])
            if current["text"].strip() or current["heading"] != "(preamble)":
                chunks.append(current)
            level = len(m.group(1))
            heading = m.group(2).strip()
            hpath = push_path(level, heading)
            current = {"file": rel, "heading": heading, "heading_path": hpath,
                       "level": level, "start": i, "lines": [line]}
        else:
            current["lines"].append(line)

    current["end"] = len(lines)
    current["text"] = "\n".join(current["lines"])
    if current["text"].strip():
        chunks.append(current)

    return chunks


def normalize_tokens(text):
    # Strip code fences and inline code so syntax noise doesn't dominate.
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]*`", " ", text)
    text = text.lower()
    tokens = [t for t in TOKEN_RE.findall(text)
              if t not in STOPWORDS and len(t) > 2]
    return tokens


def extract_terms(text):
    """Salient defined terms: bold phrases, code spans, IDs/callout labels."""
    terms = set()
    for m in BOLD_RE.finditer(text):
        terms.add((m.group(1) or m.group(2)).strip().lower())
    for m in CODE_SPAN_RE.finditer(text):
        val = m.group(1).strip()
        if val and len(val) <= 40:
            terms.add(val.lower())
    for m in ID_RE.finditer(text):
        terms.add(m.group(1))
    return {t for t in terms if t}


def build_tfidf(chunks):
    """Return (vectors, idf). vectors[i] is a dict token->tfidf weight."""
    n = len(chunks)
    token_lists = [normalize_tokens(c["text"] + " " + c["heading"])
                   for c in chunks]
    df = defaultdict(int)
    for toks in token_lists:
        for t in set(toks):
            df[t] += 1
    idf = {t: math.log((1 + n) / (1 + d)) + 1.0 for t, d in df.items()}

    vectors = []
    for toks in token_lists:
        tf = defaultdict(int)
        for t in toks:
            tf[t] += 1
        if not toks:
            vectors.append({})
            continue
        maxtf = max(tf.values())
        vec = {t: (0.5 + 0.5 * c / maxtf) * idf[t] for t, c in tf.items()}
        vectors.append(vec)
    return vectors, idf, token_lists


def cosine(a, b):
    if not a or not b:
        return 0.0
    # Iterate the smaller dict.
    if len(a) > len(b):
        a, b = b, a
    dot = sum(w * b.get(t, 0.0) for t, w in a.items())
    if dot == 0.0:
        return 0.0
    na = math.sqrt(sum(w * w for w in a.values()))
    nb = math.sqrt(sum(w * w for w in b.values()))
    return dot / (na * nb)


def decompose(root, threshold=0.25, min_tokens=10):
    root = os.path.abspath(root)
    files = list(iter_md_files(root))

    chunks = []
    for path in files:
        rel = os.path.relpath(path, root)
        chunks.extend(chunk_file(path, rel))

    for idx, c in enumerate(chunks):
        c["id"] = idx
        c["terms"] = extract_terms(c["text"] + " " + c["heading"])

    vectors, idf, token_lists = build_tfidf(chunks)

    # Term rarity: a term in few chunks is more discriminating.
    term_chunks = defaultdict(set)
    for c in chunks:
        for t in c["terms"]:
            term_chunks[t].add(c["id"])

    n_chunks = max(len(chunks), 1)

    # Content-thin chunks (a bare "## Steps" header whose body lives in
    # subsections) match each other trivially at cosine 1.0. Exclude them from
    # edge generation; they remain as nodes.
    thin = {i for i, toks in enumerate(token_lists) if len(set(toks)) < min_tokens}

    edges = []
    for i in range(len(chunks)):
        if i in thin:
            continue
        for j in range(i + 1, len(chunks)):
            if j in thin:
                continue
            # Cross-file only; within-file duplication is usually intentional.
            if chunks[i]["file"] == chunks[j]["file"]:
                continue
            cos = cosine(vectors[i], vectors[j])
            shared = chunks[i]["terms"] & chunks[j]["terms"]
            # Rare-term boost: sum over shared terms of how discriminating each is.
            boost = 0.0
            for t in shared:
                rarity = math.log(n_chunks / len(term_chunks[t]))
                boost += rarity
            boost = min(boost / 10.0, 0.4)  # cap the contribution
            score = cos + boost
            if score >= threshold:
                edges.append({
                    "a": i, "b": j,
                    "cosine": round(cos, 4),
                    "shared_terms": sorted(shared),
                    "score": round(score, 4),
                })

    edges.sort(key=lambda e: e["score"], reverse=True)

    # Connected components over kept edges -> clusters.
    parent = list(range(len(chunks)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        parent[find(x)] = find(y)

    for e in edges:
        union(e["a"], e["b"])
    comp = defaultdict(list)
    for c in chunks:
        comp[find(c["id"])].append(c["id"])
    clusters = [sorted(ids) for ids in comp.values() if len(ids) > 1]
    clusters.sort(key=len, reverse=True)

    # term_index: terms spanning 2+ distinct files (duplicate-definition radar).
    term_index = {}
    for t, ids in term_chunks.items():
        file_count = len({chunks[i]["file"] for i in ids})
        if file_count >= 2:
            term_index[t] = sorted(ids)

    nodes = [{
        "id": c["id"],
        "file": c["file"],
        "heading_path": c["heading_path"],
        "lines": "%d-%d" % (c["start"], c["end"]),
        "terms": sorted(c["terms"]),
        "top_terms": sorted(vectors[c["id"]], key=lambda t: vectors[c["id"]][t],
                            reverse=True)[:8],
    } for c in chunks]

    return {
        "root": root,
        "files_scanned": len(files),
        "chunk_count": len(chunks),
        "threshold": threshold,
        "nodes": nodes,
        "edges": edges,
        "clusters": clusters,
        "term_index": term_index,
    }


def node_label(node):
    return "%s :: %s (L%s)" % (node["file"], node["heading_path"], node["lines"])


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir", help="directory of markdown files to decompose")
    ap.add_argument("--json", action="store_true",
                    help="pretty-print the JSON graph to stdout")
    ap.add_argument("--threshold", type=float, default=0.25,
                    help="minimum edge score to keep (default 0.25)")
    ap.add_argument("--top", type=int, default=20,
                    help="how many candidate pairs to list in the summary")
    ap.add_argument("--min-tokens", type=int, default=10,
                    help="min distinct tokens for a chunk to form edges "
                         "(filters content-thin heading-only chunks)")
    args = ap.parse_args(argv)

    if not os.path.isdir(args.dir):
        sys.stderr.write("error: not a directory: %s\n" % args.dir)
        return 2

    graph = decompose(args.dir, threshold=args.threshold,
                      min_tokens=args.min_tokens)

    if args.json:
        print(json.dumps(graph, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(graph, ensure_ascii=False))

    nodes = {n["id"]: n for n in graph["nodes"]}
    sys.stderr.write("\n=== decompose: %d file(s), %d chunk(s), %d edge(s) ===\n"
                     % (graph["files_scanned"], graph["chunk_count"],
                        len(graph["edges"])))
    sys.stderr.write("Top candidate pairs (compare for contradiction / "
                     "differing detail):\n")
    for e in graph["edges"][:args.top]:
        shared = (" shared:[%s]" % ", ".join(e["shared_terms"])
                  if e["shared_terms"] else "")
        sys.stderr.write("  score=%.3f (cos=%.3f)%s\n    A: %s\n    B: %s\n" % (
            e["score"], e["cosine"], shared,
            node_label(nodes[e["a"]]), node_label(nodes[e["b"]])))

    return 0


if __name__ == "__main__":
    sys.exit(main())
