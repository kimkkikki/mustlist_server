from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from datetime import timedelta
import datetime


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def date_range(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)


def must_point(start_date, end_date, deposit):
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S')

    date_diff = end_date - start_date

    point = deposit * 100 + (date_diff.days + 1) * 10

    return point
