from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from accounts.models import Accounts
from accounts.api.serializers import AccountsSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from core.pagination import CustomPagination
import json
from django.db.models import Q

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
        destination = request.data['destination']
        amount = request.data['amount']
        request.data['id'] = int(destination)
        del request.data['destination']
        try:
            account = Accounts.objects.get(pk=destination)
            request.data['amount'] = int(account.amount) + int(amount)
            serializer = AccountsSerializer(account, data=request.data)
        except Accounts.DoesNotExist:
            serializer = AccountsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"destination": {"id":serializer.data['id'], "balance":serializer.data['amount']}}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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