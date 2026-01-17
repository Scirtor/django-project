from django.contrib import admin
from .models import Item, Category, Location


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
    list_display = ("title", "status", "category", "location", "author", "date")
    search_fields = ("title", "description", "contact", "author__username")
    list_filter = ("status", "category", "location", "date")
    date_hierarchy = "date"
