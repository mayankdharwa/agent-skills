# consistency-review

A Claude Code skill that reviews a set of markdown files (a skill, a `docs/`
tree, a multi-file spec) for **internal consistency** — cross-file
contradictions, the same rule stated at differing levels of detail, and broken
cross-file links / heading anchors.

Runtime usage lives in [`SKILL.md`](SKILL.md). This README is for maintainers of
the skill itself.

## Layout

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Runtime instructions the agent reads when the skill is invoked. |
| `reference/checks.md` | Issue catalogue; loaded only when classifying a finding. |
| `scripts/check_links.py` | Deterministic link & `#anchor` verifier. |
| `scripts/decompose.py` | Cross-file similarity graph for pointed comparison. |
| `tests/` | Maintainer regression tests (not used at runtime). |

## Running the tests

```
python3 tests/run_tests.py
```

This runs both scripts against `tests/fixtures/` — a deliberately defective
two-file corpus — and asserts each planted defect is caught:

1. **anchor-missing** — `auth-rules.md` links `retention.md#session-timeout`, a
   heading that does not exist.
2. **leveling mismatch** — both files have a "Token expiry" section; only one
   carries the service-account exception. Must surface as the top decompose
   edge.
3. **contradiction** — refresh token "valid for 30 days" vs "valid for 7 days".
   Must surface as an edge between Refresh policy and Cleanup job.

Stdlib only, no framework; exits non-zero if any assertion fails, so it drops
straight into CI. The scripts are deterministic (same input → same graph), so
the assertions are stable.
