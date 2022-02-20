from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('telegramCallback/', telegram_callback),
    path('saveUsername/', save_username),
    path('l/<username>/', get_list),
    path('extensionCallback/',save_e_value),
    path('e/<username>/', get_e_list),
    ]

print(urlpatterns)
print(settings.STATIC_URL)
print(settings.STATIC_ROOT)