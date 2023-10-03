from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Idea

class IdeaAdmin(admin.ModelAdmin):
    list_display = ('user', 'text', 'created_at', 'visibility')
    search_fields = ('user__username', 'text')
    list_filter = ('visibility', 'created_at')

admin.site.register(Idea, IdeaAdmin)