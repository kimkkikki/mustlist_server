from ..models import PaySerializer, MustSerializer
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def pay(request):
    if 'HTTP_ID' not in request.META or 'HTTP_KEY' not in request.META:
        return HttpResponse(status=401)

    if request.method == 'POST':
        if request.body:
            return payment(request)
        else:
            return HttpResponse(status=204)
    return HttpResponse(status=404)


def payment(request):
    data = JSONParser().parse(request)

    pay_data = data['pay']
    must_data = data['must']

    pay_data['user'] = request.META['HTTP_ID']
    must_data['user'] = request.META['HTTP_ID']

    print(pay_data)
    print(must_data)

    must_serializer = MustSerializer(data=must_data)

    if must_serializer.is_valid():
        saved_must = must_serializer.save()

        pay_data['must'] = saved_must.index
        pay_serializer = PaySerializer(data=pay_data)

        if pay_serializer.is_valid():
            pay_serializer.save()
        else:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=500)

    return HttpResponse(status=200)
