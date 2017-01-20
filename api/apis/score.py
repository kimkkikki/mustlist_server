from ..models import Score, User
from django.http import HttpResponse
from . import util
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist


@csrf_exempt
def score(request):
    if 'HTTP_ID' not in request.META or 'HTTP_KEY' not in request.META or 'HTTP_DATE' not in request.META:
        return HttpResponse(status=400)

    try:
        user = User.objects.get(id=request.META['HTTP_ID'], key=request.META['HTTP_KEY'])
    except ObjectDoesNotExist:
        return HttpResponse(status=401)

    if request.method == 'GET':
        scores = Score.objects.filter(user_id=user.id)
        print(scores)

        score_list = []
        for score_object in scores:
            item = {'type': score_object.type, 'score': score_object.score, 'must_title': score_object.must.title}
            score_list.append(item)
        print(score_list)

        return util.JSONResponse(score_list)

    else:
        return HttpResponse(status=404)
