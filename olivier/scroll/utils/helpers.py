import json

from ..message.m import *
from .db import *


def handle_reply(message):
    ic('^^^^^^^^^^^^ handle_reply')
    try:

        msg = get_telegram_msg(
            cid=message["chat"]["id"],
            fid=message["from"]["id"],
            mid=message["reply_to_message"]["message_id"],
        )

        t = TelegramData.objects.get(
            primary_msg=msg
        )
        t.sub_text += '<li>' +message["text"] + f'</li>'

        t.save()

        ic(t.sub_text)
        ackURL(mid=message["message_id"], cid=message["chat"]["id"])

    except Exception as e:
        print("error occurred",e)

    return 0


def handle_message(message):
    ic("handle_message")
    try:
        user = TelegramUser.objects.get(
            cid=message["chat"]["id"],
            fid=message["from"]["id"],
        )

    except TelegramUser.DoesNotExist as e:
        ic(e)
        user = create_telegram_user(message)


    msg = TelegramMessage(
        user=user,
        mid=message["message_id"],
        reply_to=None,
        msg_type="message",
        text=message["text"],
        msg_body=json.dumps(message),
        sent_at=datetime.datetime.fromtimestamp(message["date"]),
    )
    msg.save()

    d = TelegramData(
        primary_msg=msg,
        text=message["text"],
        sub_text="",
        created_at=datetime.datetime.fromtimestamp(message["date"]),
    )

    d.save()
    ackURL(mid=message["message_id"], cid=message["chat"]["id"])
    return 0


def create_telegram_user(message):
    ic('create_telegram_user')
    try:
        u = User(
            name="",
            username=str(message["chat"]["id"]),
        )
        u.save()
        t = TelegramUser(
            user=u,
            cid=message["chat"]["id"],
            fid=message["from"]["id"]
        )

        t.save()

        sendWelcomeAndPin(cid=message["chat"]["id"])

    except Exception as e:
        ic("create_telegram_user ", e)

    return t