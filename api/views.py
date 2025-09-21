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

        subject = f"[Portfolio Contact] {contact.subject}"
        message = (
            f"📩 You have received a new portfolio inquiry\n\n"
            f"👤 Name: {contact.sender_name}\n"
            f"✉️ Email: {contact.sender_email}\n\n"
            f"📝 Message:\n{contact.message}\n\n"
            f"---\n"
            f"This message was sent via your portfolio contact form."
        )

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.EMAIL_HOST_USER],  
                fail_silently=False,
            )
        except Exception as e:
            return Response({"error": f"Email not sent: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)







# # send email to you
# subject = f"[Portfolio Contact] {contact.subject}"
# message = (
#     f"📩 You have received a new portfolio inquiry\n\n"
#     f"👤 Name: {contact.sender_name}\n"
#     f"✉️ Email: {contact.sender_email}\n\n"
#     f"📝 Message:\n{contact.message}\n\n"
#     f"---\n"
#     f"This message was sent via your portfolio contact form."
# )
# send_mail(
#     subject,
#     message,
#     settings.EMAIL_HOST_USER,
#     [settings.EMAIL_HOST_USER],  # your email
#     fail_silently=False,
# )

# # auto-reply to sender
# auto_subject = "✅ Thank you for contacting Ragul's Portfolio"
# auto_message = (
#     f"Hello {contact.sender_name},\n\n"
#     f"Thank you for reaching out through my portfolio. "
#     f"I have received your message with the subject: \"{contact.subject}\".\n\n"
#     f"I’ll review your inquiry and get back to you as soon as possible.\n\n"
#     f"Best regards,\n"
#     f"Ragul\n"
#     f"---\n"
#     f"Portfolio Website: https://your-portfolio-link.com"
# )
# send_mail(
#     auto_subject,
#     auto_message,
#     settings.EMAIL_HOST_USER,
#     [contact.sender_email],  # sender’s email
#     fail_silently=False,
# )
