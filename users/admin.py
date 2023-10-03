from django.contrib import admin
from .models import User
from django.apps import apps

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'last_login')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active', 'last_login')

admin.site.register(User, UserAdmin)

app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)