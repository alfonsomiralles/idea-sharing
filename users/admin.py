from django.contrib import admin
from .models import User, Idea
from django.apps import apps

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'last_login')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active', 'last_login')

admin.site.register(User, UserAdmin)

class IdeaAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at', 'visibility')
    search_fields = ('user__username', 'text')
    list_filter = ('visibility', 'created_at')

admin.site.register(Idea, IdeaAdmin)

app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)