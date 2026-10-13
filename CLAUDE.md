# Conventions for this repo

- D&D only. Do not put client or non-D&D project work in this public repo.
- Each campaign is `campaigns/<slug>/`; start from `_shared/templates/campaign-skeleton/`.
- Markdown is the master. HTML is generated (`_shared/tools/build_html.py`); never hand-edit generated HTML.
- Map images go in `campaigns/<slug>/maps/{dm,players}/` and are listed with public raw URLs in `maps/LINKS.md`.
- The default branch is `main`. Do the work on a branch and merge after the DM has looked.
- Players can read this repo: keep spoilers in `dm/`, player-facing files in `players/`.
