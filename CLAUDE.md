# Uzbekistan Trek website

Static site for uzbekistantrek.com. The home page leads with the ambassador program: Uzbek graduate students at universities outside Uzbekistan bring their classmates on a trek, with our materials and support. Group trips stay as secondary pages for graduate students at any university (big groups of 10 or more, small groups under 10), linked from "Group trips" in the header and from the footer. GitHub Pages serves the root of `main`; merging into `main` publishes the site in a minute or two.

## How the site is built
- `index.html`, `big-group.html`, `small-group.html`, `founder.html` and `contact.html` are generated, and so are their Uzbek copies in `uz/`. Never edit them by hand.
- All text lives in `shared/content.py`, including the interface words in `UI`, `META` and `FORMS`. Photo captions and alt text live in `shared/photos.json`.
- Layout and CSS live in `shared/build.py`, with motion pieces in `shared/motion_parts.py`, forms in `shared/forms_html.py` and the logo in `shared/logos.py`.
- The Uzbek text lives in `shared/content_uz.py`, with the same names (photo captions in `PHOTO_TEXT`). When you change English text, change the Uzbek text too.
- Rebuild: `pip install fonttools` (once per machine), then `python3 shared/build.py` from the repository root.
- Both checks must pass before you commit:
  - `python3 shared/check.py . uz`: each photo once per site (per language), missing files and links, banned text.
  - `python3 shared/requirements.py`: content decisions the owner asked for.
- Edit the scripts directly: `assets/trek.js` (forms, menu, scroll to top, sliding FAQ, copy buttons, visitor counter, visit alerts) and `assets/motion.js` (motion and hover effects).
- `assets/config.js` belongs to the owner: it holds the relay address and the analytics token. Never overwrite, regenerate or reformat it. Change a line in it only when the owner asks.
- `worker/telegram-relay.js` is the Cloudflare Worker. GitHub does not deploy it: after changing it, tell the owner to paste it into the Worker in Cloudflare and deploy.
- `assets/trek.js` and `assets/motion.js` show a few words of their own; they pick English or Uzbek from `<html lang>`.
- `img/` holds only the photos the site uses. To add one, put a `.webp` (about 2000 px on the long side) in `img/` and add its entry to `shared/photos.json`.
- `files/` holds downloads linked from the site, such as the Harvard 2027 brochure next to the WhatsApp sample. In those files, prices show as [$X] and personal emails are removed (true redaction, not a box over the text).
- To look at the pages, run `python3 -m http.server 8000` in the repository root and open http://localhost:8000.

## Content rules
- No prices or dollar amounts anywhere.
- Graduate students, fellows and postdocs only; never undergraduates.
- Uzbekistan Trek is independent. Keep the independence line on every page, and never use a university's name or logo in a way that suggests it runs or endorses the trips.
- Formal government meetings are not part of the standard program for new universities; never promise them.
- Do not name or link to any tour operator or travel company.
- Never invent quotes, names, numbers or reviews. Use people's names and titles exactly as they appear in `shared/content.py`, and list government before the private sector.
- Never promise ambassadors pay, a discount, a free place or any other reward. Describe them as students organizing a trip for their own classmates.
- Co-Founders: Jakhongir Sadiev and Zokirjon Khabibullaev (Boston University). Never call Jakhongir just "Founder". Say only that Jakhongir's hometown is Samarkand. Never say he was born or raised there.
- Jakhongir's card on the home page uses `jakhongir_sadiev`, a different photo from the portrait on the founder page. Never use a crop of `founder_portrait` there.
- Contact: jsadiev@hks.harvard.edu (Jakhongir), zkhabib@bu.edu (Zokirjon) and Telegram @uzbtrek_bot. The Contact page (`contact.html`, text in `CONTACT` in `shared/content.py`) lists all three.
- No em dashes. Short, plain sentences.
- Uzbek pages (`uz/`) use the new Latin letters from the law of October 2026: Ö, Ğ, Ş, Ç (not Oʻ, Gʻ, Sh, Ch). In `content_uz.py`, write the familiar spelling (o', g', sh, ch); `newlat()` converts it when the module loads and leaves names in `PROTECT`, tags and links alone. Titles: Co-Founder is "Hammuassis", never just "asoschi". Ambassador is "elchi".
- On the Uzbek pages these stay in English: the sample texts and the brochure (ambassadors send them to international classmates), participants' quotes, the English names of schools and companies, and the Uzbekistan Trek brand.
- On the Uzbek pages, names use their Uzbek spelling, as in `content_uz.py`: Jaxongir Sadiyev and Zokirjon Xabibullayev (the owner's own spellings), and officials as Uzbek media write them (Tanzila Norboyeva, Shahnoza Mirziyoyeva, Qoʻngʻirotboy Sharipov, Hilola Umarova). The English pages keep the spellings in `content.py`.
- Each photo appears once per site, near-duplicates included (`SAME_PHOTO` in `shared/check.py`).
- When the owner asks to remove copy, also add it to `BANNED` in `shared/check.py` so it cannot come back.
- Check facts that change before stating them: visa rules, the US State Department advisory level, Uzbekistan Airways flights from New York, Nowruz dates, officials' current titles and form links. Cite the source.

## Working with the owner
- Work on a branch and open a pull request; the owner merges it.
- End every task with a short list of open items for the owner.
- When writing for Uzbek students, offer Uzbek and English versions.
