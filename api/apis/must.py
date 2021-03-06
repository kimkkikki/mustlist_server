from django.core.exceptions import ObjectDoesNotExist
from ..models import Must, MustSerializer, MustCheck, User, Score
from . import util
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
import datetime
import pytz


@csrf_exempt
def must(request):
    if 'HTTP_ID' not in request.META or 'HTTP_KEY' not in request.META or 'HTTP_DATE' not in request.META:
        return HttpResponse(status=400)

    try:
        user = User.objects.get(id=request.META['HTTP_ID'], key=request.META['HTTP_KEY'])
    except ObjectDoesNotExist:
        return HttpResponse(status=401)

    if request.method == 'GET':
        return must_list(request, user, request.GET.get('page'))
    elif request.method == 'POST':
        if request.body:
            return create_must(request, user)
        else:
            return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)


def must_list(request, user, page):
    limit = 10
    if not page:
        page = 0
    else:
        page = int(page) * limit
        limit = page + limit

    date = util.try_parsing_date(request.META['HTTP_DATE'])

    musts = Must.objects.filter(user_id=user.id).order_by('end', 'end_date')[page:limit]
    check_count_list = MustCheck.objects.filter(must__in=musts).values('must_id').annotate(count=Count('must_id'))

    today_min = datetime.datetime.combine(date, datetime.time.min).replace(tzinfo=date.tzinfo).astimezone(pytz.utc)
    today_max = datetime.datetime.combine(date, datetime.time.max).replace(tzinfo=date.tzinfo).astimezone(pytz.utc)

    serializer = MustSerializer(musts, many=True)
    in_progress_must_list = []

    for must_object in serializer.data:
        days = util.days(must_object['start_date'], must_object['end_date'])

        check_count = 0
        for count in check_count_list:
            if count['must_id'] == must_object['index']:
                check_count = count['count']

        if not must_object['end']:
            in_progress_must_list.append(must_object['index'])
            must_object['check'] = False

        must_object['check_count'] = check_count
        must_object['total_count'] = days

    must_check_list = MustCheck.objects.filter(must_id__in=in_progress_must_list, created__range=(today_min, today_max))

    for must_check in must_check_list:
        for must_object in serializer.data:
            if must_check.must_id == must_object['index']:
                must_object['check'] = True
                break

    return util.JSONResponse(serializer.data)


def create_must(request, user):
    data = JSONParser().parse(request)
    data['user'] = user.id
    serializer = MustSerializer(data=data)
    print(serializer)
    if serializer.is_valid():
        saved_must = serializer.save()

        point = util.must_score(saved_must.end_date - saved_must.start_date, saved_must.deposit)
        score = Score(user_id=user.id, must_id=saved_must.index, score=point)
        score.save()

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

        results = Must.objects.filter(user_id=user.id, end_date__lt=datetime.datetime.utcnow())
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
            data['default_point'] = util.must_point(data['start_date'], data['end_date'], data['deposit'])
            data['days'] = util.days(data['start_date'], data['end_date'])

            return util.JSONResponse(data)
        return HttpResponse(status=400)

    else:
        return HttpResponse(status=400)


@csrf_exempt
def check_must(request, index):
    if 'HTTP_ID' not in request.META or 'HTTP_KEY' not in request.META or 'HTTP_DATE' not in request.META:
        return HttpResponse(status=401)
    try:
        user = User.objects.get(id=request.META['HTTP_ID'], key=request.META['HTTP_KEY'])
    except ObjectDoesNotExist:
        return HttpResponse(status=400)

    date = util.try_parsing_date(request.META['HTTP_DATE'])

    today_min = datetime.datetime.combine(date, datetime.time.min).replace(tzinfo=date.tzinfo).astimezone(pytz.utc)
    today_max = datetime.datetime.combine(date, datetime.time.max).replace(tzinfo=date.tzinfo).astimezone(pytz.utc)
    now = datetime.datetime.now(tz=date.tzinfo).astimezone(pytz.utc)

    try:
        must_object = Must.objects.get(index=index, user=user, start_date__lte=now, end_date__gte=now)
    except ObjectDoesNotExist:
        # 기간이 지남
        return HttpResponse(status=208)

    try:
        # 다시 지움
        must_check = MustCheck.objects.get(must=must_object, created__range=[today_min, today_max])
        must_check.delete()

        return HttpResponse(status=200)

    except ObjectDoesNotExist:
        # Success
        must_check = MustCheck(must_id=index)
        must_check.save()

        return HttpResponse(status=201)
