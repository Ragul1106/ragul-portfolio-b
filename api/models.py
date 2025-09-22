from django.db import models

class Profile(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    resume_url = models.URLField(blank=True)
    # store skills as comma separated or JSON field — simple CSV for now:
    skills = models.TextField(help_text="Comma-separated skills", blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=500)
    long_description = models.TextField(blank=True)  # Detailed explanation
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    technologies = models.CharField(max_length=300, help_text="Comma-separated list")
    
    frontend = models.CharField(max_length=200, blank=True)
    backend = models.CharField(max_length=200, blank=True)
    database = models.CharField(max_length=200, blank=True)
    deployment = models.CharField(max_length=200, blank=True)
    
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def tech_list(self):
        return [t.strip() for t in self.technologies.split(',') if t.strip()]

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    sender_name = models.CharField(max_length=200)
    sender_email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_name} - {self.subject}"


class Experience(models.Model):
    title = models.CharField(max_length=200)  
    company = models.CharField(max_length=200) 
    location = models.CharField(max_length=200, blank=True, null=True)  
    description = models.TextField()  
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)  

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} - {self.company}"


class Education(models.Model):
    level = models.CharField(max_length=200)  
    institution = models.CharField(max_length=200) 
    course = models.CharField(max_length=200, blank=True, null=True)  
    start_year = models.CharField(max_length=20)
    end_year = models.CharField(max_length=20)

    class Meta:
        ordering = ['-start_year']

    def __str__(self):
        return f"{self.level} - {self.institution}"
