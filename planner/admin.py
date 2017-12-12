from django.contrib import admin
from .models import User, Unit, Assessment

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')

class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'long_name')

class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')

admin.site.register(User, UserAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Assessment, AssessmentAdmin)
