#!/usr/bin/env python3
"""Deterministic link & anchor verifier for a set of markdown files.

Walks every ``.md`` file under a directory, extracts link targets, and reports
any that resolve nowhere. Handles:

  - inline links ``[text](target)``
  - reference definitions ``[id]: target``
  - wikilinks ``[[target]]`` / ``[[target#anchor]]``
  - bare relative path mentions ending in ``.md`` (reported as a "soft" class)

For each target the path is resolved against the source file's directory and
the corpus root. ``#anchor`` fragments are checked against the GitHub-slugified
headings of the target file. External URLs (http/https/mailto) are skipped.

Also emits a per-file heading inventory: a script cannot resolve a
natural-language reference like "see file B, section E", but the inventory lets
a reviewing agent map such prose onto real headings.

Usage:
    python3 check_links.py <dir> [--json] [--soft-hard]

Exit code is non-zero when any hard (file-missing / anchor-missing) finding is
present, so the checker is CI-friendly. Soft findings alone do not fail.

Pure standard library; no third-party dependencies.
"""

import argparse
import json
import os
import re
import sys


# ---------------------------------------------------------------------------
# Markdown parsing helpers
# ---------------------------------------------------------------------------

# Inline link: [text](target "optional title"). Negative lookbehind avoids
# matching the image syntax ![alt](src) being treated specially -- images are
# fine to check too, so we keep them. We do skip the leading "!" capture.
INLINE_LINK_RE = re.compile(r"\[(?:[^\]]*)\]\(\s*([^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")

# Reference definition: [id]: target "optional title"
REF_DEF_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(\S+)")

# Wikilink: [[target]] or [[target#anchor]] or [[target|alias]]
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(#[^\]|]+)?(?:\|[^\]]+)?\]\]")

# Bare relative path mention ending in .md, optionally with #anchor. Not inside
# an inline link's parens (those are caught above). We grab tokens that look
# like a/b/c.md or c.md, allowing a trailing #anchor.
BARE_PATH_RE = re.compile(r"(?<![(\[/\w])([\w./-]+\.md(?:#[\w-]+)?)")

ATX_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")

URL_SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*://|^mailto:|^#")


def slugify(text):
    """GitHub-style heading slug.

    Lowercase, strip anything that's not word-char / space / hyphen, then
    collapse spaces to hyphens. Mirrors the common GFM behaviour closely enough
    for cross-reference checking.
    """
    text = text.strip().lower()
    # Drop inline markdown formatting markers and links, keep their text.
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)  # [t](u) -> t
    text = re.sub(r"[`*_~]", "", text)
    # Remove characters that are not alnum, space, or hyphen.
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = text.strip().replace(" ", "-")
    text = re.sub(r"-+", "-", text)
    return text


def parse_headings(lines):
    """Return list of (slug, raw_text, line_no) for ATX headings, skipping
    fenced code blocks. Duplicate slugs get GitHub-style ``-1``/``-2`` suffixes.
    """
    headings = []
    seen = {}
    in_fence = False
    for i, line in enumerate(lines, start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = ATX_HEADING_RE.match(line)
        if not m:
            continue
        raw = m.group(2)
        base = slugify(raw)
        slug = base
        if base in seen:
            seen[base] += 1
            slug = "%s-%d" % (base, seen[base])
        else:
            seen[base] = 0
        headings.append((slug, raw, i))
    return headings


def iter_md_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip hidden directories (.git, etc.)
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for name in sorted(filenames):
            if name.endswith(".md"):
                yield os.path.join(dirpath, name)


def extract_links(lines):
    """Yield (line_no, raw_target, kind) for each link-like token in a file.

    kind is one of: inline, refdef, wikilink, bare.
    Skips fenced code blocks and inline code spans.
    """
    in_fence = False
    for i, line in enumerate(lines, start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        # Blank out inline code spans so we don't parse links inside them.
        scrubbed = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)

        for m in INLINE_LINK_RE.finditer(scrubbed):
            yield i, m.group(1), "inline"

        refm = REF_DEF_RE.match(scrubbed)
        if refm:
            yield i, refm.group(1), "refdef"

        for m in WIKILINK_RE.finditer(scrubbed):
            target = m.group(1)
            if m.group(2):
                target += m.group(2)
            yield i, target, "wikilink"

        # Bare paths: blank out inline links first so we don't double-report.
        bare_scrub = INLINE_LINK_RE.sub(
            lambda m: " " * len(m.group(0)), scrubbed)
        bare_scrub = WIKILINK_RE.sub(
            lambda m: " " * len(m.group(0)), bare_scrub)
        for m in BARE_PATH_RE.finditer(bare_scrub):
            yield i, m.group(1), "bare"


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------

def split_anchor(target):
    if "#" in target:
        path, anchor = target.split("#", 1)
        return path, anchor
    return target, None


def closest(name, candidates, limit=3):
    """Return up to ``limit`` closest candidate strings by edit distance."""
    if not candidates:
        return []
    scored = sorted(candidates, key=lambda c: _levenshtein(name, c))
    return scored[:limit]


def _levenshtein(a, b):
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        cur = [i]
        for j, cb in enumerate(b, start=1):
            cost = 0 if ca == cb else 1
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost))
        prev = cur
    return prev[-1]


def check(root):
    root = os.path.abspath(root)
    files = list(iter_md_files(root))

    # Pre-parse headings for every file so anchor checks are O(1) lookups.
    headings_by_file = {}
    lines_by_file = {}
    for path in files:
        with open(path, "r", encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        lines_by_file[path] = lines
        headings_by_file[path] = parse_headings(lines)

    file_set = set(files)
    findings = []

    for path in files:
        rel_src = os.path.relpath(path, root)
        src_dir = os.path.dirname(path)
        own_slugs = {h[0] for h in headings_by_file[path]}

        for line_no, target, kind in extract_links(lines_by_file[path]):
            if URL_SCHEME_RE.match(target) and not target.startswith("#"):
                continue  # external URL

            # Template placeholders like <path> or fileB.md#<anchor> are not
            # real targets -- skip anything containing angle-bracket syntax.
            if "<" in target or ">" in target:
                continue

            path_part, anchor = split_anchor(target)

            # Same-file anchor (#foo with empty path part).
            if path_part == "" and anchor is not None:
                if anchor not in own_slugs:
                    findings.append(_finding(
                        rel_src, line_no, target, "anchor-missing", kind,
                        "no heading '%s' in this file" % anchor,
                        closest(anchor, sorted(own_slugs))))
                continue

            if path_part == "":
                continue

            # Resolve path against source dir, then corpus root.
            resolved = None
            for base in (src_dir, root):
                cand = os.path.normpath(os.path.join(base, path_part))
                if cand in file_set or os.path.isfile(cand):
                    resolved = cand
                    break

            if resolved is None:
                all_rel = sorted(os.path.relpath(f, root) for f in files)
                findings.append(_finding(
                    rel_src, line_no, target, "file-missing", kind,
                    "path does not resolve from source dir or corpus root",
                    closest(path_part, all_rel)))
                continue

            if anchor is not None:
                target_slugs = {h[0] for h in headings_by_file.get(resolved, [])}
                if anchor not in target_slugs:
                    findings.append(_finding(
                        rel_src, line_no, target, "anchor-missing", kind,
                        "no heading '%s' in %s" % (
                            anchor, os.path.relpath(resolved, root)),
                        closest(anchor, sorted(target_slugs))))

    heading_inventory = {
        os.path.relpath(p, root): [
            {"slug": s, "text": t, "line": ln}
            for (s, t, ln) in headings_by_file[p]
        ]
        for p in files
    }

    return {
        "root": root,
        "files_scanned": len(files),
        "findings": findings,
        "heading_inventory": heading_inventory,
    }


def _finding(src, line, raw, reason, kind, detail, suggestions):
    return {
        "source": "%s:%d" % (src, line),
        "raw": raw,
        "reason": reason,       # file-missing | anchor-missing
        "kind": kind,           # inline | refdef | wikilink | bare
        "detail": detail,
        "suggestions": suggestions,
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def is_hard(f, include_soft):
    # Bare-path findings are "soft" -- a prose path mention may be illustrative
    # rather than a real link. They never fail the build unless --soft-hard.
    if f["kind"] == "bare" and not include_soft:
        return False
    return True


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dir", help="directory of markdown files to check")
    ap.add_argument("--json", action="store_true",
                    help="emit full JSON report to stdout")
    ap.add_argument("--soft-hard", action="store_true",
                    help="treat bare-path (soft) findings as failures too")
    args = ap.parse_args(argv)

    if not os.path.isdir(args.dir):
        sys.stderr.write("error: not a directory: %s\n" % args.dir)
        return 2

    report = check(args.dir)
    findings = report["findings"]

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        # Default stdout: just the inventory is noisy, so emit findings here.
        print(json.dumps({"root": report["root"],
                          "files_scanned": report["files_scanned"],
                          "findings": findings}, indent=2, ensure_ascii=False))

    hard = [f for f in findings if is_hard(f, args.soft_hard)]
    soft = [f for f in findings if not is_hard(f, args.soft_hard)]

    # Human summary to stderr.
    sys.stderr.write("\n=== check_links: %d file(s) scanned ===\n"
                     % report["files_scanned"])
    if not findings:
        sys.stderr.write("No broken links found.\n")
    else:
        sys.stderr.write("%d hard finding(s), %d soft finding(s):\n"
                         % (len(hard), len(soft)))
        for f in hard + soft:
            tag = "HARD" if f in hard else "soft"
            sugg = (" | did you mean: %s" % ", ".join(f["suggestions"])
                    if f["suggestions"] else "")
            sys.stderr.write("  [%s] %s  ->  %s  (%s)%s\n" % (
                tag, f["source"], f["raw"], f["reason"], sugg))

    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
