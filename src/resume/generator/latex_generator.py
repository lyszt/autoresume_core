"""Render LaTeX Jinja2 templates to .tex files."""

from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader

# Template filenames under templates/latex/ (output name = stem without .j2)
LATEX_TEMPLATE_NAMES = [
    "cv.tex.j2",
    "section_headline.tex.j2",
    "section_competences.tex.j2",
    "section_experience_short.tex.j2",
    "section_langues.tex.j2",
    "section_scolarite.tex.j2",
    "section_interets.tex.j2",
    "section_projets.tex.j2",
    "section_references.tex.j2",
]


def _template_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "templates" / "latex"


def get_default_latex_context() -> dict:
    """Minimal context so all LaTeX templates render without missing variables."""
    return {
        "name_first": "First",
        "name_last": "Last",
        "tagline": "Tagline",
        "photo_size": "4cm",
        "photo_file": "Menshots-nobg",
        "linkedin": "username",
        "smartphone": "+00 0 0000 0000",
        "email": "email@example.com",
        "address": "Address",
        "footer_date": "\\today",
        "footer_title": "First Last - CV",
        "include_interests": False,
        "headline_text": "Summary or headline paragraph.",
        "competence_entries": [],
        "experience_entries": [],
        "language_skills": [],
        "it_skills": [],
        "education_entries": [],
        "interests_content": "",
        "project_entries": [],
        "reference_entries": [],
    }


def _env(loader_path: Path | None = None) -> Environment:
    path = loader_path or _template_dir()
    return Environment(
        loader=FileSystemLoader(str(path)),
        autoescape=False,
    )


def render_latex_template(
    template_name: str,
    context: dict,
    env: Environment | None = None,
) -> str:
    """Render a single LaTeX Jinja2 template to a string."""
    if env is None:
        env = _env()
    template = env.get_template(template_name)
    return template.render(**context)


def _project_entry_from_config(proj: dict) -> dict:
    """Build a project entry with link_markup from link_url/link_text if present."""
    out = dict(proj)
    url = proj.get("link_url")
    text = proj.get("link_text")
    if url and text:
        out["link_markup"] = f"\\website{{{url}}}{{{text}}}"
    else:
        out.setdefault("link_markup", "")
    return out


def load_context_from_config(config_path: Path | str | None = None) -> dict:
    """
    Load config.yaml and return a context dict for generate_latex().

    config_path defaults to config.yaml in the repository root.
    Merges with get_default_latex_context() so missing keys have defaults.
    project_entries: link_url + link_text are turned into link_markup (\\website{url}{text}).
    """
    if config_path is None:
        repo_root = Path(__file__).resolve().parent.parent.parent.parent
        config_path = repo_root / "config.yaml"
    path = Path(config_path)
    if not path.exists():
        return get_default_latex_context()

    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    base = get_default_latex_context()
    base.update(raw)

    # Build project link_markup from link_url/link_text
    if base.get("project_entries"):
        base["project_entries"] = [
            _project_entry_from_config(p) for p in base["project_entries"]
        ]

    return base


def generate_latex(
    context: dict | None = None,
    output_dir: Path | None = None,
    template_dir: Path | None = None,
) -> list[Path]:
    """
    Render all LaTeX Jinja2 templates and write .tex files to output_dir.

    Uses get_default_latex_context() as base; keys in context override.
    output_dir defaults to latex/template/ relative to repo root.
    Returns the list of written .tex paths.
    """
    base = get_default_latex_context()
    if context:
        base.update(context)
    ctx = base

    if output_dir is None:
        # Repo root: generator -> resume -> src -> repo root
        output_dir = (
            Path(__file__).resolve().parent.parent.parent.parent / "latex" / "template"
        )
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    loader_path = template_dir or _template_dir()
    env = _env(loader_path)
    written: list[Path] = []

    for name in LATEX_TEMPLATE_NAMES:
        if not name.endswith(".j2"):
            continue
        out_name = name.removesuffix(".j2")
        content = render_latex_template(name, ctx, env=env)
        out_path = output_dir / out_name
        out_path.write_text(content, encoding="utf-8")
        written.append(out_path)

    return written
