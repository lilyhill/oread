from ..models import *
from icecream import ic
import datetime


def saveURL(mid, fid, cid, url, cat):
    # try:
    #     u = Url(
    #         message_id=mid,
    #         from_id=fid,
    #         chat_id=cid,
    #         url=url,
    #         created_at = cat
    #     )
    #     u.save()
    # except Exception as e:
    #     return e

    return 1


def getURL(mid, fid, cid):

    # try:
    #     u = Url.objects.all().filter(
    #         message_id = mid,
    #         from_id = fid,
    #         chat_id = cid
    #     )
    #
    # except Exception as e:
    #     return e

    return 0


def saveMessage(body):
    ic(body)
    chat = body["message"]["chat"]
    message = body["message"]
    # try:
    #     m = Messages(
    #         message_id=message["message_id"],
    #         from_id=message["from"]["id"],
    #         chat_id=chat["id"],
    #
    #         msg_type="reply_to_message",
    #         reply_to=None,
    #         text=message["text"],
    #         msg_body=body,
    #         sent_at=datetime.datetime.fromtimestamp(message["date"])
    #     )
    #     m.save()
    #
    #     l = Messages.objects.all().filter(
    #         message_id=message["message_id"]
    #     )
    #     ic(l)
    # except Exception as e:
    #     ic(e)

    return 0


def saveReplyTo(body):

    # chat = body["message"]["chat"]
    # message = body["message"]
    #
    # prev = Messages.objects.all().filter(
    #     message_id=message["reply_to_message"]["message_id"],
    #     from_id=message["reply_to_message"]["from"]["id"],
    #     chat_id=message["reply_to_message"]["chat"]["id"]
    # )
    #
    # try:
    #     ic(chat)
    #     m = Messages(
    #         message_id=message["message_id"],
    #         from_id=message["from"]["id"],
    #         chat_id=chat["id"],
    #
    #         msg_type="reply_to_message",
    #         reply_to=prev[0] if list(prev) else None,
    #         text=message["text"],
    #         msg_body=body,
    #         sent_at=datetime.datetime.fromtimestamp(message["date"])
    #     )
    #     ic(m.save())
    # except Exception as e:
    #     ic("Error occured while writing reply", e)

    return 0


def get_telegram_msg(fid,cid,mid):
    user = TelegramUser.objects.get(
        cid=cid,
        fid=fid,
    )

    msg = TelegramMessage.objects.get(
        user=user,
        mid=mid,
    )


    return msg