# Variant review in VS Code

This draft template slice connects VS Code to the existing installed
math-exercise authoring commands. It does not introduce a generic `ctm` launcher.
Install an authoring-capable CTM Assessment pack including `ctm-checkers`' native
authoring distribution and the math-exercise `variants-review.py` helper first.
Use a Python environment with the native authoring dependencies, including SymPy
and PyYAML, and Quarto available on PATH. The template's legacy `scripts/setup.py`
alone installs the individual extensions and is insufficient for this route.
From the saved template checkout, install its reviewed native pack:

```sh
python -m pip install sympy==1.13.3 PyYAML==6.0.2
python scripts/install-native-authoring.py
```

This single-purpose bootstrap fetches the exact canonical assessment installer
and passes every component ref from `native-authoring-refs.json` explicitly.
That file includes the native authoring math PR32; using only assessment's
default registry can select the older math PR31 without native authoring.
The same command and shared refs drive the artifact-only CI proof. Installation
replaces only the canonical pack's owned extensions, verifies installed file
hashes, and records provenance under `.private-extensions/resolved-repos.json`.
It makes no teaching decisions. Git, Quarto1.8.27 and network access to the
public source repositories are required. This is a reviewed draft tuple, not a
release or a student rollout authorization. Do not run legacy `scripts/setup.py`
afterward: it installs individual extensions independently of this tuple.

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

The installed helper links to student previews rendered through the canonical
Quarto filters and shows native test reports. Browser runtime and preview
acceptance remain separate from the task transport check below. For terminal-only
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

The editor tasks add no publishing step, deployment, automatic generation or
filesystem watcher. GitHub teaching-decision workflows remain a separately
reviewed integration. Ordinary `quarto preview` detection is still
unresolved; these tasks use the explicit native review route and do not weaken
the default required-approval publish gate.

The separate **Installed native authoring tasks (artifacts only)** PR check now
installs a frozen published review pack through its canonical assessment
installer into a temporary minimal project. It validates both process tasks,
including a saved filename with spaces, resolves one synthetic proposal with
real teacher and authored tests, checks that resolution leaves its manifest
unchanged, and fetches the token-bound local review page. The fixture makes no
teaching decisions. Its artifacts record the installed component commits.
This check does not exercise the legacy `scripts/setup.py`, publish a site,
or establish VS Code GUI, multilingual student rendering, ordinary-preview
detection, browser grading, or project-wide strict approval acceptance.
