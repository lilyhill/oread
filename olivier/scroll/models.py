from django.db import models


class User(models.Model):
    name = models.TextField(max_length=1000, default="")
    username = models.TextField(max_length=100, default="default_user", unique=True)


class TelegramUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cid = models.IntegerField(default=0, null=True)
    fid = models.IntegerField(default=0, null=True)


class TelegramMessage(models.Model):

    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, null=True)
    mid = models.IntegerField(default=0, null=True)

    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None)
    msg_type = models.CharField(max_length=100, null=False)
    text = models.TextField(max_length=10000, default="", null=True)
    msg_body = models.JSONField()
    sent_at = models.DateTimeField(null=True)


class TelegramData(models.Model):

    primary_msg = models.ForeignKey(TelegramMessage, on_delete=models.CASCADE, null=True)
    text = models.TextField(max_length=10000, default="", null=True)
    sub_text = models.TextField(max_length=1000, default="", null=True)
    created_at = models.DateTimeField(null=True)


class ExtensionUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    uname = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.uname


class ExtensionData(models.Model):
    user = models.ForeignKey(ExtensionUser, on_delete=models.CASCADE, null=True)
    text = models.URLField(max_length=1000, null=True, default="")
    sub_text = models.TextField(max_length=1000, null=True, default="")
    created_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.uname


# class Url(models.Model):
#
#     message_id = models.IntegerField(default=0)
#     from_id = models.IntegerField(default=0)
#     chat_id = models.IntegerField(default=0)
#     main_text = models.TextField(max_length=10000, default="", null=True)
#     text = models.TextField(max_length=10000, default="", null=True)
#     created_at = models.DateTimeField(null=True)
#     parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
#
#
#
# class Messages(models.Model):
#
#     message_id = models.IntegerField(default=0)
#     from_id = models.IntegerField(default=0)
#     chat_id = models.IntegerField(default=0)
#
#     reply_to=models.ForeignKey('self', on_delete=models.CASCADE, null=True)
#     msg_type = models.CharField(max_length=100, null=False)
#     text = models.TextField(max_length=10000, default="", null=True)
#     msg_body = models.JSONField()
#     sent_at = models.DateTimeField(null=True)