from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self) -> str:
        return self.username


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Blueprint(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blueprints",
    )
    created_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    blueprint_string = models.TextField()
    blueprint_image = models.ImageField(upload_to="blueprints")
    tags = models.ManyToManyField(Tag, related_name="tags", blank=True)
    likes = models.ManyToManyField(User, related_name="likes")

    class Meta:
        ordering = ["-created_time", ]

    def __str__(self) -> str:
        return f"{self.title} ({self.owner.username})"


class Commentary(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    blueprint = models.ForeignKey(
        Blueprint,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    created_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ["-created_time"]
