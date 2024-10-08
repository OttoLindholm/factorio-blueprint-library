from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse, reverse_lazy


# Creates a dir for the current user where their drawings are stored
def user_blueprint_path(instance: models.Model, filename: str) -> str:
    return f"user_{instance.user.id}/{filename}"


class User(AbstractUser):
    def __str__(self) -> str:
        return self.username

    def get_absolute_url(self):
        return reverse("bp_manager:user-detail", kwargs={"pk": self.pk})


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Blueprint(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="blueprints",
    )
    created_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    blueprint_string = models.TextField()
    blueprint_image = models.ImageField(upload_to=user_blueprint_path)
    tags = models.ManyToManyField(Tag, related_name="tags", blank=True)

    class Meta:
        ordering = [
            "-created_time",
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.user.username})"

    def get_absolute_url(self):
        return reverse("bp_manager:blueprint-detail", kwargs={"pk": self.pk})


class Commentary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    blueprint = models.ForeignKey(
        Blueprint, on_delete=models.CASCADE, related_name="comments"
    )
    created_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ["-created_time"]

    def get_absolute_url(self):
        return (
            reverse_lazy(
                "bp_manager:blueprint-detail", kwargs={"pk": self.blueprint.pk}
            )
            + f"#comment-{self.pk}"
        )


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    blueprint = models.ForeignKey(
        Blueprint, on_delete=models.CASCADE, related_name="likes"
    )

    class Meta:
        unique_together = (("user", "blueprint"),)
