# nirvarr.github.io

Academic website and CV of Nirvar Roy Vaskar: https://nirvarr.github.io

## Editing (the dashboard)

1. Go to https://app.pagescms.org and sign in with GitHub.
2. Open this repository. You will see: Projects, Publications, News,
   Research and work experience, Profile.
3. Change anything and press **Save**.

About two minutes later the website **and** the CV PDF are both updated from the same text.

## How it works

```
data/*.yml  ──►  scripts/build.py  ──►  website (index.html)
 (dashboard)        (on GitHub)    └──►  CV (LaTeX → PDF)
```

- `data/`: all content. This is the only place to edit.
- `templates/`: the website design and the CV layout.
- `.pages.yml`: what the dashboard shows.
- `.github/workflows/deploy.yml`: builds, checks (valid HTML, working links, CV is 2 pages)
  and publishes on every save. If a check fails, the old site stays up and GitHub emails you.

Text fields accept `*italic*`, `**bold**` and `[link text](https://...)`.

Local preview: `pip install pyyaml jinja2 && python scripts/build.py`, then open `_site/index.html`.
