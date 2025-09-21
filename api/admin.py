from django.contrib import admin
from .models import Profile, Project, ContactMessage

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')

# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ('title', 'project_url', 'github_url', 'created_at')
#     search_fields = ('title', 'technologies')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'frontend', 'backend', 'database', 'deployment', 'project_url', 'github_url', 'created_at')
    search_fields = ('title', 'technologies', 'frontend', 'backend')
    list_filter = ('frontend', 'backend', 'deployment')


@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'sender_email', 'subject', 'date_sent')
    readonly_fields = ('date_sent',)
