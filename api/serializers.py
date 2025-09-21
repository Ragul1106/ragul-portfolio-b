from rest_framework import serializers
from .models import Profile, Project, ContactMessage

class ProfileSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    profile_image = serializers.ImageField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'name', 'title', 'bio', 'resume_url', 'skills', 'profile_image']

    def get_skills(self, obj):
        return obj.skills_list()

class ProjectSerializer(serializers.ModelSerializer):
    technologies = serializers.SerializerMethodField()
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'short_description',
            'long_description',   # add this
            'image',
            'technologies',
            'frontend',           # add these fields
            'backend',
            'database',
            'deployment',
            'project_url',
            'github_url',
            'created_at',
        ]

    def get_technologies(self, obj):
        return obj.tech_list()


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'sender_name', 'sender_email', 'subject', 'message', 'date_sent']
        read_only_fields = ['id', 'date_sent']

    def validate(self, data):
        if len(data.get('message','')) < 10:
            raise serializers.ValidationError("Message must be at least 10 characters.")
        return data
