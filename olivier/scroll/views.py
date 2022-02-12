from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from datetime import date

from .utils.helpers import *
import sqlite3
from datetime import datetime, time
import pytz
import time

my_url = os.environ.get("BASE_URL")

@csrf_exempt
def telegram_callback(request):
    body = json.loads(request.body)
    ic(body)
    avoid = ["reply_to_message", "pinned_message"]
    # ic(any(key not in body["message"] for key in ["reply_to_message", "pinned_message"]))
    if "message" in body and all(key not in body["message"] for key in avoid):
        message = body["message"]


        try:
            ic("****")
            if "reply_to_message" not in message and "pinned_message" not in message:
                handle_message(message)

        except KeyError as e:

            print(f'KeyError :{e}')

        except Exception as e:
            print(f'Some exception occured :{e}')

    elif "edited_message" in body:

        print(0)

    elif "message" in body and "reply_to_message" in body["message"]:

        handle_reply(body["message"])
    else:
        ic(body)

    return JsonResponse({'foo': 'bar'})


def collate_dates(qset):

    d = {}

    for i in qset:
        if i.created_at:
            created_at = i.created_at
            stri = date.isoformat(created_at)
            o = {
                "text":i.text,
                "sub_text":i.sub_text
            }
            if stri in d:
                d[stri].append(o)
            else:
                d[stri] = [o]
        else:
            o = {
                "text": i.text,
                "sub_text": i.sub_text
            }
            if "none" not in d:
                d["none"]= [0]
            else:
                d["none"].append(o)

    return d


@csrf_exempt
def get_list(request, username):
    ctx ={}
    if request.method == 'GET':

        try:

            td = list(TelegramData.objects.filter(
                primary_msg__user__user__username=username
            ))

            ctx["url_list"] = collate_dates(td)
            ic(ctx)

        except Exception as e:
            ic('get_list :', e)

    return render(request,"list.html", ctx)


@csrf_exempt
def get_username(request):

    body = json.loads(request.body)
    ic(body)
    response = JsonResponse({"Success": True})
    uname = body["username"]
    obj, created = ExtensionUser.objects.get_or_create(
        uname = uname
    )

    ic(created)

    d = {
        "url": f'https://{my_url}/e/{uname}'
    }
    return JsonResponse(d)

@csrf_exempt
def get_e_list(request, username):

    ctx ={}
    if request.method == 'GET':

        try:

            ed = list(ExtensionData.objects.filter(
                user__uname=username
            ))

            ctx["url_list"] = collate_dates(ed)
            ic(ctx)

        except Exception as e:
            ic('get_e_list :', e)

    return render(request, "list.html", ctx)


@csrf_exempt
def save_e_value(request):


    try:
        body = json.loads(request.body)
        eu = list(ExtensionUser.objects.filter(
            uname = body["username"]
        ))
        if eu:

            today = date.today()
            edl = list(ExtensionData.objects.filter(
                user = eu[0],
                text = body["url"],
                created_at__year=today.year,
                created_at__month=today.month,
                created_at__day=today.day,

            ))
            if edl:
                ed = edl[0]
                ed.sub_text += f'<li>{body["selection"]}</li>'
                ed.save()
            else:
                ed = ExtensionData.objects.create(
                    user=eu[0],
                    text = body["url"],
                    sub_text = f'<li>{body["selection"]}</li>',
                    created_at =datetime.now()
                )
                ed.save()

    except Exception as e:
        ic(e)
        ic(request.body)

    return JsonResponse({"success": True})