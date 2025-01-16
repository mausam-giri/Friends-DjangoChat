from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Messages(models.Model):
    sender = models.ForeignKey(User, related_name="sender_id", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name="receiver_id", on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Message"

    def __str__(self):
        return super().__str__()