import uuid

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from apps.core.user.like_manager import LikeManager

from apps.core.abstract.models import (
    AbstractModel,
    AbstractManager
)


def user_directory_path(instance, filename):
    return f'user_{instance.public_id}/{filename}'


class UserManager(BaseUserManager,
                  AbstractManager):
    def create_user(self, username, email, password=None, **kwargs):
        """
        Создать и вернуть объект "User"
        с email, phone_number, username, password

        :param username:
        :param email:
        :param password:
        :param kwargs:
        :return:
        """
        if username is None:
            raise TypeError('Users must have username')
        if email is None:
            raise TypeError('Users must have email')
        if password is None:
            raise TypeError('Users must have password')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **kwargs):
        """
        Создать и вернуть объект "User" с admin правами
        :param username:
        :param email:
        :param password:
        :param kwargs:
        :return:
        """

        if password is None:
            raise TypeError('Superusers must have password')
        if email is None:
            raise TypeError('Superusers must have email')
        if username is None:
            raise TypeError('Superusers must have username')

        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
            **kwargs
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractModel,
           AbstractBaseUser,
           PermissionsMixin):
    username = models.CharField(db_index=True,
                                max_length=255,
                                unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True,
                              unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    bio = models.TextField(null=True,
                           blank=True)
    avatar = models.ImageField(upload_to=user_directory_path,
                               null=True,
                               blank=True)

    posts_liked = models.ManyToManyField(to='core_post.Post',
                                         related_name='liked_by')
    comments_liked = models.ManyToManyField(to='core_comment.Comment',
                                            related_name='liked_by')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def posts_likes(self):
        return LikeManager(self.posts_liked)

    @property
    def comments_likes(self):
        return LikeManager(self.comments_liked)

    # def like(self, post):
    #     return self.posts_liked.add(post)
    #
    # def remove_like(self, post):
    #     return self.posts_liked.remove(post)
    #
    # def has_liked(self, post):
    #     return self.posts_liked.filter(pk=post.pk).exists()
