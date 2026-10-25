import os, re, sys, requests

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

if not BOT_TOKEN or not APP_TOKEN:
    sys.exit("Missing SLACK_BOT_TOKEN or SLACK_APP_TOKEN, copy .env.example to .env and fill them in")

app = App(token=BOT_TOKEN)

# These only work when "Escape channels, users, and links sent to your app" is ticked on the command
pattern_member = r"<@([^|>]+)(?:\|[^>]+)?>"   # <@U123|name> or <@U123>  -> group(1) = user id
pattern_channel = r"<#([^|>]+)(?:\|[^>]*)?>"  # <#C123|name> or <#C123>  -> group(1) = channel id


@app.command("/mybot")
def main_command(ack, respond, command):
    ack()
    text = command.get("text", "").strip()
    print(f"/mybot ran with: {text!r}")

    if text == "help":
        respond(
            "Heyo :wave:, here is what you can run:\n"
            "- `/mybot help` - show this message\n"
            "- `/mybot ping` - check the bot is alive\n"
            "- `/mybot user @someone` - example user mention parsing\n"
            "- `/mybot channel #somewhere` - example channel mention parsing"
        )
    elif text == "ping":
        respond("pong :ping_pong:")
    elif text.startswith("user"):
        match = re.fullmatch(pattern_member, text[len("user"):].strip())
        if not match:
            respond(f"You need to @-mention exactly one user, you ran `/mybot {text}`")
            return
        respond(f"Got <@{match.group(1)}> (id: `{match.group(1)}`)")
    elif text.startswith("channel"):
        match = re.fullmatch(pattern_channel, text[len("channel"):].strip())
        if not match:
            respond(f"You need to #-mention a channel, you ran `/mybot {text}`")
            return
        respond(f"Got <#{match.group(1)}> (id: `{match.group(1)}`)")
    else:
        respond("Sorry, I didn't get that, try `/mybot help`")


# Template for commands that call an external API, copy and rename
def call_api(url):
    """Returns parsed JSON, or raises with a user-friendly message."""
    try:
        r = requests.get(url, headers={"accept": "application/json"}, timeout=10)
    except requests.exceptions.RequestException:
        raise RuntimeError("Could not connect to the API :sob:")
    if r.status_code != 200:
        print(f"API error: {r.status_code}")
        raise RuntimeError(f"API error ({r.status_code}). idk what happened.")
    return r.json()


@app.event("app_mention")
def on_mention(event, say):
    say(f"Hey <@{event['user']}>! Try `/mybot help`", thread_ts=event.get("ts"))


if __name__ == "__main__":
    print("Starting bot in Socket Mode...")
    SocketModeHandler(app, APP_TOKEN).start()
