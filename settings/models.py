from django.db import models
from django.conf import settings


class UserSettings(models.Model):

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('te', 'Telugu'),
        ('kn', 'Kannada'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    # LANGUAGE
    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='en'
    )
    gender = models.CharField(
    max_length=20,
    blank=True,
    null=True
)
    profile_image = models.ImageField(
    upload_to="profiles/",
    blank=True,
    null=True
)

    # APPEARANCE
    dark_mode = models.BooleanField(default=False)

    # NOTIFICATIONS
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)

    # SECURITY
    fingerprint_login = models.BooleanField(default=False)
    two_factor_auth = models.BooleanField(default=False)

    # LEARNING
    autoplay_videos = models.BooleanField(default=True)
    offline_downloads = models.BooleanField(default=False)

    # COMMUNITY
    allow_chat = models.BooleanField(default=True)
    allow_discussions = models.BooleanField(default=True)

    # REMINDERS
    live_class_reminders = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} Settings"