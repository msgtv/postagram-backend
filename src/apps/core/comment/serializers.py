from rest_framework import serializers

from apps.core.abstract.serializers import AbstractSerializer
from apps.core.user.models import User
from apps.core.user.serializers import UserSerializer
from apps.core.comment.models import Comment
from apps.core.post.models import Post


class CommentSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='public_id'
    )
    post = serializers.SlugRelatedField(
        queryset=Post.objects.all(),
        slug_field='public_id'
    )
    liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_liked(self, instance):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False

        return request.user.comments_likes.has_liked(instance)

    @staticmethod
    def get_likes_count(instance):
        return instance.liked_by.count()

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(rep['author'])
        rep['author'] = UserSerializer(author).data

        return rep

    def validate_post(self, value):
        if self.instance:
            return self.instance.post
        return value

    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True
        instance = super().update(instance, validated_data)

        return instance

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'author',
            'body',
            'edited',
            'liked',
            'likes_count',
            'created',
            'updated',
        ]
        read_only_fields = ['edited']
