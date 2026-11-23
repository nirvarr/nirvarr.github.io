# nirvarr.github.io

Personal academic website of Nirvar Roy Vaskar: https://nirvarr.github.io

A single static page (`index.html`, no build step) with Home, CV, Publications,
Research and Contact tabs (deep links such as `/#cv` work). The CV PDF is
`Nirvar_Roy_Vaskar_CV.pdf`; its page previews and the profile photo are in `assets/`. Every push to `main` runs
`.github/workflows/deploy.yml`, which validates the HTML, checks links, and deploys
to GitHub Pages. Pull requests run the checks only.

To edit: change `index.html`, commit, push. The site updates in about a minute.
