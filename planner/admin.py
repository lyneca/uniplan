from django.contrib import admin
from .models import Profile, Unit, Assessment

class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'long_name')

class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'week')

admin.site.register(Profile)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Assessment, AssessmentAdmin)
