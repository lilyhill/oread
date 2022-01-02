from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Url
import json
from .message.m import sendWelcomeAndPin, ackURL
from icecream import ic
from datetime import date
from .utils.db import saveURL, getURL
import datetime
import os


@csrf_exempt
def telegram_callback(request):
    body = json.loads(request.body)
    count = 0
    ic(body)
    d = datetime.datetime.fromtimestamp(body["message"]["date"])
    ic(date.isoformat(d))
    ic(str(d))
    if "pinned_message" not in body["message"]:
        try:
            b = list(Url.objects.all().filter(chat_id=body["message"]["chat"]["id"]))
            print(not b)
            print(b)
            if not b:
                sendWelcomeAndPin(cid=body["message"]["chat"]["id"])
                # Saving placeholder to bypass the invalid message 2nd time issue
                saveURL(
                    mid=body["message"]["message_id"],
                    fid=body["message"]["from"]["id"],
                    cid=body["message"]["chat"]["id"],
                    url=None,
                    cat=datetime.datetime.fromtimestamp(body["message"]["date"])
                )

            if "entities" in body["message"] and "reply_to_message" not in body["message"]:
                for i in body["message"]["entities"]:
                    if i["type"] == "url":
                        txt = body["message"]["text"]
                        url = txt[i["offset"]:i["offset"] + i["length"]]
                        count += saveURL(
                            mid=body["message"]["message_id"],
                            fid=body["message"]["from"]["id"],
                            cid=body["message"]["chat"]["id"],
                            url=url,
                            cat=datetime.datetime.fromtimestamp(body["message"]["date"])
                        )
                if count:
                    ackURL(mid=body["message"]["message_id"], cid=body["message"]["chat"]["id"])

            elif "reply_to_message" in body["message"]:
                ic("reply_to_message")
                qset = list(getURL(
                    mid=body["message"]["reply_to_message"]["message_id"],
                    fid=body["message"]["reply_to_message"]["from"]["id"],
                    cid=body["message"]["reply_to_message"]["chat"]["id"],
                ))
                ic(
                    body["message"]["reply_to_message"]["message_id"],
                    body["message"]["reply_to_message"]["from"]["id"],
                    body["message"]["reply_to_message"]["chat"]["id"],
                )
                ic(qset)

                if qset:
                    qset = qset[0]
                    ic(qset.url)






        except KeyError as e:

            print(f'KeyError :{e}')

        except Exception as e:
            print(f'Some exception occured :{e}')

    return JsonResponse({'foo': 'bar'})


def collate_dates(qset):

    d = {}

    for i in qset:
        created_at = i.created_at
        ic(created_at)
        current_datetime = datetime.datetime.now()
        ic(str(created_at))
        ic(str(current_datetime))
        ic(os.environ['TZ'])
        stri = date.isoformat(created_at)

        if stri in d and i.url != "None":
            d[stri].append(i.url)
        else:
            d[stri] = [i.url]

    return d


@csrf_exempt
def get_list(request, id):
    ctx ={}
    if request.method == 'GET':
        print(f'***{id}')
        qset = Url.objects.all().filter(chat_id=id, url__isnull=False)

        dates = collate_dates(qset)
        ctx["url_list"] = dates
        ic(ctx)
    return render(request,"list.html", ctx)