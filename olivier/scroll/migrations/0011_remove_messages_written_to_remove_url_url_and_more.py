# Generated by Django 4.0 on 2022-01-08 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scroll', '0010_messages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messages',
            name='written_to',
        ),
        migrations.RemoveField(
            model_name='url',
            name='url',
        ),
        migrations.AddField(
            model_name='messages',
            name='reply_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scroll.messages'),
        ),
        migrations.AddField(
            model_name='messages',
            name='sent_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='url',
            name='main_text',
            field=models.TextField(default='', max_length=10000, null=True),
        ),
        migrations.AddField(
            model_name='url',
            name='parent_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='scroll.url'),
        ),
    ]