from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from bp_manager.models import User, Blueprint, Tag, Commentary


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("username", "email")


admin.site.register(Blueprint)
admin.site.register(Tag)
admin.site.register(Commentary)
admin.site.unregister(Group)
