from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from datetime import date

from .utils.helpers import *
from .forms import HighlightForm

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
            ))

            ctx["url_list"] = collate_dates(td)
            ic(ctx)

        except Exception as e:
            ic('get_list :', e)

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

    allhighlights = get_e_data(uname)
    euser, created = ExtensionUser.objects.get_or_create(
        uname=body['username']
    )

    d = {
        "url": f'https://{my_url}/e/{uname}',
        "highlights": allhighlights,
    }

    return JsonResponse(d)


@csrf_exempt
def get_e_list(request, username):
    ctx = {}
    ic(request)
    if request.method == 'GET':

       ctx["data"] = get_e_data(uname=username)

    ic(ctx, username)

    return render(request, "Elist.html", ctx)


def get_e_data(uname):
    euserobj, created = ExtensionUser.objects.get_or_create(
        uname=uname
    )
    ic(created)
    ic(euserobj)
    if not created:
        allhighlights = {}
        if not created:
            highlights = ExtensionHighlightMetaData.objects.filter(edata__user=euserobj)
            ic(list(highlights))
            for i in highlights:
                ic(i.text)
                print(i.text)
                created_date = date.isoformat(i.created_at)
                url = i.edata.href
                if created_date in allhighlights:
                    if url in allhighlights[created_date]:
                        allhighlights[created_date][url].append(i.text)
                    else:
                        allhighlights[created_date][url] = [i.text]

                else:
                    allhighlights[created_date] = {
                        url : [i.text]
                    }

    return allhighlights


@csrf_exempt
def save_e_value(request):
    body = json.loads(request.body)
    highlightData = body['highlight']
    ic(body)
    highlight = HighlightForm(highlightData)
    if highlight.is_valid():
        ic(highlight)

        euser, created = ExtensionUser.objects.get_or_create(
            uname = body['username']
        )
        ic(euser)
        extension, created = ExtensionData.objects.get_or_create(
            user = euser,
            href=highlightData["href"]
        )
        ic(extension)
        print()
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
        ic(meta_data)
    ic(highlight)
    return JsonResponse({"success": True})
