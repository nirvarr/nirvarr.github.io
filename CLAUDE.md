# nirvarr.github.io: instructions for Claude

Academic website and CV of Nirvar Roy Vaskar, used for PhD applications.

## How it works
- All content lives in `data/*.yml` (profile, projects, publications, experience, news).
  The owner edits it in the Pages CMS dashboard (config: `.pages.yml`) or asks Claude.
- `scripts/build.py` fills `templates/index.html.j2` and `templates/cv.tex.j2` from the data.
  Output goes to `_site/` and `build/` (never committed).
- Every push to `main` runs `.github/workflows/deploy.yml`: build, validate, compile the CV
  (must be 2 pages), deploy to GitHub Pages.
- So: to change content, edit only `data/*.yml`. Never hand-edit generated output.

## House rules
- Keep the single-page profile-card design. No tabs or redesigns unless asked.
- No em dashes (the build fails on them). Use "2020 to 2021" for ranges.
- Never invent metrics, dates, co-authors or venues. Ask if something is missing.
- Concise academic prose, no hype words.
- No phone number, referee emails or home address in data files.
- Text fields accept `*italic*`, `**bold**`, `[text](https://...)`.

## Before finishing a change
`python scripts/build.py && npx --yes html-validate@9 _site/index.html && (cd build && latexmk -pdf -interaction=nonstopmode Nirvar_Roy_Vaskar_CV.tex)` and check the log says 2 pages.
