from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class AccountAdmin(UserAdmin):

    list_display = [
        'first_name', 'last_name', 'username', 'email', 'last_login', 'user_join', 'is_active',
    ]
    list_display_links = [
        'email', 'username',
    ]
    search_fields = [
     'first_name', 'last_name', 'username', 'last_login'
    ]
    readonly_fields = [
        'user_join', 'last_login',
    ]
    ordering = ('-user_join', )
    list_per_page = 10
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, AccountAdmin)