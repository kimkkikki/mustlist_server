from django.core.management.base import BaseCommand
from ...models import Must, MustCheck, Score, Pay
from ...apis import util
from django.db.models import Count
from datetime import datetime
import pytz


class Command(BaseCommand):
    help = 'must end update command'

    def handle(self, *args, **options):
        musts = Must.objects.filter(end=False, end_date__lte=datetime.utcnow().replace(tzinfo=pytz.utc))
        must_checks = MustCheck.objects.filter(must__in=musts).values('must_id').annotate(count=Count('must_id'))
        pays = Pay.objects.filter(must__in=musts)

        for must in musts:
            days = (must.end_date - must.start_date).days + 1
            check_count = 0
            for count in must_checks:
                if count['must_id'] == must.index:
                    check_count = count['count']

            # 80% 이상일때 성공 표기
            if days * 0.8 < check_count:
                must.success = True

                point = util.must_score(must.end_date - must.start_date, must.deposit)
                score = Score(user=must.user, must_id=must.index, score=point, type='S')
                score.save()

                for pay in pays:
                    if pay.must == must:
                        pay.refund = 'N'
                        pay.save()

            must.end = True
            must.save()

            print('must ' + str(must) + ' end update success')
