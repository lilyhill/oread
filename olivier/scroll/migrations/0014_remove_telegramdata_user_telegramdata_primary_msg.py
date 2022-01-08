# Generated by Django 4.0 on 2022-01-08 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scroll', '0013_alter_telegrammessage_mid_alter_telegramuser_cid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegramdata',
            name='user',
        ),
        migrations.AddField(
            model_name='telegramdata',
            name='primary_msg',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scroll.telegrammessage'),
        ),
    ]
