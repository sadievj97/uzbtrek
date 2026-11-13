"""Shared copy for every Uzbekistan Trek site style.

Every builder (deck, registan, campus, parallax) imports this module so the words stay identical across styles.
Strings are HTML-safe fragments: they may contain entities (&rsquo;, &hellip;) and simple inline tags (<a>, <strong>).
House rules: no em dashes, no prices, no "2027" in side labels, government meetings never promised for new treks,
no pay, discount or free place promised to ambassadors.
"""

SITE = {
    "name": "Uzbekistan Trek",
    "tagline": "Explore the hidden gem in Central Asia",
    "since": "Since 2025",
    "side_label": "UZBEKISTAN TREK",
    "email": "jsadiev@hks.harvard.edu",
    "emails": ["jsadiev@hks.harvard.edu", "zkhabib@bu.edu"],   # both shown in the footer of every page
    "telegram_bot": "uzbtrek_bot",
    "telegram_url": "https://t.me/uzbtrek_bot",
    "visa_url": "https://gov.uz/en/mfa/pages/o-zbekiston-respublikasi-vizasi",
    "description": ("Become an Uzbekistan Trek ambassador: bring your graduate school classmates to Uzbekistan, with our materials "
                    "and support at every step. Built on the 2025 and 2026 Harvard and MIT treks."),
}

# Header links. On the home page the "index.html" part is dropped, so the links scroll instead of reloading the page.
NAV = [
    ("index.html#how", "How it works", "how"),
    ("index.html#team", "Who we are", "team"),
    ("index.html#groups", "Group trips", "groups"),
    ("index.html#faq", "FAQ", "faq"),
    ("contact.html", "Contact", "contact"),
]
NAV_CTA = ("index.html#apply", "Apply now")

DISCLAIMER = ("Uzbekistan Trek is independent. It is not affiliated with, sponsored or endorsed by Harvard University, "
              "the Massachusetts Institute of Technology or any other university. University names describe where past participants study.")
FOOTER_BLURB = "The ambassador program and group trips to Uzbekistan for graduate students. Trips are land-only; international flights are not included."
COPYRIGHT = "&copy; 2026 Uzbekistan Trek. Photos from the 2025 and 2026 treks."

# ---------------------------------------------------------------- home: the ambassador program
HERO = {
    "kicker": "Ambassador program",
    "title": "Become an Uzbekistan Trek Ambassador",
    # the owner chose this: these words show as white letters with a navy outline and shadow
    "title_sticker": "Uzbekistan Trek",
    "lede": ("Bring Uzbekistan to your campus. You coordinate your students. We give you the materials, the promotion techniques "
             "and support at every step, and you travel to Uzbekistan with your group."),
    "cta_primary": ("#apply", "Apply now"),
    "cta_secondary": ("#how", "How it works"),
    # the owner's choice from the Harvard 2027 PowerPoint (Nov 2026): two photos from its "From the previous treks" slide and
    # the first trek at the Senate. Captions and years come from photos.json. Each photo appears once per site.
    "photos": ["y2025_circle", "y2025_bukhara_arch", "y2025_senate"],
}

TEAM = {
    "title": "Who we are",
    "lede": ("We are Jakhongir and Zokirjon, two Uzbek graduate students in Boston who love showing our country "
             "to classmates from around the world."),
    # photo None shows the initials. Jakhongir's avatar is a different photo from founder_portrait, which is on the founder page:
    # each photo appears once per site.
    "members": [
        {"role": "Co-Founder", "name": "Jakhongir Sadiev", "initials": "JS", "photo": "jakhongir_sadiev",
         "text": "Harvard Kennedy School. Started the trek at Harvard in 2025: two treks, 95 travelers.",
         "link": ("founder.html", "Read his story")},
        {"role": "Co-Founder", "name": "Zokirjon Khabibullaev", "initials": "ZK", "photo": "zokirjon_khabibullaev",
         "text": "Boston University. Coordinates the ambassador program and the trek&rsquo;s growth to new universities.",
         "link": None},
    ],
}

# Never promise ambassadors pay, a discount or a free place: many of them study on student visas.
GETS = {
    "title": "What you get",
    "lede": "Everything we learned from two treks, ready for your university.",
    "items": [
        ("slides", "Ready-made materials", "Info-session slides, a flyer, sample texts and a registration page for your group."),
        ("megaphone", "Promotion techniques",
         "How we brought 95 travelers on two treks: where to share the trip, how to run an info session and how to turn interest into sign-ups."),
        ("chat", "Support at every step",
         "We plan the trip with you, answer your classmates&rsquo; questions and prepare a quote and a day-by-day plan for your dates."),
        ("plane", "Travel with your group", "You travel to Uzbekistan with your classmates. We plan and run everything on the ground."),
    ],
}

APPLY = {
    "title": "Apply to become an ambassador",
    "lede": "Tell us about yourself and the classmates you want to bring. We get back to you by email or Telegram.",
    "who_title": "Who can apply",
    "who": ["Uzbek graduate students, fellows and postdocs at universities outside Uzbekistan",
            "No experience organizing trips needed",
            "Your classmates can be from any country"],
}

# ---------------------------------------------------------------- the two choices (home page "Group trips" band)
GROUPS = {
    "title": "Already have a group?",
    "lede": "Clubs, cohorts and friends can also travel with us directly. Pick your group size.",
}
CHOICES = {
    "big": {
        "href": "big-group.html", "count": "10+", "unit": "travelers", "title": "Big group trek",
        "desc": "For a class, club or program. Choose your dates; we plan the whole trip as a full package.",
        "short": "Full package on your dates.", "cta": "Plan a big group trek",
    },
    "small": {
        "href": "small-group.html", "count": "1&ndash;9", "unit": "travelers", "title": "Small group trip",
        "desc": "Solo, as a couple or with a few friends. Join a planned departure or travel privately.",
        "short": "Join a departure or go private.", "cta": "See small group options",
    },
}

# ---------------------------------------------------------------- testimonials
QUOTES = {
    "best": {"text": "After eight treks, Uzbekistan was the best one. By far!", "cite": "2025 participant"},
    "guided": {"text": "Name something better than being guided around the beauties of the Silk Road by HKS classmates that truly love their country.",
               "cite": "2026 participant, Harvard Kennedy School classmate"},
    "dancing": {"text": "Dancing at almost every meal, private access to Registan&rsquo;s light show&hellip; Truly one of the most special weeks of my Harvard experience.",
                "cite": "2025 participant"},
    "long": {"text": ("After 8 treks, I can safely say that Uzbekistan was the best trek ever&hellip; HKS offers plenty of incredible treks and I have been on many of them, "
                      "yet this one still holds a special place in my heart. If you are looking for a great blend of culture, policy engagements and fun, this trek is for you. "
                      "You will get delicious food, an unforgettable welcome ceremony and meaningful exchanges&hellip; You will also enjoy a laser show at Registan Square."),
             "cite": "2025 participant, Harvard Kennedy School"},
}

# ---------------------------------------------------------------- home
PREVIOUS = {
    "title": "From the previous treks",
    "bullets": [
        "In March 2025, 45 graduate students from Harvard and MIT traveled with us to Tashkent, Bukhara and Samarkand.",
        "In March 2026, the second trek grew to 50 travelers.",
        "Now Uzbek students at other universities can bring their own classmates, as Uzbekistan Trek ambassadors.",
    ],
    "script": "What are the participants saying?",
}

STATS = [
    ("40", "sign-ups on the first day we announced the trek"),
    ("200", "people interested in joining the first treks"),
    ("45", "graduate students on the March 2025 trek"),
    ("50", "graduate students on the March 2026 trek"),
]

ITINERARY = {
    "title": "Sample itinerary",
    "intro": ("This is how our Harvard and MIT treks ran, shown for information. It is a starting point, not a fixed package: "
              "we can make it longer, add cities such as Khiva or the Fergana Valley, and shape every day around your group. "
              "Past treks ran over spring break, but a trek can run in any month."),
    "days": [
        {"n": 1, "where": "Arrival in <strong>Tashkent</strong>", "items": ["Check-in and rest", "Tashkent city walk"]},
        {"n": 2, "where": "Fast train to <strong>Bukhara</strong>", "items": ["Lyab-i Hauz", "Old City", "Kalyan Minaret"]},
        {"n": 3, "where": "In <strong>Bukhara</strong>", "items": ["Ark Fortress", "Sitorai Mohi Hosa Palace", "Mausoleum of Ismail Samani"]},
        {"n": 4, "where": "Fast train to <strong>Samarkand</strong>", "items": ["Registan and Shah-i-Zinda", "Bibi-Khanym Mosque", "Laser show at the Registan"]},
        {"n": 5, "where": "<strong>Samarkand</strong> to <strong>Tashkent</strong>", "items": ["Gur-e-Amir", "Ulugbek Observatory"]},
        {"n": 6, "where": "In <strong>Tashkent</strong>", "items": ["Company and university visits", "Chorsu Bazaar"]},
        {"n": 7, "where": "By bus to the <strong>Tashkent mountains</strong>", "items": ["Lake Charvak", "Amirsoy cable car"]},
        {"n": 8, "where": "Departures from <strong>Tashkent</strong>", "items": ["Tashkent International Airport"]},
    ],
    "tailor_title": "Make it yours",
    "tailor": [
        "Any month, not only during the school break",
        "Longer or shorter than eight days",
        "Add Khiva, the Fergana Valley or a desert yurt camp",
        "Visits shaped around your field of study",
    ],
    "footnote": "Sample itinerary from the Harvard and MIT treks, for information only. Every trek is tailored: dates, length, cities and visits are agreed with your group.",
}

INCLUDED = [
    "Accommodation with breakfast",
    "Meals (lunches and dinners)",
    "City tours in Tashkent, Samarkand and Bukhara",
    "Cultural experiences with guides, such as Nowruz in March",
    "Transportation (fast trains and transfers)",
    "Local guide, museum entrance fees and a SIM card",
]
NOT_INCLUDED = [
    "International flights",
    "Travel medical and evacuation insurance",
    "Visa fees, if your passport needs a visa",
    "Alcohol and personal expenses",
    "Anything not listed as included",
]

PAYMENT = {
    "title": "Dates and payment",
    "lede": ("Most groups travel during a school break, but a trek can run in any month. "
             "Every trek is quoted for its group, dates and length, so we do not publish a single price."),
    "tranches_title": "Payment in three installments",
    "tranches": [
        ("First deposit", "a fixed amount to hold your place"),
        ("Second deposit", "a fixed amount, closer to the trip"),
        ("Remaining balance", "paid before departure"),
    ],
    "note": "Your quote lists the exact amounts and due dates.",
}

# ---------------------------------------------------------------- how it works (home page guide for ambassadors)
START = {
    "title": "How it works",
    "lede": ("No trek program at your university? You do not need one. Every trek starts with one student, "
             "a few interested classmates and our support."),
    "steps": [
        ("Apply",
         "Tell us about yourself, your university and the classmates you want to bring. It takes a few minutes.",
         ("#apply", "Apply now")),
        ("Get your kit",
         "We talk through your plan and share the organizer kit: info-session slides, a flyer and sample texts.",
         None),
        ("Check the interest",
         "Share a short note and a one-minute form in your class group chat. Aim for 10 or more classmates who say yes; fewer can still travel as a small group.",
         ("#sample-note", "Use the sample note")),
        ("Open sign-ups",
         "We send a quote and a day-by-day plan for your dates. Hold a short info session and share the registration link. Everyone registers and pays through our page.",
         ("#sample-announcement", "Use the sample announcement")),
        ("Travel together",
         "You travel to Uzbekistan with your group. We plan and run everything on the ground and host you there.",
         ("#itinerary", "See the sample itinerary")),
    ],
    "where_title": "Where to find your group",
    "where": ["Your class or cohort group chat", "Student clubs: regional, international affairs, policy, business",
              "Your program&rsquo;s student newsletter", "The graduate student council", "Professors who teach the region",
              "Friends in other programs"],
    "tips_title": "Keep it student-led",
    "tips": ["Write as a classmate: say why you want to go and who you hope will come.",
             "Team up with one or two classmates, and ask a student club to share the trip with its members. Clubs have the mailing lists you may not have.",
             "Be open about how it works: Uzbekistan Trek plans the trip and handles registration and payments; you bring the group together.",
             "Do not use your university&rsquo;s name or logo as if the trip were an official program."],
    "samples_title": "Sample texts you can copy",
}

# Plain text (not HTML): shown with line breaks. Words in [brackets] are for the organizer to fill in.
# **bold**, __italic__ and !!bold red!! follow the owner's originals (Nov 2026). Copy keeps them: the email copies as formatted text for
# Gmail or Outlook, the WhatsApp message ("copy_as": "whatsapp") as WhatsApp's own *bold* and _italic_ marks.
SAMPLES = [
    {"id": "sample-note", "step": "Step 3", "title": "Sample note to check interest", "when": "Send it before you ask for a quote.",
     "text": ("Subject: Uzbekistan over spring break? Quick interest check\n\n"
              "Hi everyone,\n\n"
              "I am thinking of organizing a trip to Uzbekistan for graduate students at [University], around [spring break or other dates]. "
              "Graduate students from Harvard and MIT went in 2025 and 2026: about a week in Tashkent, Samarkand and Bukhara, "
              "with Silk Road cities, great food and a day in the mountains.\n\n"
              "Uzbekistan Trek would plan and run the trip, and everyone would pay for their own place. I am only bringing the group together.\n\n"
              "If you might want to come, please fill out this one-minute form by [date]: [form link]. It is not a commitment. "
              "If 10 or more of us are interested, I will share the dates, the program and the price per person.\n\n"
              "More about the trek: [website link]\n\n"
              "[Your name]")},
    # The two Harvard samples are the owner's own texts (November 2026), kept close to the original. Changes, for the content rules:
    # prices and deposits are [placeholders]; no promise of government officials, policymakers or exclusive meetings;
    # "graduate students, fellows and postdocs", never just "students"; the WhatsApp heading said 2026 for the 3rd edition, which is
    # March 2027; the balance was due "February 27, 2025", now 2027; "the FAQs below" points to the site FAQ instead; the email ends
    # with the not-official line. The owner asked to keep "Uzbekistan Trek 2027".
    {"id": "sample-announcement", "step": "Step 4", "title": "Sample announcement from Harvard (email)",
     "when": "Send it once you have your quote. Swap the Harvard details and the words in [brackets] for your own.",
     "text": ("Dear friends!\n\n"
              "After the tremendous success of our March 2025 and 2026 treks with 95 Harvard and MIT graduate students, "
              "we are excited to announce the **Uzbekistan Trek 2027!** This is the right opportunity to explore the heart of Central Asia! "
              "Want to join? Follow the instructions below.\n\n"
              "📅 **When?**\n"
              "• March 14-21, 2027 (Spring Break)\n"
              "• Arrive in Tashkent by March 14, and departures begin any time on March 21.\n\n"
              "📍 **Where?**\n"
              "• Tashkent, Tashkent region (mountains), Samarkand, Bukhara\n\n"
              "💰 **How much?**\n"
              "• [price] per person for double occupancy\n"
              "• [price] per person for single occupancy\n\n"
              "📦 **What's included?**\n"
              "• The cost covers nearly everything: hotel accommodations, guide, city tours, local transportation, and in-country transfers "
              "(bullet train tickets), all meals, SIM card, museum and cultural site admissions.\n"
              "__Note: Personal expenses, visa fees (if any), alcohol, and international airfare are not included.__\n\n"
              "🟢 **How to join?**\n"
              "• Submit the form here: [form link] (the form is open until !!December 1!!, 2026, EOD. If you have already submitted the form, "
              "there is no need to submit it again).\n"
              "• Make the first deposit of **[amount]** by **December 20, 2026**, to confirm your spot. The second deposit of [amount] is due by "
              "January 20, 2027, and the remaining balance must be paid by February 27, 2027. Payment details will be sent to the email "
              "address provided in your application form.\n\n"
              "👥 **Who Can Join?**\n"
              "• All current Harvard and MIT graduate students, fellows, and postdocs\n\n"
              "🎉 **Program Highlights**\n"
              "• Visit iconic Silk Road cities, see the stunning bazaars, visit the oldest carpet and paper-making workshop, "
              "and attend the Nowruz celebration.\n"
              "• Meet local entrepreneurs and visit companies and universities.\n"
              "• Experience authentic Uzbek cuisine, music, shows, and hospitality.\n\n"
              "If you have any questions, refer to the **FAQ** at https://uzbekistantrek.com/#faq, or feel free to reach out to us! We are here to help!\n\n"
              "We look forward to exploring Uzbekistan with you!\n\n"
              "This trip is organized by students. It is not an official Harvard or MIT program.\n\n"
              "Best regards,\n"
              "**Uzbekistan Trek 2027 Team**")},
    {"id": "sample-whatsapp", "step": "Step 4", "title": "Sample WhatsApp message from Harvard",
     "when": "Post it in your class group chats when sign-ups open. Swap the Harvard details for your own.",
     "copy_as": "whatsapp",
     "text": ("🌟 **UZBEKISTAN TREK 2027** (3rd edition) 🌟\n\n"
              "Hi everyone!\n"
              "🇺🇿 After the tremendous success of our March 2025 and 2026 treks with 95 Harvard and MIT graduate students, "
              "we are excited to bring the Uzbekistan Trek experience back for a new cohort. "
              "An incredible opportunity awaits in the heart of the Silk Road!\n\n"
              "Previous years' participants described the trek as “the best ever,” “a week packed with unforgettable moments,” "
              "and “one of the most inspiring journeys at Harvard.”\n\n"
              "**Get ready to**:\n"
              "• Explore magnificent sites in Samarkand, Tashkent and Bukhara\n"
              "• Experience authentic Nowruz celebrations\n"
              "• Meet entrepreneurs and investors\n"
              "• Visit cutting-edge tech hubs\n\n"
              "🏛 **Highlights:**\n"
              "• Ancient bazaars & the legendary Registan\n"
              "• Traditional crafts: carpet weaving & paper making\n"
              "• Crystal-clear mountain lakes\n\n"
              "**Who can join?** Current Harvard & MIT graduate students, fellows and postdocs\n\n"
              "🗓 The dates: March 14-21, 2027\n"
              "🌆 Cities: Tashkent, Tashkent region, Samarkand & Bukhara\n"
              "❗️ Application Deadline: December 1, 2026\n"
              "Limited spots available.\n\n"
              "Registration form: [form link]")},
    # the owner's Harvard brochure as the fourth block: prices show as [$X], the organizers' emails and the form link are removed
    {"id": "sample-brochure", "step": "Step 4", "title": "Harvard info brochure (PDF)",
     "when": "Sample info brochure used for the Harvard trek 2027",
     "file": ("files/uzbekistan_trek_2027_harvard_info.pdf", "Open the brochure", "Download the PDF (17 pages, 3 MB)")},
]

# Home FAQ in two groups: (group title, [(question, [paragraphs])])
FAQ_HOME = [
  ("For ambassadors", [
    ("Who can become an ambassador?",
     ["Uzbek graduate students, fellows and postdocs at universities outside Uzbekistan. You do not need experience organizing trips: "
      "we give you the materials and support at every step."]),
    ("What does an ambassador do?",
     ["You bring your classmates together: you share the trip, hold an info session and keep your group informed. "
      "We plan the trip, run registration and payments, and host your group in Uzbekistan."]),
    ("Who is funding the travel?",
     ["The students themselves. Each traveler pays for their own place on the trek, through our registration page, and books their own international flights."]),
    ("My university has no trek program. Can I still start one?",
     ["Yes. You do not need one. Every trek starts with one student and a few interested classmates. See <a href=\"#how\">how it works</a>."]),
    ("How can I check the demand at my university?",
     ["Send a short note with a one-minute form to your classmates. You do not need a mailing list: a class group chat or a student club is enough.",
      "<a href=\"#sample-note\">Use our sample note</a>, and see <a href=\"#how\">how it works</a> for the next steps."]),
    ("I am not Uzbek. Can I bring my classmates?",
     ["Yes. Plan a <a href=\"big-group.html\">big group trek</a> for 10 or more travelers, or a <a href=\"small-group.html\">small group trip</a> for fewer than 10."]),
  ]),
  ("For travelers", [
    ("Who can join?",
     ["Graduate students, fellows and postdocs. The trek is open to citizens of all countries. Partners can join when space allows. We do not run trips for undergraduates."]),
    ("Do I need a visa?",
     ["The trek is open to citizens of all countries. US citizens can enter Uzbekistan without a visa for up to 30 days (since January 1, 2026).",
      "For other passports, check the official visa page: <a href=\"https://gov.uz/en/mfa/pages/o-zbekiston-respublikasi-vizasi\" target=\"_blank\" rel=\"noopener\">Visa to the Republic of Uzbekistan</a>."]),
    ("Is Uzbekistan safe?",
     ["The US State Department rates Uzbekistan Level 1, its lowest advisory level, with the advice to exercise normal precautions (advisory issued January 26, 2026). Every group gets a safety briefing before departure."]),
    ("Are international flights included?",
     ["No. Trips are land-only, so you book your own flights.",
      "Uzbekistan Airways flies nonstop between New York (JFK) and Tashkent a few times a week, in about 13 hours. You can also connect through hubs such as Istanbul or Dubai."]),
    ("What is not included in the cost?",
     ["International flights, travel medical and evacuation insurance, visa fees if your passport needs a visa, alcohol and personal expenses, and anything not listed as included."]),
    ("How does payment work?",
     ["In three installments: a fixed first deposit, a fixed second deposit, and the remaining balance before departure. Your quote lists the exact amounts and due dates."]),
    ("Can a trek run outside spring break?",
     ["Yes. Most groups travel during a school break, but we can run a trek in any month and for any length."]),
    ("Will we meet government officials?",
     ["The standard program focuses on companies, universities and/or culture (subject to approval). Formal government meetings are not part of it."]),
    ("Is there a refund if I withdraw?",
     ["You can transfer your place to another graduate student with our approval. Refund terms are set out in the booking terms you accept when you pay. We strongly recommend trip cancellation insurance."]),
    ("Is this run by my university?",
     ["No. Groups organize themselves, and Uzbekistan Trek is not affiliated with any university. Please do not present the trip as an official university program."]),
  ]),
]

# ---------------------------------------------------------------- big group page
BIG = {
    "kicker": "10 or more travelers",
    "title": "Big group trek",
    "lede": "For a class, a club, a caucus or a whole program. You bring the group and choose the dates. We plan and run everything on the ground as one full package.",
    "cta_primary": ("#quote", "Request a group quote"),
    "cta_secondary": ("index.html#itinerary", "See the sample itinerary"),
    "for_title": "Who it is for",
    "for": [
        ("Student clubs and caucuses", "Regional, policy, energy, finance or business clubs that want a week of real exposure to Central Asia."),
        ("A cohort or class", "A program year traveling together during a school break, like our Harvard and MIT groups in 2025 and 2026."),
        ("Friends across programs", "Ten or more graduate students from different programs or schools who want their own private trip."),
    ],
    "gets_title": "What your group gets",
    "gets": [
        "A private itinerary on your dates",
        "Hotels, meals, fast trains, transfers and licensed guides",
        "Company, university and cultural visits matched to your field (subject to approval)",
        "An Uzbek graduate student host with your group all week (subject to confirmation and availability)",
        "A dinner with your school&rsquo;s alumni in Uzbekistan, where we can arrange one (subject to availability)",
        "An organizer kit: info-session slides, a flyer and a registration page",
    ],
    "split_title": "Who does what",
    "you": ["Gather at least 10 participants", "Pick the week, usually your school break", "Share the registration link with your group", "Tell us what your group cares about"],
    "we": ["Build the itinerary and the quote", "Run registration and payments", "Book hotels, trains, guides and visits", "Brief everyone before departure", "Host your group in Uzbekistan"],
    "timeline_title": "Example timeline for a March trek",
    "timeline_note": "Traveling in another month? We shift the same steps to fit your dates.",
    "timeline": [
        ("Oct to Nov", "Request a quote"),
        ("November", "Info session; registration opens"),
        ("Late Dec", "First deposit"),
        ("Late Jan", "Second deposit"),
        ("Late Feb", "Remaining balance and rooming list"),
        ("Early Mar", "Pre-departure briefing"),
        ("School break", "Travel"),
    ],
    "form_title": "Request a group quote",
    "form_lede": "Tell us about your group. We reply with a quote and a day-by-day plan, usually within three working days.",
    "faq_title": "Big group questions",
    "faq": [
        ("What if fewer than 10 people sign up?", ["We can still run your trip as a private small-group trip, or your travelers can join one of our planned departures."]),
        ("Can we travel outside spring break?", ["Yes. Most groups travel during a school break, but we can run your trek in any month."]),
        ("Can our group meet government officials?", ["The standard program focuses on companies, universities and/or culture (subject to approval). Formal government meetings are not part of it."]),
        ("Can we change the route?", ["Yes. Add days, add Khiva or the Fergana Valley, or spend a night at a desert yurt camp. Your quote changes accordingly."]),
        ("Who collects the money?", ["Each participant pays the operator directly through our registration page. Organizers never handle payments."]),
        ("Is the trip affiliated with our university?", ["No. Your group organizes itself and travels independently. Please do not present the trip as an official university program."]),
    ],
}

# ---------------------------------------------------------------- small group page
SMALL = {
    "kicker": "Fewer than 10 travelers",
    "title": "Small group trip",
    "lede": "Traveling solo, as a couple or with a few friends? Join a planned departure with graduate students from other universities, or take a private trip on your own dates.",
    "cta_primary": ("#departures", "See planned dates"),
    "cta_secondary": ("#interest", "Ask about a private trip"),
    "ways_title": "Two ways to go",
    "join": {
        "tag": "Planned dates", "title": "Join a departure",
        "items": ["Fixed dates around school breaks and after graduation", "Travel with graduate students from other universities",
                  "The same route and hosts as our big group treks", "Share a double room with another participant, or book a single"],
        "cta": ("#departures", "See planned dates"),
    },
    "private": {
        "tag": "Your own dates", "title": "Private small-group trip",
        "items": ["Two to nine travelers, on the dates you choose", "A private car with a driver and an English-speaking guide",
                  "Your pace and your interests", "Price per person depends on how many of you travel"],
        "cta": ("#interest", "Ask for a private quote"),
    },
    "dep_title": "Planned departures",
    "dep_lede": "Some planned dates you can already join. Register your interest, and we confirm the dates and price before taking any deposit.",
    "departures": [
        {"name": "Spring break", "len": "8 days", "dates": "March 13 to 20, 2027", "why": "Fits the most common mid-March spring breaks", "status": "Planned", "pick": "Spring break, March 13 to 20, 2027"},
        {"name": "Nowruz", "len": "8 days", "dates": "March 20 to 27, 2027", "why": "In Uzbekistan for Nowruz on March 21", "status": "Planned", "pick": "Nowruz, March 20 to 27, 2027"},
        {"name": "After graduation", "len": "8 days", "dates": "Late May to June 2027", "why": "Warm weather, before the July heat", "status": "Dates to come", "pick": "After graduation, May to June 2027"},
    ],
    "cmp_title": "Which option fits you?",
    "cmp_head": ["", "Join a departure", "Private small-group trip", "Big group trek"],
    "cmp_rows": [
        ("Group size", "1 to 9 of you, in a larger mixed group", "2 to 9, just your group", "10 or more, just your group"),
        ("Dates", "Planned", "Your choice", "Your choice"),
        ("Price per person", "Lowest", "Higher, shared by fewer people", "Depends on group size"),
        ("Planning on your side", "None", "Pick dates and interests", "Gather the group"),
        ("Best for", "Solo travelers and pairs", "Couples and small friend groups", "Clubs, cohorts and programs"),
    ],
    "cmp_note": "Ten or more of you? <a href=\"big-group.html\">See big group treks</a>.",
    "form_title": "Register your interest",
    "form_lede": "No payment now. We confirm dates and price first, usually within three working days.",
    "faq_title": "Small group questions",
    "faq": [
        ("Can I come alone?", ["Yes. Many people join a departure on their own. We pair you with another participant for a shared room, or you can book a single."]),
        ("Who will I travel with?", ["Graduate students, fellows and postdocs from different universities and countries, with licensed local guides and an Uzbek host (subject to availability)."]),
        ("Can my partner come?", ["Yes, when space allows."]),
        ("Why does a private trip cost more per person?", ["The car, driver and guide are shared by fewer people. The more of you travel, the lower the price per person."]),
        ("Do I need a visa?", ["The trek is open to citizens of all countries. US citizens can enter Uzbekistan without a visa for up to 30 days (since January 1, 2026).",
                               "For other passports, check the official visa page: <a href=\"https://gov.uz/en/mfa/pages/o-zbekiston-respublikasi-vizasi\" target=\"_blank\" rel=\"noopener\">Visa to the Republic of Uzbekistan</a>."]),
        ("Are international flights included?", ["No. You book your own flights. Uzbekistan Airways flies nonstop between New York (JFK) and Tashkent a few times a week, in about 13 hours. You can also connect through hubs such as Istanbul or Dubai."]),
    ],
}

# ---------------------------------------------------------------- founder page
FOUNDER = {
    "kicker": "About the co-founder",
    "name": "Jakhongir Sadiev",
    "lede": "Co-Founder of the Uzbekistan Trek",
    "facts": [
        ("Harvard University (HKS)", "Master&rsquo;s in economics (MPA/ID)"),
        ("Two treks organized", "2025 and 2026, 95 travelers"),
        ("Before Harvard", "World Bank, United Nations, Auburn University (AL)"),
        ("Fellowships", "Fulbright, Edmund S. Muskie, Harvard Full Scholarship"),
    ],
    "story": [
        ("A photo I never forgot",
         ["When I was a child, I saw a photo of a student traveling through his home country with his university classmates. "
          "That image stayed with me. One day, I told myself, I would bring my own classmates to my hometown, Samarkand."]),
        ("The first Uzbek in my program in 25 years",
         ["When I came to Harvard, I was the first Uzbek in my program at the Harvard Kennedy School in 25 years, and I felt I needed to do something with that. "
          "At the American universities where I studied, Uzbekistan and Central Asia rarely came up. I wanted to change that, so I decided to bring my Harvard and MIT classmates to Uzbekistan."]),
        ("Forty sign-ups on the first day",
         ["Honestly, I was not sure 20 people would join. On the first day we announced the trek, 40 had already signed up. "
          "Eventually, we had around 200 interested participants for the first treks, so we had to make a selection."]),
        ("March 2025: 45 travelers",
         ["The first trek was a huge success. Forty-five graduate students traveled with us. We met ministers, the Governor of Bukhara and the leadership of the Senate, "
          "exchanged ideas with students at Nordic University, and celebrated Nowruz together with the President. "
          "The feedback from participants, from the university community and from our hosts in Uzbekistan was so strong that we decided to do it again.",
          "Moreover, the trek contributed further: some students did their research and theses on Uzbekistan, some looked for investment opportunities, "
          "and some joined efforts with local universities to launch courses."]),
        ("March 2026: 50 travelers",
         ["The second trek was bigger, with 50 travelers, and it covered more policy areas. On the government side, we met the Chairwoman of the Senate, "
          "the leadership of the National Agency for Social Protection, the Governor of Bukhara, the Minister of Digital Technologies "
          "and the Deputy Chairman of the Central Bank.",
          "In the private sector, we discussed renewable energy with the leadership of ACWA Power, financial markets with TBC Bank, "
          "and technology at IT Park."]),
        ("What comes next",
         ["My goal is to run more treks and open them to graduate students at other universities. That is why we started the ambassador program: "
          "Uzbek students studying abroad can now bring their own classmates, and we support them at every step. "
          "After two treks, we know what students want from a week in Uzbekistan, and we can help you organize one for your group."]),
    ],
    "signature": "Jakhongir Sadiev",
    "timeline_title": "How it grew",
    "timeline": [
        ("Childhood", "", "A photo plants the idea"),
        ("2024", "", "Arrives at Harvard University"),
        ("Day one", "40", "sign-ups when the trek is announced"),
        ("March 2025", "45", "travelers on the first trek"),
        ("March 2026", "50", "travelers on the second trek"),
        ("Next", "", "More treks, more universities"),
    ],
    "quotes_title": "From 2025 and 2026 participants",
    "quotes": ["long", "guided"],
    "areas_title": "Who the Harvard and MIT treks met",
    "areas": {
        "Government": [
            "Senate: Chairwoman Tanzila Narbaeva",
            "National Agency for Social Protection: Shakhnoza Mirziyoyeva",
            "Bukhara region: Governor Botir Zaripov",
            "Ministry of Digital Technologies: Minister Sherzod Shermatov",
            "Ministry of Higher Education, Science and Innovation: Minister Kongratbay Sharipov",
            "Ministry of Preschool and School Education: Minister Khilola Umarova",
            "Central Bank: Deputy Chairman Dr. Nodirbek Achilov",
        ],
        "Private sector and universities": [
            "ACWA Power: Dr. Jon Zaidi, CEO Uzbekistan and Vice President",
            "TBC Bank: Nika Kurdiani, CEO Uzbekistan",
            "IT Park",
            "New Uzbekistan University",
            "Nordic University: Dr. Alisher Juraev",
        ],
    },
    "areas_note": ("Treks for other universities focus on companies, universities and/or culture (subject to approval). "
                   "Formal government meetings are not part of the standard program."),
    "cta_title": "Bring Uzbekistan to your campus",
    "cta_lede": "Become an ambassador and travel to Uzbekistan with your classmates.",
    "cta_groups": ("Already have a group? See <a href=\"big-group.html\">big group treks</a> "
                   "and <a href=\"small-group.html\">small group trips</a>."),
    "moments_title": "Moments from the treks",
    # (photo key, aspect ratio); the captions carry the year
    "moments": [("navoi_theater", "4/3"), ("y2025_nowruz_concert", "4/3"), ("y2025_bukhara_classmates", "3/4"),
                ("y2026_chimgan", "4/3"), ("y2025_football", "4/3")],
}

# ---------------------------------------------------------------- press (home page)
# Each item: (kind, source, one line on what it covers, action word, link). Lines summarize the posts
# (headlines translated from Uzbek where known). Kinds: tv, article, telegram, instagram, video, news.
PRESS = {
    "title": "In the news",
    "lede": "Uzbek TV, the national news agency, the Senate, ministries and universities covered both treks.",
    "note": "Most coverage is in Uzbek.",
    "ticker": ["Uzbekistan 24", "MY5", "UzA", "Senate of Uzbekistan", "Ministry of Higher Education, Science and Innovation",
               "National Agency for Social Protection", "New Uzbekistan University", "Nordic University", "Bright Uzbekistan"],
    "years": [
        ("2025", "March 2025, 45 travelers", [
            ("tv", "Uzbekistan 24", "Harvard University students in Uzbekistan", "Watch", "https://t.me/uzmtrk_official/5341"),
            ("tv", "Uzbekistan 24", "The students visit New Uzbekistan University", "Watch", "https://t.me/uzmtrk_official/5365"),
            ("tv", "MY5", "Harvard University students in Uzbekistan", "Watch", "https://t.me/hududtv/32780"),
            ("article", "Nordic University", "The visit to Uzbekistan begins", "Read",
             "https://nordicuniversity.org/uz/press-service/news/garvard-universiteti-delegatsiyasining-ozbekistonga-tashrifi-qizgin-boshlandi"),
            ("telegram", "Senate", "A meeting with Harvard and MIT students on joint education projects", "View", "https://t.me/senatuz/33351"),
            ("telegram", "Senate", "The Chairwoman of the Senate meets the students", "View", "https://t.me/senatuz/33360"),
            ("telegram", "New Uzbekistan University", "43 Harvard Kennedy School and MIT students on campus", "View", "https://t.me/newuzbekistanuniversity/3497"),
            ("telegram", "Nordic University", "Celebrating Nowruz with the Uzbekistan Trek 2025", "View", "https://t.me/nordic_edu/5562"),
            ("video", "Nordic University", "Video of the visit", "Watch", "https://youtu.be/FuITHJNq-3c"),
        ]),
        ("2026", "March 2026, 50 travelers", [
            ("news", "UzA", "52 students studying in the US visit Bukhara", "Read", "https://uza.uz/uz/posts/aqshda-tahsil-olayotgan-52-nafar-talaba-buxoroda_833625"),
            ("telegram", "Tanzila Narbaeva", "The Chairwoman of the Senate meets the students", "View", "https://t.me/tanzilanarbaeva/6816"),
            ("telegram", "Ministry of Higher Education, Science and Innovation", "Telegram post", "View", "https://t.me/eduuz/43656?single"),
            ("telegram", "National Agency for Social Protection", "Telegram post", "View", "https://t.me/ijtimoiyhimoya_agentligi/7623?single"),
            ("instagram", "Shakhnoza Mirziyoyeva", "Instagram reel", "Watch", "https://www.instagram.com/reel/DV_Y0zKsTp1/"),
            ("instagram", "Senate", "Instagram reel", "Watch", "https://www.instagram.com/reel/DV-zNqYDfgu/"),
            ("instagram", "Bright Uzbekistan", "Instagram post", "View", "https://www.instagram.com/p/DV_LRhZinHA/"),
            ("instagram", "Mari Wellness Restaurant", "Instagram reel", "Watch", "https://www.instagram.com/reel/DWBC_QsDKh-/"),
        ]),
    ],
}

# ---------------------------------------------------------------- forms
FORM_COMMON = {
    "privacy": "We use your details only to answer this request.",
    "privacy_apply": "We use your details only to review your application and get back to you.",
    "telegram_hint": "Prefer chatting? Message us on Telegram at <a href=\"https://t.me/uzbtrek_bot\" target=\"_blank\" rel=\"noopener\">@uzbtrek_bot</a>.",
}
INTERESTS = ["Business and finance", "Public policy", "Technology", "Energy and climate", "Culture and food", "Mountains and outdoors"]

# ---------------------------------------------------------------- contact page (contact.html)
# Names, roles and schools as in TEAM. No photos here: each photo appears once per site, and both portraits are on the home page.
CONTACT = {
    "kicker": "Contact",
    "title": "Contact us",
    "lede": "Questions about the ambassador program or a group trip? Write to either of us, or message us on Telegram.",
    "people": [
        {"role": "Co-Founder", "name": "Jakhongir Sadiev", "initials": "JS", "school": "Harvard Kennedy School", "email": "jsadiev@hks.harvard.edu"},
        {"role": "Co-Founder", "name": "Zokirjon Khabibullaev", "initials": "ZK", "school": "Boston University", "email": "zkhabib@bu.edu"},
    ],
    "telegram_role": "Telegram",
    "telegram_title": "@uzbtrek_bot",
    "telegram_text": "Prefer chatting? Send us a message on Telegram.",
    "telegram_cta": "Message us on Telegram",
    "next_title": "Looking for something else?",
    "next": [("index.html#apply", "Become an ambassador"), ("big-group.html", "Plan a big group trek, 10 or more"),
             ("small-group.html", "Plan a small group trip, under 10"), ("index.html#faq", "Read the FAQ")],
}

# ---------------------------------------------------------------- interface words (used by shared/build.py and shared/forms_html.py)
# shared/content_uz.py gives the same names in Uzbek, for the pages in uz/.
LANG = "en"
UI = {
    "logo_label": "Uzbekistan Trek, home",
    "menu": "Menu",
    "nav_label": "Main",
    "footer_label": "Footer",
    "email": "Email:",
    "telegram": "Telegram:",
    "footer_links": [("index.html#apply", "Become an ambassador"), ("index.html#how", "How it works"),
                     ("big-group.html", "Big group trek, 10 or more"), ("small-group.html", "Small group trip, under 10"),
                     ("founder.html", "About the co-founder"), ("contact.html", "Contact us"), ("index.html#faq", "Questions")],
    # EN and UZ buttons in the header: the current language is highlighted, the other links to the same page in it.
    # The hints are written in the language they lead to.
    "langs": [("en", "EN", "Read this page in English"), ("uz", "UZ", "Bu sahifani özbek tilida öqing")],
    "lang_label": "Language",
    "new_tab": " (opens in a new tab)",
    "press_kind": {"tv": "TV", "article": "Article", "news": "News agency", "telegram": "Telegram", "instagram": "Instagram", "video": "YouTube"},
    "copy_text": "Copy the text",
    "read_text": "Read the text",
    "copy": "Copy",
    "day": "Day {n}",
    "stop_of": "Stop {i} of {total}",
    "map_hints": ["Scroll to ride the fast train", "To the mountains by bus", "Back to Tashkent by bus"],
    "how_started": "How the trek started",
    "cohort_sub": "March 2026",
    "moments": "Uzbekistan Trek moments",
    "includes_title": "What the trek includes",
    "included": "Included in the cost",
    "not_included": "Not included",
    "faq": "FAQ",
    "you": "You",
    "we": "We",
    "dep_head": ["Departure", "Dates", "Why these dates", "Status", "Action"],
    "register_interest": "Register interest",
    "cofounder": "Co-Founder",
    "signature_role": "Co-Founder, Uzbekistan Trek",
    "story_label": "The story",
    "how_it_works": "How it works",
    "reach_label": "How to reach us",
}
# (title, description) for each page's <title> and search snippet
META = {
    "index.html": (SITE["name"], SITE["description"]),
    "big-group.html": ("Big Group Trek", "Big group treks to Uzbekistan for 10 or more graduate students: your dates, a private itinerary and a full package."),
    "small-group.html": ("Small Group Trip", "Small group trips to Uzbekistan for fewer than 10 graduate students: join a planned departure or travel privately on your own dates."),
    "founder.html": ("Co-Founder Jakhongir Sadiev", "Jakhongir Sadiev, co-founder of the Uzbekistan Trek: from a childhood dream to two Harvard and MIT treks with 95 travelers."),
    "contact.html": ("Contact us", "Contact Uzbekistan Trek: email Jakhongir Sadiev or Zokirjon Khabibullaev, or message @uzbtrek_bot on Telegram."),
}
# words on the route map of the sample itinerary; None keeps the English in shared/motion_parts.py
MAP = None
STOP_CAPS = {}   # photo key: caption on a stop card of the route, when it differs from photos.json
PHOTO_TEXT = {}  # photo key: (caption, alt), when it differs from photos.json

# Form words. data-form-title stays in English on every page, so the Telegram messages read the same; "title_note" marks the language.
FORMS = {
    "title_note": "",
    "honeypot": "Leave this field empty",
    "name": "Your name", "req_name": "your name",
    "email": "Email", "req_email": "a valid email",
    "university": "University", "req_university": "your university", "ph_university": "e.g. Columbia University",
    "telegram": "Telegram or WhatsApp (optional)", "ph_telegram": "@username or phone",
    "anything": "Anything else",
    "choose": "Choose one",
    "a_ph_email": "Your university email, if you can",
    "a_program": "Program and degree", "a_req_program": "your program and degree", "a_ph_program": "e.g. MBA, MPP or PhD",
    "a_grad": "Expected graduation", "a_grad_opts": ["2027", "2028", "2029 or later"],
    "a_size": "Classmates who might come", "a_size_opts": ["Not sure yet", "Fewer than 10", "10 to 20", "20 to 40", "More than 40"],
    "a_dates": "When could your group travel?", "a_ph_dates": "e.g. Spring break 2027",
    "a_notes": "Why do you want to bring your classmates?",
    "a_ph_notes": "A few lines about you, your classmates and the student clubs you are part of",
    "a_send": "Send application",
    "b_program": "Program or club", "b_ph_program": "e.g. SIPA, Energy Club",
    "b_size": "Group size (10 or more)", "b_req_size": "a group size of 10 or more", "b_ph_size": "e.g. 25",
    "b_dates": "Preferred dates or month", "b_ph_dates": "e.g. School break in March",
    "b_flex": "Are your dates flexible?", "b_flex_opts": ["Yes, within a week or two", "No, they are fixed", "Not sure yet"],
    "b_focus": "What should the trip focus on?", "b_focus_label": "Focus",
    "b_ph_notes": "Extra cities, length, visits you would like, dietary needs, questions",
    "b_send": "Send request",
    "s_which": "Which option?", "s_option_label": "Option",
    # (value sent to the bot, label shown); assets/trek.js looks for the value "Join a departure"
    "s_options": [("Join a departure", "Join a departure"), ("Private small-group trip", "Private trip"), ("Not sure yet", "Not sure yet")],
    "s_university": "University and program", "s_req_university": "your university and program", "s_ph_university": "e.g. NYU Stern",
    "s_travelers": "Number of travelers",
    "s_departure": "Departure or dates", "s_own_dates": "My own dates (private trip)",
    "s_room": "Room", "s_room_opts": ["Share a double room", "Single room", "Not sure yet"],
    "s_ph_notes": "Your dates if private, dietary needs, questions",
    "s_send": "Send",
}
