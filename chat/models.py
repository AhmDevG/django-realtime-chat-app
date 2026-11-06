from django.db import models
from django.contrib.auth.models import AbstractUser
import os
import uuid
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator



def uuid_upload_to(_, filename):
    ext = os.path.splitext(filename)[1].lower()
    new_filename = f"{uuid.uuid4()}{ext}"
    return os.path.join('users/', new_filename)



class UserProfile(AbstractUser):
    email = models.EmailField(unique=True , blank=False , null=False)
    profile = models.ImageField(upload_to=uuid_upload_to , default = 'defaults/default-img.png' , validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])])
    is_online = models.BooleanField(default=False)


    def clean(self):
        super().clean()
        if self.profile:
            max_size = 2 * 1024 * 1024 
            if self.profile.size > max_size:
                raise ValidationError("Image file too large ( > 2MB )")

    def __str__(self) -> str:
        return self.email

class Room(models.Model):
    room_name = models.CharField(max_length=100)
    room_description = models.CharField(max_length=300)
    room_author = models.ForeignKey(UserProfile , on_delete=models.CASCADE , related_name="rooms")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['room_name' , 'room_author']
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.room_name


class Message(models.Model):
    message_content = models.CharField(max_length=4000)
    message_author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="messages")
    created_at = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")

    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replies',
        help_text='Reply to another message'
    )

    def clean(self):
        if self.reply_to and self.reply_to == self:
            raise ValidationError("A message cannot reply to itself.")

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.message_content
