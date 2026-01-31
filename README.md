# Resume (generator)

This repository contains tooling to generate a PDF resume using LaTeX templates and a small Python codebase that helps build derived artifacts (for example: a GitHub README from user data). It is an in-progress personal project and the codebase is organized to separate data, generators, templates and utilities.

What this project does (currently)

- Generates a PDF resume using LaTeX templates located under `latex/template/`.
  - The LaTeX class and templates (e.g. `yaac-another-awesome-cv.cls`, `main.tex`, `cv.tex`) provide the visual/resume layout.
  - Fonts required for the resume are stored in `latex/fonts/`.
- Contains Python code under `src/resume/` that supports:
  - Data models (under `src/resume/data`) used to assemble resume content.
  - Generators (under `src/resume/generator`) that can produce files from templates (there is a `readme_generator.py` that renders a README from Jinja templates and user data).
  - Template helpers and utilities under `src/resume/template` and `src/resume/utils`.
- Includes a lightweight, Rich-powered logger utility at `src/resume/utils/logger.py` and a module-level `logger` exported from `src/resume/utils/__init__.py` for convenient imports (`from resume.utils import logger`).

Repository layout (important files/folders)

- `main.py` — entry point script (simple runner) at repository root.
- `requirements.txt` — Python dependencies used by the project.
- `latex/` — LaTeX templates, fonts and Makefile used to compile the PDF resume.
  - `latex/template/` — template files and supporting images.
- `src/resume/` — Python package source.
  - `data/` — user data models and sample data used by generators.
  - `generator/` — code that renders templated output (e.g. README generator using Jinja2).
  - `utils/` — utility modules including the `logger` (Rich-backed) and other helpers.

Quick start (developer)

1. Create a virtual environment (recommended) and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

2. Run the Python code (set PYTHONPATH so `src` is importable):

```bash
PYTHONPATH=src python3 main.py
```

Notes:
- Many modules expect the package to be importable as `resume` (the code is under `src/resume`). Setting `PYTHONPATH=src` or installing the package in editable mode (pip install -e .) will make imports work.
- The package includes a simple README generator at `src/resume/generator/readme_generator.py` which uses Jinja2 templates (templates are expected under `src/resume/generator/templates/` or similar) and a `UserData` model from `src/resume/data/user_data.py`.

Logging

- A simple Rich-based logger is available at `src/resume/utils/logger.py` and exported as the module-level `logger` (import via `from resume.utils import logger`).
- The logger prints colored, structured output to the terminal (when a TTY) and appends timestamped lines to `logs/<name>.log` by default.

Extensibility and next steps

- Wire-up the `main.py` entrypoint to call the generator codepaths you want (generate README, build LaTeX files, call `make` in `latex/template/` to compile PDF).
- Add tests for generators and file outputs (a couple of unit tests for `readme_generator` would be valuable).
- Consider packaging the Python code (setup.cfg/pyproject.toml) so the `resume` package can be installed into a virtualenv instead of relying on PYTHONPATH.

Contact / Notes

This README was generated to document the current state of the project and the main places to look when developing or running the code. If you want, I can also:

- Add a tiny example `scripts/` runner that shows how to render the README and compile the LaTeX PDF.
- Add tests and CI config (GitHub Actions) to automate builds.

