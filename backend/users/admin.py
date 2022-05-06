from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role') 
    search_fields = ('username', 'email') 
    list_filter = ('username', 'email','role', 'is_superuser') 