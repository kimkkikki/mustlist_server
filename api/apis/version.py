from ..models import Version
from django.http import HttpResponse


def version(request):
    if 'HTTP_VERSION' not in request.META:
        return HttpResponse(status=400)

    request_version = int(request.META['HTTP_VERSION'])
    latest = Version.objects.latest('version')

    if request_version < latest.version:
        if latest.force:
            return HttpResponse(status=205)
        else:
            return HttpResponse(status=206)

    return HttpResponse(status=200)
