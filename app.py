import os, re, sys, subprocess, platform

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SERVER = os.getenv("SERVER_IP")


if not BOT_TOKEN or not APP_TOKEN:
    sys.exit("Missing SLACK_BOT_TOKEN or SLACK_APP_TOKEN, copy .env.example to .env and fill them in")

app = App(token=BOT_TOKEN)

def ping_host(ip):
    count_flag = '-n' if platform.system() == 'Windows' else '-c'
    result = subprocess.run(
        ['ping', count_flag, '4', ip],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return result.returncode == 0

@app.command("/server")
def main_command(ack, respond, command):
    ack()
    text = command.get("text", "").strip()

    if text == "ping":
        print("someone pinged us")
        respond("Well *I'm* awake, checking your server now! :beachball:")
        if ping_host(SERVER):
            print(f"{SERVER} is reachable")
            respond("Your server is ALIVE!!! ")
        else:
            print(f"{SERVER} is not reachable")
            respond("Sorry to break it to you, ya server isn't showing up on my sweep! You should take a look at that.")

@app.event("app_mention")
def on_mention(event, respond, client):
    client.reactions_add(channel=event["channel"], timestamp=event["ts"], name="no-no")
    respond("sorry, you can't do that!")
    print("someone pinged us, i delt with it!")

if __name__ == "__main__":
    print("Starting bot in Socket Mode...")
    SocketModeHandler(app, APP_TOKEN).start()
