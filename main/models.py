from django.db import models
from django.contrib.auth.models import User
import os


def item_image_upload_path(instance, filename):
    """Генерирует путь для сохранения изображения объявления"""
    ext = filename.split('.')[-1]
    filename = f"{instance.id}_{instance.title[:50]}.{ext}"
    return os.path.join('items', filename)


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Item(models.Model):
    STATUS_CHOICES = [
        ("lost", "Lost"),
        ("found", "Found"),
        ("returned", "Returned"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    contact = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="items",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="items",
    )
    image = models.ImageField(
        upload_to=item_image_upload_path,
        null=True,
        blank=True,
        help_text="Upload a photo of the item"
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Comment by {self.author.username} on {self.item.title}"
