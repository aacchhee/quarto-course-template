# Quarto Course Template

A reusable Quarto website template for course material with interactive
Python and mathematics exercises.

The template uses a reviewed CTM Assessment pack from the public
`Erasmus-CTM` source repositories.

## New course checklist

1.  On GitHub, choose **Use this template → Create a new repository**.
2.  Review `native-authoring-refs.json`, the shared explicit component tuple
    used for local installation, artifact checks and normal publishing.
3.  Clone the new course repository locally.
4.  For the reviewed native authoring pack, install dependencies with
    `python -m pip install sympy==1.13.3 PyYAML==6.0.2`.
5.  Run `python scripts/install-native-authoring.py`; see
    [the reviewed authoring installation](docs/variants-authoring.md) for its
    explicit draft tuple and scope. Legacy `scripts/setup.py` installs individual
    extensions and does not provide this native authoring pack.
6.  Edit `_quarto.yml`, `index.qmd`, and the example pages for the new
    course.
7.  Run `quarto render` before the first push.

## Included interactive extensions

The template currently uses:

-   `pyodide-interaktiv`
    -   interactive Python cells
    -   runs Python directly in the browser using Pyodide
    -   no server-side Python kernel required for students
-   `math-exercise`
    -   interactive mathematical exercises
    -   symbolic answer checking with SymPy/Pyodide
-   `py-exercise`
    -   interactive Python programming exercises
    -   starter code in a Monaco editor
    -   hidden unit tests
    -   runs entirely in the browser

Installed extensions are **not committed to this repository**; the shared
reviewed refs record which public source commits to install.

## Creating a new course

On GitHub, click:

**Use this template → Create a new repository**

Choose a repository name for your course.

After creating the new repository, clone it locally:

``` bash
git clone https://github.com/YOUR-ACCOUNT/YOUR-COURSE.git
cd YOUR-COURSE
```

## Requirements

Install the following on your development machine:

-   Git
-   Python 3
-   Quarto
-   VS Code is recommended but optional

The native authoring route above uses public reviewed sources. The retained
legacy reference sections below describe the separate older
individual-extension workflow and its private-access assumptions. They do not
install the native authoring pack. Use `scripts/install-native-authoring.py`
to install or refresh that pack; do not rerun `scripts/setup.py` afterward.

## Legacy first-time local setup

Install PyYAML:

``` bash
python -m pip install pyyaml
```

On systems where Python is called `python3`:

``` bash
python3 -m pip install pyyaml
```

Then install the private Quarto extensions:

``` bash
python scripts/setup.py
```

or:

``` bash
python3 scripts/setup.py
```

The setup script reads:

``` text
quarto-extensions.yml
```

and automatically:

1.  clones the private extension repositories
2.  stores the source repositories under `.private-extensions/`
3.  installs the requested Quarto extensions into `_extensions/`
4.  updates existing extension clones on later runs

The private source repositories and installed extensions are excluded
from Git.

## Preview the course locally

For the draft CTM native variants authoring tasks, see
[Variant review in VS Code](docs/variants-authoring.md). These tasks require an
installed authoring-capable assessment pack; the legacy setup above does not
provide its native authoring distribution.

Start the Quarto development server:

``` bash
quarto preview
```

For a complete render:

``` bash
quarto render
```

A full `quarto render` is recommended before pushing changes.

## Legacy updates of individual extensions

Run:

``` bash
python scripts/setup.py
```

again.

The setup script performs a `git pull --ff-only` on existing plugin
repositories and reinstalls the configured extensions.

## Legacy private extension configuration

Extensions are configured in:

``` text
quarto-extensions.yml
```

For example:

``` yaml
plugins:
  - name: pyodide-interaktiv
    repo: https://github.com/Erasmus-CTM/pyodide-interaktiv.git
    path: _extensions/pyodide-interaktiv

  - name: math-exercise
    repo: https://github.com/Erasmus-CTM/math-exercise.git
    path: _extensions/math-exercise

  - name: py-exercise
    repo: https://github.com/Erasmus-CTM/py-exercise.git
    path: _extensions/py-exercise
```

The `path` value is important.

A private repository may contain more than one Quarto extension or
development dependencies. The setup script installs only the extension
explicitly listed here.

## Using the extensions

The extensions can be enabled globally in `_quarto.yml`:

``` yaml
filters:
  - ctm-assessment
```

### Interactive Python cell

```` markdown
```{pyodide-python}
import numpy as np

x = np.arange(5)
print(x**2)
```
````

### Mathematics exercise

```` markdown
```{math-exercise}
#| label: math-1
#| caption: Simple calculation

What is $2+3$? _[5]
```
````

### Python programming exercise

```` markdown
```{py-exercise}
#| label: python-1
#| caption: Implement addition

def add(a, b):
    pass

## TESTS ##
assert add(1, 2) == 3
assert add(-1, 1) == 0
```
````

Everything below `## TESTS ##` is hidden from the student and used to
check the submitted code.

## GitHub Actions and GitHub Pages

The normal publisher and artifact-only PR check both install the explicit
`native-authoring-refs.json` tuple through `scripts/install-native-authoring.py`.
The publisher pins Quarto1.8.27 and the native SymPy/PyYAML dependencies, then
renders through the canonical `ctm-assessment` filter. It does not reinstall
individual extensions from unpinned default branches or require App secrets.

The existing push triggers, concurrency and main-only Pages publication guard
are unchanged. A PR workflow edit does not deploy a site. Publishing uses the
ordinary required-approval mode: unapproved native variants stop the render;
the publisher never switches to optional/review mode or approves questions.

## Legacy GitHub App configuration

The following App/security instructions are retained only as historical
reference for optional legacy individual-extension workflows. They are not
used by the current publisher or canonical native installation. Do not run
legacy setup over the installed native pack.

Repositories created from this template **do not inherit GitHub secrets
or variables**.

Before GitHub Actions can access the private Erasmus-CTM extensions,
configure the new course repository.

Go to:

**Repository → Settings → Secrets and variables → Actions**

### Repository variable

Create:

``` text
ERASMUS_CTM_APP_CLIENT_ID
```

with the Client ID of the Erasmus-CTM GitHub App.

### Repository secret

Create:

``` text
ERASMUS_CTM_APP_PRIVATE_KEY
```

and paste the complete private key for the GitHub App, including its
`BEGIN` and `END` lines.

Do not commit the private key to the repository.

## Legacy GitHub App access

The GitHub App used by the workflow must be installed on the required
private Erasmus-CTM repositories.

It only needs:

``` text
Repository permissions
Contents: Read-only
```

For that legacy configuration it would need access to:

``` text
Erasmus-CTM/pyodide-interaktiv
Erasmus-CTM/math-exercise
Erasmus-CTM/py-exercise
```

A configured legacy workflow creates a short-lived GitHub App token.

The private key itself remains stored as a GitHub Actions secret.

## Legacy private-extension security model

This template repository may be public.

The names and URLs of the private extensions are visible in
`quarto-extensions.yml`, but that does **not** give anyone access to
them.

For local development:

``` text
python scripts/setup.py
        ↓
Git authenticates the local user
        ↓
GitHub checks whether the user has access
        ↓
private plugin is cloned
```

A user without permission to the Erasmus-CTM repositories cannot
download the private extensions.

For GitHub Actions:

``` text
GitHub App private key
        ↓
short-lived installation token
        ↓
private extension repositories
        ↓
quarto render
```

## Legacy addition of a private Quarto extension

First give the Erasmus-CTM GitHub App read access to the new repository.

Then add an entry to `quarto-extensions.yml`:

``` yaml
plugins:
  - name: example-extension
    repo: https://github.com/Erasmus-CTM/example-extension.git
    path: _extensions/example-extension
```

Add the installed extension to `.gitignore`:

``` gitignore
/_extensions/example-extension/
```

Then install it locally:

``` bash
python scripts/setup.py
```

Verify:

``` bash
quarto list extensions
quarto render
```

## Typical development workflow

Refresh the reviewed pack if necessary:

``` bash
python scripts/install-native-authoring.py
```

Preview locally:

``` bash
quarto preview
```

Before publishing:

``` bash
quarto render
```

Then commit and push:

``` bash
git add .
git commit -m "Update course material"
git push
```

GitHub Actions will render and publish the site.

## Repository structure

``` text
.
├── .github/
│   └── workflows/
│       └── quarto.yml
├── .private-extensions/        # generated locally, ignored
├── _extensions/
│   ├── pyodide-interaktiv/     # generated locally, ignored
│   ├── math-exercise/          # generated locally, ignored
│   └── py-exercise/            # generated locally, ignored
├── pages/
│   └── ...                     # example/course pages
├── scripts/
│   ├── install-native-authoring.py
│   └── setup.py                 # optional legacy reference
├── _quarto.yml
├── native-authoring-refs.json  # current explicit pack tuple
├── quarto-extensions.yml       # optional legacy configuration
├── .gitignore
└── README.md
```

## Customising the template

At minimum, a new course should normally change:

-   the website title in `_quarto.yml`
-   the sidebar/navigation in `_quarto.yml`
-   `index.qmd`
-   the example pages under `pages/`

The included content can be kept as examples or replaced with actual
course material.

## Troubleshooting

### Legacy `Could not clone private plugin`

Check that:

-   your GitHub account has access to the Erasmus-CTM repository
-   Git authentication works locally

A useful test is:

``` bash
git ls-remote https://github.com/Erasmus-CTM/pyodide-interaktiv.git
```

### `Could not run ... as a JSON filter`

Install the shared canonical pack:

``` bash
python scripts/install-native-authoring.py
```

Then:

``` bash
quarto list extensions
```

### GitHub Actions cannot fetch the reviewed pack

Check network access to the public source repositories and that the exact
commits in `native-authoring-refs.json` remain available. The current publisher
uses the same canonical helper as local setup; it does not read the legacy
GitHub App variables or private-key secret.

### Local site is stale

Stop the preview server and run:

``` bash
quarto render
quarto preview
```

If browser caching is involved, perform a hard refresh.
