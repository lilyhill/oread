import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from icecream import ic
import os
from datetime import timedelta
from datetime import timezone as t


class Url(models.Model):

    message_id = models.IntegerField(default=0)
    from_id = models.IntegerField(default=0)
    chat_id = models.IntegerField(default=0)
    url = models.URLField(max_length=10000, default="", null=True)
    created_at = models.DateTimeField(null=True)


class Reply(models.Model):

    reply_to = models.ForeignKey(Url, on_delete=models.CASCADE, null=True)
    text = models.TextField(max_length=10000, default="", null=True)

