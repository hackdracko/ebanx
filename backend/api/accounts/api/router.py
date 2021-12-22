from accounts.api.views.accounts import *
from django.urls import path


urlpatterns = [
    # /balance?account_id=1234
    # path('balance/(?P<int:account_id>)', get_balance),
    path('event/', account_list),
    path('balance/', get_balance),
    #  path('language/<uuid:id>', views.language_detail),
]