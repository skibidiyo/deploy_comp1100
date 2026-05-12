from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import PeerlyUser


@admin.register(PeerlyUser)
class PeerlyUserAdmin(UserAdmin):
    model = PeerlyUser
    list_display = ('email', 'full_name', 'is_email_verified', 'is_staff', 'created_at')
    list_filter = ('is_email_verified', 'is_staff', 'is_active')
    search_fields = ('email', 'full_name')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_email_verified', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('created_at',)

