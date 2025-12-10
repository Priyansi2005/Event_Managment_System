from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='events', null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title


class RSVP(models.Model):
    STATUS_CHOICES = [
        ('Going', 'Going'),
        ('Not Going', 'Not Going')
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')  # Prevent duplicate RSVPs
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.status})"


class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # Newest reviews first
        unique_together = ('event', 'user')  # One review per user per event

    def __str__(self):
        return f"{self.user.username} - {self.rating}"
