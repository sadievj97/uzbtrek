# Uzbekistan Trek website

The public site for Uzbekistan Trek: [uzbekistantrek.com](https://uzbekistantrek.com) once the domain is connected (see "Your domain" below), until then [sadievj97.github.io/uzbtrek](https://sadievj97.github.io/uzbtrek/). Forms, chat and visit alerts go to the Telegram bot [@uzbtrek_bot](https://t.me/uzbtrek_bot).

## What is in this repository

| Path | What it is |
|---|---|
| `index.html`, `big-group.html`, `small-group.html`, `founder.html` | The site. These pages are generated from `shared/`: do not edit them by hand |
| `shared/content.py` | All the text on the site |
| `shared/photos.json` | Captions and alt text of the photos in `img/` |
| `shared/build.py` | Builds the four pages (layout and design), with `motion_parts.py`, `forms_html.py`, `logos.py` and `fonts/` |
| `shared/check.py`, `shared/requirements.py` | Checks that run after every change: each photo once, no missing files or links, no prices or em dashes, and the content decisions you asked for |
| `assets/config.js` | Your settings: relay address, visitor statistics token, bot name, email. Only you change this file |
| `assets/trek.js` | Forms, mobile menu, sliding FAQ, sample texts, visitor counter and visit alerts |
| `assets/motion.js` | Motion: the khatam stars on the home banner, the train and bus on the sample itinerary, button hover effects and the drifting watermark. Visitors who turn on "reduce motion" get a still page |
| `img/` | The photos the site uses (your other trek photos stay out of this public repository) |
| `brand/` | The khatam star logo as SVG files |
| `worker/telegram-relay.js` | The Telegram relay on Cloudflare: website requests, two-way chat and visit alerts. It holds no secrets |
| `CLAUDE.md` | Instructions Claude Code reads before it changes anything |
| `.nojekyll` | Tells GitHub Pages to serve the files as they are |

## Changing the site with Claude Code

1. Open [claude.ai/code](https://claude.ai/code) (or the Code tab in the Claude desktop or mobile app). The first time, connect your GitHub account when it asks.
2. Choose the repository `sadievj97/uzbtrek` under the message box and describe the change, for example: "Add a FAQ answer about travel insurance".
3. Claude edits the sources, rebuilds the pages, runs the checks and pushes a branch. Look at the changes, then select **Create PR**.
4. On GitHub, open the pull request and select **Merge**. The site updates in a minute or two. To undo a change later, ask Claude to revert it.

Small fixes you can also make yourself on github.com, but change the text in `shared/content.py`, not in the HTML pages: the next build would overwrite an HTML edit.

## Your domain: uzbekistantrek.com

Do these in order. Until step 3 is done, keep using the github.io address.

1. **GoDaddy (where you bought the domain):** open your domain list, choose `uzbekistantrek.com`, then **DNS**.
   - Delete the `A` record for `@` that points to GoDaddy's parking page.
   - Add four `A` records with the name `@` and these values: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`.
   - Change the `CNAME` record named `www` so it points to `sadievj97.github.io`.
   - Optional, for IPv6: four `AAAA` records named `@` with `2606:50c0:8000::153`, `2606:50c0:8001::153`, `2606:50c0:8002::153`, `2606:50c0:8003::153`.
   - Do not add a wildcard (`*`) record and do not turn on domain forwarding.
2. **Verify the domain on GitHub (recommended):** on GitHub, open your profile picture > **Settings** > **Pages** > **Add a domain**, enter `uzbekistantrek.com`, add the `TXT` record GitHub shows to GoDaddy's DNS, then select **Verify**. Keep that TXT record. It stops anyone else from using your domain on GitHub.
3. **Point the site at the domain:** in this repository open **Settings** > **Pages**, type `uzbekistantrek.com` under **Custom domain** and select **Save**. GitHub adds a `CNAME` file to the repository. When the DNS check turns green, tick **Enforce HTTPS** (this can take up to 24 hours to become available).
4. **Relay:** in Cloudflare open **Workers & Pages** > `uzbtrek-relay` > **Settings** > **Variables and Secrets** and set `ALLOWED_ORIGINS` to
   `https://uzbekistantrek.com,https://www.uzbekistantrek.com,https://sadievj97.github.io`
   then deploy. Without this the forms and visit alerts stop working on the new address.
5. **Visitor statistics:** a Cloudflare Web Analytics site counts only its own domain. Add `uzbekistantrek.com` as a new site in Web Analytics and put its token in `analyticsToken` in `assets/config.js`.
6. Update the link in your Instagram bio and anywhere else you shared the github.io address.

## Telegram relay

### 1. Get your bot token and your chat ID

1. In Telegram, open [@BotFather](https://t.me/BotFather), send `/mybots`, choose **@uzbtrek_bot**, then **API Token**. Copy the token. Treat it like a password: never put it in the website, in GitHub, or in a chat.
2. From your personal Telegram account, open [@uzbtrek_bot](https://t.me/uzbtrek_bot), press **Start** and send any message, for example `hi`. A bot can only write to people who started it.
3. In a browser, open
   `https://api.telegram.org/botYOUR_TOKEN/getUpdates`
   (replace `YOUR_TOKEN`). Find `"chat":{"id":` followed by a number, for example `"chat":{"id":123456789`. That number is your **chat ID**.
   Do this before step 4: once a webhook is set, `getUpdates` stops working.

### 2. Deploy the relay on Cloudflare (free plan is enough)

1. Create a free account at [dash.cloudflare.com](https://dash.cloudflare.com).
2. Go to **Workers & Pages**, create a new Worker from the "Hello World" starter, name it `uzbtrek-relay`, and deploy it.
3. Click **Edit code**, delete the sample code, paste the whole content of `worker/telegram-relay.js`, and click **Deploy**. Do the same whenever `worker/telegram-relay.js` changes in this repository: GitHub does not deploy the Worker.
4. Note the Worker address, for example `https://uzbtrek-relay.YOUR-ACCOUNT.workers.dev`. Opening it in a browser should show "Uzbekistan Trek relay is running."

### 3. Add the relay settings

In the Worker, open **Settings > Variables and Secrets** and add:

| Name | Type | Value |
|---|---|---|
| `BOT_TOKEN` | Secret | The token from step 1.1 |
| `ADMIN_CHAT_ID` | Text | Your chat ID from step 1.3 |
| `WEBHOOK_SECRET` | Secret | A long random string you make up. Only letters, digits, `_` and `-`, up to 256 characters |
| `ALLOWED_ORIGINS` | Text | Your site addresses without a path, separated by commas: `https://uzbekistantrek.com,https://www.uzbekistantrek.com,https://sadievj97.github.io` |
| `WELCOME_TEXT` | Text (optional) | The greeting visitors see after they press Start |
| `VISIT_ALERTS` | Text (optional) | `on` (the default: a silent note for each new visitor), `loud` (with a sound) or `off`. See "Visit alerts in Telegram" |

Deploy again if the dashboard asks you to.

### 4. Connect the bot and the website to the relay

1. Turn on two-way chat. In a browser, open this address (one line, with your values):
   `https://api.telegram.org/botYOUR_TOKEN/setWebhook?url=https://uzbtrek-relay.YOUR-ACCOUNT.workers.dev/telegram&secret_token=YOUR_WEBHOOK_SECRET`
   You should see `"ok":true` and "Webhook was set".
2. Connect the website forms: `endpoint` in `assets/config.js` holds `https://uzbtrek-relay.YOUR-ACCOUNT.workers.dev/submit`.
3. Test both:
   - Submit a form on the live site. The request arrives in your chat with @uzbtrek_bot.
   - Ask a friend to write to @uzbtrek_bot. Their message arrives in your chat, tagged with `#u` and a number.

The forms show a green "Your message has been successfully sent!" when a request reaches the bot, and a red message pointing to Telegram and email when it cannot be sent.

## How to answer people

Everything arrives in your own chat with @uzbtrek_bot:

- **Website requests** arrive as a formatted message. Its title says which form it came from: "Ambassador application" (home page), "Big group quote request" or "Small group interest". Reply by email, or write to the person on Telegram if they left a handle.
- **Chat messages** arrive tagged `#u123456789`. To answer, **reply** to that message (swipe it, or right-click > Reply). The bot sends your reply to the visitor and confirms "Sent." Text, photos and files all work.
- If you write to the bot without replying to a tagged message, nothing is sent to anyone.

## Visitor statistics (only you can see them)

The site counts its visitors with Cloudflare Web Analytics. It is free, it sets no cookies, and the numbers appear only inside your Cloudflare account. Visitors see nothing.

1. Open [Web Analytics in the Cloudflare dashboard](https://dash.cloudflare.com/?to=/:account/web-analytics) and select **Add a site**.
2. Enter the hostname without `https://` or a path: `uzbekistantrek.com`. Then select **Done**.
3. Open **Manage site**. Cloudflare shows a short snippet of code. Copy only the token from it: the letters and digits after `"token": "`.
4. Put the token in the `analyticsToken` line of `assets/config.js` and commit.
5. Open your site, wait a few minutes, then open Web Analytics again. You see visits, page views, the most viewed pages, where visitors came from, countries and devices.

Good to know:

- The token can only send visits to your account; it cannot read your statistics. That is why it may sit in this public file, unlike the bot token.
- A token counts only its own domain (and its subdomains), so a new domain needs a new site and token.
- "Visits" counts arrivals at the site from somewhere else (a link, a search, typing the address); "page views" counts every page opened. Cloudflare does not count unique people, because it does not follow individuals.
- Some ad blockers block the counter, so the real numbers are somewhat higher. Cloudflare keeps the data for six months.
- To leave out your own visits, open `https://uzbekistantrek.com/?count=off` once in each browser you use (laptop and phone). A short message confirms it. It also stops the visit alerts for that browser. `?count=on` turns both back on.
- GitHub's own Insights > Traffic page counts visits to the repository on github.com, not visits to the website.

## Visit alerts in Telegram

Each time someone arrives at the site, @uzbtrek_bot sends you a short note in your chat with it, for example:

> 👀 **New visitor**: Home page\
> From: Instagram (link tag: instagram)\
> Where: Cambridge, Massachusetts, United States (approximate)\
> Device: iPhone, Instagram app

They need the relay (the alerts use the same Worker as the forms) running the current `worker/telegram-relay.js`.

- One note per arrival, not one per page: moving between pages, reloading or going back sends nothing. Someone who comes back another day sends a new note. The site stores nothing in visitors' browsers, so it cannot tell first-time visitors from returning ones.
- Notes arrive without a sound, so website requests and chat messages still stand out. For a sound, set the Worker variable `VISIT_ALERTS` to `loud`; to stop the notes, set it to `off`.
- "Where" is the city and country that Cloudflare estimates from the visitor's internet address. It is approximate (a VPN shows the VPN's location), and the address itself is not sent to you.
- Search engines and link previews are filtered out. A flood guard sends at most one note every 10 seconds and 20 an hour for one internet address, and 30 a minute in total, so several people on one campus network within a few seconds may share one note. Web Analytics still counts all of them.
- To see which of your links bring people, add `?utm_source=NAME` to the link you share, for example `https://uzbekistantrek.com/?utm_source=instagram` in your Instagram bio. The note then says "link tag: instagram".

## Changing settings later

- **Email shown on the site:** edit `email` in `assets/config.js` and the contact text in `shared/content.py`, then rebuild.
- **New bot token:** if the token ever leaks, revoke it in @BotFather, put the new one in `BOT_TOKEN`, and open the `setWebhook` link again with the new token.
- **Turn off the chat relay:** open `https://api.telegram.org/botYOUR_TOKEN/deleteWebhook`.

## Rules this site follows

- Every photo appears once per site; no photo repeats across pages.
- No prices are shown. Payment is described as three installments: a fixed first deposit, a fixed second deposit, then the remaining balance.
- The site states that Uzbekistan Trek is independent and not affiliated with any university.
- The ambassador program promises no pay, discount or free place. Many ambassadors study on student visas.
