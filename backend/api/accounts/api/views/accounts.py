from rest_framework.viewsets import ModelViewSet
from accounts.models import *
from accounts.api.serializers import *

class AccountsEventModelViewSet(ModelViewSet):
    serializer_class = AccountsSerializer
    queryset = Accounts.objects.all()
    # http_method_names = ['get']