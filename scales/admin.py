from django.contrib import admin
from .models import Ministry, Function, Program, ProgramTime

# Register your models here.

class MinistryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'slug']
    prepopulated_fields = {"slug": ("name",)}

class ProgramAdmin(admin.ModelAdmin):
    search_fields = ['name', 'slug']
    #prepopulated_fields = {"slug": ("name",)}

admin.site.register(Ministry, MinistryAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Function)
admin.site.register(ProgramTime)