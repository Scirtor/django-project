from rest_framework import serializers

from .models import Item, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "item",
            "author",
            "author_username",
            "text",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["author", "created_at", "updated_at"]


class ItemSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Item
        fields = [
            "id",
            "title",
            "description",
            "status",
            "contact",
            "date",
            "author",
            "category",
            "location",
            "comments",
            "comments_count",
        ]

