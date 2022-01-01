from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Url
import json
from .message.m import sendWelcomeAndPin
from icecream import ic
from datetime import date


@csrf_exempt
def telegram_callback(request):
    body = json.loads(request.body)

    print(body)
    if "pinned_message" not in body["message"]:
        try:
            b = Url.objects.all().filter(chat_id=body["message"]["chat"]["id"])
            if not b:
                sendWelcomeAndPin(cid=body["message"]["chat"]["id"])

            if "entities" in body["message"]:
                for i in body["message"]["entities"]:
                    if i["type"] == "url":
                        txt = body["message"]["text"]
                        url = txt[i["offset"]:i["offset"] + i["length"]]
                        u = Url(
                            message_id=body["message"]["message_id"],
                            from_id=body["message"]["from"]["id"],
                            chat_id=body["message"]["chat"]["id"],
                            url=url,
                        )
                        u.save()

        except KeyError as e:

            print(f'KeyError :{e}')

    return JsonResponse({'foo': 'bar'})

def collate_dates(qset):

    d = {}

    for i in qset:
        created_at = i.created_at
        str = date.isoformat(created_at)

        if str in d:
            d[str].append(i.url)
        else:
            d[str] = [i.url]

    return d

@csrf_exempt
def get_list(request, id):
    ctx ={}
    if request.method == 'GET':
        print(f'***{id}')
        qset = Url.objects.all().filter(chat_id=id)
        dates = collate_dates(qset)
        ctx["url_list"] = dates

    return render(request,"list.html", ctx)