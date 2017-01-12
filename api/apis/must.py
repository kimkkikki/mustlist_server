from django.core.exceptions import ObjectDoesNotExist
from ..models import Must, MustSerializer, MustCheck, User
from . import util
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import datetime


@csrf_exempt
def must(request):
    if 'HTTP_ID' not in request.META or 'HTTP_KEY' not in request.META:
        return HttpResponse(status=400)

    try:
        user = User.objects.get(id=request.META['HTTP_ID'], key=request.META['HTTP_KEY'])
    except ObjectDoesNotExist:
        return HttpResponse(status=401)

    if request.method == 'GET':
        return must_list(user)
    elif request.method == 'POST':
        if request.body:
            return create_must(request, user)
        else:
            return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)


def must_list(user):
    musts = Must.objects.filter(user_id=user.id, end_date__gte=datetime.datetime.now())
    must_check_list = MustCheck.objects.filter(must__in=musts)

    serializer = MustSerializer(musts, many=True)
    today = util.get_today()

    print(serializer.data)
    for must_object in serializer.data:
        check = False
        for must_check in must_check_list:
            if must_check.must_id == must_object['index'] and str(must_check.date) == today:
                check = must_check.check_yn

        must_object['check'] = check

    return util.JSONResponse(serializer.data)


def create_must(request, user):
    data = JSONParser().parse(request)
    data['user'] = user.id
    serializer = MustSerializer(data=data)
    print(serializer)
    if serializer.is_valid():
        print(serializer.validated_data)
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        must_object = serializer.save()
        for date in util.date_range(start_date, end_date):
            must_check = MustCheck()
            must_check.must = must_object
            must_check.date = date
            must_check.save()

        return HttpResponse(status=201)

    return util.JSONResponse(serializer.errors, status=400)


def must_history(request):
    if request.method == 'GET':
        if 'HTTP_ID' not in request.META or 'HTTP_KEY' not in request.META:
            return HttpResponse(status=401)
        try:
            user = User.objects.get(id=request.META['HTTP_ID'], key=request.META['HTTP_KEY'])
        except ObjectDoesNotExist:
            return HttpResponse(status=400)

        results = Must.objects.filter(user_id=user.id, end_date__lt=datetime.datetime.now())
        serializer = MustSerializer(results, many=True)
        print(serializer.data)

        return util.JSONResponse(serializer.data)

    else:
        return HttpResponse(status=404)


@csrf_exempt
def must_preview(request):
    if request.method == 'POST':
        if 'HTTP_ID' not in request.META or 'HTTP_KEY' not in request.META:
            return HttpResponse(status=401)
        try:
            user = User.objects.get(id=request.META['HTTP_ID'], key=request.META['HTTP_KEY'])
        except ObjectDoesNotExist:
            return HttpResponse(status=400)

        data = JSONParser().parse(request)
        data['user'] = user.id
        print(data)
        serializer = MustSerializer(data=data)
        if serializer.is_valid():
            print(serializer.data)

            point = util.must_point(data['start_date'], data['end_date'], data['deposit'])
            data['default_point'] = point

            return util.JSONResponse(data)
        return HttpResponse(status=400)

    else:
        return HttpResponse(status=400)


def check_must(request, index):
    # TODO: User Check Required

    try:
        must_check = MustCheck.objects.get(must_id=index, date=util.get_today())
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
