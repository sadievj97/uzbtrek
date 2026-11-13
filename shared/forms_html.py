"""Form markup shared by every site style. forms.js reads these hooks; each theme styles the classes.

Hooks: form.tform[data-form][data-form-title], .tf (field wrapper), .tf.full, fieldset.tf, .tchips, .tchip,
.tform-hp (honeypot, hidden), .tform-foot, .tform-msg (status), .tform-alt (Telegram hint).
Inputs carry data-label (used in the Telegram message) and data-req (required, with the phrase used in errors).
"""
from content import FORM_COMMON, INTERESTS

HONEYPOT = ('<div class="tform-hp" aria-hidden="true"><label>Leave this field empty'
            '<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>')


def _field(fid, name, label, kind="text", req=None, extra="", full=False, placeholder=""):
    cls = "tf full" if full else "tf"
    reqa = f' data-req="{req}"' if req else ""
    ph = f' placeholder="{placeholder}"' if placeholder else ""
    if kind == "textarea":
        ctl = f'<textarea id="{fid}" name="{name}" data-label="{label}"{reqa}{ph}></textarea>'
    else:
        ctl = f'<input id="{fid}" name="{name}" type="{kind}" data-label="{label}"{reqa}{ph}{extra}>'
    return f'<div class="{cls}"><label for="{fid}">{label}</label>{ctl}</div>'


def _select(fid, name, label, options, selected=None, full=False):
    cls = "tf full" if full else "tf"
    opts = "".join(f'<option{" selected" if o == selected else ""}>{o}</option>' for o in options)
    return f'<div class="{cls}"><label for="{fid}">{label}</label><select id="{fid}" name="{name}" data-label="{label}">{opts}</select></div>'


def big_group_form(btn_class="btn", prefix="b"):
    p = prefix
    chips = "".join(
        f'<label class="tchip"><input type="checkbox" name="interests" id="{p}-i{i}" value="{v}" data-label="Focus"> {v}</label>'
        for i, v in enumerate(INTERESTS, 1))
    return f"""<form class="tform" data-form="big-group" data-form-title="Big group quote request" novalidate>
  {HONEYPOT}
  {_field(p+"-name", "name", "Your name", req="your name", extra=' autocomplete="name"')}
  {_field(p+"-email", "email", "Email", kind="email", req="a valid email", extra=' autocomplete="email"')}
  {_field(p+"-school", "university", "University", req="your university", placeholder="e.g. Columbia University")}
  {_field(p+"-program", "program", "Program or club", placeholder="e.g. SIPA, Energy Club")}
  {_field(p+"-size", "group_size", "Group size (10 or more)", kind="number", req="a group size of 10 or more", extra=' min="10" max="300" inputmode="numeric"', placeholder="e.g. 25")}
  {_field(p+"-dates", "dates", "Preferred dates or month", placeholder="e.g. School break in March")}
  {_field(p+"-telegram", "telegram", "Telegram or WhatsApp (optional)", placeholder="@username or phone")}
  {_select(p+"-flex", "flexible", "Are your dates flexible?", ["Yes, within a week or two", "No, they are fixed", "Not sure yet"])}
  <fieldset class="tf full"><legend>What should the trip focus on?</legend><div class="tchips">{chips}</div></fieldset>
  {_field(p+"-notes", "notes", "Anything else", kind="textarea", full=True, placeholder="Extra cities, length, visits you would like, dietary needs, questions")}
  <div class="tform-foot"><small>{FORM_COMMON["privacy"]}</small><button class="{btn_class}" type="submit">Send request</button></div>
  <div class="tform-msg" role="status" hidden></div>
  <p class="tform-alt">{FORM_COMMON["telegram_hint"]}</p>
</form>"""


def small_group_form(btn_class="btn", prefix="s", departures=None):
    p = prefix
    deps = [d["pick"] for d in (departures or [])] + ["My own dates (private trip)"]
    return f"""<form class="tform" data-form="small-group" data-form-title="Small group interest" novalidate>
  {HONEYPOT}
  <fieldset class="tf full"><legend>Which option?</legend><div class="tchips">
    <label class="tchip"><input type="radio" name="option" id="{p}-opt-join" value="Join a departure" data-label="Option" checked> Join a departure</label>
    <label class="tchip"><input type="radio" name="option" id="{p}-opt-private" value="Private small-group trip" data-label="Option"> Private trip</label>
    <label class="tchip"><input type="radio" name="option" id="{p}-opt-unsure" value="Not sure yet" data-label="Option"> Not sure yet</label>
  </div></fieldset>
  {_field(p+"-name", "name", "Your name", req="your name", extra=' autocomplete="name"')}
  {_field(p+"-email", "email", "Email", kind="email", req="a valid email", extra=' autocomplete="email"')}
  {_field(p+"-school", "university", "University and program", req="your university and program", placeholder="e.g. NYU Stern")}
  {_select(p+"-size", "travelers", "Number of travelers", [str(i) for i in range(1, 10)], selected="2")}
  {_select(p+"-departure", "departure", "Departure or dates", deps)}
  {_select(p+"-room", "room", "Room", ["Share a double room", "Single room", "Not sure yet"])}
  {_field(p+"-telegram", "telegram", "Telegram or WhatsApp (optional)", placeholder="@username or phone", full=True)}
  {_field(p+"-notes", "notes", "Anything else", kind="textarea", full=True, placeholder="Your dates if private, dietary needs, questions")}
  <div class="tform-foot"><small>{FORM_COMMON["privacy"]}</small><button class="{btn_class}" type="submit">Send</button></div>
  <div class="tform-msg" role="status" hidden></div>
  <p class="tform-alt">{FORM_COMMON["telegram_hint"]}</p>
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
