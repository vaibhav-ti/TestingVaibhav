from django.contrib import admin

from .models import User, Note

admin.site.site_header = '{{cookiecutter.project.name}}'


class UserAdmin(admin.ModelAdmin):
    model = User
    ordering = ['first_name']
    list_display = [
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    ]
    list_display_links = [
        'username',
        'first_name',
        'email',
    ]
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name',
    ]
    list_filter = []


admin.site.register(User, UserAdmin)
admin.site.register(Note)