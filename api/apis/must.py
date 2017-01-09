from django.core.exceptions import ObjectDoesNotExist
from ..models import Must, MustSerializer, MustCheck
from . import util
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import datetime


@csrf_exempt
def must(request):
    if 'HTTP_ID' not in request.META or 'HTTP_KEY' not in request.META:
        return HttpResponse(status=401)
    if request.method == 'GET':
        return must_list(request)
    elif request.method == 'POST':
        if request.body:
            return create_must(request)
        else:
            return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)


def must_list(request):
    user_id = request.META['HTTP_ID']

    results = Must.objects.filter(user_id=user_id, end_date__gte=datetime.datetime.now())
    serializer = MustSerializer(results, many=True)
    print(serializer.data)

    return util.JSONResponse(serializer.data)



def create_must(request):
    data = JSONParser().parse(request)
    data['user'] = request.META['HTTP_ID']
    serializer = MustSerializer(data=data)
    print(serializer)
    if serializer.is_valid():
        print(serializer.validated_data)
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        must = serializer.save()
        for date in util.date_range(start_date, end_date):
            must_check = MustCheck()
            must_check.must = must
            must_check.date = date
            must_check.save()

        return HttpResponse(status=201)

    return util.JSONResponse(serializer.errors, status=400)


def must_history(request):
    if request.method == 'GET':
        if 'HTTP_ID' not in request.META or 'HTTP_KEY' not in request.META:
            return HttpResponse(status=401)

        user_id = request.META['HTTP_ID']

        results = Must.objects.filter(user_id=user_id, end_date__lt=datetime.datetime.now())
        serializer = MustSerializer(results, many=True)
        print(serializer.data)

        return util.JSONResponse(serializer.data)

    else:
        return HttpResponse(status=404)


def check_must(request, index):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    print(today)

    try:
        must_check = MustCheck.objects.get(must_id=index, date=today)
        print(must_check)
        if must_check.check_yn == False:
            must_check.check_yn = True
            must_check.save()

        # Already Checked
        else:
            return HttpResponse(status=204)

    # Not Found
    except ObjectDoesNotExist:
        return HttpResponse(status=400)

    # Success
    return HttpResponse(status=200)
