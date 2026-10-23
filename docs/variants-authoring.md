# Variant review in VS Code

This draft template slice connects VS Code to the existing installed
math-exercise authoring commands. It does not introduce a generic `ctm` launcher.
Install an authoring-capable CTM Assessment pack including `ctm-checkers`' native
authoring distribution and the math-exercise `variants-review.py` helper first.
Use a Python environment with the native authoring dependencies, including SymPy
and PyYAML, and Quarto available on PATH. The template's legacy `scripts/setup.py`
alone installs the individual extensions and is insufficient for this route.
Follow the assessment pack's native authoring installation guide; don't copy
native modules out of unrelated working directories.

## Prepare and review one question

Save the authored `.qmd` or included Markdown file. Its `math-exercise` block
needs a stable `#| label:` unique across the project and supported `variables` authoring. Generate retained
proposals explicitly once, using that file and label, for example:

```sh
python _extensions/math-exercise/question-variants.py --project . --file pages/lesson.qmd --label tangent generate25more
```

This writes `_variants/tangent.yml`; inspect that change in Source Control.
Then keep the saved source file active in the editor and select
**Terminal → Run Task → CTM: Review variants**. Enter the exact exercise label
and Python executable when prompted. The task passes the active file as one
process argument, so spaces in file paths are preserved.

The helper opens a random-token URL on `127.0.0.1`. Individual and bulk decisions
save immediately through the canonical native wrapper, which rereads current
source and validates the complete batch before one leased manifest write. A
successful save rebuilds the view. If the source changed or a response is
uncertain, use **Rebuild review** before another decision. Save editor changes
first; the helper reads disk and does not watch files. Stop with Ctrl-C.

The current view contains resolved text previews and test reports, rather than
full filter-rendered multilingual cards or a live Check button. For terminal-only
use, run the same helper with `--no-browser`; it prints the local URL.

## Read-only resolution

**CTM: Check variants (resolve proposals)** runs the installed wrapper's existing
`review` command for the active file and entered label. It resolves retained
proposals against current source without writing decisions and prints JSON with
records, tests, warnings and manifest state. Inspect that output: successful
command completion is not proof that all variants are approved or that all test
verdicts passed. A project-wide `ctm variants check --strict` command is not
supplied by these tasks.

Commit the authored source and `_variants/LABEL.yml` together after reviewing
them. The `/_variants/` CODEOWNERS entry requests review by the template
maintainer; replace it with your course's teaching maintainer. It adds no
required-code-owner branch protection rule.

This slice adds no workflow activation, publishing step, deployment, automatic
generation or filesystem watcher. GitHub review/check workflow templates remain
a separately reviewed integration. Ordinary `quarto preview` detection is still
unresolved; these tasks use the explicit native review route and do not weaken
the default required-approval publish gate.
