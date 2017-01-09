from ..models import Notice, NoticeSerializer
from . import util
from django.http import HttpResponse


def notice(request):
    if request.method == 'GET':
        return notice_get()

    return HttpResponse(status=404)


def notice_get():
    results = Notice.objects.all()
    serializer = NoticeSerializer(results, many=True)
    print(serializer.data)
    return util.JSONResponse(serializer.data)
