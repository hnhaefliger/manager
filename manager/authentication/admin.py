from django.contrib import admin
from django.contrib.admin.utils import quote
from django.contrib.admin.views.main import ChangeList
from django.core.exceptions import ValidationError
from django.urls import reverse

from .models import User, Token


class UserAdmin(admin.ModelAdmin):
    fields = ('id', 'first_name', 'last_name', 'email', 'password', 'confirmed', 'is_staff', 'is_active', 'is_superuser', 'date_joined', 'groups', 'user_permissions',)
    readonly_fields = ('id', 'date_joined',)

    def id(self, obj): return obj.id
    def date_joined(self, obj): return obj.last_login


class TokenAdmin(admin.ModelAdmin):
    fields = ('id', 'user', 'token', 'valid_until', 'created_at')
    readonly_fields = ('id', 'user', 'token', 'valid_until', 'created_at')

    def id(self, obj): return obj.id
    def user(self, obj): return obj.user
    def token(self, obj): return obj.token
    def valid_until(self, obj): return obj.valid_until
    def created_at(self, obj): return obj.created_at


admin.site.register(User, UserAdmin)
admin.site.register(Token, TokenAdmin)
