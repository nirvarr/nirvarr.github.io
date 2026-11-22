# nirvarr.github.io

Personal academic website of Nirvar Roy Vaskar: https://nirvarr.github.io

A single static page (`index.html`, no build step). Every push to `main` runs
`.github/workflows/deploy.yml`, which validates the HTML, checks links, and deploys
to GitHub Pages. Pull requests run the checks only.

To edit: change `index.html`, commit, push. The site updates in about a minute.
