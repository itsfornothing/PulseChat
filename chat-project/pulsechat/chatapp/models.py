from django.db import models
from django.conf import settings
import uuid
from django.contrib.auth.models import User


class Group(models.Model):
    name  = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_groups")
    members =  models.ManyToManyField(User, blank=True, related_name="member_groups")
    online_members = models.ManyToManyField(User, blank=True, related_name='online_in_groups')

class PulseChatUsers(models.Model):
    username = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    bio = models.TextField(null=True, blank=True, default='None')
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField('Group', blank=True, symmetrical=False, related_name="joined_groups")
    is_online = models.BooleanField(default=False)


class Chat(models.Model):
    name = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text_content = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message by {self.sender.username} in {self.chat.name} - {self.text_content}"
    
    class Meta:
        ordering = ['-timestamp']


class GroupMessages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    group =  models.ForeignKey(Group, on_delete=models.CASCADE)
    text_content = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)