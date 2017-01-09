from ..models import Purchase, PurchaseSerializer
from . import util
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def pay(request):
    if 'HTTP_ID' not in request.META or 'HTTP_KEY' not in request.META:
        return HttpResponse(status=401)

    if request.method == 'GET':
        return payload(request)
    elif request.method == 'POST':
        if request.body:
            return payment(request)
        else:
            return HttpResponse(status=204)
    return HttpResponse(status=404)


def payload(request):
    user_id = request.META['HTTP_ID']
    purchase = Purchase(user_id=user_id)
    purchase.save()
    print(purchase)

    serializer = PurchaseSerializer(purchase)
    return util.JSONResponse(serializer.data)


def payment(request):
    data = JSONParser().parse(request)

    purchase = Purchase.objects.get(developer_payload=data.get('developer_payload'))
    serializer = PurchaseSerializer(purchase, data=data, partial=True)
    print(serializer)
    if serializer.is_valid():
        serializer.save()
        return HttpResponse(status=201)

    return util.JSONResponse(serializer.errors, status=400)
