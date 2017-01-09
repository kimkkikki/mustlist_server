from django.conf.urls import url
from .apis import user, must, pay

urlpatterns = [
    url(r'user', user.user),
    url(r'must', must.must),
    url(r'must/history', must.must_history),
    url(r'pay', pay.pay),
]
