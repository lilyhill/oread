from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
import json
from .message.m import ackURL
from icecream import ic
from datetime import date
from .utils.db import *
import datetime
import os
from .utils.helpers import *
import sqlite3
from datetime import datetime
import pytz
import time




@csrf_exempt
def telegram_callback(request):
    body = json.loads(request.body)
    ic(body)
    avoid = ["reply_to_message", "pinned_message"]
    if "message" in body and all(key in body["message"] for key in avoid):
        message = body["message"]

        ic(any(key in body["message"] for key in ["reply_to_message", "pinned_message"]))

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

    elif "reply_to_message" in body["message"]:

        handle_reply(body["message"])

    return JsonResponse({'foo': 'bar'})


def collate_dates(qset):

    d = {}

    for i in qset:
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


def create_message(mid, fid, cid, created, data):
    local = pytz.timezone("Asia/Kolkata")
    naive = datetime.strptime(created, "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    ic(utc_dt)
    x = int(time.mktime(utc_dt.timetuple()))
    ic(x)
    ic(datetime.fromtimestamp(x))
    ic(mid,fid,cid, created, data)
    return {"message": {"chat": {"first_name": "Suriya",
                                 "id": cid,
                                 "type": "private",
                                 "username": "SuriyaGanesh"},
              "date": x,
              "from": {"first_name": "Suriya",
                       "id": fid,
                       "is_bot": False,
                       "language_code": "en",
                       "username": "SuriyaGanesh"},
              "message_id": mid,
              "text": data},
  "update_id": 326096742 }


def m(request):

    server = sqlite3.connect('scroll/db.sqlite3')
    local = sqlite3.connect('db.sqlite3')
    cur = server.execute("PRAGMA database_list;")
    print(cur.fetchone())
    cur = server.execute("SELECT * FROM scroll_url")

    for i in cur.fetchall():

        ic(i)
        msg = create_message(i[1], i[2], i[3], i[4], i[5])
        ic(msg)

        handle_message(msg["message"])

    return JsonResponse({})