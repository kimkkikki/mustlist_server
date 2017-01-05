from ..models import User
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def user(request):
    if request.method == 'GET':
        return get(request)

    elif request.method == 'POST':
        return post(request)


def get(request):
    print(request.content_params)

    user_id = request.content_params
    user = User.objects.filter(id=user_id).values()

    return JsonResponse(json.dumps(user), cls=DjangoJSONEncoder)


def post(request):
    new_user = User()
    new_user.save()

    print(new_user)
    return JsonResponse(json.dumps(new_user), cls=DjangoJSONEncoder)
