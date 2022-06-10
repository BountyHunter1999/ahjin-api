from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'ahjin_coin']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # (_('Personal Info'), {'fields': ('ahjin_coin', 'gender', 'user_hash')}),
        (_('Personal Info'), {'fields': ('ahjin_coin', 'user_hash', 'phone_number')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.CustomUser, UserAdmin)
# admin.site.register(models.User, UserAdmin)
