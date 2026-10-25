# MyBot

What this bot does, in a sentence or two.

## Commands / Features

- `/mybot help` - list commands
- `/mybot ping` - check the bot is alive

## Tech Stack

Slack Bolt for Python, using Socket Mode.

## Self Host

1. Clone the repo and navigate into the folder

```
git clone https://github.com/hippogriff101/REPO_NAME
cd REPO_NAME
```

2. Create a virtual environment and install dependencies

```
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate.bat

pip install -r requirements.txt
```

3. Copy `.env.example` to `.env`

```
cp .env.example .env
```

4. Set up the Slack App

- Go to [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **From a manifest**, and paste in `manifest.json` (rename the bot and command first)
- Under **Basic Information → App-Level Tokens**, create a token with `connections:write` and put it in `SLACK_APP_TOKEN`
- Install to the workspace and put the **Bot User OAuth Token** in `SLACK_BOT_TOKEN`

_On the Hack Club Slack, give commands unique names so they don't clash with other bots._

5. Add the bot to a channel and start it

```
python app.py
```

Slack recommends HTTP mode rather than Socket Mode for production; this bot only supports Socket Mode for now.

## AI Transparency

Describe how AI was used here.
