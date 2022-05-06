from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Telegram bot urls
    path('telegramCallback/', telegram_callback),
    path('l/<username>/', get_list),

    # Extension URLs
    path('extensionCallback/',save_e_value),
    path('saveUsername/', save_username),
    path('e/<username>/', get_e_list),

    # Card URLs
    path('c/<username>/',get_card),
    path('c/<username>/add', add_cards),
    path('c/<username>/all', view_all_cards),
]


print(urlpatterns)
print(settings.STATIC_URL)
print(settings.STATIC_ROOT)