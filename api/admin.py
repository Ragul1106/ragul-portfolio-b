from django.contrib import admin
from .models import Profile, Project, ContactMessage, Experience, Education

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'start_date', 'end_date')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('level', 'institution', 'course', 'start_year', 'end_year')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'frontend', 'backend', 'database', 'deployment', 'project_url', 'github_url', 'created_at')
    search_fields = ('title', 'technologies', 'frontend', 'backend')
    list_filter = ('frontend', 'backend', 'deployment')


@admin.register(ContactMessage)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('sender_name', 'sender_email', 'subject', 'date_sent')
    readonly_fields = ('date_sent',)
