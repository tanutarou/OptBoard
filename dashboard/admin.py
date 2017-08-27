from django.contrib import admin
from .models import Solver, Result, Project


class ResultAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name']


admin.site.register(Solver)
admin.site.register(Result, ResultAdmin)
admin.site.register(Project)
