from django.http import HttpResponse
from django.shortcuts import render

from post.models import Post


def post_list(request):
    # 모든 Post목록을 'post'라는 key로 context에 담아 return render 처리
    # post/post_list.html을 template으로 사용하도록 한다.
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context)
