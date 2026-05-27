<!-- Replace placeholders in <angle-brackets> when filling this in. One finding per item. -->

> **Finding #N** *(YYYY-MM-DD)* — <one-line summary>
>
> **Where:** <file:line or symbol under review>
> **Severity:** blocker | major | minor | nit
> **Detail:** <what's wrong and why it matters — enough for the Coding Agent to act without a back-and-forth>
> **Suggested direction:** <optional — a way to address it; not binding on the Coding Agent>

<!--
The Review Agent appends the finding. The Coding Agent then appends its response block
directly beneath (shape in `reference/doc-ownership.md`). The Review Agent independently
verifies against the code and appends the resolution tag as the final line of the item:

> **Resolution:** fixed *(YYYY-MM-DD)*
> **Resolution:** wont-fix: <reason> *(YYYY-MM-DD)*
> **Resolution:** decision: <text> *(YYYY-MM-DD)*
> **Resolution:** spec-changed: <link> *(YYYY-MM-DD)*

Finding numbers (`Finding #N`) are per-file monotonic — see `reference/sequence-rules.md`.
On file split they keep their original number. Numbers never reuse, even after archive.

The Coding Agent never writes a Resolution line. The Review Agent never edits the
Coding Agent's response block. See `reference/doc-ownership.md`.
-->
