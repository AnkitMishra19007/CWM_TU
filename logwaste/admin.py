from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Ewaste, MyUser
# Register your models here.


@admin.register(Ewaste)
class EwasteAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'mobile', 'address',
                    'item_name', 'item_description', 'item_image', 'date']


class MyUserAdmin(BaseUserAdmin):
    list_display = ['id', 'full_name', 'email', 'date_joined',
                    'last_login', 'is_admin', 'is_active']
    search_fields = ['email', 'full_name']
    readonly_fields = ['date_joined', 'last_login']
    filter_horizontal = ()
    list_filter = ['last_login']
    fieldsets = ()

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'full_name', 'mobile', 'password1', 'password2', 'address'),
        }),
    )

    ordering = ['email', ]


admin.site.register(MyUser, MyUserAdmin)
