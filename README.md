# Wenjun Zheng — Academic Homepage

Static academic website for Wenjun Zheng, hosted at [simpleboyguy.github.io](https://simpleboyguy.github.io/).

Repository: [SimpleBoyGuy/SimpleBoyGuy.github.io](https://github.com/SimpleBoyGuy/SimpleBoyGuy.github.io).

## Files

- `index.html`: biography, research, publications, experience, and contact information.
- `project-apdpo.html`: RL Solver for FJSP project, figures, benchmark results, and related papers.
- `styles.css`: shared layout, typography, and responsive styles.
- `assets/wenjun-zheng.jpg`: profile photograph.
- `assets/APDPO_CDC2025.pdf`: downloadable paper.
- `assets/*.webp`: optimized project figures used on the website (about 394 KB combined). Original PNG figures are retained and open when a project figure is clicked.
- `assets/Wenjun_Zheng_CV.pdf`: CV linked from the homepage.
- `scripts/generate_project_benchmark_figure.py`: source script for the benchmark comparison figure.

## Local preview

Open a terminal in this repository and run:

```sh
python -m http.server 8765 --bind 127.0.0.1
```

Then open [http://127.0.0.1:8765](http://127.0.0.1:8765). On Windows, `py -m http.server 8765 --bind 127.0.0.1` also works when the Python launcher is installed. Stop the server with `Ctrl+C`.

Local editing and previewing require no GitHub password, access token, or repository authorization. The website has no build step and uses system fonts.

## GitHub Pages

The repository already exists and its local branch is `main`. To publish reviewed changes, use an authenticated Git client to commit and push them to this repository. Editing or previewing the files locally does not publish them.

In the repository's **Settings → Pages**, choose **Deploy from a branch**, then select **main** and **/ (root)**. Save the configuration and allow the Pages deployment to complete before checking [https://simpleboyguy.github.io/](https://simpleboyguy.github.io/).

## Content updates

Edit the relevant HTML file directly. Keep paper titles, publication status, author lists, numerical results, and contact details aligned with the author's confirmed information. When editing shared styles, update the stylesheet query string in both HTML pages if cache invalidation is needed.
