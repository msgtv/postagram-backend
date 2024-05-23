from django.http import Http404

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from apps.core.abstract.viewsets import AbstractViewSet
from apps.core.comment.models import Comment
from apps.core.comment.serializers import CommentSerializer
from apps.core.auth.permissions import UserPermission


class CommentViewSet(AbstractViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = (UserPermission, )
    serializer_class = CommentSerializer
    ordering = ('-created',)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Comment.objects.all()

        post_pk = self.kwargs.get('post_pk')
        if post_pk is None:
            return Http404

        return Comment.objects.filter(post__public_id=post_pk)

    def get_object(self):
        obj = Comment.objects.get_object_by_public_id(self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['post']
    )
    def like(self, request, *args, **kwargs):
        comment = self.get_object()

        request.user.comments_likes.like(comment)

        serializer = self.get_serializer(comment)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(methods=['post'],
            detail=True)
    def remove_like(self, request, *args, **kwargs):
        comment = self.get_object()

        request.user.comments_likes.remove_like(comment)
        serializer = self.get_serializer(comment)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
