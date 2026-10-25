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

#bot's code goes here

if __name__ == "__main__":
    print("Starting bot in Socket Mode...")
    SocketModeHandler(app, APP_TOKEN).start()
