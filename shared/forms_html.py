"""Form markup shared by every site style. forms.js reads these hooks; each theme styles the classes.

Hooks: form.tform[data-form][data-form-title], .tf (field wrapper), .tf.full, fieldset.tf, .tchips, .tchip,
.tform-hp (honeypot, hidden), .tform-foot, .tform-msg (status), .tform-alt (Telegram hint).
Inputs carry data-label (used in the Telegram message) and data-req (required, with the phrase used in errors).
"""
import content
from content import FORM_COMMON, INTERESTS

# The words come from FORMS, FORM_COMMON and INTERESTS in content.py; shared/build.py passes the Uzbek ones (content_uz.py)
# for the pages in uz/. data-form-title stays in English, so the Telegram messages read the same in both languages.


def _honeypot(t):
    return (f'<div class="tform-hp" aria-hidden="true"><label>{t["honeypot"]}'
            '<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>')


HONEYPOT = _honeypot(content.FORMS)


def _field(fid, name, label, kind="text", req=None, extra="", full=False, placeholder=""):
    cls = "tf full" if full else "tf"
    reqa = f' data-req="{req}"' if req else ""
    ph = f' placeholder="{placeholder}"' if placeholder else ""
    if kind == "textarea":
        ctl = f'<textarea id="{fid}" name="{name}" data-label="{label}"{reqa}{ph}></textarea>'
    else:
        ctl = f'<input id="{fid}" name="{name}" type="{kind}" data-label="{label}"{reqa}{ph}{extra}>'
    return f'<div class="{cls}"><label for="{fid}">{label}</label>{ctl}</div>'


def _select(fid, name, label, options, selected=None, full=False, prompt=None):
    """prompt adds an empty first option (for example "Choose one"); an empty value is left out of the request."""
    cls = "tf full" if full else "tf"
    first = f'<option value="">{prompt}</option>' if prompt else ""
    opts = first + "".join(f'<option{" selected" if o == selected else ""}>{o}</option>' for o in options)
    return f'<div class="{cls}"><label for="{fid}">{label}</label><select id="{fid}" name="{name}" data-label="{label}">{opts}</select></div>'


def _foot(t, common, privacy, btn_class, send):
    return f"""<div class="tform-foot"><small>{common[privacy]}</small><button class="{btn_class}" type="submit">{t[send]}</button></div>
  <div class="tform-msg" role="status" hidden></div>
  <p class="tform-alt">{common["telegram_hint"]}</p>"""


def ambassador_form(btn_class="btn", prefix="a", t=None, common=None):
    """Home page application. It goes to the bot like the other forms, titled "Ambassador application"."""
    t, common, p = t or content.FORMS, common or FORM_COMMON, prefix
    return f"""<form class="tform" data-form="ambassador" data-form-title="Ambassador application{t["title_note"]}" novalidate>
  {_honeypot(t)}
  {_field(p+"-name", "name", t["name"], req=t["req_name"], extra=' autocomplete="name"')}
  {_field(p+"-email", "email", t["email"], kind="email", req=t["req_email"], extra=' autocomplete="email"', placeholder=t["a_ph_email"])}
  {_field(p+"-school", "university", t["university"], req=t["req_university"], placeholder=t["ph_university"])}
  {_field(p+"-program", "program", t["a_program"], req=t["a_req_program"], placeholder=t["a_ph_program"])}
  {_select(p+"-grad", "graduation", t["a_grad"], t["a_grad_opts"], prompt=t["choose"])}
  {_select(p+"-size", "group_size", t["a_size"], t["a_size_opts"])}
  {_field(p+"-dates", "dates", t["a_dates"], placeholder=t["a_ph_dates"])}
  {_field(p+"-telegram", "telegram", t["telegram"], placeholder=t["ph_telegram"])}
  {_field(p+"-notes", "notes", t["a_notes"], kind="textarea", full=True, placeholder=t["a_ph_notes"])}
  {_foot(t, common, "privacy_apply", btn_class, "a_send")}
</form>"""


def big_group_form(btn_class="btn", prefix="b", t=None, common=None, interests=None):
    t, common, p = t or content.FORMS, common or FORM_COMMON, prefix
    chips = "".join(
        f'<label class="tchip"><input type="checkbox" name="interests" id="{p}-i{i}" value="{v}" data-label="{t["b_focus_label"]}"> {v}</label>'
        for i, v in enumerate(interests or INTERESTS, 1))
    return f"""<form class="tform" data-form="big-group" data-form-title="Big group quote request{t["title_note"]}" novalidate>
  {_honeypot(t)}
  {_field(p+"-name", "name", t["name"], req=t["req_name"], extra=' autocomplete="name"')}
  {_field(p+"-email", "email", t["email"], kind="email", req=t["req_email"], extra=' autocomplete="email"')}
  {_field(p+"-school", "university", t["university"], req=t["req_university"], placeholder=t["ph_university"])}
  {_field(p+"-program", "program", t["b_program"], placeholder=t["b_ph_program"])}
  {_field(p+"-size", "group_size", t["b_size"], kind="number", req=t["b_req_size"], extra=' min="10" max="300" inputmode="numeric"', placeholder=t["b_ph_size"])}
  {_field(p+"-dates", "dates", t["b_dates"], placeholder=t["b_ph_dates"])}
  {_field(p+"-telegram", "telegram", t["telegram"], placeholder=t["ph_telegram"])}
  {_select(p+"-flex", "flexible", t["b_flex"], t["b_flex_opts"])}
  <fieldset class="tf full"><legend>{t["b_focus"]}</legend><div class="tchips">{chips}</div></fieldset>
  {_field(p+"-notes", "notes", t["anything"], kind="textarea", full=True, placeholder=t["b_ph_notes"])}
  {_foot(t, common, "privacy", btn_class, "b_send")}
</form>"""


def small_group_form(btn_class="btn", prefix="s", departures=None, t=None, common=None):
    t, common, p = t or content.FORMS, common or FORM_COMMON, prefix
    deps = [d["pick"] for d in (departures or [])] + [t["s_own_dates"]]
    ids = ["join", "private", "unsure"]
    radios = "".join(
        f'\n    <label class="tchip"><input type="radio" name="option" id="{p}-opt-{ids[i]}" value="{v}" data-label="{t["s_option_label"]}"'
        f'{" checked" if i == 0 else ""}> {lab}</label>' for i, (v, lab) in enumerate(t["s_options"]))
    return f"""<form class="tform" data-form="small-group" data-form-title="Small group interest{t["title_note"]}" novalidate>
  {_honeypot(t)}
  <fieldset class="tf full"><legend>{t["s_which"]}</legend><div class="tchips">{radios}
  </div></fieldset>
  {_field(p+"-name", "name", t["name"], req=t["req_name"], extra=' autocomplete="name"')}
  {_field(p+"-email", "email", t["email"], kind="email", req=t["req_email"], extra=' autocomplete="email"')}
  {_field(p+"-school", "university", t["s_university"], req=t["s_req_university"], placeholder=t["s_ph_university"])}
  {_select(p+"-size", "travelers", t["s_travelers"], [str(i) for i in range(1, 10)], selected="2")}
  {_select(p+"-departure", "departure", t["s_departure"], deps)}
  {_select(p+"-room", "room", t["s_room"], t["s_room_opts"])}
  {_field(p+"-telegram", "telegram", t["telegram"], placeholder=t["ph_telegram"], full=True)}
  {_field(p+"-notes", "notes", t["anything"], kind="textarea", full=True, placeholder=t["s_ph_notes"])}
  {_foot(t, common, "privacy", btn_class, "s_send")}
</form>"""


def general_form(btn_class="btn", prefix="g"):
    """One form for single-page styles: the group-size choice decides which request it is."""
    p = prefix
    return f"""<form class="tform" data-form="general" data-form-title="Trek request" novalidate>
  {HONEYPOT}
  <fieldset class="tf full"><legend>How many people are traveling?</legend><div class="tchips">
    <label class="tchip"><input type="radio" name="group" id="{p}-big" value="Big group (10 or more)" data-label="Group" checked> 10 or more</label>
    <label class="tchip"><input type="radio" name="group" id="{p}-small" value="Small group (1 to 9)" data-label="Group"> 1 to 9</label>
  </div></fieldset>
  {_field(p+"-name", "name", "Your name", req="your name", extra=' autocomplete="name"')}
  {_field(p+"-email", "email", "Email", kind="email", req="a valid email", extra=' autocomplete="email"')}
  {_field(p+"-school", "university", "University and program", req="your university and program", placeholder="e.g. Kellogg, Northwestern")}
  {_field(p+"-size", "travelers", "Number of travelers", kind="number", extra=' min="1" max="300" inputmode="numeric"', placeholder="e.g. 12")}
  {_field(p+"-dates", "dates", "Preferred dates or month", placeholder="e.g. Spring break 2027", full=True)}
  {_field(p+"-notes", "notes", "Anything else", kind="textarea", full=True, placeholder="Cities, length, interests, questions")}
  <div class="tform-foot"><small>{FORM_COMMON["privacy"]}</small><button class="{btn_class}" type="submit">Send request</button></div>
  <div class="tform-msg" role="status" hidden></div>
  <p class="tform-alt">{FORM_COMMON["telegram_hint"]}</p>
</form>"""
