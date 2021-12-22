from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Accounts
from accounts.api.serializers import AccountsSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from core.pagination import CustomPagination
import json
from django.db.models import Q
from django.db.models import Sum


@api_view(['GET', 'POST'])
def account_list(request):
    """
    List all accounts, or create a new accounts.
    """
    pagination_class = CustomPagination
    if request.method == 'GET':
        data = Accounts.objects.all()
        filter = request.GET.get('filter', None)
        # orders = request.GET.getlist('order', None)
        # if filter is not None:
        #     data = data.filter(Q(name__icontains=filter) | Q(value__icontains=filter))
        # if len(orders) > 0:
        #     for order in orders:
        #         orderDict = json.loads(order)
        #         orderBy = '' if (orderDict['order'] == 'asc') else '-'
        #         data = data.order_by(orderBy + orderDict['field'])
        paginator = pagination_class()
        result_page = paginator.paginate_queryset(data, request)
        serializer = AccountsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
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
            print(serializer.data)
            return JsonResponse({"destination": {"id":serializer.data['destination'], "balance":int(amount)}}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_balance(request):
    """
    Get Balance by Account
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
        # serializer = AccountsSerializer(account)
        return HttpResponse(deposit, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def tax_detail(request, id):
    """
    Retrieve, update or delete a brand.
    """
    try:
        brand = Accounts.objects.get(pk=id)
    except Accounts.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = AccountsSerializer(brand)
        return JsonResponse(serializer.data)
    """
    elif request.method == 'PUT': 
        serializer = TaxesSerializer(brand, data=request.data) 
        if serializer.is_valid(): 
            serializer.save() 
            return JsonResponse(serializer.data) 
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE': 
        brand.delete() 
        return JsonResponse({'message': 'Item was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    """