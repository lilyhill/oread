import requests

# Setting telegram webhook
u = "https://joel-plain-completely-hop.trycloudflare.com"

with open("keys.txt") as f:
    x = f.read()
    print(x)


url = f'https://api.telegram.org/bot{x}/pinChatMessage'

d = {
    "url": f'{u}/telegramCallback/',
    "chat_id":575182560,
    "message_id": 1123,
}

req = requests.post(url=url, data=d).json()

print(req)

