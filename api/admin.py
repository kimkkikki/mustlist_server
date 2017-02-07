from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.Must, models.MustAdmin)
admin.site.register(models.User, models.UserAdmin)
admin.site.register(models.Pay, models.PayAdmin)
admin.site.register(models.MustCheck, models.MustCheckAdmin)
admin.site.register(models.Score, models.ScoreAdmin)
admin.site.register(models.Version, models.VersionAdmin)
