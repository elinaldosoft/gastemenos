from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as GenericUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(GenericUserAdmin):
    list_display = ['id', 'name', 'email', 'created_at']
    search_fields = ['name', 'email']
    ordering = ['-id']

    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            },
        ),
    )
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('name', 'email', 'avatar', 'password1', 'password2')}),)
