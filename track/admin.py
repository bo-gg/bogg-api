from django.contrib import admin

from track.models import Choices, Bogger, CalorieEntry, DailyEntry, Measurement, Goal

admin.site.register([Bogger, CalorieEntry, DailyEntry, Measurement, Goal])
