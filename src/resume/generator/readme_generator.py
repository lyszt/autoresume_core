from pathlib import Path
from urllib.parse import quote

from jinja2 import Environment, FileSystemLoader

from src.resume.data.user_data import UserData

# GitHub language name -> (logo, color, logo_color). logo_color omitted => white.
LANG_BADGES: dict[str, tuple[str, str, str]] = {
    "Assembly": ("assemblyscript", "007AAC", "white"),
    "C": ("c", "A8B9CC", "white"),
    "C++": ("cplusplus", "00599C", "white"),
    "Elixir": ("elixir", "4B275F", "white"),
    "HTML": ("html5", "E34F26", "white"),
    "Java": ("openjdk", "ED8B00", "white"),
    "JavaScript": ("javascript", "F7DF1E", "black"),
    "PHP": ("php", "777BB4", "white"),
    "Python": ("python", "3776AB", "white"),
    "TeX": ("latex", "008080", "white"),
    "TypeScript": ("typescript", "3178C6", "white"),
}


def _badge_markdown(name: str, logo: str, color: str, logo_color: str) -> str:
    label = quote(name)
    url = f"https://img.shields.io/badge/{label}-{color}?style=for-the-badge&logo={logo}&logoColor={logo_color}"
    return f"![{name}]({url})"


def _format_skill_badges(skills: list[str]) -> str:
    lines = []
    for lang in skills:
        if lang in LANG_BADGES:
            logo, color, logo_color = LANG_BADGES[lang]
            lines.append(_badge_markdown(lang, logo, color, logo_color))
        else:
            # Generic badge for unknown languages
            label = quote(lang)
            url = f"https://img.shields.io/badge/{label}-000000?style=for-the-badge"
            lines.append(f"![{lang}]({url})")
    return "\n".join(lines)


def _format_projects_overview(user_data: UserData) -> str:
    lines = []
    if user_data.core_projects:
        lines.append("### Core projects")
        for repo in user_data.core_projects:
            desc = repo.get("desc") or ""
            lines.append(f"- [{repo['name']}]({repo['url']}): {desc}")
    if user_data.edu_projects:
        lines.append("### Education projects")
        for repo in user_data.edu_projects:
            desc = repo.get("desc") or ""
            lines.append(f"- [{repo['name']}]({repo['url']}): {desc}")
    if user_data.legacy_projects:
        lines.append("### Legacy projects")
        for repo in user_data.legacy_projects:
            desc = repo.get("desc") or ""
            lines.append(f"- [{repo['name']}]({repo['url']}): {desc}")
    return "\n\n".join(lines) if lines else ""


def _find_academy_repo_url(user_data: UserData) -> str | None:
    default = "https://github.com/lyszt/Academie-de-Lyszt"
    for repo in user_data.user_info.values():
        name = repo.get("name", "")
        if "academie" in name.lower():
            return repo.get("url") or default
    return default


def build_context(user_data: UserData) -> dict:
    return {
        "github_username": "lyszt",
        "academy_repo_url": _find_academy_repo_url(user_data),
        "projects_overview_text": _format_projects_overview(user_data),
        "skill_badges": _format_skill_badges(user_data.skills),
    }


def render_readme(context: dict | None = None) -> str:
    template_dir = Path(__file__).resolve().parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    template = env.get_template("readme.md.j2")
    return template.render(**(context or {}))


def generate_readme_md(user_data: UserData, output_path: Path) -> None:
    context = build_context(user_data)
    content = render_readme(context)
    output_path.write_text(content, encoding="utf-8")
