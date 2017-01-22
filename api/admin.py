from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.Must)
admin.site.register(models.User)
admin.site.register(models.Pay)
admin.site.register(models.MustCheck)
admin.site.register(models.Score)
