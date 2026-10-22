# Uzbekistan Trek website

A static website (plain HTML, no build step), ready for GitHub Pages. Forms and chat go to the Telegram bot [@uzbtrek_bot](https://t.me/uzbtrek_bot).

## What is in this folder

| Path | What it is |
|---|---|
| `index.html`, `big-group.html`, `small-group.html`, `founder.html` | The main site (yellow and navy style) |
| `assets/config.js` | Settings: relay address, bot name, email. The only file you edit to connect Telegram |
| `assets/trek.js` | Forms, mobile menu, departure picker |
| `img/` | Photos from the 2025 and 2026 treks |
| `styles/registan/` | Preview of the Registan gold and blue style (same pages) |
| `styles/campus/` | Preview of the crimson and silver campus style (same pages) |
| `styles/parallax/` | Preview of the parallax style |
| `logos/` | Logo options page and the SVG logo files |
| `worker/telegram-relay.js` | The Telegram relay you deploy on Cloudflare (step 3). It holds no secrets |
| `.nojekyll` | Tells GitHub Pages to serve the files as they are |

## 1. Publish on GitHub Pages

1. Create a new repository on GitHub, for example `uzbekistan-trek`. On a free GitHub account the repository must be **public** for Pages to work.
2. Upload everything in this folder to the repository root (drag the files into "Add file > Upload files", or use `git push`). If your computer hides the `.nojekyll` file, that is fine: the site works without it.
3. In the repository, open **Settings > Pages**. Under "Build and deployment", choose **Deploy from a branch**, branch **main**, folder **/ (root)**, then **Save**.
4. After a minute or two the site is live at `https://YOUR-USERNAME.github.io/uzbekistan-trek/`.
   The style previews are at `.../styles/registan/`, `.../styles/campus/`, `.../styles/parallax/` and the logo options at `.../logos/`.
5. Optional: to use your own domain, add it under **Settings > Pages > Custom domain** and follow GitHub's DNS instructions.

The site works right away. Until you finish steps 2 to 5 below, a submitted form shows the visitor their request with two buttons: copy it and open Telegram, or send it by email.

**Important:** a Telegram bot answers nobody on its own. Until the relay in steps 3 to 5 is running, messages people send to @uzbtrek_bot are not forwarded to you. Either finish the relay before you share the site, or rely on the email option for now.

## 2. Get your bot token and your chat ID

1. In Telegram, open [@BotFather](https://t.me/BotFather), send `/mybots`, choose **@uzbtrek_bot**, then **API Token**. Copy the token. Treat it like a password: never put it in the website, in GitHub, or in a chat.
2. From your personal Telegram account, open [@uzbtrek_bot](https://t.me/uzbtrek_bot), press **Start** and send any message, for example `hi`. A bot can only write to people who started it.
3. In a browser, open
   `https://api.telegram.org/botYOUR_TOKEN/getUpdates`
   (replace `YOUR_TOKEN`). Find `"chat":{"id":` followed by a number, for example `"chat":{"id":123456789`. That number is your **chat ID**.
   Do this before step 5: once a webhook is set, `getUpdates` stops working.

## 3. Deploy the relay on Cloudflare (free plan is enough)

1. Create a free account at [dash.cloudflare.com](https://dash.cloudflare.com).
2. Go to **Workers & Pages**, create a new Worker from the "Hello World" starter, name it `uzbtrek-relay`, and deploy it.
3. Click **Edit code**, delete the sample code, paste the whole content of `worker/telegram-relay.js`, and click **Deploy**.
4. Note the Worker address, for example `https://uzbtrek-relay.YOUR-ACCOUNT.workers.dev`. Opening it in a browser should show "Uzbekistan Trek relay is running."

## 4. Add the relay settings

In the Worker, open **Settings > Variables and Secrets** and add:

| Name | Type | Value |
|---|---|---|
| `BOT_TOKEN` | Secret | The token from step 2.1 |
| `ADMIN_CHAT_ID` | Text | Your chat ID from step 2.3 |
| `WEBHOOK_SECRET` | Secret | A long random string you make up. Only letters, digits, `_` and `-`, up to 256 characters, for example `uzbtrek_8f3K2q_77Lp` |
| `ALLOWED_ORIGINS` | Text | Your site address without a path, for example `https://YOUR-USERNAME.github.io`. Add a custom domain after a comma if you use one |
| `WELCOME_TEXT` | Text (optional) | The greeting visitors see after they press Start |

Deploy again if the dashboard asks you to.

## 5. Connect the bot and the website to the relay

1. Turn on two-way chat. In a browser, open this address (one line, with your values):
   `https://api.telegram.org/botYOUR_TOKEN/setWebhook?url=https://uzbtrek-relay.YOUR-ACCOUNT.workers.dev/telegram&secret_token=YOUR_WEBHOOK_SECRET`
   You should see `"ok":true` and "Webhook was set".
2. Connect the website forms. In `assets/config.js`, set
   `endpoint: "https://uzbtrek-relay.YOUR-ACCOUNT.workers.dev/submit",`
   then commit the change to GitHub. Pages republishes in a minute or two.
3. Test both:
   - Submit a form on the live site. The request arrives in your chat with @uzbtrek_bot.
   - Ask a friend to write to @uzbtrek_bot. Their message arrives in your chat, tagged with `#u` and a number.

## How to answer people

Everything arrives in your own chat with @uzbtrek_bot:

- **Website requests** arrive as a formatted message. Reply by email, or write to the person on Telegram if they left a handle.
- **Chat messages** arrive tagged `#u123456789`. To answer, **reply** to that message (swipe it, or right-click > Reply). The bot sends your reply to the visitor and confirms "Sent." Text, photos and files all work.
- If you write to the bot without replying to a tagged message, nothing is sent to anyone.

## Changing settings later

- **Email shown on the site:** edit `email` in `assets/config.js` (and the footer text in the HTML pages).
- **New bot token:** if the token ever leaks, revoke it in @BotFather, put the new one in `BOT_TOKEN`, and run the `setWebhook` link in step 5.1 again with the new token.
- **Turn off the chat relay:** open `https://api.telegram.org/botYOUR_TOKEN/deleteWebhook`.

## No-code alternative for the chat

If you prefer not to use Cloudflare for chat, [@LivegramBot](https://t.me/LivegramBot) can turn @uzbtrek_bot into a feedback bot that forwards messages to you. Two things to know:

- You give your bot token to a third-party service, and messages pass through their servers.
- Livegram sets its own webhook, so skip step 5.1. Steps 3, 4 and 5.2 still work for the website forms, because sending a message does not conflict with Livegram.

## Rules this site follows

- Every photo appears once per site; no photo repeats across pages.
- No prices are shown. Payment is described as three installments: a fixed first deposit, a fixed second deposit, then the remaining balance.
- The site states that Uzbekistan Trek is independent and not affiliated with any university.
