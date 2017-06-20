from django.contrib import messages
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
    # URL에 전달되어온 post_pk로 특정 Post객체 가져옴
    post = get_object_or_404(Post, pk=post_pk)
    # URL의 GET parameter의 'next'값을 가져옴
    next = request.GET.get('next')
    # CommentForm data binding
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()

    else:
        result = '<br>'.join(['<br>'.join(v) for v in form.errors.values()])
        messages.error(request, result)
    if next:
        return redirect(next)
    return redirect('post:post_detail', post_pk=post.pk)


def comment_modify(request, post_pk, comment_pk):
    pass


def comment_delete(request, post_pk, comment_pk):
    pass
