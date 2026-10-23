# Quarto Course Template

A reusable Quarto website template for course material with interactive
Python and mathematics exercises.

The template is designed for course repositories that use private Quarto
extensions maintained by `Erasmus-CTM`.

## New course checklist

1.  On GitHub, choose **Use this template → Create a new repository**.
2.  Configure the GitHub App variable and private-key secret in the new
    repository.
3.  Clone the new course repository locally.
4.  Install PyYAML with `python -m pip install pyyaml`.
5.  Run `python scripts/setup.py`.
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

The extensions themselves are private and are **not committed to this
repository**.

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

You must also have GitHub access to the private `Erasmus-CTM` extension
repositories.

## First-time local setup

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

## Updating the private extensions

Run:

``` bash
python scripts/setup.py
```

again.

The setup script performs a `git pull --ff-only` on existing plugin
repositories and reinstalls the configured extensions.

## Private extension configuration

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
  - pyodide-interaktiv
  - math-exercise
  - py-exercise
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

The repository contains a GitHub Actions workflow that:

1.  checks out the course repository
2.  installs Quarto
3.  installs Python
4.  creates a temporary GitHub App token
5.  downloads the private Erasmus-CTM Quarto extensions
6.  runs `scripts/setup.py`
7.  renders the Quarto website
8.  publishes the rendered site to the `gh-pages` branch

Pushing to `main` triggers the build and deployment.

## Required GitHub configuration

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

## GitHub App access

The GitHub App used by the workflow must be installed on the required
private Erasmus-CTM repositories.

It only needs:

``` text
Repository permissions
Contents: Read-only
```

For the current template it should have access to:

``` text
Erasmus-CTM/pyodide-interaktiv
Erasmus-CTM/math-exercise
Erasmus-CTM/py-exercise
```

The workflow creates a short-lived GitHub App token when it runs.

The private key itself remains stored as a GitHub Actions secret.

## Security model

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

## Adding another private Quarto extension

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

Update the private extensions if necessary:

``` bash
python scripts/setup.py
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
│   └── setup.py
├── _quarto.yml
├── quarto-extensions.yml
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

### `Could not clone private plugin`

Check that:

-   your GitHub account has access to the Erasmus-CTM repository
-   Git authentication works locally

A useful test is:

``` bash
git ls-remote https://github.com/Erasmus-CTM/pyodide-interaktiv.git
```

### `Could not run ... as a JSON filter`

Check that the private extensions have been installed:

``` bash
python scripts/setup.py
```

Then:

``` bash
quarto list extensions
```

### GitHub Actions cannot clone an extension

Check:

-   `ERASMUS_CTM_APP_CLIENT_ID`
-   `ERASMUS_CTM_APP_PRIVATE_KEY`
-   that the GitHub App is installed on the private extension repository
-   that the App has `Contents: Read-only`

### Local site is stale

Stop the preview server and run:

``` bash
quarto render
quarto preview
```

If browser caching is involved, perform a hard refresh.
