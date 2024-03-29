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
        "text": f'Hi! I\'m oread, I can manage Urls for you.\nYou can find the featurelist here https://github.com/suriya-ganesh/oread#features.'
    }

    res = requests.post(url=getMsgUrl(), data=d)

    d = {
        "chat_id": cid,
        "text": f'The collated URLs at https://{my_url}/l/{cid}',
        "url": f'https://{my_url}/l/{cid}'
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


def ackURL(cid, mid):

    d = {
        "chat_id": cid,
        "text": f'noted ✅',
        "reply_to_message_id": mid
    }

    res = requests.post(url=getMsgUrl(), data=d)

    return res.json()