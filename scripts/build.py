"""Build the website and the CV from the files in data/.

Usage:  python scripts/build.py
Output: _site/index.html, _site/assets/, build/Nirvar_Roy_Vaskar_CV.tex
Then:   latexmk -pdf -outdir=build build/Nirvar_Roy_Vaskar_CV.tex

Text fields may use *italic*, **bold** and [link text](https://...).
"""
import datetime
import re
import shutil
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from markupsafe import Markup, escape

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SITE = ROOT / "_site"
BUILD = ROOT / "build"
CV_NAME = "Nirvar_Roy_Vaskar_CV"

TOKEN = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)|\*\*(.+?)\*\*|\*(.+?)\*")


def load(name):
    with open(DATA / f"{name}.yml", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


# ---------- text conversion ----------

def tex_escape(s):
    s = str(s)
    rep = {
        "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#",
        "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    }
    s = "".join(rep.get(c, c) for c in s)
    s = s.replace("LaTeX", r"\LaTeX{}")
    # spacing after abbreviations and between initials
    s = re.sub(r"\b(Assoc|Prof|Dr|Pte|Ltd|vs|e\.g|i\.e)\. ", r"\1.\\ ", s)
    s = re.sub(r"\b([A-Z])\. (?=[A-Z]\.)", r"\1.\\,", s)
    s = re.sub(r"\b([A-Z])\. (?=[A-Z][a-z])", r"\1.\\ ", s)
    return s


def tex_url(u):
    return str(u).replace("%", r"\%").replace("#", r"\#").replace("&", r"\&")


def convert(text, mode):
    """Convert light markup to HTML (mode='html') or LaTeX (mode='tex')."""
    text = "" if text is None else str(text)
    esc = (lambda s: str(escape(s))) if mode == "html" else tex_escape
    out, pos = [], 0
    for m in TOKEN.finditer(text):
        out.append(esc(text[pos:m.start()]))
        link_text, url, bold, ital = m.groups()
        if link_text is not None:
            inner = convert(link_text, mode)
            out.append(f'<a href="{escape(url)}">{inner}</a>' if mode == "html"
                       else rf"\href{{{tex_url(url)}}}{{{inner}}}")
        elif bold is not None:
            inner = convert(bold, mode)
            out.append(f"<strong>{inner}</strong>" if mode == "html" else rf"\textbf{{{inner}}}")
        else:
            inner = convert(ital, mode)
            out.append(f"<em>{inner}</em>" if mode == "html" else rf"\emph{{{inner}}}")
        pos = m.end()
    out.append(esc(text[pos:]))
    return "".join(out)


def html(text):
    return Markup(convert(text, "html"))


def tex(text):
    return convert(text, "tex")


# ---------- publications ----------

def pub_status(p):
    status = (p.get("status") or "Published").strip()
    venue, details = p.get("venue") or "", p.get("details") or ""
    tail = f", {details}" if details else ""
    if status == "Published":
        return f"In *{venue}*{tail}." if venue else f"{details}."
    if status == "Accepted":
        return f"Accepted at *{venue}*{tail}." if venue else "Accepted."
    if status == "Under review":
        return f"Under review at *{venue}*." if venue else "Under review."
    return "Manuscript in preparation."


def main():
    profile = load("profile")
    projects = load("projects")
    pubs = load("publications")
    experience = load("experience")
    news = load("news")

    me = profile["short_name"]
    for p in pubs:
        p["authors_marked"] = p["authors"].replace(me, f"**{me}**")
        p["status_text"] = pub_status(p)

    ctx = dict(
        p=profile,
        site_projects=[x for x in projects if x.get("show_on_site")][:6],
        cv_projects=[x for x in projects if x.get("show_on_cv")][:4],
        pubs=pubs,
        research=[x for x in experience if x.get("type") == "Research"],
        professional=[x for x in experience if x.get("type") == "Professional"],
        news=news[:6],
        year=datetime.date.today().year,
        cv_file=f"{CV_NAME}.pdf",
    )

    # website
    env = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=True,
                      undefined=StrictUndefined, keep_trailing_newline=True,
                      trim_blocks=True, lstrip_blocks=True)
    env.filters["md"] = html
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    (SITE / "index.html").write_text(env.get_template("index.html.j2").render(**ctx), encoding="utf-8")
    (SITE / ".nojekyll").write_text("")
    shutil.copytree(ROOT / "assets", SITE / "assets")

    # CV (LaTeX-friendly delimiters)
    tenv = Environment(loader=FileSystemLoader(ROOT / "templates"), autoescape=False,
                       undefined=StrictUndefined, keep_trailing_newline=True,
                       block_start_string="((*", block_end_string="*))",
                       variable_start_string="(((", variable_end_string=")))",
                       comment_start_string="((#", comment_end_string="#))",
                       trim_blocks=True, lstrip_blocks=True)
    tenv.filters["md"] = tex
    tenv.filters["url"] = tex_url
    BUILD.mkdir(exist_ok=True)
    (BUILD / f"{CV_NAME}.tex").write_text(tenv.get_template("cv.tex.j2").render(**ctx), encoding="utf-8")

    # house rule: no em dashes anywhere in the output
    for f in [SITE / "index.html", BUILD / f"{CV_NAME}.tex"]:
        if "—" in f.read_text(encoding="utf-8"):
            sys.exit(f"Em dash found in {f.name}. Replace it in the data files.")
    print("Built _site/index.html and build/%s.tex" % CV_NAME)


if __name__ == "__main__":
    main()
