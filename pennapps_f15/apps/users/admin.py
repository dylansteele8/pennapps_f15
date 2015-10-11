from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from models import *

# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
#     verbose_name_plural = 'Profiles'

# class UserAdmin(UserAdmin):
#     inlines = (ProfileInline, )

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
admin.site.register(Song)
admin.site.register(StationSong)
admin.site.register(Station)
admin.site.register(Account)
