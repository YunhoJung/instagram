from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.template import loader

from post.models import Post


def post_list(request):
    # 모든 Post목록을 'post'라는 key로 context에 담아 return render 처리
    # post/post_list.html을 template으로 사용하도록 한다.
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'post/post_list.html', context)


def post_detail(request, post_pk):
    # post_pk에 해당하는 Post객체를 리턴, 보여줌
    # Model(DB)에서 post_pk에 해당하는 Post객체를 가져와 변수에 할당
    # ModelManager의 get메서드를 사용해서 단 한개의 객체만 가져온다
    # https://docs/djanggoproject.com/en/1.11/ref/models/querysets/#get

    # 가져오는 과정에서 예외처리를 한다 (Model.DoesNotExist)
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist as e:
        # 1. 404 Not found를 띄어준다
        # return HttpResponseNotFound('Post not found, detail: {}'.format(e))
        # 2. post_list view로 들어간다
        # redirect
        return redirect('post:post_list')

    # request에 대해 response를 돌려줄 때는 HttpResponse나 render를 사용가능
    # template을 사용하려면 render 함수를 사용한다
    # render 함수는
    # django.template.loader.get_template함수와
    # django.http.HttpResponse함수를 축약해 놓은 shortcut이다
    #   http://docs.djangoproject.com/en/1.1/topics/template

    # ! 이 뷰에서는 render를 사용하지 않고 전체 과정 (loader, HttpResponse)을 기술.
    # Django가 템플릿을 검색할 수 이는 모든 디렉토리를 순회하며
    # 인자로 주어진 문자열값과 일치하는 템플릿이 있는지 확인 후
    # 결과를 리턴 django.template.backends.django.Template at 0x103809160>

    template = loader.get_template('post/post_detail.html')
    # dict형 변수 context의 'post'키에 post(Post객체)를 할당
    context = {
        'post': post,  # context로 전달될 dict의 '키'값이 템플릿에서 사용가능한 변수명이됨
    }
    rendered_string = template.render(context=context, request=request)
    return HttpResponse(rendered_string)


def post_create(request):
    # POST요청을 받아 Post객체를 생성 후 post_list페이지로 redirect
    pass


def post_delete(request):
    # post_pk에 해당하는 Post에 대한 delete요청만을 받음
    # 처리완료 후에는 post_list페이지로 redirect
    pass


def comment_create(request, post_pk):
    # POST요청을 받아 Commemnt객체를 생성 후 post_detail 페이지로 redirect
    pass


def comment_modify(reuest, post_pk):
    # 수정
    pass


def comment_delete(request, post_pk, comment_pk):
    pass
