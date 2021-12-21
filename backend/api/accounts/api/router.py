from accounts.api.views.accounts import *
from django.urls import path


urlpatterns = [
    path('event/', account_list),
    #  path('language/<uuid:id>', views.language_detail),
]