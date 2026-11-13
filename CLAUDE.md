# Uzbekistan Trek website

Static site for uzbekistantrek.com: trips to Uzbekistan for graduate students at any university (big groups of 10 or more, small groups under 10). GitHub Pages serves the root of `main`; merging into `main` publishes the site in a minute or two.

## How the site is built
- `index.html`, `big-group.html`, `small-group.html` and `founder.html` are generated. Never edit them by hand.
- All text lives in `shared/content.py`. Photo captions and alt text live in `shared/photos.json`. Layout and CSS live in `shared/build.py`, with motion pieces in `shared/motion_parts.py`, forms in `shared/forms_html.py` and the logo in `shared/logos.py`.
- Rebuild: `pip install fonttools` (once per machine), then `python3 shared/build.py` from the repository root.
- Both checks must pass before you commit:
  - `python3 shared/check.py .`: each photo once per site, missing files and links, banned text.
  - `python3 shared/requirements.py`: content decisions the owner asked for.
- Edit the scripts directly: `assets/trek.js` (forms, menu, scroll to top, sliding FAQ, copy buttons, visitor counter, visit alerts) and `assets/motion.js` (motion and hover effects).
- `assets/config.js` belongs to the owner: it holds the relay address and the analytics token. Never overwrite, regenerate or reformat it. Change a line in it only when the owner asks.
- `worker/telegram-relay.js` is the Cloudflare Worker. GitHub does not deploy it: after changing it, tell the owner to paste it into the Worker in Cloudflare and deploy.
- `img/` holds only the photos the site uses. To add one, put a `.webp` (about 2000 px on the long side) in `img/` and add its entry to `shared/photos.json`.
- To look at the pages, run `python3 -m http.server 8000` in the repository root and open http://localhost:8000.

## Content rules
- No prices or dollar amounts anywhere.
- Graduate students, fellows and postdocs only; never undergraduates.
- Uzbekistan Trek is independent. Keep the independence line on every page, and never use a university's name or logo in a way that suggests it runs or endorses the trips.
- Formal government meetings are not part of the standard program for new universities; never promise them.
- Do not name or link to any tour operator or travel company.
- Never invent quotes, names, numbers or reviews. Use people's names and titles exactly as they appear in `shared/content.py`, and list government before the private sector.
- Founder: say only that his hometown is Samarkand. Never say he was born or raised there.
- Contact: jsadiev@hks.harvard.edu and Telegram @uzbtrek_bot.
- No em dashes. Short, plain sentences.
- Each photo appears once per site, near-duplicates included (`SAME_PHOTO` in `shared/check.py`).
- When the owner asks to remove copy, also add it to `BANNED` in `shared/check.py` so it cannot come back.
- Check facts that change before stating them: visa rules, the US State Department advisory level, Uzbekistan Airways flights from New York, Nowruz dates, officials' current titles and form links. Cite the source.

## Working with the owner
- Work on a branch and open a pull request; the owner merges it.
- End every task with a short list of open items for the owner.
- When writing for Uzbek students, offer Uzbek and English versions.
