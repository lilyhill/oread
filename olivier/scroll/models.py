from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from icecream import ic


class Url(models.Model):

    message_id = models.IntegerField(default=0)
    from_id = models.IntegerField(default=0)
    chat_id = models.IntegerField(default=0)
    url = models.URLField(max_length=1000, default="", null=True)
    created_at = models.DateTimeField(auto_now_add=True)

