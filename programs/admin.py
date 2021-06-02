from django.contrib import admin
from .models import Program, ProgramTime

# Register your models here.
class ProgramAdmin(admin.ModelAdmin):
    search_fields = ['name', 'slug']
    #prepopulated_fields = {"slug": ("name",)}

admin.site.register(Program, ProgramAdmin)
admin.site.register(ProgramTime)