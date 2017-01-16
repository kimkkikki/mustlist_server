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
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def try_parsing_date(text):
    for fmt in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%dT%H:%M:%S%z'):
        try:
            return datetime.datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')


def must_point(start_date, end_date, deposit):
    start_date = try_parsing_date(start_date)
    end_date = try_parsing_date(end_date)

    date_diff = end_date - start_date

    point = deposit * 100 + (date_diff.days + 1) * 10

    return point


def days(start_date, end_date):
    start_date = try_parsing_date(start_date)
    end_date = try_parsing_date(end_date)

    date_diff = end_date - start_date

    return date_diff.days + 1


def get_today_string():
    today = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    return today
