from django.contrib import admin
from share_manager import models


@admin.register(models.Share)
class ShareAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Portfolio)
class ShareAdmin(admin.ModelAdmin):
    pass
