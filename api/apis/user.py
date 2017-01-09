from ..models import User, UserSerializer
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def user(request):
    if request.method == 'GET':
        return get(request)

    elif request.method == 'POST':
        return post()


def get(request):
    if 'HTTP_ID' not in request.META or 'HTTP_KEY' not in request.META:
        return HttpResponse(status=401)
    else:
        user_id = request.META['HTTP_ID']
        user_key = request.META['HTTP_KEY']

    login_user = User.objects.get(id=user_id, key=user_key)
    serializer = UserSerializer(login_user, many=False)
    print(serializer.data)

    return JsonResponse(serializer.data)


def post():
    new_user = User()
    new_user.save()

    serializer = UserSerializer(new_user)
    print(serializer.data)
    return JsonResponse(serializer.data)
