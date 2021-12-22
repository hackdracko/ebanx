from rest_framework import serializers
from accounts.models import *

class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['type', 'amount', 'destination']