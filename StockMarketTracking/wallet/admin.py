from django.contrib import admin

from wallet import models


@admin.register(models.Wallet)
class WalletAdmin(admin.ModelAdmin):
    pass
