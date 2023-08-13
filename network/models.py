from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", related_name="follower", symmetrical=False)

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="author")
    title = models.CharField(max_length=250)
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True, null=True)
    like = models.ManyToManyField("User", related_name="user_liked", blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
        }