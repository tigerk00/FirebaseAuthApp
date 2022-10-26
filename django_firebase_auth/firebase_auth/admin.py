from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('uid', 'refresh_token', 'email')


admin.site.register(User, UserAdmin)