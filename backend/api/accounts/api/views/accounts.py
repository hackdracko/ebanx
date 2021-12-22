from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Accounts
from accounts.api.serializers import AccountsSerializer, AccountsWithdrawSerializer, AccountsTransferSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Q
from django.db.models import Sum


@api_view(['POST'])
def reset(request):
    """
    Reset state before starting tests
    """
    Accounts.objects.all().delete()
    return HttpResponse('OK', status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
def event(request):
    """
    Create account with initial balance
    Deposit into existing account
    Get balance for existing account
    Withdraw from non-existing account
    Withdraw from existing account
    Transfer from existing account
    Transfer from non-existing account
    """
    if request.method == 'POST':
        type = request.data['type']
        if type == 'withdraw':
            origin = request.data['origin']
            account = Accounts.objects.filter(Q(destination=origin) | Q(origin=origin))
            if len(account) > 0:
                serializerWithdraw = AccountsWithdrawSerializer(data=request.data)
                if serializerWithdraw.is_valid():
                    serializerWithdraw.save()
                    accountAll = Accounts.objects.filter(Q(destination=origin) | Q(origin=origin))
                    deposits = 0
                    withdraws = 0
                    if len(accountAll) > 0:
                        for item in accountAll.iterator():
                            if item.type == 'deposit':
                                deposits = deposits + int(item.amount)
                            elif item.type == 'withdraw':
                                withdraws = withdraws + int(item.amount)
                    else:
                        return HttpResponse(0, status=404)
                    return JsonResponse({"origin": {"id":serializerWithdraw.data['origin'], "balance":(deposits - withdraws)}}, status=status.HTTP_201_CREATED)
            else:
                return HttpResponse(0, status=404)
        if type == 'transfer':
            origin = request.data['origin']
            accountTransfer = Accounts.objects.filter(Q(destination=origin) | Q(origin=origin))
            if len(accountTransfer) > 0:
                serializerTransfer = AccountsTransferSerializer(data=request.data)
                if serializerTransfer.is_valid():
                    serializerTransfer.save()
                    balance = Accounts.objects.filter(Q(destination=origin) | Q(origin=origin))
                    deposits = 0
                    withdraws = 0
                    transfer = 0
                    if len(balance) > 0:
                        for item in balance.iterator():
                            if item.type == 'deposit':
                                deposits = deposits + int(item.amount)
                            elif item.type == 'withdraw':
                                withdraws = withdraws + int(item.amount)
                            elif item.type == 'transfer':
                                transfer = transfer + int(item.amount)
                    else:
                        return HttpResponse(0, status=404)
                    return JsonResponse({"origin":{"id":serializerTransfer.data['origin'],"balance":(deposits - withdraws - transfer)},"destination":{"id":serializerTransfer.data['destination'],"balance":(transfer)},}, status=status.HTTP_201_CREATED)
            else:
                return HttpResponse(0, status=404)
        else:
            serializer = AccountsSerializer(data=request.data)
        amount = 0
        if serializer.is_valid():
            serializer.save()
            try:
                account = Accounts.objects.filter(destination=serializer.data['destination']).aggregate(Sum('amount'))
                serializer.data['amount'] = account['amount__sum']
                amount = account['amount__sum']
            except Accounts.DoesNotExist:
                amount = serializer.data['amount']
            return JsonResponse({"destination": {"id":serializer.data['destination'], "balance":int(amount)}}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_balance(request):
    """
    Get balance for non-existing account
    Get balance for existing account
    """
    account_id = request.GET.get('account_id', None)
    account = Accounts.objects.filter(destination=account_id)
    deposit = 0
    if len(account) > 0:
        for item in account.iterator():
            deposit = deposit + int(item.amount)
    else:
        return HttpResponse(deposit, status=404)
    if request.method == 'GET':
        return HttpResponse(deposit, status=status.HTTP_200_OK)