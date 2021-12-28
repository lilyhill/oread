import requests

# Setting telegram webhook
u = "https://lack-ids-forecasts-either.trycloudflare.com"

with open("keys.txt") as f:
    x = f.read()
    print(x)


url = f'https://api.telegram.org/bot{x}/setWebhook'

d = {
    "url": f'{u}/telegramCallback/'
}

req = requests.post(url=url, data=d).json()

print(req)

