from django.contrib import admin
from .models import Notification

# Register your models here.

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user_notified', 'user_creator', 'idea', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username', 'idea__text', 'created_at')

    def user_notified(self, obj):
        return obj.user.username
    
    user_notified.admin_order_field = 'user'
    user_notified.short_description = 'User Notified'

    def user_creator(self, obj):
        return obj.idea.user.username

    user_creator.admin_order_field = 'idea__user'
    user_creator.short_description = 'User Creator'

admin.site.register(Notification, NotificationAdmin)