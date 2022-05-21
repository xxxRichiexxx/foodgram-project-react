from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email', 'role', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': (
                'role', 'authors', 'favorite_recipes', 'shopping_list',
            )
        }),
    )
