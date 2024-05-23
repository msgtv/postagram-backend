import pytest

from apps.core.fixtures.post import post
from apps.core.fixtures.user import user
from apps.core.comment.models import Comment


@pytest.mark.django_db
def test_create_comment(user, post):
    comment = Comment.objects.create(
        author=user,
        post=post,
        body="This is a test comment",
    )

    assert comment.author == user
    assert comment.post == post
    assert comment.body == "This is a test comment"
