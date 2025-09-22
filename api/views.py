from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from .models import Profile, Project, ContactMessage
from .serializers import ProfileSerializer, ProjectSerializer, ContactMessageSerializer
from rest_framework.decorators import action
from django.core.mail import send_mail
from django.conf import settings


class ProfileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.order_by('-created_at')
    serializer_class = ProjectSerializer
    lookup_field = 'id'


class ContactViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.save()

        # Email subject & message for you (site owner)
        subject = f"New Contact Form Submission: {contact.subject}"
        message = f"""
        You have received a new message from your portfolio website contact form.

        Sender Details:
        -----------------------
        Name: {contact.sender_name}
        Email: {contact.sender_email}

        Message:
        -----------------------
        {contact.message}

        Please respond to the sender promptly.

        This email was automatically sent via your portfolio contact form.
        """

        try:
            # Send email to YOU
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],  
                fail_silently=False,
            )

            # Send "Thank You" email to the SENDER
            thank_you_subject = "Thank You for Contacting Me"
            thank_you_message = f"""
            Hi {contact.sender_name},

            Thank you for reaching out to me through my portfolio contact form. 
            I have received your message and will get back to you as soon as possible.

            Here’s a copy of your message for your reference:
            -----------------------
            Subject: {contact.subject}
            Message: {contact.message}

            I truly appreciate you taking the time to connect with me. 

            Best regards,  
            {getattr(settings, 'SITE_OWNER_NAME', 'Portfolio Owner')}
            """

            send_mail(
                thank_you_subject,
                thank_you_message,
                settings.DEFAULT_FROM_EMAIL,
                [contact.sender_email],  
                fail_silently=False,
            )

        except Exception as e:
            return Response(
                {"error": f"Email not sent: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
