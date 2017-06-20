from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
# 자동으로 Django에서 인증에 사용하는 User모델클래스를 리턴
#   https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#django.contrib.auth.get_user_model
from django.views.decorators.http import require_POST

from post.forms.comment import CommentForm

User = get_user_model()

from ..models import Post

__all__ = (
    'comment_create',
    'comment_modify',
    'comment_delete',
)


@require_POST
@login_required
def comment_create(request, post_pk):
    # POST요청을 받아 Commemnt객체를 생성 후 post_detail 페이지로 redirect
    post = get_object_or_404(Post, pk=post_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('post:post_detail', post_pk=post.pk)


def comment_modify(request, post_pk, comment_pk):
    pass


def comment_delete(request, post_pk, comment_pk):
    pass
