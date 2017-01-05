from django.conf.urls import url
from .apis import user

urlpatterns = [
    url(r'user', user.user),
]
