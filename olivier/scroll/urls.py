from django.contrib import admin
from django.urls import path, include
from .models import Url
from .views import telegram_callback, get_list
urlpatterns = [
    path('telegramCallback/', telegram_callback),
    path('l/<int:id>/', get_list),
]
