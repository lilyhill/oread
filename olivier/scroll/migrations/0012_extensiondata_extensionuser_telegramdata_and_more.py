# Generated by Django 4.0 on 2022-01-08 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scroll', '0011_remove_messages_written_to_remove_url_url_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtensionData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(default='', max_length=1000, null=True)),
                ('sub_text', models.TextField(default='', max_length=1000, null=True)),
                ('created_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExtensionUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='TelegramData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(default='', max_length=10000, null=True)),
                ('sub_text', models.TextField(default='', max_length=1000, null=True)),
                ('created_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TelegramMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mid', models.IntegerField(default=0, max_length=100, null=True)),
                ('msg_type', models.CharField(max_length=100)),
                ('text', models.TextField(default='', max_length=10000, null=True)),
                ('msg_body', models.JSONField()),
                ('sent_at', models.DateTimeField(null=True)),
                ('reply_to', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='scroll.telegrammessage')),
            ],
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.IntegerField(default=0, max_length=100, null=True)),
                ('fid', models.IntegerField(default=0, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='', max_length=1000)),
                ('username', models.TextField(default='default_user', max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='url',
            name='parent_id',
        ),
        migrations.DeleteModel(
            name='Messages',
        ),
        migrations.DeleteModel(
            name='Url',
        ),
        migrations.AddField(
            model_name='telegramuser',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scroll.user'),
        ),
        migrations.AddField(
            model_name='telegrammessage',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scroll.telegramuser'),
        ),
        migrations.AddField(
            model_name='telegramdata',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scroll.telegramuser'),
        ),
        migrations.AddField(
            model_name='extensionuser',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scroll.user'),
        ),
        migrations.AddField(
            model_name='extensiondata',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scroll.extensionuser'),
        ),
    ]
