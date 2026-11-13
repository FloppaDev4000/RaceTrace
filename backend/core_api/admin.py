from django.contrib import admin

from .models import Race, Result

# register data models with relevant fields on admin view
@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ("title", "dateRan", "location", "distanceKm", "source")
    search_fields = ("title", "location")
    list_filter = ("source", "dateRan")
    
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("rawTitle", "rawDate", "race", "source")
    search_fields = ("rawTitle", "source")
    list_filter = ["source"]