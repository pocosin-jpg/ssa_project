from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "first_name", "surname", "nickname")
    search_fields = ("user__username", "nickname")
    list_filter = ("nickname",)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(CustomUser, UserAdmin)
