from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff',
                          'is_active', 'balance')


@admin.register(models.Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'balance', 'card_number')

