from django.contrib import admin
from .models import Program, ProgramTime

# Register your models here.
class ProgramAdmin(admin.ModelAdmin):
    search_fields = ['name']
    #prepopulated_fields = {"slug": ("name",)}

class ProgramTimeAdmin(admin.ModelAdmin):
    search_fields = ['program']
    list_display = ('program', 'desc', 'function', 'lookup')

admin.site.register(Program, ProgramAdmin)
admin.site.register(ProgramTime,ProgramTimeAdmin)