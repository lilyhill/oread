from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from datetime import date
import random
from .utils.helpers import *
from .forms import *

my_url = os.environ.get("BASE_URL")


@csrf_exempt
def telegram_callback(request):
    body = json.loads(request.body)
    avoid = ["reply_to_message", "pinned_message"]
    # ic(any(key not in body["message"] for key in ["reply_to_message", "pinned_message"]))
    if "message" in body and all(key not in body["message"] for key in avoid):
        message = body["message"]

        try:
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
        pass

    return JsonResponse({'foo': 'bar'})


def collate_dates(qset):
    d = {}

    for i in qset:
        if i.created_at:
            created_at = i.created_at
            stri = date.isoformat(created_at)
            o = {
                "text": i.text,
                "sub_text": i.sub_text
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
                d["none"] = [o]
            else:
                d["none"].append(o)

    return d


@csrf_exempt
def get_list(request, username):
    ctx = {}
    if request.method == 'GET':

        try:

            td = list(TelegramData.objects.filter(
                primary_msg__user__user__username=username
            ))[::-1]

            ctx["url_list"] = collate_dates(td)

        except Exception as e:
            pass

    return render(request, "list.html", ctx)


def collate_data(data):
    res = {}

    for i in data:
        d = date.isoformat(i.created_at)
        if d in res:
            res[d][d.edata.href].append(d.text)
        else:
            res[d] = {
                d.edata.href: [d.text],
            }
    return res


@csrf_exempt
def save_username(request):
    body = json.loads(request.body)
    ic(body)
    uname = body["username"]

    d = {
        "url": f'https://{my_url}/e/{uname}',
    }

    return JsonResponse(d)


@csrf_exempt
def get_e_list(request, username):
    ctx = {}

    if request.method == 'GET':
        ctx["data"] = get_e_data(uname=username)
        # ic(ctx)

    return render(request, "Elist.html", ctx)


def get_e_data(uname):
    ic(uname)
    euserobj, created = ExtensionUser.objects.get_or_create(
        uname=uname
    )

    allhighlights = {}

    if not created:
        just_highlights = list(ExtensionData.objects.filter(user=euserobj))[::-1]
        # ic(just_highlights)

        for i in just_highlights:
            # print("!!!!!",i.href)
            created_date = date.isoformat(i.created_at)
            url = i.href
            if created_date in allhighlights:
                allhighlights[created_date][url] = []
            else:
                allhighlights[created_date] = {
                    url : []
                }
        # ic(allhighlights)

        highlights = list(ExtensionHighlightMetaData.objects.filter(edata__user=euserobj))[::-1]
        for i in highlights:
            # print("!!!!!!!")
            # ic(i.text)
            # ic(i.edata.href)
            # ic(allhighlights)
            created_date = date.isoformat(i.created_at)
            url = i.edata.href
            if created_date in allhighlights:
                if url in allhighlights[created_date]:
                    # ic("!!!1")
                    # ic(url)
                    allhighlights[created_date][url].append(i.text)
                else:
                    allhighlights[created_date][url] = [i.text]

            else:
                allhighlights[created_date] = {
                    url: [i.text]
                }
        # ic(allhighlights)

    return allhighlights


@csrf_exempt
def save_e_value(request):
    body = json.loads(request.body)
    ic(body)
    highlightData = body['highlight']
    pass
    highlight = HighlightForm(highlightData)
    if highlight.is_valid():

        euser, created = ExtensionUser.objects.get_or_create(
            uname=body['username']
        )

        extension, created = ExtensionData.objects.get_or_create(
            user=euser,
            href=highlightData["href"]
        )
        meta_data = ExtensionHighlightMetaData(
            edata=extension,
            anchorNode=highlightData["anchorNode"],
            anchorOffset=highlightData["anchorOffset"],
            color=highlightData["color"],
            container=highlightData["container"],
            focusNode=highlightData["focusNode"],
            focusOffset=highlightData["focusOffset"],
            text=highlightData["string"],
            uuid=highlightData["uuid"],
        )
        meta_data.save()

    else:
        pass
    return JsonResponse({"success": True})


@csrf_exempt
def save_e_url(req):
    ctx = {}
    body = json.loads(req.body)
    ic(body)
    ic(body['url'])
    try:

        user = ExtensionUser.objects.get(
            uname=body['username']
        )

        edata = ExtensionData.objects.get_or_create(
            user=user,
            href=body["url"],
        )
        ctx["success"] = True
    except Exception as e:
        # ic("!!!!!!!!!")
        # ic(e)
        ctx = {
            "error": e,
        }

    return JsonResponse(ctx)


@csrf_exempt
def get_card(req, username):
    ctx = {
        "username": username
    }
    cards = list(Cards.objects.filter(
        username=username
    ))

    card = random.choice(cards)

    ic(card.visible)
    ic(card.hidden)
    ctx["card"] = {
        "visible": card.visible,
        "hidden": card.hidden,
    }

    return render(req, "card.html", ctx)


@csrf_exempt
def view_all_cards(req, username):
    ctx = {
        "username": username,
        "cards": []
    }

    cards = list(Cards.objects.filter(
        username=username
    ))

    for card in cards:
        ctx["cards"].append({
            "visible": card.visible,
            "hidden": card.hidden,
        })

    return render(req, "cards.html", ctx)


@csrf_exempt
def add_cards(req, username):
    ctx = {
        "username": username
    }
    if req.POST:
        card_form = AddCardsForm(req.POST)
        body = json.loads(json.dumps(req.POST))
        if card_form.is_valid():
            card = Cards(
                username=username,
                **body,
            )
            ctx["added"] = True
            card.save()

    form = AddCardsForm()
    ctx["form"] = form
    return render(req, "addcard.html", ctx)


def get_req_body(req):
    body = json.loads(req.body)
    return body
