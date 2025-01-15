from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Messages(models.Model):
    senderId = models.ForeignKey(User, related_name="sender_id", on_delete=models.CASCADE)
    recipientId = models.ForeignKey(User, related_name="receiver_id", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return super().__str__()