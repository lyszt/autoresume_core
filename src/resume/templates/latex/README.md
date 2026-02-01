# LaTeX Jinja2 templates

Templates mirror the structure in `latex/template/` (yaac-another-awesome-cv). Render with Jinja2, then copy the generated `.tex` files into `latex/template/` and run `make` to produce the PDF.

## Main template: `cv.tex.j2`

**Variables:**

| Variable | Description |
|----------|-------------|
| `name_first`, `name_last` | Header name |
| `tagline` | Subtitle under name |
| `photo_size` | Photo width (default `4cm`) |
| `photo_file` | Photo filename without extension (e.g. `Menshots-nobg`) |
| `linkedin`, `smartphone`, `email`, `address` | Social block |
| `footer_date` | Footer left (default `\today`) |
| `footer_title` | Footer center (default name + " - CV") |
| `include_interests` | If true, `\input{section_interets}` is included |

## Section templates (each renders to a `.tex` file)

- **section_headline.tex.j2** — `headline_text` (raw LaTeX paragraph).
- **section_competences.tex.j2** — `competence_section_title`, `competence_entries`: list of `{ category, text }`.
- **section_experience_short.tex.j2** — `experience_section_title`, `experience_entries`: list of `{ date_from, date_to, title, company, location, description, tags }` (description can be raw LaTeX, e.g. `\begin{itemize}...`).
- **section_langues.tex.j2** — `languages_section_title`, `language_skills`: list of `{ name, level }`; `it_section_title`, `it_skills`: list of `{ name, level }`.
- **section_scolarite.tex.j2** — `education_section_title`, `education_entries`: list of `{ period, description }`.
- **section_interets.tex.j2** — `interests_section_title`, `interests_content` (raw LaTeX tabular rows).
- **section_projets.tex.j2** — `projects_section_title`, `project_entries`: list of `{ title, subtitle, link_markup, description, tags }` (link_markup can be e.g. `\website{url}{text}`).
- **section_references.tex.j2** — `references_section_title`, `reference_entries`: list of `{ name, role, company, email }`.

All section titles have defaults (e.g. "Kompetencer", "Job Erfaring"). Omit a section by passing an empty list for its entries (or skip rendering that section file).
