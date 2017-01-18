from rest_framework.exceptions import ParseError
from ..models import User, UserSerializer
from django.http import JsonResponse, HttpResponse
from . import util
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist


@csrf_exempt
def user(request):
    if request.method == 'GET':
        return get(request)

    elif request.method == 'POST':
        return post(request)


def get(request):
    if 'HTTP_ID' not in request.META or 'HTTP_KEY' not in request.META:
        return HttpResponse(status=400)

    try:
        login_user = User.objects.get(id=request.META['HTTP_ID'], key=request.META['HTTP_KEY'])
    except ObjectDoesNotExist:
        return HttpResponse(status=401)

    serializer = UserSerializer(login_user, many=False)
    print(serializer.data)

    return JsonResponse(serializer.data)


def post(request):
    try:
        data = JSONParser().parse(request)
        print(data)
    except ParseError:
        return HttpResponse(status=400)

    try:
        user = User.objects.get(id=data['id'])
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return util.JSONResponse(serializer.data, status=200)

    except ObjectDoesNotExist:
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return util.JSONResponse(serializer.data, status=201)

        else:
            return HttpResponse(status=400)

    serializer = UserSerializer(user)
    return util.JSONResponse(serializer.data, status=200)
