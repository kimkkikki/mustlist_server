from django.conf.urls import url
from .apis import user, must, pay, notice, score, version

urlpatterns = [
    url(r'user$', user.user),
    url(r'must$', must.must),
    url(r'must/history$', must.must_history),
    url(r'must/preview$', must.must_preview),
    url(r'must/(?P<index>\d+)$', must.check_must),
    url(r'pay$', pay.pay),
    url(r'notice$', notice.notice),
    url(r'score$', score.score),
    url(r'version$', version.version),
]
