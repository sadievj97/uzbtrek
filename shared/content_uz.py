"""Uzbek copy for the pages in uz/, in the new Uzbek Latin alphabet (law of October 2026: Oʻ to Ö, Gʻ to Ğ, Sh to Ş, Ch to Ç).

The text below is written in the familiar Latin spelling, with o' and g' for Oʻ and Gʻ and an apostrophe for the tutuq belgisi.
newlat() turns it into the new letters when this module loads: o' to ö, g' to ğ, sh to ş, ch to ç, any other apostrophe
between letters to ʼ. It leaves HTML tags, entities, web addresses, emails, @handles and the names in PROTECT as they are.
Kept in English on purpose: the sample texts and the brochure (ambassadors send them to international classmates), the
participants' quotes (their own words) and the English names of schools and companies. People's names use their Uzbek
spelling (the owner, Nov 2026): Jaxongir Sadiyev, Zokirjon Xabibullayev, and the officials as Uzbek media write them.
The same rules as content.py apply: no prices, graduate students only, no promised government meetings, no em dashes.
"""
import json
import os
import re

from content import *   # noqa: F401,F403  every name not set below stays as in content.py
import content as EN

LANG = "uz"

# ---------------------------------------------------------------- new letters
# Names and English titles that contain sh, ch or an apostrophe and must stay exactly as written.
PROTECT = ["Harvard Kennedy School", "Harvard Full Scholarship", "Massachusetts Institute of Technology", "fellowship",
           "English", "WhatsApp", "Ctrl+C", "Cmd+C"]
_SKIP = re.compile("|".join([r"<[^>]*>", r"&[#\w]+;", r"https?://[^\s\"<>]+", r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", r"@\w+"]
                            + [re.escape(p) for p in sorted(PROTECT, key=len, reverse=True)]))
_PAIRS = (("SH", "Ş"), ("Sh", "Ş"), ("sh", "ş"), ("CH", "Ç"), ("Ch", "Ç"), ("ch", "ç"))
_OG = {"O": "Ö", "o": "ö", "G": "Ğ", "g": "ğ"}


def _letters(t):
    t = re.sub(r"([OoGg])['ʻ‘]", lambda m: _OG[m.group(1)], t)
    t = re.sub(r"(?<=\w)['’](?=\w)", "ʼ", t)   # tutuq belgisi: ma'lumot to maʼlumot
    for a, b in _PAIRS:
        t = t.replace(a, b)
    return t


def newlat(s):
    """One string in the new letters, leaving tags, links, emails, handles and PROTECT as they are."""
    out, pos = [], 0
    for m in _SKIP.finditer(s):
        out += [_letters(s[pos:m.start()]), m.group(0)]
        pos = m.end()
    return "".join(out) + _letters(s[pos:])


_PHOTO_KEYS = set(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "photos.json"), encoding="utf-8")))
# words that are keys, not text: photo keys, icon names, quote keys, press kinds
_KEYS = _PHOTO_KEYS | {"slides", "megaphone", "chat", "plane", "tv", "article", "news", "telegram", "instagram", "video",
                       "long", "guided", "best", "dancing"}


def _deep(v):
    if isinstance(v, str):
        if v in _KEYS or v.startswith(("#", "http")) or re.fullmatch(r"[\w./-]+\.(html|pdf)(#[\w-]+)?", v):   # keys and links
            return v
        return newlat(v)
    if isinstance(v, list):
        return [_deep(x) for x in v]
    if isinstance(v, tuple):
        return tuple(_deep(x) for x in v)
    if isinstance(v, dict):
        return {k: _deep(x) for k, x in v.items()}
    return v


# ---------------------------------------------------------------- site
SITE = dict(EN.SITE, description=(
    "Uzbekistan Trek elchisi bo'ling: magistratura va doktoranturadagi kursdoshlaringizni O'zbekistonga olib keling, "
    "har bir qadamda materiallarimiz va yordamimiz bilan. 2025 va 2026-yillardagi Garvard va MIT treklari asosida."))

NAV = [
    ("index.html#how", "Qanday ishlaydi", "how"),
    ("index.html#team", "Biz kimmiz", "team"),
    ("index.html#groups", "Guruh sayohatlari", "groups"),
    ("index.html#faq", "Savollar", "faq"),
    ("contact.html", "Aloqa", "contact"),
]
NAV_CTA = ("index.html#apply", "Ariza topshirish")

DISCLAIMER = ("Uzbekistan Trek mustaqil loyiha. U Garvard universiteti, Massachusets texnologiya instituti yoki boshqa biror universitet "
              "bilan bog'liq emas, ular tomonidan homiylik qilinmaydi va ma'qullanmaydi. Universitet nomlari o'tgan ishtirokchilar "
              "qayerda tahsil olishini bildiradi.")
FOOTER_BLURB = ("Magistrant va doktorantlar uchun elchilar dasturi va O'zbekistonga guruh sayohatlari. Sayohatlar faqat O'zbekiston "
                "ichidagi xizmatlarni o'z ichiga oladi; xalqaro parvozlar kiritilmagan.")
COPYRIGHT = "&copy; 2026 Uzbekistan Trek. Suratlar 2025 va 2026-yillardagi treklardan."

# ---------------------------------------------------------------- home: the ambassador program
HERO = dict(EN.HERO,
            kicker="Elchilar dasturi",
            title="Uzbekistan Trek elchisi bo'ling",
            lede=("O'zbekistonni kampusingizga olib keling. Siz kursdoshlaringizni yig'asiz. Biz materiallar, targ'ibot usullari va "
                  "har bir qadamda yordam beramiz, siz esa guruhingiz bilan O'zbekistonga sayohat qilasiz."),
            cta_primary=("#apply", "Ariza topshirish"),
            cta_secondary=("#how", "Qanday ishlaydi"))

TEAM = {
    "title": "Biz kimmiz",
    "lede": ("Biz, Jaxongir va Zokirjon, Bostonda tahsil olayotgan ikki o'zbek talabasimiz. Yurtimizni dunyoning turli "
             "burchaklaridan kelgan kursdoshlarimizga ko'rsatishni yaxshi ko'ramiz."),
    "members": [
        dict(EN.TEAM["members"][0], role="Hammuassis", name="Jaxongir Sadiyev",
             text="Harvard Kennedy School. Trekni 2025-yilda Garvardda boshlagan: ikki trek, 95 nafar sayohatchi.",
             link=("founder.html", "Uning hikoyasini o'qing")),
        dict(EN.TEAM["members"][1], role="Hammuassis", name="Zokirjon Xabibullayev", initials="ZX",
             text="Boston University. Elchilar dasturini va trekning yangi universitetlarga kengayishini muvofiqlashtiradi."),
    ],
}

GETS = {
    "title": "Sizga nima beramiz",
    "lede": "Ikki trekdan olgan barcha tajribamiz, universitetingiz uchun tayyor holda.",
    "items": [
        ("slides", "Tayyor materiallar",
         "Tanishtiruv uchrashuvi uchun slaydlar, flayer, namuna matnlar va guruhingiz uchun ro'yxatdan o'tish sahifasi."),
        ("megaphone", "Targ'ibot usullari",
         "Ikki trekda 95 nafar sayohatchini qanday jalb qilganimiz: sayohat haqida qayerda xabar berish, tanishtiruv uchrashuvini "
         "qanday o'tkazish va qiziqishni ro'yxatdan o'tishga qanday aylantirish."),
        ("chat", "Har bir qadamda yordam",
         "Sayohatni siz bilan birga rejalashtiramiz, kursdoshlaringiz savollariga javob beramiz hamda sanalaringiz uchun narx "
         "taklifi va kunma-kun reja tayyorlaymiz."),
        ("plane", "Guruhingiz bilan sayohat",
         "O'zbekistonga kursdoshlaringiz bilan birga borasiz. Joyida hamma narsani biz rejalashtiramiz va tashkil qilamiz."),
    ],
}

APPLY = {
    "title": "Elchi bo'lish uchun ariza topshiring",
    "lede": "O'zingiz va olib kelmoqchi bo'lgan kursdoshlaringiz haqida yozing. Sizga elektron pochta yoki Telegram orqali javob beramiz.",
    "who_title": "Kimlar ariza topshirishi mumkin",
    "who": ["O'zbekistondan tashqaridagi universitetlarda tahsil olayotgan o'zbek magistrantlari, doktorantlari, fellowship "
            "ishtirokchilari va postdoktorantlari",
            "Sayohat tashkil qilish tajribasi shart emas",
            "Kursdoshlaringiz istalgan davlatdan bo'lishi mumkin"],
}

GROUPS = {
    "title": "Guruhingiz allaqachon bormi?",
    "lede": "Klublar, kurslar va do'stlar biz bilan to'g'ridan-to'g'ri sayohat qilishi ham mumkin. Guruhingiz hajmini tanlang.",
}
CHOICES = {
    "big": dict(EN.CHOICES["big"], unit="sayohatchi", title="Katta guruh treki",
                desc="Kurs, klub yoki dastur uchun. Sanalarni o'zingiz tanlaysiz; butun sayohatni to'liq paket sifatida rejalashtiramiz.",
                short="Sizning sanalaringizda to'liq paket.", cta="Katta guruh trekini rejalashtirish"),
    "small": dict(EN.CHOICES["small"], unit="sayohatchi", title="Kichik guruh sayohati",
                  desc="Yolg'iz, juftlikda yoki bir necha do'st bilan. Rejalashtirilgan safarga qo'shiling yoki alohida sayohat qiling.",
                  short="Safarga qo'shiling yoki alohida boring.", cta="Kichik guruh variantlari"),
}

# ---------------------------------------------------------------- testimonials: the quotes stay in the participants' own English
QUOTES = {k: dict(v) for k, v in EN.QUOTES.items()}
_CITES = {"best": "2025-yil ishtirokchisi", "guided": "2026-yil ishtirokchisi, Harvard Kennedy School kursdoshi",
          "dancing": "2025-yil ishtirokchisi", "long": "2025-yil ishtirokchisi, Harvard Kennedy School"}

PREVIOUS = {
    "title": "O'tgan treklardan",
    "bullets": [
        "2025-yil mart oyida Garvard va MITning 45 nafar magistrant va doktoranti biz bilan Toshkent, Buxoro va Samarqandga sayohat qildi.",
        "2026-yil mart oyida ikkinchi trek 50 nafar sayohatchiga yetdi.",
        "Endi boshqa universitetlardagi o'zbek talabalari ham Uzbekistan Trek elchisi sifatida o'z kursdoshlarini olib kelishi mumkin.",
    ],
    "script": "Ishtirokchilar nima deydi?",
}

ITINERARY = {
    "title": "Namunaviy marshrut",
    "intro": ("Garvard va MIT treklarimiz shunday o'tgan, ma'lumot uchun ko'rsatilgan. Bu tayyor paket emas, balki boshlang'ich "
              "nuqta: uni uzaytirishimiz, Xiva yoki Farg'ona vodiysi kabi shaharlarni qo'shishimiz va har bir kunni guruhingizga "
              "moslashimiz mumkin. O'tgan treklar bahorgi ta'tilda bo'lgan, lekin trek istalgan oyda o'tishi mumkin."),
    "days": [
        {"n": 1, "where": "Kelish: <strong>Toshkent</strong>", "items": ["Mehmonxonaga joylashish va dam olish", "Toshkent bo'ylab sayr"]},
        {"n": 2, "where": "Tezyurar poyezdda <strong>Buxoroga</strong>", "items": ["Labi Hovuz", "Eski shahar", "Minorai Kalon"]},
        {"n": 3, "where": "<strong>Buxoroda</strong>", "items": ["Ark qal'asi", "Sitorai Mohi Xosa saroyi", "Ismoil Somoniy maqbarasi"]},
        {"n": 4, "where": "Tezyurar poyezdda <strong>Samarqandga</strong>", "items": ["Registon va Shohizinda", "Bibixonim masjidi", "Registondagi lazer shou"]},
        {"n": 5, "where": "<strong>Samarqanddan</strong> <strong>Toshkentga</strong>", "items": ["Go'ri Amir", "Ulug'bek rasadxonasi"]},
        {"n": 6, "where": "<strong>Toshkentda</strong>", "items": ["Kompaniya va universitetlarga tashrif", "Chorsu bozori"]},
        {"n": 7, "where": "Avtobusda <strong>Toshkent tog'lariga</strong>", "items": ["Chorvoq suv ombori", "Amirsoy kanat yo'li"]},
        {"n": 8, "where": "<strong>Toshkentdan</strong> qaytish", "items": ["Toshkent xalqaro aeroporti"]},
    ],
    "tailor_title": "O'zingizga moslang",
    "tailor": [
        "Faqat ta'til emas, istalgan oyda",
        "Sakkiz kundan uzunroq yoki qisqaroq",
        "Xiva, Farg'ona vodiysi yoki cho'ldagi o'tov lagerini qo'shing",
        "Ta'lim yo'nalishingizga mos tashriflar",
    ],
    "footnote": ("Garvard va MIT treklaridagi namunaviy marshrut, faqat ma'lumot uchun. Har bir trek moslashtiriladi: sanalar, "
                 "davomiylik, shaharlar va tashriflar guruhingiz bilan kelishiladi."),
}

INCLUDED = [
    "Nonushta bilan turar joy",
    "Ovqatlanish (tushlik va kechki ovqat)",
    "Toshkent, Samarqand va Buxoroda shahar ekskursiyalari",
    "Gid hamrohligidagi madaniy tadbirlar, masalan, mart oyida Navro'z",
    "Transport (tezyurar poyezdlar va transferlar)",
    "Mahalliy gid, muzeylarga kirish chiptalari va SIM karta",
]
NOT_INCLUDED = [
    "Xalqaro parvozlar",
    "Tibbiy va evakuatsiya sug'urtasi",
    "Pasportingizga viza kerak bo'lsa, viza to'lovlari",
    "Alkogol va shaxsiy xarajatlar",
    "Kiritilgan deb ko'rsatilmagan har qanday narsa",
]

PAYMENT = {
    "title": "Sanalar va to'lov",
    "lede": ("Aksariyat guruhlar ta'til paytida sayohat qiladi, lekin trek istalgan oyda o'tishi mumkin. Har bir trek narxi guruh, "
             "sanalar va davomiylikka qarab hisoblanadi, shuning uchun yagona narx e'lon qilmaymiz."),
    "tranches_title": "To'lov uch bosqichda",
    "tranches": [
        ("Birinchi avans", "joyingizni band qilish uchun belgilangan summa"),
        ("Ikkinchi avans", "sayohatga yaqinroq to'lanadigan belgilangan summa"),
        ("Qolgan summa", "jo'nab ketishdan oldin to'lanadi"),
    ],
    "note": "Aniq summalar va muddatlar narx taklifingizda ko'rsatiladi.",
}

START = {
    "title": "Qanday ishlaydi",
    "lede": ("Universitetingizda trek dasturi yo'qmi? U shart emas. Har bir trek bitta talaba, bir nechta qiziqqan kursdosh va "
             "bizning yordamimiz bilan boshlanadi."),
    "steps": [
        ("Ariza topshiring",
         "O'zingiz, universitetingiz va olib kelmoqchi bo'lgan kursdoshlaringiz haqida yozing. Bu bir necha daqiqa oladi.",
         ("#apply", "Hozir ariza topshiring")),
        ("To'plamni oling",
         "Rejangizni birga muhokama qilamiz va tashkilotchi to'plamini beramiz: tanishtiruv uchrashuvi slaydlari, flayer va namuna matnlar.",
         None),
        ("Qiziqishni tekshiring",
         "Kurs chatingizda qisqa xabar va bir daqiqalik so'rovnomani ulashing. 10 va undan ortiq kursdoshingiz rozi bo'lishini "
         "maqsad qiling; kamroq bo'lsa ham kichik guruh sifatida sayohat qilish mumkin.",
         ("#sample-note", "Namuna xabardan foydalaning")),
        ("Ro'yxatdan o'tishni oching",
         "Sanalaringiz uchun narx taklifi va kunma-kun reja yuboramiz. Qisqa tanishtiruv uchrashuvi o'tkazing va ro'yxatdan o'tish "
         "havolasini ulashing. Hamma bizning sahifamiz orqali ro'yxatdan o'tadi va to'laydi.",
         ("#sample-announcement", "Namuna e'londan foydalaning")),
        ("Birga sayohat qiling",
         "Guruhingiz bilan O'zbekistonga borasiz. Joyida hamma narsani biz rejalashtiramiz, tashkil qilamiz va sizni kutib olamiz.",
         ("#itinerary", "Namunaviy marshrutni ko'ring")),
    ],
    "where_title": "Guruhingizni qayerdan topish mumkin",
    "where": ["Kursingiz yoki guruhingiz chati", "Talabalar klublari: mintaqaviy, xalqaro munosabatlar, siyosat, biznes",
              "Dasturingizning talabalar axborotnomasi", "Magistratura talabalari kengashi", "Mintaqa haqida dars beradigan professorlar",
              "Boshqa dasturlardagi do'stlar"],
    "tips_title": "Tashabbus talabalardan bo'lsin",
    "tips": ["Kursdosh sifatida yozing: nega borishni xohlayotganingizni va kimlar kelishini kutayotganingizni ayting.",
             "Bir-ikki kursdosh bilan birlashing va talabalar klubidan sayohat haqida a'zolariga xabar berishni so'rang. Klublarda "
             "sizda bo'lmagan pochta ro'yxatlari bor.",
             "Qanday ishlashi haqida ochiq bo'ling: Uzbekistan Trek sayohatni rejalashtiradi, ro'yxatdan o'tish va to'lovlarni "
             "yuritadi; siz guruhni yig'asiz.",
             "Universitetingiz nomi yoki logotipidan sayohat rasmiy dastur bo'lgandek foydalanmang."],
    "samples_title": "Nusxa olish mumkin bo'lgan namuna matnlar (ingliz tilida)",
}

# The sample texts and the brochure stay in English (the owner, Nov 2026); only the words around them are in Uzbek.
_SAMPLE_UZ = {
    "sample-note": ("3-qadam", "Qiziqishni tekshirish uchun namuna xabar", "Narx taklifini so'rashdan oldin yuboring."),
    "sample-announcement": ("4-qadam", "Garvard trekidan namuna e'lon (email)",
                            "Narx taklifini olganingizdan keyin yuboring. Garvard ma'lumotlari va [qavs ichidagi] so'zlarni o'zingiznikiga almashtiring."),
    "sample-whatsapp": ("4-qadam", "Garvard trekidan namuna WhatsApp xabari",
                        "Ro'yxatdan o'tish ochilganda kurs chatlaringizga joylang. Garvard ma'lumotlarini o'zingiznikiga almashtiring."),
    "sample-brochure": ("4-qadam", "Garvard trekining ma'lumot broshyurasi (PDF)",
                        "Garvard treki 2027 uchun ishlatilgan namuna ma'lumot broshyurasi"),
}
_FILE_UZ = ("Broshyurani ochish", "PDF yuklab olish (17 sahifa, 3 MB)")

_VISA = ("Boshqa pasportlar uchun rasmiy viza sahifasini tekshiring: <a href=\"https://gov.uz/en/mfa/pages/o-zbekiston-respublikasi-vizasi\" "
         "target=\"_blank\" rel=\"noopener\">O'zbekiston Respublikasi vizasi</a>.")
_VISA_US = "Trek barcha davlatlar fuqarolari uchun ochiq. AQSh fuqarolari O'zbekistonga 30 kungacha vizasiz kirishi mumkin (2026-yil 1-yanvardan)."
_FLIGHTS = ("Uzbekistan Airways Nyu-York (JFK) va Toshkent o'rtasida haftasiga bir necha marta to'xtovsiz parvozlarni amalga oshiradi, "
            "parvoz taxminan 13 soat davom etadi. Istanbul yoki Dubay kabi xablar orqali ham uchishingiz mumkin.")
_GOV = ("Standart dastur kompaniyalar, universitetlar va/yoki madaniyatga qaratilgan (tasdiqlanishiga qarab). "
        "Rasmiy davlat uchrashuvlari unga kirmaydi.")

FAQ_HOME = [
  ("Elchilar uchun", [
    ("Kim elchi bo'la oladi?",
     ["O'zbekistondan tashqaridagi universitetlarda tahsil olayotgan o'zbek magistrantlari, doktorantlari, fellowship ishtirokchilari "
      "va postdoktorantlari. Sayohat tashkil qilish tajribasi shart emas: har bir qadamda materiallar va yordam beramiz."]),
    ("Elchi nima qiladi?",
     ["Kursdoshlaringizni bir joyga yig'asiz: sayohat haqida xabar berasiz, tanishtiruv uchrashuvi o'tkazasiz va guruhingizni "
      "xabardor qilib turasiz. Sayohatni biz rejalashtiramiz, ro'yxatdan o'tish va to'lovlarni yuritamiz hamda guruhingizni "
      "O'zbekistonda kutib olamiz."]),
    ("Sayohat xarajatlarini kim qoplaydi?",
     ["Talabalarning o'zlari. Har bir sayohatchi trekdagi o'z joyi uchun ro'yxatdan o'tish sahifamiz orqali to'laydi va xalqaro "
      "parvozini o'zi band qiladi."]),
    ("Universitetimda trek dasturi yo'q. Baribir boshlasam bo'ladimi?",
     ["Ha. Dastur shart emas. Har bir trek bitta talaba va bir nechta qiziqqan kursdosh bilan boshlanadi. "
      "<a href=\"#how\">Qanday ishlashini</a> ko'ring."]),
    ("Universitetimdagi qiziqishni qanday tekshirsam bo'ladi?",
     ["Kursdoshlaringizga bir daqiqalik so'rovnoma bilan qisqa xabar yuboring. Pochta ro'yxati shart emas: kurs chati yoki "
      "talabalar klubi kifoya.",
      "<a href=\"#sample-note\">Namuna xabarimizdan foydalaning</a> va keyingi qadamlar uchun <a href=\"#how\">qanday ishlashini</a> ko'ring."]),
    ("Men o'zbek emasman. Kursdoshlarimni olib kela olamanmi?",
     ["Ha. 10 va undan ortiq sayohatchi uchun <a href=\"big-group.html\">katta guruh trekini</a> yoki 10 kishidan kam guruh uchun "
      "<a href=\"small-group.html\">kichik guruh sayohatini</a> rejalashtiring."]),
  ]),
  ("Sayohatchilar uchun", [
    ("Kimlar qatnashishi mumkin?",
     ["Magistrantlar, doktorantlar, fellowship ishtirokchilari va postdoktorantlar. Trek barcha davlatlar fuqarolari uchun ochiq. "
      "Joy bo'lsa, turmush o'rtoqlar va juftlar ham qo'shilishi mumkin. Bakalavriat talabalari uchun sayohat tashkil qilmaymiz."]),
    ("Viza kerakmi?", [_VISA_US, _VISA]),
    ("O'zbekiston xavfsizmi?",
     ["AQSh Davlat departamenti O'zbekistonga eng past ogohlantirish darajasi bo'lgan 1-darajani bergan va odatiy ehtiyot "
      "choralarini ko'rishni maslahat beradi (ogohlantirish 2026-yil 26-yanvarda e'lon qilingan). Har bir guruh jo'nab ketishdan "
      "oldin xavfsizlik bo'yicha yo'riqnoma oladi."]),
    ("Xalqaro parvozlar narxga kiradimi?",
     ["Yo'q. Sayohatlar faqat O'zbekiston ichidagi xizmatlarni o'z ichiga oladi, shuning uchun parvozlarni o'zingiz band qilasiz.", _FLIGHTS]),
    ("Narxga nimalar kirmaydi?",
     ["Xalqaro parvozlar, tibbiy va evakuatsiya sug'urtasi, pasportingizga viza kerak bo'lsa viza to'lovlari, alkogol va shaxsiy "
      "xarajatlar hamda kiritilgan deb ko'rsatilmagan har qanday narsa."]),
    ("To'lov qanday amalga oshiriladi?",
     ["Uch bosqichda: belgilangan birinchi avans, belgilangan ikkinchi avans va jo'nab ketishdan oldin qolgan summa. Aniq summalar "
      "va muddatlar narx taklifingizda ko'rsatiladi."]),
    ("Trek bahorgi ta'tildan boshqa vaqtda o'tishi mumkinmi?",
     ["Ha. Aksariyat guruhlar ta'til paytida sayohat qiladi, lekin trekni istalgan oyda va istalgan davomiylikda tashkil qila olamiz."]),
    ("Davlat rasmiylari bilan uchrashamizmi?", [_GOV]),
    ("Voz kechsam, pul qaytariladimi?",
     ["Bizning roziligimiz bilan joyingizni boshqa magistrant yoki doktorantga o'tkazishingiz mumkin. Pulni qaytarish shartlari "
      "to'lov paytida qabul qiladigan bron shartlarida belgilangan. Sayohatni bekor qilish sug'urtasini olishni qat'iy tavsiya qilamiz."]),
    ("Buni universitetim tashkil qiladimi?",
     ["Yo'q. Guruhlar o'zlarini o'zlari tashkil qiladi va Uzbekistan Trek hech qaysi universitet bilan bog'liq emas. Iltimos, "
      "sayohatni rasmiy universitet dasturi sifatida ko'rsatmang."]),
  ]),
]

# ---------------------------------------------------------------- big group page
BIG = dict(EN.BIG,
    kicker="10 va undan ortiq sayohatchi",
    title="Katta guruh treki",
    lede=("Kurs, klub, talabalar birlashmasi yoki butun dastur uchun. Guruhni siz yig'asiz va sanalarni tanlaysiz. Joyida hamma "
          "narsani biz yagona to'liq paket sifatida rejalashtiramiz va tashkil qilamiz."),
    cta_primary=("#quote", "Guruh uchun narx so'rash"),
    cta_secondary=("index.html#itinerary", "Namunaviy marshrutni ko'ring"),
    for_title="Kimlar uchun",
    **{"for": [
        ("Talabalar klublari va birlashmalari",
         "Markaziy Osiyo bilan bir hafta davomida yaqindan tanishmoqchi bo'lgan mintaqaviy, siyosat, energetika, moliya yoki biznes klublari."),
        ("Kurs yoki guruh",
         "Ta'til paytida birga sayohat qiladigan dastur talabalari, xuddi 2025 va 2026-yillardagi Garvard va MIT guruhlarimiz kabi."),
        ("Turli dasturlardagi do'stlar",
         "Turli dastur yoki maktablardan o'z alohida sayohatini xohlagan o'n va undan ortiq magistrant yoki doktorant."),
    ]},
    gets_title="Guruhingiz nimalarga ega bo'ladi",
    gets=[
        "Sizning sanalaringizda alohida marshrut",
        "Mehmonxonalar, ovqatlanish, tezyurar poyezdlar, transferlar va litsenziyali gidlar",
        "Yo'nalishingizga mos kompaniya, universitet va madaniy tashriflar (tasdiqlanishiga qarab)",
        "Butun hafta guruhingiz bilan birga bo'ladigan o'zbek magistrant yoki doktorant mezbon (tasdiqlanishi va imkoniyatga qarab)",
        "Imkon bo'lsa, O'zbekistondagi universitetingiz bitiruvchilari bilan kechki ovqat (imkoniyatga qarab)",
        "Tashkilotchi to'plami: tanishtiruv uchrashuvi slaydlari, flayer va ro'yxatdan o'tish sahifasi",
    ],
    split_title="Kim nima qiladi",
    you=["Kamida 10 nafar ishtirokchini yig'ish", "Haftani tanlash, odatda ta'tilingiz", "Ro'yxatdan o'tish havolasini guruhingizga ulashish",
         "Guruhingizni nima qiziqtirishini bizga aytish"],
    we=["Marshrut va narx taklifini tuzish", "Ro'yxatdan o'tish va to'lovlarni yuritish", "Mehmonxona, poyezd, gid va tashriflarni band qilish",
        "Jo'nab ketishdan oldin hammaga yo'riqnoma berish", "Guruhingizni O'zbekistonda kutib olish"],
    timeline_title="Mart oyidagi trek uchun namunaviy jadval",
    timeline_note="Boshqa oyda sayohat qilmoqchimisiz? Xuddi shu qadamlarni sanalaringizga moslaymiz.",
    timeline=[
        ("Oktabr va noyabr", "Narx taklifini so'rash"),
        ("Noyabr", "Tanishtiruv uchrashuvi; ro'yxatdan o'tish ochiladi"),
        ("Dekabr oxiri", "Birinchi avans"),
        ("Yanvar oxiri", "Ikkinchi avans"),
        ("Fevral oxiri", "Qolgan summa va xonalar ro'yxati"),
        ("Mart boshi", "Jo'nashdan oldingi yo'riqnoma"),
        ("Ta'til", "Sayohat"),
    ],
    form_title="Guruh uchun narx so'rash",
    form_lede="Guruhingiz haqida yozing. Odatda uch ish kuni ichida narx taklifi va kunma-kun reja bilan javob beramiz.",
    faq_title="Katta guruh bo'yicha savollar",
    faq=[
        ("10 kishidan kam ro'yxatdan o'tsa-chi?",
         ["Sayohatingizni baribir alohida kichik guruh sayohati sifatida o'tkazishimiz mumkin yoki sayohatchilaringiz rejalashtirilgan "
          "safarlarimizdan biriga qo'shilishi mumkin."]),
        ("Bahorgi ta'tildan boshqa vaqtda sayohat qila olamizmi?",
         ["Ha. Aksariyat guruhlar ta'til paytida sayohat qiladi, lekin trekingizni istalgan oyda tashkil qila olamiz."]),
        ("Guruhimiz davlat rasmiylari bilan uchrasha oladimi?", [_GOV]),
        ("Marshrutni o'zgartira olamizmi?",
         ["Ha. Kun qo'shing, Xiva yoki Farg'ona vodiysini qo'shing yoki cho'ldagi o'tov lagerida bir kecha qoling. Narx taklifingiz "
          "shunga mos o'zgaradi."]),
        ("Pulni kim yig'adi?",
         ["Har bir ishtirokchi ro'yxatdan o'tish sahifamiz orqali operatorga to'g'ridan-to'g'ri to'laydi. Tashkilotchilar hech qachon "
          "to'lovlar bilan shug'ullanmaydi."]),
        ("Sayohat universitetimiz bilan bog'liqmi?",
         ["Yo'q. Guruhingiz o'zini o'zi tashkil qiladi va mustaqil sayohat qiladi. Iltimos, sayohatni rasmiy universitet dasturi "
          "sifatida ko'rsatmang."]),
    ])

# ---------------------------------------------------------------- small group page
_DEP = [
    ("Bahorgi ta'til", "2027-yil 13-martdan 20-martgacha", "Mart o'rtasidagi eng keng tarqalgan bahorgi ta'tillarga mos", "Rejalashtirilgan"),
    ("Navro'z", "2027-yil 20-martdan 27-martgacha", "21-martdagi Navro'zda O'zbekistonda bo'lasiz", "Rejalashtirilgan"),
    ("Bitiruvdan keyin", "2027-yil may oxiri va iyun", "Iyul jaziramasidan oldin, iliq havo", "Sanalar keyinroq"),
]
SMALL = dict(EN.SMALL,
    kicker="10 kishidan kam sayohatchi",
    title="Kichik guruh sayohati",
    lede=("Yolg'iz, juftlikda yoki bir necha do'st bilan sayohat qilmoqchimisiz? Boshqa universitetlarning magistrant va "
          "doktorantlari bilan rejalashtirilgan safarga qo'shiling yoki o'z sanalaringizda alohida sayohat qiling."),
    cta_primary=("#departures", "Rejalashtirilgan sanalar"),
    cta_secondary=("#interest", "Alohida sayohat haqida so'rash"),
    ways_title="Ikki yo'l",
    join={"tag": "Rejalashtirilgan sanalar", "title": "Safarga qo'shiling",
          "items": ["Ta'tillar va bitiruvdan keyingi belgilangan sanalar", "Boshqa universitetlarning magistrant va doktorantlari bilan sayohat",
                    "Katta guruh treklarimizdagi marshrut va mezbonlar", "Boshqa ishtirokchi bilan ikki kishilik xona yoki bir kishilik xona"],
          "cta": ("#departures", "Rejalashtirilgan sanalar")},
    private={"tag": "O'z sanalaringiz", "title": "Alohida kichik guruh sayohati",
             "items": ["Siz tanlagan sanalarda ikki kishidan to'qqiz kishigacha", "Haydovchili alohida avtomobil va ingliz tilida so'zlashadigan gid",
                       "Sizning sur'atingiz va qiziqishlaringiz", "Bir kishi uchun narx necha kishi sayohat qilishingizga bog'liq"],
             "cta": ("#interest", "Alohida sayohat narxini so'rash")},
    dep_title="Rejalashtirilgan safarlar",
    dep_lede=("Allaqachon qo'shilishingiz mumkin bo'lgan ba'zi sanalar. Qiziqishingizni bildiring, biz har qanday avans olishdan "
              "oldin sanalar va narxni tasdiqlaymiz."),
    departures=[dict(d, name=n, len="8 kun", dates=dt, why=w, status=st, pick=f"{n}, {dt}")
                for d, (n, dt, w, st) in zip(EN.SMALL["departures"], _DEP)],
    cmp_title="Qaysi variant sizga mos?",
    cmp_head=["", "Safarga qo'shilish", "Alohida kichik guruh sayohati", "Katta guruh treki"],
    cmp_rows=[
        ("Guruh hajmi", "1 dan 9 kishigacha, kattaroq aralash guruhda", "2 dan 9 kishigacha, faqat sizning guruhingiz", "10 va undan ortiq, faqat sizning guruhingiz"),
        ("Sanalar", "Rejalashtirilgan", "Siz tanlaysiz", "Siz tanlaysiz"),
        ("Bir kishi uchun narx", "Eng past", "Yuqoriroq, kamroq odamga taqsimlanadi", "Guruh hajmiga bog'liq"),
        ("Siz tomondan rejalashtirish", "Yo'q", "Sanalar va qiziqishlarni tanlash", "Guruhni yig'ish"),
        ("Kimlar uchun qulay", "Yolg'iz sayohatchilar va juftliklar", "Juftliklar va kichik do'stlar guruhlari", "Klublar, kurslar va dasturlar"),
    ],
    cmp_note="O'n va undan ortiq kishimisiz? <a href=\"big-group.html\">Katta guruh treklarini ko'ring</a>.",
    form_title="Qiziqishingizni bildiring",
    form_lede="Hozir to'lov yo'q. Avval sanalar va narxni tasdiqlaymiz, odatda uch ish kuni ichida.",
    faq_title="Kichik guruh bo'yicha savollar",
    faq=[
        ("Yolg'iz kelsam bo'ladimi?",
         ["Ha. Ko'pchilik safarga yolg'iz qo'shiladi. Sizni umumiy xona uchun boshqa ishtirokchi bilan juftlaymiz yoki bir kishilik "
          "xonani band qilishingiz mumkin."]),
        ("Kim bilan sayohat qilaman?",
         ["Turli universitet va davlatlardan kelgan magistrantlar, doktorantlar, fellowship ishtirokchilari va postdoktorantlar bilan, "
          "litsenziyali mahalliy gidlar va o'zbek mezbon hamrohligida (imkoniyatga qarab)."]),
        ("Turmush o'rtog'im yoki juftim kela oladimi?", ["Ha, joy bo'lsa."]),
        ("Nega alohida sayohat bir kishi uchun qimmatroq?",
         ["Avtomobil, haydovchi va gid kamroq odam o'rtasida taqsimlanadi. Qancha ko'p kishi sayohat qilsa, bir kishi uchun narx "
          "shuncha past bo'ladi."]),
        ("Viza kerakmi?", [_VISA_US, _VISA]),
        ("Xalqaro parvozlar narxga kiradimi?", ["Yo'q. Parvozlarni o'zingiz band qilasiz. " + _FLIGHTS]),
    ])

# ---------------------------------------------------------------- co-founder page
FOUNDER = dict(EN.FOUNDER,
    kicker="Hammuassis haqida",
    name="Jaxongir Sadiyev",
    signature="Jaxongir Sadiyev",
    lede="Uzbekistan Trek hammuassisi",
    facts=[
        ("Harvard University (HKS)", "Iqtisodiyot magistri (MPA/ID)"),
        ("Tashkil qilingan ikki trek", "2025 va 2026-yillar, 95 nafar sayohatchi"),
        ("Garvarddan oldin", "Jahon banki, Birlashgan Millatlar Tashkiloti, Auburn University (AL)"),
        ("Stipendiyalar", "Fulbright, Edmund S. Muskie, Harvard Full Scholarship"),
    ],
    story=[
        ("Hech qachon unutmagan suratim",
         ["Bolaligimda bir talabaning universitetdagi kursdoshlari bilan o'z yurti bo'ylab sayohat qilayotgan suratini ko'rgandim. "
          "Bu surat yodimda qoldi. Bir kun kelib o'z kursdoshlarimni ona shahrim Samarqandga olib kelaman, deb o'zimga so'z bergandim."]),
        ("Dasturimda 25 yil ichidagi birinchi o'zbek",
         ["Garvardga kelganimda, Harvard Kennedy Schooldagi dasturimda 25 yil ichida birinchi o'zbek edim va shu imkoniyatdan "
          "foydalanib biror ish qilishim kerakligini his qildim. Men o'qigan Amerika universitetlarida O'zbekiston va Markaziy Osiyo "
          "haqida kam gapirilardi. Buni o'zgartirmoqchi edim, shuning uchun Garvard va MITdagi kursdoshlarimni O'zbekistonga olib "
          "kelishga qaror qildim."]),
        ("Birinchi kuniyoq qirq kishi",
         ["Rostini aytsam, 20 kishi qo'shilishiga ishonchim komil emasdi. Trekni e'lon qilgan birinchi kunimizdayoq 40 kishi "
          "ro'yxatdan o'tgan edi. Oxir-oqibat birinchi treklar uchun 200 ga yaqin qiziquvchi bo'ldi, shuning uchun saralash "
          "o'tkazishimizga to'g'ri keldi."]),
        ("2025-yil mart: 45 nafar sayohatchi",
         ["Birinchi trek juda muvaffaqiyatli o'tdi. Biz bilan 45 nafar magistrant va doktorant sayohat qildi. Vazirlar, Buxoro "
          "viloyati hokimi va Senat rahbariyati bilan uchrashdik, Nordic University talabalari bilan fikr almashdik va Navro'zni "
          "Prezident bilan birga nishonladik. Ishtirokchilar, universitet hamjamiyati va O'zbekistondagi mezbonlarimizning "
          "fikrlari shunchalik yaxshi bo'ldiki, buni yana takrorlashga qaror qildik.",
          "Bundan tashqari, trek yana foyda keltirdi: ba'zi talabalar O'zbekiston haqida tadqiqot va dissertatsiya yozdi, ba'zilari "
          "investitsiya imkoniyatlarini izladi, ba'zilari esa mahalliy universitetlar bilan birgalikda kurslar ochish ustida ishladi."]),
        ("2026-yil mart: 50 nafar sayohatchi",
         ["Ikkinchi trek kattaroq bo'ldi: 50 nafar sayohatchi va ko'proq siyosat yo'nalishlari. Davlat tomonidan Senat raisi, "
          "Ijtimoiy himoya milliy agentligi rahbariyati, Buxoro viloyati hokimi, raqamli texnologiyalar vaziri va Markaziy bank "
          "raisi o'rinbosari bilan uchrashdik.",
          "Xususiy sektorda ACWA Power rahbariyati bilan qayta tiklanuvchi energiya, TBC Bank bilan moliya bozorlari va IT Parkda "
          "texnologiyalar haqida suhbatlashdik."]),
        ("Keyingi qadam",
         ["Maqsadim ko'proq trek o'tkazish va ularni boshqa universitetlarning magistrant va doktorantlariga ochish. Shuning uchun "
          "elchilar dasturini boshladik: endi xorijda o'qiyotgan o'zbek talabalari o'z kursdoshlarini olib kelishi mumkin, biz esa "
          "ularga har bir qadamda yordam beramiz. Ikki trekdan keyin talabalar O'zbekistondagi bir haftadan nimani kutishini "
          "bilamiz va guruhingiz uchun shunday trek tashkil qilishga yordam bera olamiz."]),
    ],
    timeline_title="Qanday o'sdi",
    timeline=[
        ("Bolalik", "", "Bir surat g'oyaga turtki beradi"),
        ("2024", "", "Garvard universitetiga keladi"),
        ("Birinchi kun", "40", "trek e'lon qilinganda ro'yxatdan o'tganlar"),
        ("2025-yil mart", "45", "birinchi trekdagi sayohatchilar"),
        ("2026-yil mart", "50", "ikkinchi trekdagi sayohatchilar"),
        ("Keyin", "", "Ko'proq trek, ko'proq universitet"),
    ],
    quotes_title="2025 va 2026-yil ishtirokchilaridan",
    areas_title="Garvard va MIT treklari kimlar bilan uchrashdi",
    areas={
        "Davlat": [
            "Senat: Senat raisi Tanzila Norboyeva",
            "Ijtimoiy himoya milliy agentligi: Shahnoza Mirziyoyeva",
            "Buxoro viloyati: hokim Botir Zaripov",
            "Raqamli texnologiyalar vazirligi: vazir Sherzod Shermatov",
            "Oliy ta'lim, fan va innovatsiyalar vazirligi: vazir Qo'ng'irotboy Sharipov",
            "Maktabgacha va maktab ta'limi vazirligi: vazir Hilola Umarova",
            "Markaziy bank: rais o'rinbosari Dr. Nodirbek Achilov",
        ],
        "Xususiy sektor va universitetlar": [
            "ACWA Power: Dr. Jon Zaidi, O'zbekiston bo'yicha bosh ijrochi direktor va vitse-prezident",
            "TBC Bank: Nika Kurdiani, O'zbekiston bo'yicha bosh ijrochi direktor",
            "IT Park",
            "Yangi O'zbekiston universiteti",
            "Nordic University: Dr. Alisher Jo'rayev",
        ],
    },
    areas_note=("Boshqa universitetlar uchun treklar kompaniyalar, universitetlar va/yoki madaniyatga qaratiladi (tasdiqlanishiga qarab). "
                "Rasmiy davlat uchrashuvlari standart dasturga kirmaydi."),
    cta_title="O'zbekistonni kampusingizga olib keling",
    cta_lede="Elchi bo'ling va kursdoshlaringiz bilan O'zbekistonga sayohat qiling.",
    cta_groups=("Guruhingiz bormi? <a href=\"big-group.html\">Katta guruh treklari</a> va "
                "<a href=\"small-group.html\">kichik guruh sayohatlarini</a> ko'ring."),
    moments_title="Treklardan lavhalar",
)

# ---------------------------------------------------------------- press (home page)
_PRESS_LINES = {   # English line: Uzbek line
    "Harvard University students in Uzbekistan": "Garvard universiteti talabalari O'zbekistonda",
    "The students visit New Uzbekistan University": "Talabalar Yangi O'zbekiston universitetiga tashrif buyurdi",
    "The visit to Uzbekistan begins": "O'zbekistonga tashrif boshlandi",
    "A meeting with Harvard and MIT students on joint education projects": "Garvard va MIT talabalari bilan qo'shma ta'lim loyihalari bo'yicha uchrashuv",
    "The Chairwoman of the Senate meets the students": "Senat raisi talabalar bilan uchrashdi",
    "43 Harvard Kennedy School and MIT students on campus": "Harvard Kennedy School va MITning 43 nafar talabasi kampusda",
    "Celebrating Nowruz with the Uzbekistan Trek 2025": "Uzbekistan Trek 2025 bilan Navro'z bayrami",
    "Video of the visit": "Tashrif videosi",
    "52 students studying in the US visit Bukhara": "AQShda tahsil olayotgan 52 nafar talaba Buxoroda",
    "Telegram post": "Telegram posti",
    "Instagram reel": "Instagram rolik",
    "Instagram post": "Instagram posti",
}
_PRESS_SRC = {"Uzbekistan 24": "O'zbekiston 24", "UzA": "O'zA", "Senate": "Senat",
              "Tanzila Narbaeva": "Tanzila Norboyeva", "Shakhnoza Mirziyoyeva": "Shahnoza Mirziyoyeva",
              "New Uzbekistan University": "Yangi O'zbekiston universiteti",
              "Ministry of Higher Education, Science and Innovation": "Oliy ta'lim, fan va innovatsiyalar vazirligi",
              "National Agency for Social Protection": "Ijtimoiy himoya milliy agentligi"}
_PRESS_ACT = {"Watch": "Ko'rish", "Read": "O'qish", "View": "Ochish"}
PRESS = {
    "title": "OAVda",
    "lede": "O'zbekiston televideniyesi, milliy axborot agentligi, Senat, vazirliklar va universitetlar ikkala trekni ham yoritgan.",
    "note": "Materiallarning aksariyati o'zbek tilida.",
    "ticker": ["O'zbekiston 24", "MY5", "O'zA", "O'zbekiston Senati", "Oliy ta'lim, fan va innovatsiyalar vazirligi",
               "Ijtimoiy himoya milliy agentligi", "Yangi O'zbekiston universiteti", "Nordic University", "Bright Uzbekistan"],
    "years": [(yr, sub, [(k, _PRESS_SRC.get(s, s), _PRESS_LINES[l], _PRESS_ACT[a], u) for k, s, l, a, u in items])
              for (yr, _, items), sub in zip(EN.PRESS["years"], ["2025-yil mart, 45 nafar sayohatchi", "2026-yil mart, 50 nafar sayohatchi"])],
}

# ---------------------------------------------------------------- forms
FORM_COMMON = {
    "privacy": "Ma'lumotlaringizdan faqat ushbu so'rovga javob berish uchun foydalanamiz.",
    "privacy_apply": "Ma'lumotlaringizdan faqat arizangizni ko'rib chiqish va sizga javob berish uchun foydalanamiz.",
    "telegram_hint": "Yozishmani afzal ko'rasizmi? Bizga Telegramda yozing: <a href=\"https://t.me/uzbtrek_bot\" target=\"_blank\" rel=\"noopener\">@uzbtrek_bot</a>.",
}
INTERESTS = ["Biznes va moliya", "Davlat siyosati", "Texnologiya", "Energetika va iqlim", "Madaniyat va oshxona", "Tog'lar va tabiat"]

# ---------------------------------------------------------------- contact page
CONTACT = dict(EN.CONTACT,
    kicker="Aloqa",
    title="Biz bilan bog'laning",
    lede="Elchilar dasturi yoki guruh sayohati haqida savolingiz bormi? Ikkimizdan biriga yozing yoki Telegram orqali xabar yuboring.",
    people=[dict(EN.CONTACT["people"][0], role="Hammuassis", name="Jaxongir Sadiyev"),
            dict(EN.CONTACT["people"][1], role="Hammuassis", name="Zokirjon Xabibullayev", initials="ZX")],
    telegram_text="Yozishmani afzal ko'rasizmi? Bizga Telegramda xabar yuboring.",
    telegram_cta="Telegramda yozish",
    next_title="Boshqa narsa qidiryapsizmi?",
    next=[("index.html#apply", "Elchi bo'ling"), ("big-group.html", "Katta guruh trekini rejalashtiring, 10 va undan ortiq"),
          ("small-group.html", "Kichik guruh sayohatini rejalashtiring, 10 kishidan kam"), ("index.html#faq", "Savollarni o'qing")],
)

# ---------------------------------------------------------------- interface words
UI = dict(EN.UI,
    logo_label="Uzbekistan Trek, bosh sahifa",
    menu="Menyu",
    nav_label="Asosiy menyu",
    footer_label="Pastki menyu",
    email="Elektron pochta:",
    footer_links=[("index.html#apply", "Elchi bo'ling"), ("index.html#how", "Qanday ishlaydi"),
                  ("big-group.html", "Katta guruh treki, 10 va undan ortiq"), ("small-group.html", "Kichik guruh sayohati, 10 kishidan kam"),
                  ("founder.html", "Hammuassis haqida"), ("contact.html", "Biz bilan bog'laning"), ("index.html#faq", "Savollar")],
    new_tab=" (yangi oynada ochiladi)",
    press_kind=dict(EN.UI["press_kind"], article="Maqola", news="Axborot agentligi"),
    copy_text="Matndan nusxa olish",
    read_text="Matnni o'qish",
    copy="Nusxa olish",
    day="{n}-kun",
    stop_of="{i}-bekat, jami {total}",
    map_hints=["Tezyurar poyezdda yurish uchun sahifani aylantiring", "Avtobusda tog'larga", "Avtobusda Toshkentga qaytish"],
    how_started="Trek qanday boshlangan",
    cohort_sub="2026-yil mart",
    moments="Uzbekistan Trek lavhalari",
    includes_title="Trek narxiga nimalar kiradi",
    included="Narxga kiradi",
    not_included="Narxga kirmaydi",
    faq="Savollar",
    you="Siz",
    we="Biz",
    dep_head=["Safar", "Sanalar", "Nega bu sanalar", "Holati", "Amal"],
    register_interest="Qiziqish bildirish",
    cofounder="Hammuassis",
    signature_role="Hammuassis, Uzbekistan Trek",
    story_label="Hikoya",
    how_it_works="Qanday ishlaydi",
    reach_label="Biz bilan qanday bog'lanish mumkin",
)
META = {
    "index.html": ("Uzbekistan Trek", SITE["description"]),
    "big-group.html": ("Katta guruh treki", "10 va undan ortiq magistrant va doktorant uchun O'zbekistonga katta guruh treklari: "
                       "sizning sanalaringiz, alohida marshrut va to'liq paket."),
    "small-group.html": ("Kichik guruh sayohati", "10 kishidan kam magistrant va doktorant uchun O'zbekistonga kichik guruh sayohatlari: "
                         "rejalashtirilgan safarga qo'shiling yoki o'z sanalaringizda alohida sayohat qiling."),
    "founder.html": ("Hammuassis Jaxongir Sadiyev", "Uzbekistan Trek hammuassisi Jaxongir Sadiyev: bolalik orzusidan 95 nafar "
                     "sayohatchi bilan o'tgan ikki Garvard va MIT trekigacha."),
    "contact.html": ("Biz bilan bog'laning", "Uzbekistan Trek bilan aloqa: Jaxongir Sadiyev yoki Zokirjon Xabibullayevga yozing yoki "
                     "Telegramda @uzbtrek_bot ga xabar yuboring."),
}
MAP = {
    "cities": {"tas": ("Toshkent", "1, 6 va 8-kunlar"), "buk": ("Buxoro", "2 va 3-kunlar"), "sam": ("Samarqand", "4 va 5-kunlar"),
               "mtn": ("Tog'lar", "7-kun, avtobusda")},
    "cards": {"tas": "Toshkent", "buk": "Buxoro", "sam": "Samarqand", "mtn": "Toshkent tog'lari"},
    "khiva": ("Xiva", "Qo'shimcha variant"),
    "title": ("Namunaviy marshrut: Toshkentga kelish, tezyurar poyezdda Buxoroga, tezyurar poyezdda Samarqandga, Toshkentga "
              "qaytish, avtobusda Toshkent tog'larida bir kun, Toshkentdan qaytish. Xivani qo'shimcha variant sifatida qo'shish mumkin."),
}
STOP_CAPS = {"tashkent_minor_mosque": "Koshinli peshtoq, Toshkent", "a006": "Moviy gumbazlar, Toshkent"}

FORMS = dict(EN.FORMS,
    honeypot="Bu maydonni bo'sh qoldiring",
    name="Ismingiz", req_name="ismingizni",
    email="Email", req_email="to'g'ri email manzilni",
    university="Universitet", req_university="universitetingizni", ph_university="masalan, Columbia University",
    telegram="Telegram yoki WhatsApp (ixtiyoriy)", ph_telegram="@username yoki telefon",
    anything="Qo'shimcha ma'lumot",
    choose="Tanlang",
    a_ph_email="Iloji bo'lsa, universitet emailingiz",
    a_program="Dastur va daraja", a_req_program="dasturingiz va darajangizni", a_ph_program="masalan, MBA, MPP yoki PhD",
    a_grad="Taxminiy bitirish yili", a_grad_opts=["2027", "2028", "2029 yoki keyinroq"],
    a_size="Kelishi mumkin bo'lgan kursdoshlar", a_size_opts=["Hali aniq emas", "10 kishidan kam", "10 dan 20 gacha", "20 dan 40 gacha", "40 dan ortiq"],
    a_dates="Guruhingiz qachon sayohat qila oladi?", a_ph_dates="masalan, 2027-yil bahorgi ta'til",
    a_notes="Nega kursdoshlaringizni olib kelmoqchisiz?",
    a_ph_notes="O'zingiz, kursdoshlaringiz va a'zo bo'lgan talabalar klublaringiz haqida bir necha qator",
    a_send="Arizani yuborish",
    b_program="Dastur yoki klub", b_ph_program="masalan, SIPA, Energy Club",
    b_size="Guruh hajmi (10 va undan ortiq)", b_req_size="10 va undan ortiq guruh hajmini", b_ph_size="masalan, 25",
    b_dates="Afzal sanalar yoki oy", b_ph_dates="masalan, mart oyidagi ta'til",
    b_flex="Sanalaringiz o'zgarishi mumkinmi?", b_flex_opts=["Ha, bir-ikki hafta ichida", "Yo'q, ular aniq", "Hali aniq emas"],
    b_focus="Sayohat nimaga qaratilsin?", b_focus_label="Yo'nalish",
    b_ph_notes="Qo'shimcha shaharlar, davomiylik, xohlagan tashriflaringiz, ovqatlanish talablari, savollar",
    b_send="So'rovni yuborish",
    s_which="Qaysi variant?", s_option_label="Variant",
    s_options=[("Join a departure", "Safarga qo'shilish"), ("Private small-group trip", "Alohida sayohat"), ("Not sure yet", "Hali aniq emas")],
    s_university="Universitet va dastur", s_req_university="universitetingiz va dasturingizni", s_ph_university="masalan, NYU Stern",
    s_travelers="Sayohatchilar soni",
    s_departure="Safar yoki sanalar", s_own_dates="O'z sanalarim (alohida sayohat)",
    s_room="Xona", s_room_opts=["Boshqa ishtirokchi bilan ikki kishilik xona", "Bir kishilik xona", "Hali aniq emas"],
    s_ph_notes="Alohida sayohat bo'lsa sanalaringiz, ovqatlanish talablari, savollar",
    s_send="Yuborish",
)

PHOTO_TEXT = {   # photo key: (caption, alt)
    "samarkand_registan_night": ("Tungi Registon", "Kechasi yoritilgan Registon, ho'l maydonda aksi ko'rinadi"),
    "samarkand_shahizinda": ("Shohizinda, Samarqand", "Shohizinda majmuasidagi baland moviy koshinli peshtoq"),
    "samarkand_tillakari_dome": ("Tillakori, Samarqand", "Pastdan ko'rinib turgan Tillakori madrasasining zarhal gumbazi"),
    "samarkand_circle": ("Oltin gumbaz ostida", "Zarhal gumbaz ostida doira bo'lib yotgan, yuzlari tepaga qaragan talabalar"),
    "cohort_registan": ("Registonda 50 nafar sayohatchi", "Registondagi 2026-yilgi magistrant va doktorantlar guruhi"),
    "bukhara_palace_ceiling": ("Saroy shifti, Buxoro", "Sitorai Mohi Xosa saroyidagi naqshli va oynali shift"),
    "bukhara_golf_cart": ("Eski Buxoro aravachada", "Buxoroda elektr aravachada jilmayib turgan uch talaba"),
    "hero_mir_i_arab": ("Mir Arab madrasasi, Buxoro", "Kech quyosh nurida feruza gumbazli Mir Arab madrasasi"),
    "tashkent_minor_mosque": ("Toshkent", "Toshkentdagi ko'k gilamli ulkan koshinli peshtoq"),
    "tashkent_civilization_dome": ("Moviy gumbaz, Toshkent", "To'q moviy rangda yoritilgan gumbaz ichki ko'rinishi"),
    "food_plov": ("Mahorat darsida pishirgan palovimiz", "Oshpazlik mahorat darsida qozonga qatlab solingan palov masalliqlari"),
    "food_tandir": ("Loy tandirda non yopish", "Loy tandir yonida novvoy va talaba"),
    "workshop_cooking": ("Somsa pishirish darsi", "Somsa pishirish darsida xamir yoyayotgan talaba"),
    "mountains_amirsoy_group": ("Amirsoyda qor", "Amirsoyda qor ustidagi talabalar"),
    "mountains_snow": ("Amirsoy kanat yo'li", "Amirsoyda qorli yonbag'irlar ustidagi kanat yo'li kabinasi"),
    "mountains_charvak": ("Chorvoq suv ombori", "Tepaliklar orasidagi Chorvoq suv ombori"),
    "mountains_horse": ("Chorvoq tepasida", "Chorvoq yaqinida oq otda ketayotgan talaba"),
    "nowruz_trees": ("Buxoro davlat tibbiyot institutida bahor uchun daraxt ekish",
                     "Buxoro davlat tibbiyot institutida mahalliy ko'ngillilar bilan daraxt ekayotgan talabalar"),
    "train_afrosiyob": ("Tezyurar poyezd", "Bekat platformasidagi Afrosiyob tezyurar poyezdi"),
    "y2025_circle": ("Samarqandda gumbaz ostida", "Samarqandda naqshli gumbaz ostida doira bo'lib yotgan talabalar"),
    "y2025_bukhara_arch": ("Buxoro", "Buxorodagi ravoq ostida turgan talabalar guruhi"),
    "y2025_workshop": ("Rasm darsi, Buxoro", "Mahorat darsida chizgan rasmlarini ushlab turgan talabalar"),
    "y2025_registan": ("Registon, Samarqand", "Registonda suratga tushayotgan talabalar guruhi"),
    "y2025_suzani": ("So'zana ustaxonasi, Buxoro", "So'zanalar orasida o'tirgan 2025-yilgi guruh"),
    "y2025_hazrati_imam": ("Birinchi trek, 2025-yil mart", "Quyosh botayotganda moviy gumbazli majmua oldida 2025-yilgi guruh"),
    "y2025_kalyan": ("Minorai Kalon, Buxoro", "Minorai Kalon poyida 2025-yilgi guruh"),
    "y2025_dancer": ("Kutib olish kechasi", "Guruh uchun raqs ijro etayotgan milliy libosdagi raqqosa"),
    "y2025_nowruz": ("Toshkentda Navro'z", "Navro'z bayramida milliy liboslardagi talabalar"),
    "founder_portrait": ("Jaxongir Sadiyev", "Samarqanddagi moviy koshinli Shohizinda oldida o'tirgan Jaxongir Sadiyev"),
    "senate_group": ("Senatda Senat raisi Tanzila Norboyeva va Ijtimoiy himoya milliy agentligi rahbariyati bilan",
                     "O'zbekiston Senati zinapoyalarida rasmiy kiyimdagi katta talabalar guruhi"),
    "with_shakhnoza": ("Shahnoza Mirziyoyeva bilan, Ijtimoiy himoya milliy agentligi", "Shahnoza Mirziyoyeva bilan turgan Jaxongir Sadiyev"),
    "a006": ("Toshkent", "Toshkentdagi moviy gumbazli masjid majmuasi"),
    "a030": ("Toshkentda quyosh botishi", "Toshkentda quyosh botayotganda qorayib ko'ringan ulkan bino"),
    "a060": ("ACWA rahbariyati bilan nonushta", "ACWA rahbariyati bilan nonushtada taqdimot qilayotgan ma'ruzachi"),
    "a070": ("TBC Bankka tashrif, Toshkent", "Toshkentdagi TBC Bankka tashrif buyurgan 2026-yilgi guruh"),
    "a315": ("Tungi Registon", "Kechasi pushti va yashil rangda yoritilgan Registon madrasasi"),
    "a365": ("Go'ri Amir, Samarqand", "Go'ri Amirning qovurg'ali moviy gumbazi"),
    "a474": ("Tillakori eshigi oldida, Registon", "Registondagi Tillakori madrasasining katta yog'och eshigi oldida yig'ilgan guruh"),
    "a489": ("Shohizinda gumbazi", "Shohizindadagi koshinli gumbaz ichki ko'rinishi"),
    "a626": ("Cho'qqida issiq ichimliklar", "Tog'dagi kafeda jilmayib o'tirgan uch do'st"),
    "a634": ("Tog'da selfi", "Ortida tog'lar ko'rinib turgan ayvonda guruh selfisi"),
    "a693": ("Gumbaz ostida", "Naqshli gumbaz ostidagi yorug'lik halqasi"),
    "a822": ("Labi Hovuz, Buxoro", "Buxorodagi Labi Hovuz"),
    "a916": ("Ark qal'asi, Buxoro", "Moviy osmon fonida Ark qal'asining g'ishtin minorasi"),
    "a947": ("Buxoro", "Buxorodagi koshinli peshtoq va feruza gumbaz"),
    "y2025_senate": ("Birinchi trek Senatda Senat raisi Tanzila Norboyeva bilan, 2025",
                     "Bayroqlar o'rnatilgan Senat zalida rasmiy kiyimdagi 2025-yilgi guruh"),
    "navoi_theater": ("Alisher Navoiy nomidagi opera va balet teatrida",
                      "Toshkentdagi Alisher Navoiy nomidagi opera va balet teatri zalidagi guruh"),
    "y2025_nowruz_concert": ("Prezident bilan Navro'z konsertida, 2025",
                             "Navro'z konsertida rang-barang liboslarda chiqish qilayotgan raqqosalar, tomoshabinlar orasidan ko'rinish"),
    "y2025_bukhara_classmates": ("Buxoroda kursdoshlar bilan, 2025", "Buxorodagi koshinli ravoqli tokchada suratga tushayotgan kursdoshlar"),
    "y2026_chimgan": ("Chimyon tog'larida, 2026", "Chimyon tog'larida qorli cho'qqilar oldida turgan olti do'st"),
    "y2025_football": ("Toshkentdagi Milliy stadionda futbol o'yinida, 2025", "Stadiondagi futbol o'yinida o'zbek bayroqlari bilan guruh selfisi"),
    "a573": ("Amirsoyda qor ustida", "Amirsoyda qor ustidagi guruh"),
    "zokirjon_khabibullaev": ("Zokirjon Xabibullayev", "Uzbekistan Trek hammuassisi Zokirjon Xabibullayev"),
    "jakhongir_sadiev": ("Jaxongir Sadiyev", "Uzbekistan Trek hammuassisi Jaxongir Sadiyev"),
    "train_group": ("Poyezdda", "Kameraga qo'l silkitib, jilmayib turgan talabalar bilan to'la poyezd vagoni"),
    "senate_handshake": ("Senatda", "O'zbek bayroqlari oldida, Senat zalida o'tirib qo'l berib ko'rishayotgan kostyumdagi ikki kishi"),
}

# ---------------------------------------------------------------- everything above into the new letters
for _name in ["SITE", "NAV", "NAV_CTA", "DISCLAIMER", "FOOTER_BLURB", "COPYRIGHT", "HERO", "TEAM", "GETS", "APPLY", "GROUPS",
              "CHOICES", "PREVIOUS", "ITINERARY", "INCLUDED", "NOT_INCLUDED", "PAYMENT", "START", "FAQ_HOME", "BIG", "SMALL",
              "FOUNDER", "PRESS", "FORM_COMMON", "INTERESTS", "CONTACT", "UI", "META", "MAP", "STOP_CAPS", "FORMS", "PHOTO_TEXT"]:
    globals()[_name] = _deep(globals()[_name])

# set after the conversion, so they stay as written
for _k, _cite in _CITES.items():
    QUOTES[_k]["cite"] = newlat(_cite)
SAMPLES = []
for _s in EN.SAMPLES:
    _step, _title, _when = (newlat(x) for x in _SAMPLE_UZ[_s["id"]])
    _u = dict(_s, step=_step, title=_title, when=_when)
    if "file" in _s:
        _u["file"] = (_s["file"][0],) + tuple(newlat(x) for x in _FILE_UZ)
    SAMPLES.append(_u)
UI["other_lang"] = ("en", "English", "Read this page in English")
FORMS["title_note"] = " (Uzbek page)"
FORMS["s_options"] = [(v, lab) for (v, _), (_, lab) in zip(EN.FORMS["s_options"], FORMS["s_options"])]
