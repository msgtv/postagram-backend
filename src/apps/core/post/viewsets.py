from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from apps.core.auth.permissions import UserPermission
from apps.core.abstract.viewsets import AbstractViewSet
from apps.core.post.models import Post
from apps.core.post.serializers import PostSerializer


class PostViewSet(AbstractViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = [UserPermission]
    serializer_class = PostSerializer
    ordering = ("-created",)
    filterset_fields = ["author__public_id"]

    def get_queryset(self):
        return Post.objects.all()

    def get_object(self):
        obj = Post.objects.get_object_by_public_id(self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)

        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    @action(detail=True,
            methods=['post'])
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user

        user.posts_likes.like(post)

        serializer = self.serializer_class(post)

        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    @action(detail=True,
            methods=['post'])
    def remove_like(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user

        user.posts_likes.remove_like(post)

        serializer = self.serializer_class(post)

        return Response(serializer.data,
                        status=status.HTTP_200_OK)
