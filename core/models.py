from django.db import models 
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class CreatorProfile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    subscription_price = models.DecimalField(max_digits=6, decimal_places=2)

def __str__(self):
    return self.user.username + " (Creator)"


class Content(models.Model):
    creator = models.ForeignKey(CreatorProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    media_file = models.FileField(upload_to='content_files/') # Aca se guardarán los archivos
    is_premium = models.BooleanField(default=True) # Si es True, requiere suscripción
    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
        return self.title

class Subscription(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fan_subscriptions')
    creator = models.ForeignKey(CreatorProfile, on_delete=models.CASCADE, related_name='income_subscriptions')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(default=datetime.now() + timedelta(days=30))
    is_active = models.BooleanField(default=True)

    class Meta:
        # Una persona solo puede tener una suscripción activa por creador
        unique_together = ('subscriber', 'creator')

    def __str__(self):
        return f"{self.subscriber.username} subscribed to {self.creator.user.username}"