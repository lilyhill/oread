import os
import requests

def getMsgUrl():
    t_key = os.environ.get("TELEGRAM_KEY")
    url = f'https://api.telegram.org/bot{t_key}/sendMessage'

    return url

def getPinUrl():
    t_key = os.environ.get("TELEGRAM_KEY")
    url = f'https://api.telegram.org/bot{t_key}/pinChatMessage'

    return url

def sendWelcome(cid, ):

    my_url = os.environ.get("BASE_URL")

    d = {
        "chat_id": cid,
        "text": f'Hi! You can view your collated URls at http://{my_url}/l/{cid}'
    }


    res = requests.post(url=getMsgUrl(), data=d)

    return res.json()

def sendWelcomeAndPin(cid):

    r = sendWelcome(cid)
    print(f'$$${r}')
    if r["ok"]:
        d = {
            "chat_id": cid,
            "message_id": r["result"]["message_id"],
            "disable_notification": True
        }
        print(f'd, {d}')
        res = requests.post(url=getPinUrl(), data=d)
        print(f'%% {res.json()}')