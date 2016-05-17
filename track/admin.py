from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


from track.models import Choices, Bogger, CalorieEntry, DailyEntry, Measurement, Goal

admin.site.register([CalorieEntry, DailyEntry, Measurement, Goal])


admin.site.unregister(User)

class BoggerInline(admin.StackedInline):
    model = Bogger

class BoggerAdmin(UserAdmin):
    inlines = [ BoggerInline, ]

admin.site.register(User, BoggerAdmin)

