from rest_framework_nested import routers

from apps.core.auth.viewsets import RefreshViewSet
from apps.core.auth.viewsets.login import LoginViewSet
from apps.core.auth.viewsets.register import RegisterViewSet
from apps.core.comment.viewsets import CommentViewSet
from apps.core.post.viewsets import PostViewSet
from apps.core.user.viewsets import UserViewSet

router = routers.SimpleRouter()


## USER ##
router.register(r'user',
                UserViewSet,
                basename='user')

## AUTH ##
router.register(r'auth/register',
                RegisterViewSet,
                basename='auth-register')

router.register(r'auth/login',
                LoginViewSet,
                basename='auth-login')
router.register(r'auth/refresh',
                RefreshViewSet,
                basename='auth-refresh')

## POST ##
router.register(r'post', PostViewSet, basename='post')

posts_router = routers.NestedSimpleRouter(router,
                                          r'post',
                                          lookup='post')
posts_router.register(r'comment',
                      CommentViewSet,
                      basename='post-comment')

urlpatterns = [
    *router.urls,
    *posts_router.urls,
]
