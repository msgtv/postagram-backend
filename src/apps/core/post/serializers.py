from django.conf import settings

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.core.abstract.serializers import AbstractSerializer
from apps.core.post.models import Post
from apps.core.user.models import User
from apps.core.user.serializers import UserSerializer


class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="public_id",
    )
    liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    def get_liked(self, instance):
        request = self.context.get("request", None)
        if request is None or request.user.is_anonymous:
            return False

        return request.user.posts_likes.has_liked(instance)

    @staticmethod
    def get_likes_count(instance):
        return instance.liked_by.count()

    @staticmethod
    def get_comments_count(instance):
        return instance.comments.count()

    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError(
                "You cannot create a post for another user")
        return value

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(rep["author"])
        rep["author"] = UserSerializer(author).data

        if settings.DEBUG:
            rep['author']['avatar'] = self.context['request'].build_absolute_uri(rep['author']['avatar'])

        return rep

    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True

        return super().update(instance, validated_data)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "body",
            "edited",
            "liked",
            "likes_count",
            "comments_count",
            "created",
            "updated"
        ]
        read_only_fields = ["edited"]