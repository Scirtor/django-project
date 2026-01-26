from django.contrib import admin
from .models import Item, Category, Location, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "category", "location", "author", "date", "has_image")
    search_fields = ("title", "description", "contact", "author__username")
    list_filter = ("status", "category", "location", "date")
    date_hierarchy = "date"
    readonly_fields = ("image_preview",)
    fieldsets = (
        ("Основная информация", {
            "fields": ("title", "description", "status", "author")
        }),
        ("Контактная информация", {
            "fields": ("contact", "category", "location")
        }),
        ("Изображение", {
            "fields": ("image", "image_preview")
        }),
    )

    def has_image(self, obj):
        return bool(obj.image)
    has_image.boolean = True
    has_image.short_description = "Has Image"

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 200px; max-width: 200px;" />'
        return "No image"
    image_preview.allow_tags = True
    image_preview.short_description = "Image Preview"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("item", "author", "created_at", "updated_at")
    search_fields = ("text", "author__username", "item__title")
    list_filter = ("created_at", "updated_at")
    date_hierarchy = "created_at"
