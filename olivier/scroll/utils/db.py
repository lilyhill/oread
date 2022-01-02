from ..models import Url

def saveURL(mid,fid,cid,url):
    try:
        u = Url(
            message_id=mid,
            from_id=fid,
            chat_id=cid,
            url=url
        )
        u.save()
    except Exception as e:
        return e

    return 1