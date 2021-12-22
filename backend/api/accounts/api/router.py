from accounts.api.views.accounts import *
from django.urls import path


urlpatterns = [
    path('reset/', reset),
    path('event/', event),
    path('balance/', get_balance),
]