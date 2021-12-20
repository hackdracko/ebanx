from rest_framework.routers import DefaultRouter
from accounts.api.views.accounts import *

router_accounts = DefaultRouter()

router_accounts.register(prefix='event', basename='event', viewset=AccountsEventModelViewSet)
# router_accounts.register(prefix='event', basename='event', viewset=CatLanguagesModelViewSet)