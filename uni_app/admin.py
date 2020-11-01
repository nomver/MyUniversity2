from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.University)
admin.site.register(models.Department)
admin.site.register(models.Subject)
class AdminProgram(admin.ModelAdmin):
    list_filter=['department',]

admin.site.register(models.Program,AdminProgram)
admin.site.register(models.Lecture)
admin.site.register(models.Assignment)