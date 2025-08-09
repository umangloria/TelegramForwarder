![img](images/logo/png/logo-title.png)

<h3><div align="center">Telegram Forwarder</div>

---

<div align="center">

[![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=white)][docker-url] [![License: GPL-3.0](https://img.shields.io/badge/License-GPL%203.0-4CAF50?style=flat-square)](https://github.com/Heavrnl/TelegramForwarder/blob/main/LICENSE)

[docker-url]: https://hub.docker.com/r/heavrnl/telegramforwarder

</div>

## 📖 Overview
Telegram Forwarder is a powerful forwarding and filtering tool for Telegram. If your account has joined the source channels/groups, it can read and process their messages and send the processed output to another chat. The bot does not need to be in the source chat. It’s great for information aggregation, notifications, and content curation.

With Apprise integration, you can push messages to many platforms (apps, email, SMS, webhooks, etc.). It also includes optional AI processing and an RSS dashboard to expose selected content as RSS feeds.

## ✨ Features
- Multi-source forwarding to multiple targets
- Keyword filtering (whitelist/blacklist)
- Regex support
- Content replacement/transform rules
- AI processing (OpenAI, Claude, Gemini, etc.)
- Media filtering (types, size, extensions)
- RSS generation and web dashboard
- Push to many platforms via Apprise

## 📋 Table of contents
- [📖 Overview](#-overview)
- [✨ Features](#-features)
- [🚀 Quick start](#-quick-start)
  - [1️⃣ Prerequisites](#1️⃣-prerequisites)
  - [2️⃣ Configure](#2️⃣-configure)
  - [3️⃣ Run](#3️⃣-run)
  - [4️⃣ Update](#4️⃣-update)
- [📚 Usage guide](#-usage-guide)
  - [🌟 Basic example](#-basic-example)
  - [🔧 Special cases](#-special-cases)
- [🛠️ Details](#️-details)
  - [⚡ Filter flow](#-filter-flow)
  - [⚙️ Settings](#️-settings)
  - [🤖 AI](#-ai)
  - [📢 Push](#-push)
  - [📰 RSS](#-rss)
- [🎯 Extras](#-extras)
- [📝 Commands](#-commands)
- [💐 Thanks](#-thanks)
- [☕ Donate](#-donate)
- [📄 License](#-license)

## 🚀 Quick start

### 1️⃣ Prerequisites
1) Get Telegram API credentials:
- Visit `https://my.telegram.org/apps`
- Create an app to obtain `API_ID` and `API_HASH`

2) Create a bot and get token:
- Talk to `@BotFather`
- Obtain `BOT_TOKEN`

3) Get your own numeric user id:
- Talk to `@userinfobot` → `USER_ID`

### 2️⃣ Configure
Create a working directory and `cd` into it:

```bash
mkdir ./TelegramForwarder && cd ./TelegramForwarder
```

Create an `.env` file with at least the following (example):

```ini
API_ID=123456
API_HASH=your_api_hash
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
PHONE_NUMBER=+11234567890
USER_ID=123456789

# Optional
ADMINS=123456789
DEFAULT_TIMEZONE=Asia/Shanghai

# RSS (optional)
RSS_ENABLED=false
RSS_HOST=0.0.0.0
RSS_PORT=8000

# AI (optional)
OPENAI_API_KEY=
CLAUDE_API_KEY=
GEMINI_API_KEY=
```

If you prefer using the upstream example env file, you can download it and adapt as needed:

```bash
wget https://raw.githubusercontent.com/Heavrnl/TelegramForwarder/refs/heads/main/.env.example -O .env
```

### 3️⃣ Run

First-time run (interactive login required for the user client):

```bash
docker compose run --rm -it telegram-forwarder
```

- Follow the prompts to log in with your `PHONE_NUMBER`.
- After success, press Ctrl+C to exit (your session is saved under `./sessions`).

Then start in the background:

```bash
docker compose up -d
```

If you use the classic v1 CLI, replace `docker compose` with `docker-compose`.

Enable RSS dashboard (optional):
- Set `RSS_ENABLED=true` in `.env`
- Expose the port in `docker-compose.yml` (uncomment `9804:8000`)
- Restart: `docker compose restart`

Visit: `http://localhost:9804/`

### 4️⃣ Update
If you are using the prebuilt image from Docker Hub, you usually do not need source code. To update the running service:

```bash
docker compose down
docker compose pull
docker compose up -d
```

If you build from source locally, use:

```bash
docker compose up -d --build
```

## 📚 Usage guide

### 🌟 Basic example
Assume you follow a few channels (e.g., `https://t.me/tgnews`, `https://t.me/tgread`) but want to filter noise:

1) Create a Telegram group/channel (e.g., "My TG Filter")
2) Add your bot to that group/channel and grant admin rights
3) In the new group/channel, send:

```bash
/bind https://t.me/tgnews
/bind https://t.me/tgread
```

4) Open settings to choose handling mode and filters:

```bash
/settings
```

Select the rule for the desired source, then configure to taste.

5) Add block keywords:

```bash
/add ad promo 'this is ad'
```

6) If forwarded formatting looks off (e.g., stray symbols), use regex replace:

```bash
/replace \*\*
```

This removes all `**` in messages.

Tip: By default, keyword/replace operations apply to the first bound rule. To manage a different bound rule, use `/settings`, select that rule, then apply operations. Use `/add_all` or `/replace_all` to apply to all rules at once.

### 🔧 Special cases

#### 1) Channels that embed links and require confirmation (e.g., NodeSeek)
Original message format:

```markdown
[**Post Title**](https://www.nodeseek.com/post-xxxx-1)
```

Recommended replace sequence for your notification rule:

```plaintext
/replace \*\*
/replace \[(?:\[([^\]]+)\])?([^\]]+)\]\(([^)]+)\) [\1]\2\n(\3)
/replace \[\]\s*
```

All forwarded messages become:

```plaintext
Post Title
(https://www.nodeseek.com/post-xxxx-1)
```

#### 2) Make user messages prettier

```plaintext
/r ^(?=.) <blockquote>
/r (?<=.)(?=$) </blockquote>
```

Then set message format to HTML in settings. User messages will render more nicely.

#### 3) Sync rule operations
Enable "Sync to other rules" in the Settings menu and pick a target rule. All operations in the current rule are mirrored to the selected target(s). If the current rule is only for syncing, you can disable it via "Enable rule: off".

#### 4) Forward to Saved Messages
Not recommended because it takes more steps, but it’s possible. In short: create a helper rule, enable sync to a dedicated Saved Messages rule, set Forward mode to User, and disable the helper rule. Then manage from other rules; changes sync to Saved Messages.

## 🛠️ Details

### ⚡ Filter flow
Understand the filtering order (the labels correspond to Settings names):

![img](./images/flow_chart.png)

### ⚙️ Settings
Screenshots: main, AI, and media settings

| Main | AI | Media |
|---------|------|------|
| ![img](./images/settings_main.png) | ![img](./images/settings_ai.png) | ![img](./images/settings_media.png) |

Key options (high-level):
- Apply current rule: subsequent keyword/replace operations (add/remove/list/import/export) apply to this rule
- Enable rule: turn rule on/off
- Current keyword add mode: toggle blacklist/whitelist; ensure it matches your intended operations
- Include sender name/ID in keyword filtering context (not added to the outgoing message) to target specific users
- Process mode: Edit or Forward. Edit modifies original message; Forward sends processed text to targets. Edit requires admin rights and applicable message types
- Filter mode: Only blacklist / Only whitelist / Black then white / White then black
- Forward mode: User or Bot (use account or bot to send)
- Replace mode: process message through your replace rules before sending
- Message format: Markdown/HTML for final rendering
- Preview mode: On/Off/Follow original
- Original sender / original link / send time: append metadata to the output (templates configurable under Other Settings)
- Delayed processing: re-fetch content after a delay before processing (for channels that often edit posts). Times configurable via `config/delay_time.txt`
- Delete original message: requires permission
- Jump-to-comments button: add a button under forwarded messages when source has comments
- Sync to other rules: mirror settings and operations to the selected rules (except enable/sync toggles)

Media settings:
- Media type filter: block unselected types
- Selected media types: choose which types to block (Telegram types include photo, document, video, audio, voice; many files fall under "document")
- Media size filter and limit (MB). Custom sizes in `config/media_size.txt`
- Notify when media exceeds limit
- Media extensions filter with blacklist/whitelist mode. Custom list in `config/media_extensions.txt`
- Allow text-only pass-through: forward text even when media is blocked

Other settings:
- Copy rule, copy keywords, copy replace rules
- Clear keywords, clear replace rules, delete rule (can target other rules)
- Custom templates: user info, time, original link
- Inversion toggles for blacklist/whitelist to build two-layer filters

### 🤖 AI

What AI can do:
- Translate content
- Daily summaries of group/channel messages
- Smart ad filtering
- Auto-tagging

Configure in `.env`:

```ini
# OpenAI
OPENAI_API_KEY=your_key
OPENAI_API_BASE=

# Claude
CLAUDE_API_KEY=your_key
CLAUDE_API_BASE=

# Gemini
GEMINI_API_KEY=your_key
GEMINI_API_BASE=
```

Custom models: add entries to `config/ai_models.json`.

Prompt helpers available in AI prompts:
- `{source_message_context:N}` – last N messages from source chat
- `{target_message_context:N}` – last N messages from target chat
- `{source_message_time:MIN}` – messages from last MIN minutes in source
- `{target_message_time:MIN}` – messages from last MIN minutes in target

Example prompt (deduplicate news):
```
This channel aggregates news from multiple sources. Judge whether the new post duplicates prior content. If duplicate, reply "#do_not_forward" only. Otherwise, return the original new post, preserving its format.
History:
{target_message_context:10}
New post:
```

Scheduled summary:
- Set one or more times in `config/summary_time.txt` (default 07:00)
- Set default timezone in `.env`
- Customize the summary prompt as needed

### 📢 Push

Powered by Apprise. You can push to hundreds of services.

- Main and sub-settings are available in the Push settings page in the bot
- Modes: send media as single messages or merge media into one, depending on destination support

How to add push configs: refer to the Apprise Wiki (`https://github.com/caronc/apprise/wiki`). Example (ntfy.sh):

```
ntfy://ntfy.sh/my_topic
```

## 📰 RSS
The project can convert Telegram messages into RSS feeds and provides a small dashboard.

Enable RSS:
1) In `.env`:

```ini
RSS_ENABLED=true
RSS_BASE_URL=
RSS_MEDIA_BASE_URL=
```

2) Expose the port (compose):

```yaml
ports:
  - "9804:8000"
```

3) Restart:

```bash
docker compose restart
```

Dashboard: `http://localhost:9804/`

Nginx example:
```
location / {
  proxy_pass http://127.0.0.1:9804;
  proxy_http_version 1.1;
  proxy_set_header Upgrade $http_upgrade;
  proxy_set_header Connection "upgrade";
  proxy_set_header Host $host;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto $scheme;
  proxy_set_header X-Forwarded-Host $host;
}
```

RSS UI previews:

| Login | Dashboard | Create/Edit |
|---------|------|------|
| ![img](./images/rss_login.png) | ![img](./images/rss_dashboard.png) | ![img](./images/rss_create_config.png) |

Create/Edit form highlights:
- Rule ID: choose an existing forward rule as the source for this feed
- Copy from: clone settings from an existing RSS config
- Title/Description/Language
- Max items: default 50 (increase cautiously for media-heavy sources)
- Use AI to extract title/content: uses your AI provider and ignores other content rules below
- AI extraction prompt: must return JSON like `{ "title": "...", "content": "..." }`
- Auto-extract title/content: use pre-defined regex patterns
- Auto-convert Markdown to HTML: convert Telegram Markdown to HTML automatically
- Enable custom title/content regex and define priority (smaller number = higher priority). Results from a higher-priority regex become the input to the next one
- Regex tester to validate your patterns

Notes:
- If only title extraction is enabled (no content extraction), the content becomes the full Telegram message containing the extracted title
- If no content processing/regex is set, the first ~20 characters are used as title and the raw message as content
- If `RSS_ENABLED=true` in `.env`, the bot adds a setting "Forward to RSS only". When enabled, processing stops after the RSS filter and does not forward/edit to chats
- There is no password recovery in the RSS dashboard; store credentials safely

## 🎯 Extras

### 🔗 Quick-forward by link
Send a message link to the bot and it forwards that specific message to the current chat, ignoring forward/copy restrictions.

### 🔄 Integration with Universal Forum Block (UFB)
Project: `https://github.com/heavrnl/universalforumblock`

- Configure UFB entries in `.env`
- In a bound chat, run `/ufb_bind <domain>` to enable 3-way sync
- Use `/ufb_item_change` to switch synced type (home keywords/home usernames/content keywords/content usernames)

## 📝 Commands

```bash
Basic
/start - Start
/help (/h) - Show help

Bind & Settings
/bind (/b) <source link or title> [target link or title] - Bind a source chat
/settings (/s) [rule_id] - Manage forward rules
/changelog (/cl) - Show changelog

Rules
/copy_rule (/cr) <source_rule_id> [target_rule_id] - Copy all settings to current or target rule
/delete_rule (/dr) <rule_id> [rule_id] ... - Delete specified rules
/list_rule (/lr) - List all rules

Keywords
/add (/a) <keyword> [keyword] ['key word'] ["key word"] ... - Add plain keywords
/add_regex (/ar) <regex> [regex] ... - Add regex keywords
/add_all (/aa) <keyword> [keyword] ... - Add plain keywords to all rules bound to current channel
/add_regex_all (/ara) <regex> [regex] ... - Add regex keywords to all rules
/list_keyword (/lk) - List all keywords
/remove_keyword (/rk) <keyword> ['key word'] ["key word"] ... - Remove keywords
/remove_keyword_by_id (/rkbi) <id> [id] ... - Remove keywords by ID
/remove_all_keyword (/rak) <keyword> ['key word'] ["key word"] ... - Remove keywords from all rules bound to current channel
/clear_all_keywords (/cak) - Clear all plain keywords in current rule
/clear_all_keywords_regex (/cakr) - Clear all regex keywords in current rule
/copy_keywords (/ck) <rule_id> - Copy keywords from another rule
/copy_keywords_regex (/ckr) <rule_id> - Copy regex keywords from another rule

Replace rules
/replace (/r) <regex> [replacement] - Add a replace rule
/replace_all (/ra) <regex> [replacement] - Add a replace rule to all rules
/list_replace (/lrp) - List replace rules
/remove_replace (/rr) <index> - Remove a replace rule by index
/clear_all_replace (/car) - Clear all replace rules in current rule
/copy_replace (/crp) <rule_id> - Copy replace rules from another rule

Import/Export
/export_keyword (/ek) - Export keywords of current rule
/export_replace (/er) - Export replace rules of current rule
/import_keyword (/ik) <attach file> - Import plain keywords from a file
/import_regex_keyword (/irk) <attach file> - Import regex keywords from a file
/import_replace (/ir) <attach file> - Import replace rules from a file

RSS
/delete_rss_user (/dru) [username] - Delete an RSS user

UFB
/ufb_bind (/ub) <domain> - Bind UFB domain
/ufb_unbind (/uu) - Unbind UFB domain
/ufb_item_change (/uic) - Switch UFB sync item type

Hints
• Text in parentheses are short aliases
• <> required, [] optional
• Import commands require sending a file
```

## 💐 Thanks
- [Apprise](https://github.com/caronc/apprise)
- [Telethon](https://github.com/LonamiWebs/Telethon)

## ☕ Donate
If this project helps you, consider buying the author a coffee:

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/0heavrnl)

## 📄 License
This project is licensed under [GPL-3.0](LICENSE). See the [LICENSE](LICENSE) file for details.


