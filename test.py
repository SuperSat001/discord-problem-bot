import requests
from discord import Webhook, RequestsWebhookAdapter
from notify_run import Notify

def send_notifs(message):

    try:
        url = "https://discord.com/api/webhooks/869201861306114048/rSr3tN34DtYk6kqhBxpaqlzQAxorgKtYTFHZigPORMcWBdEPOtLMgLZ8FT-bF51d5nay"
        webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
        webhook.send("<@550683461376278530> " + message)
        print("dc")
    except:
        print("dc fail")    

    try:
        notify = Notify()
        notify.send(message)
        print("notif")
    except:
        print("notif fail")

    try:
        token = "1839222250:AAGmtvL_BUx7HVASMDle1MzJkcxgE5PekcM"
        url = f"https://api.telegram.org/bot{token}"
        params = {"chat_id": "1330483834", "text": message}
        requests.get(url + "/sendMessage", params=params)
        print("tele")
    except:
        print("tele failed")

