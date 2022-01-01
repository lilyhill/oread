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
            b = list(Url.objects.all().filter(chat_id=body["message"]["chat"]["id"]))
            print(not b)
            print(b)
            if not b:
                sendWelcomeAndPin(cid=body["message"]["chat"]["id"])
                u = Url(
                    message_id=body["message"]["message_id"],
                    from_id=body["message"]["from"]["id"],
                    chat_id=body["message"]["chat"]["id"],
                    url=None
                )
                print(u.save())

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

        except Exception as e:
            print(f'Some exception occured :{e}')

    return JsonResponse({'foo': 'bar'})

def collate_dates(qset):

    d = {}

    for i in qset:
        created_at = i.created_at
        str = date.isoformat(created_at)

        if str in d and i.url != "None":
            d[str].append(i.url)
        else:
            d[str] = [i.url]

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