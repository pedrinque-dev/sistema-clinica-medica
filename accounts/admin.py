from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Informações adicionais', {'fields': ('perfil', 'medico')}),
    )
    list_display = ['username', 'email', 'perfil', 'medico', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)
