from ..models import Score, ScoreSerializer, User
from django.http import HttpResponse
from . import util
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def score(request):
    if 'HTTP_ID' not in request.META or 'HTTP_KEY' not in request.META or 'HTTP_DATE' not in request.META:
        return HttpResponse(status=400)

    if request.method == 'GET':
        scores = Score.objects.filter(user_id=request.META['HTTP_ID'])
        print(scores)

        serializer = ScoreSerializer(scores, many=True)

        return util.JSONResponse(serializer.data)

    else:
        return HttpResponse(status=404)