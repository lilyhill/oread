import os

import requests

# Setting telegram webhook
u = os.environ.get("BASE_URL")
x = os.environ.get("TELEGRAM_KEY")


url = f'https://api.telegram.org/bot{x}/setWebhook'
print(url)

d = {
    "url": f'https://{u}/telegramCallback/',
}
print(d)

req = requests.post(url=url, data=d).json()

print(req)

