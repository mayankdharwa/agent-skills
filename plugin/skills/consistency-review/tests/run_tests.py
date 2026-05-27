#!/usr/bin/env python3
"""Regression tests for the consistency-review scripts.

Runs both scripts against tests/fixtures/ (a deliberately defective 2-file
corpus) and asserts each planted defect is caught. Pure stdlib; no framework.

The fixtures plant three defects:
  1. anchor-missing  -- auth-rules.md links retention.md#session-timeout,
                        a heading that does not exist.
  2. leveling mismatch -- both files have a "Token expiry" section; retention.md
                        adds a service-account exception auth-rules.md omits.
                        Must surface as the top decompose edge.
  3. contradiction   -- refresh token "valid for 30 days" (auth-rules.md) vs
                        "valid for 7 days" (retention.md). Must surface as an
                        edge between Refresh policy and Cleanup job.

Run:  python3 tests/run_tests.py
Exit code is non-zero if any assertion fails.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "fixtures")
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))

import check_links  # noqa: E402
import decompose  # noqa: E402


def _edge_headings(graph, edge):
    nodes = {n["id"]: n for n in graph["nodes"]}
    return nodes[edge["a"]]["heading_path"], nodes[edge["b"]]["heading_path"]


def test_anchor_missing():
    report = check_links.check(FIXTURES)
    hard = [f for f in report["findings"]
            if check_links.is_hard(f, include_soft=False)]
    assert len(hard) == 1, "expected exactly 1 hard finding, got %d" % len(hard)
    f = hard[0]
    assert f["reason"] == "anchor-missing", f["reason"]
    assert f["raw"] == "retention.md#session-timeout", f["raw"]
    assert f["source"].startswith("auth-rules.md:"), f["source"]


def test_leveling_mismatch_is_top_edge():
    graph = decompose.decompose(FIXTURES)
    assert graph["edges"], "expected at least one edge"
    top = graph["edges"][0]
    a, b = _edge_headings(graph, top)
    assert a.endswith("Token expiry") and b.endswith("Token expiry"), (a, b)


def test_refresh_token_contradiction_edge_exists():
    graph = decompose.decompose(FIXTURES)
    pairs = {frozenset(_edge_headings(graph, e)) for e in graph["edges"]}
    want = frozenset({"Authentication rules > Refresh policy",
                      "Data retention > Cleanup job"})
    assert want in pairs, "no edge linking Refresh policy <-> Cleanup job"


def main():
    tests = [test_anchor_missing,
             test_leveling_mismatch_is_top_edge,
             test_refresh_token_contradiction_edge_exists]
    failed = 0
    for t in tests:
        try:
            t()
            print("PASS %s" % t.__name__)
        except AssertionError as e:
            failed += 1
            print("FAIL %s: %s" % (t.__name__, e))
    print("\n%d passed, %d failed" % (len(tests) - failed, failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
