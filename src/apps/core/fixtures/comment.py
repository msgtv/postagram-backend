import pytest

from apps.core.fixtures.user import user
from apps.core.fixtures.post import post

from apps.core.comment.models import Comment


@pytest.fixture
def comment(db, user, post):
    return Comment.objects.create(
        author=user,
        post=post,
        body="This is a test comment",
    )
