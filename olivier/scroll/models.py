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
    url = models.URLField(max_length=1000, default="", null=True)
    created_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.now()
        tz = t(timedelta(hours=+5, minutes=+30), 'UTC')
        ic(tz)
        self.created_at = datetime.datetime.now(tz=tz)

        ic(os.environ['TZ'])
        ic(timezone.utc)
        ic(self.created_at)
        return super(Url, self).save(*args, **kwargs)

# self.created_at: datetime.datetime(2022, 1, 1, 20, 59, 51, 316162, tzinfo=datetime.timezone.utc)