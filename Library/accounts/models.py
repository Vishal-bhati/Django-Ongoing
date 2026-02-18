from django.db import models
from django.conf import settings
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    last_active = models.DateTimeField(default=timezone.now)

    def get_status(self):
        now = timezone.now()
        diff = (now - self.last_active).total_seconds() # difference in minutes
        if self.last_active > now - timezone.timedelta(minutes=5):
            return "Online"
        elif self.last_active > now - timezone.timedelta(minutes=30):
            return "Idle"
        else:
            return "Offline"
        
    def __str__(self):
        return self.user.username