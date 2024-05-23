from django.db import models

from apps.core.abstract.models import (
    AbstractModel,
    AbstractManager
)


class CommentManager(AbstractManager):
    pass


class Comment(AbstractModel):
    post = models.ForeignKey(to='core_post.Post',
                             related_name='comments',
                             on_delete=models.PROTECT)
    author = models.ForeignKey(to='core_user.User',
                               on_delete=models.PROTECT)
    body = models.TextField()
    edited = models.BooleanField(default=False)

    objects = CommentManager()

    def __str__(self):
        return self.author.name

    class Meta:
        ordering = ['-created']
