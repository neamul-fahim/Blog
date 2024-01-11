from django.contrib import admin
from . models import CustomUser, OtpVerification
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'is_active',
                    'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'groups', 'user_permissions')
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


# Register your models here.
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OtpVerification)
