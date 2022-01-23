from django.contrib import admin
from django.urls import path, include
from .views import *



urlpatterns = [
    path('telegramCallback/', telegram_callback),
    path('saveUsername/', get_username),
    path('l/<int:username>/', get_list),
    path('extensionCallback/',save_e_value),
    path('e/<username>/', get_e_list),
]
