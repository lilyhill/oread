from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('telegramCallback/', telegram_callback),
    path('l/<int:username>/', get_list),
]
