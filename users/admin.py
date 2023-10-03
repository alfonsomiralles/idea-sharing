from django.contrib import admin
from .models import User
from django.apps import apps

class FollowingInline(admin.TabularInline):
    """
    Display Following relationships in the User admin panel.
    """
    model = User.following.through
    fk_name = 'from_user'
    extra = 1 
    verbose_name = 'Following'
    verbose_name_plural = 'Following'

class FollowersInline(admin.TabularInline):
    """
    Display Follower relationships in the User admin panel.
    """
    model = User.following.through
    fk_name = 'to_user'
    extra = 1 
    verbose_name = 'Follower'
    verbose_name_plural = 'Followers'
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'last_login')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active', 'last_login')
    inlines = [FollowingInline, FollowersInline]

admin.site.register(User, UserAdmin)

app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)