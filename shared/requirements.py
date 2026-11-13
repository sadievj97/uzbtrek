#!/usr/bin/env python3
"""Requirement checks for the Uzbekistan Trek site: content decisions the owner asked for, so that a later edit
cannot quietly undo them. Run from the repository root after building:  python3 shared/requirements.py
Each rule is (page, label, pattern, expected): True = the visible text must match, False = it must not,
'raw' = the HTML source must match. When the owner changes his mind about one of these, update the rule too."""
import html, os, re, sys

SITE_ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))


def text_of(path):
    raw = open(path, encoding="utf-8").read()
    t = re.sub(r"<script\b[^>]*>.*?</script>", "", raw, flags=re.S | re.I)
    t = re.sub(r"<style\b[^>]*>.*?</style>", "", t, flags=re.S | re.I)
    vis = html.unescape(re.sub(r"<[^>]+>", " ", t))
    vis = re.sub(r"\s+", " ", vis).replace("\u2019", "'").replace("\u2018", "'")
    return raw, vis


R=[
 # ambassador program (13 Nov 2026): hero and "Who we are" from the owner's mock-ups
 ('home','hero pill and title', r'Ambassador program Become an Uzbekistan Trek Ambassador', True),
 ('home','hero lede', r'Bring Uzbekistan to your campus\. You coordinate your students\. We give you the materials, the promotion techniques and support at every step, and you travel to Uzbekistan with your group\.', True),
 ('home','hero title: Uzbekistan Trek as a white sticker', r'<h1 id="home-title">Become an <span class="sticker">Uzbekistan Trek</span> Ambassador</h1>', 'raw'),
 ('home','hero buttons', r'href="#apply">Apply now</a>\s*<a class="btn btn-line" href="#how">How it works', 'raw'),
 ('home','who we are lede', r'We are Jakhongir and Zokirjon, two Uzbek graduate students in Boston who love showing our country to classmates from around the world\.', True),
 ('home','founder card', r'Founder Jakhongir Sadiev Harvard Kennedy School\. Started the trek at Harvard in 2025: two treks, 95 travelers\. Read his story', True),
 ('home','co-founder card', r'Co-Founder Zokirjon Khabibullaev Boston University\. Coordinates the ambassador program and the trek.s growth to new universities\.', True),
 ('home','what you get', r'What you get.*Ready-made materials.*Promotion techniques.*Support at every step.*Travel with your group', True),
 ('home','application form', r'data-form="ambassador"', 'raw'),
 ('home','who can apply', r'Uzbek graduate students, fellows and postdocs at universities outside Uzbekistan', True),
 ('home','group pages still linked', r'href="big-group\.html".*href="small-group\.html"', 'raw'),
 ('home','old #start links still land', r'id="start"', 'raw'),
 ('home','old #choose links still land', r'id="choose"', 'raw'),
 ('big','header apply button', r'href="\./#apply">Apply now<', 'raw'),
 ('founder','founder cta apply', r'Bring Uzbekistan to your campus', True),
 ('any','no pay or perks for ambassadors', r'(?i)\b(commission|stipend|free (trip|place|spot|travel)|discount|get paid|earn money|rewards?\b)', False),
 ('home','how it works', r'How it works No trek program at your university\? You do not need one\.', True),
 ('home','guide five steps', r'Apply.*Get your kit.*Check the interest.*Open sign-ups.*Travel together', True),
 ('home','where to find group', r'Where to find your group', True),
 ('home','student-led tips', r'Keep it student-led', True),
 ('home','sample note', r'Quick interest check', True),
 ('home','sample announcement', r'sign-ups are open', True),
 ('home','samples not official', r'not an official \[University\] program', True),
 ('home','faq funding', r'Who is funding the travel\? The students themselves', True),
 ('home','faq demand', r'How can I check the demand at my university\?', True),
 ('home','no prices in samples', r'\$\s?\d', False),
 # (page, label, regex, should_exist)
 ('home','plov from workshop', r'[Pp]lov[^.]{0,60}workshop|workshop[^.]{0,60}plov', True),
 ('home','somsa cooking class', r'[Ss]omsa cooking class', True),
 ('home','itinerary informational', r'for information', True),
 ('home','Khiva', r'Khiva', True),
 ('home','Fergana', r'Fergana', True),
 ('home','any month', r'any month', True),
 ('home','not included', r'Not included', True),
 ('home','first deposit', r'[Ff]irst deposit', True),
 ('home','second deposit', r'[Ss]econd deposit', True),
 ('home','remaining balance', r'[Rr]emaining balance', True),
 ('home','founder named on home', r'Jakhongir Sadiev', True),
 ('home','visa link', r'gov\.uz/en/mfa/pages/o-zbekiston-respublikasi-vizasi', 'raw'),
 ('home','all countries', r'all countries|any nationality|every nationality|citizens of all', True),
 ('home','US visa-free', r'US citizens|U\.S\. citizens', True),
 ('home','NY nonstop', r'New York', True),
 ('home','program focus', r'companies, universities and/or culture \(subject to approval\)', True),
 ('home','no formal gov', r'[Ff]ormal government meetings are not part', True),
 ('big','host qualifier', r'\(subject to confirmation and availability\)', True),
 ('big','alumni qualifier', r'[Aa]lumni[^()]{0,80}\(subject to availability\)', True),
 ('big','pick the week', r'Pick the week, usually your school break', True),
 ('big','no spring in pick', r'Pick the week, usually your spring', False),
 ('big','example timeline', r'Example timeline', True),
 ('big','who collects', r'Who collects the money\?', True),
 ('big','pays operator via page', r'Each participant pays the operator directly through our registration page\. Organizers never handle payments', True),
 ('small','fixed dates', r'Fixed dates around school breaks? and after graduation', True),
 ('small','planned dates lede', r'Some planned dates you can already join\. Register your interest, and we confirm the dates and price before taking any deposit\.', True),
 ('small','visa link', r'gov\.uz/en/mfa/pages/o-zbekiston-respublikasi-vizasi', 'raw'),
 ('small','NY nonstop', r'New York', True),
 ('founder','hometown in story', r'my hometown, Samarkand', True),
 ('founder','no hometown lede', r'My hometown is Samarkand', False),
 ('founder','Auburn', r'Auburn University \(AL\)', True),
 ('founder','Sharipov', r'Ministry of Higher Education, Science and Innovation: Minister Kongratbay Sharipov', True),
 ('founder','Umarova', r'Ministry of Preschool and School Education: Minister Khilola Umarova', True),
 ('founder','Zaidi title', r'Dr\. Jon Zaidi, CEO Uzbekistan and Vice President', True),
 ('founder','Kurdiani title', r'Nika Kurdiani, CEO Uzbekistan', True),
 ('founder','Juraev', r'Nordic University: Dr\. Alisher Juraev', True),
 ('founder','quotes title', r'From 2025 and 2026 participants', True),
 ('founder','moments title', r'Moments from the treks', True),
 ('founder','theater caption', r'At the Opera and Ballet Theater named after Alisher Navoi', True),
 ('founder','nowruz concert caption', r'At the Nowruz concert with the President, 2025', True),
 ('founder','bukhara classmates caption', r'With classmates in Bukhara, 2025', True),
 ('founder','chimgan caption', r'In the Chimgan mountains, 2026', True),
 ('founder','football caption', r'At the football game at Milliy Stadium, Tashkent, 2025', True),
 ('home','press title', r'In the news', True),
 ('home','press UzA', r'52 students studying in the US visit Bukhara', True),
 ('home','press note', r'Most coverage is in Uzbek', True),
 ('founder','no press on founder', r'In the news', False),
 ('founder','before harvard order', r'World Bank, United Nations, Auburn University \(AL\)', True),
 ('founder','lede no dot', r'Founder of the Uzbekistan Trek\.', False),
 ('founder','senate caption', r'The first trek at the Senate with Chairwoman Tanzila Narbaeva, 2025', True),
 ('founder','shakhnoza caption', r'With Shakhnoza Mirziyoyeva, National Agency for Social Protection', True),
 ('big','acwa caption', r'Breakfast with the leadership of ACWA(?! Power)', True),
 ('big','tbc caption', r'TBC Bank visit, Tashkent', True),
 ('big','tilla-kari caption', r'In the doorway of\s*Tilla-Kari\s*, Registan', True),
 ('big','trees caption', r'Planting trees for spring at the Bukhara State Medical Institute', True),
 ('founder','guided cite 2026', r'2026 participant, Harvard Kennedy School classmate', True),
 ('founder','no born/raised in Samarkand', r'(born|raised|grew up) in Samarkand', False),
 ('founder','HKS', r'Harvard University \(HKS\)', True),
 ('founder','degree', r"Master's in economics \(MPA/ID\)", True),
 ('founder','World Bank', r'World Bank', True),
 ('founder','United Nations', r'United Nations', True),
 ('founder','Fulbright', r'Fulbright', True),
 ('founder','Muskie', r'Edmund S\. Muskie', True),
 ('founder','Harvard Full Scholarship', r'Harvard [Ff]ull [Ss]cholarship', True),
 ('founder','when I was a child', r'When I was a child, I saw a photo', True),
 ('founder','200 interested', r'200', True),
 ('founder','Nowruz with President', r'celebrated Nowruz together with the President', True),
 ('founder','contributions', r'theses on Uzbekistan', True),
 ('founder','investment', r'investment opportunities', True),
 ('founder','courses', r'launch courses', True),
 ('founder','Narbaeva', r'Tanzila Narbaeva', True),
 ('founder','Mirziyoyeva', r'Shakhnoza Mirziyoyeva', True),
 ('founder','Zaripov', r'Botir Zaripov', True),
 ('founder','Shermatov', r'Sherzod Shermatov', True),
 ('founder','Achilov', r'Nodirbek Achilov', True),
 ('founder','Zaidi', r'Jon Zaidi', True),
 ('founder','Kurdiani', r'Nika Kurdiani', True),
 ('founder','2024 arrives', r'Arrives at Harvard University', True),
 ('founder','laser show', r'laser show at Registan Square', True),
 ('founder','no movie night', r'movie night', False),
 ('founder','classmate quote', r'Name something better than being guided around the beauties of the Silk Road', True),
 ('any','email', r'jsadiev@hks\.harvard\.edu', True),
 ('any','telegram', r't\.me/uzbtrek_bot', 'raw'),
 ('any','no operated by', r'Operated by', False),
 ('any','no TREK 2027', r'TREK\s*2027', False),
]

PAGEFILE = {"home": "index.html", "big": "big-group.html", "small": "small-group.html", "founder": "founder.html"}


def main():
    pages = {f: text_of(os.path.join(SITE_ROOT, f)) for f in PAGEFILE.values()}
    allraw = " ".join(r for r, v in pages.values())
    allvis = " ".join(v for r, v in pages.values())
    fails = 0
    for page, label, rx, want in R:
        raw, vis = (allraw, allvis) if page == "any" else pages[PAGEFILE[page]]
        found = re.search(rx, raw if want == "raw" else vis) is not None
        if found != (want in (True, "raw")):
            fails += 1
            print(f"FAIL {page:8s} {label}")
    raw = pages["founder.html"][0]
    for need in ["founder_portrait", "senate_group", "with_shakhnoza"]:
        if need not in raw:
            fails += 1
            print(f"FAIL founder photo missing: {need}")
    if "zokirjon_khabibullaev" not in pages["index.html"][0]:
        fails += 1
        print("FAIL home page: the co-founder photo is missing")
    if "jakhongir_sadiev.webp" not in pages["index.html"][0]:
        fails += 1
        print("FAIL home page: the founder photo is missing")
    if "samarkand_registan_night" in raw:
        fails += 1
        print("FAIL founder page shows the Registan at night (it belongs to the small group page)")
    v = pages["founder.html"][1]
    i, j = v.find("Narbaeva"), v.find("Jon Zaidi")
    if not 0 <= i < j:
        fails += 1
        print("FAIL founder page: government must come before the private sector")
    print(f"{len(R) + 7} requirement checks, {fails} failed")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
