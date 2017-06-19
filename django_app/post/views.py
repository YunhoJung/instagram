from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

# 자동으로 Django에서 인증에 사용하는 User모델클래스를 리턴
#   https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#django.contrib.auth.get_user_model
from post.custom_decorator import post_owner
from .forms import PostForm

User = get_user_model()

from .models import Post


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
        # 1. 404 Notfound를 띄워준다
        # return HttpResponseNotFound('Post not found, detail: {}'.format(e))

        # 2. post_list view로 돌아간다
        # 2-1. redirect를 사용
        #   https://docs.djangoproject.com/en/1.11/topics/http/shortcuts/#redirect
        # return redirect('post:post_list')
        # 2-2. HttpResponseRedirect
        #   https://docs.djangoproject.com/en/1.11/ref/request-response/#django.http.HttpResponseRedirect
        url = reverse('post:post_list')
        return HttpResponseRedirect(url)

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


@login_required
def post_create(request):
    # POST요청을 받아 Post객체를 생성 후 post_list페이지로 redirect
    if request.method == "POST":
        # user = User.objects.first()
        # post = Post.objects.create(
        #     author=user,
        #     # request.FILES에서 파일을 가져오기
        #     # http://docs.djangoproject.com/en/1.11/topics/http/file-uploads/#basic-file-uploads
        #     # 가져온 파일을 ImageField에 넣도록 설정
        #     # 'file'은 POST요청시 input[type="file"]이 가진 name속성
        #     photo=request.FILES['photo'],
        # )
        # # POST요청시 name이 'comment'인 input에서 전달된 값을 가져옴
        # # dict.get()
        # comment_string = request.POST.get('comment', '')  # request는 딕셔러니 형태
        # # 빈 문자열 ''이나 None 모두 False로 평가되므로
        # # if not으로 댓글로 쓸 내용 도는 comment키가 전달되지 않았음을 검사 가능
        # if comment_string:
        #     # 댓글로 사용할 문자열이 전달된 경우 위에서 생성한 post객체에 연결되는 Comment객체를 생성해준다.
        #     post.comment_set.create(
        #         author=user,
        #         content=comment_string,
        #     )
        form = PostForm(data=request.POST, files=request.FILES)
        # ModeForm의 save()메서드를 사용해서 Post객체를 가져옴
        if form.is_valid():
            post = form.save(author=request.user)
            # post = form.save(commit=False)
            # post.author = request.user
            # post.save()
            #
            # comment_string = form.cleaned_data['comment']
            # if comment_string:
            #     post.comment_set.create(
            #         author=request.user,
            #         content=comment_string
            #     )

            return redirect('post:post_detail', post_pk=post.pk)
    else:
        # post/post_create.html을 render해서 리턴
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'post/post_create.html', context=context)


@post_owner
@login_required
def post_modify(request, post_pk):
    post = Post.objects.get(pk=post_pk)

    if request.method == "POST":
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        form.save()
        return redirect('post:post_detail', post_pk=post_pk)
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, 'post/post_modify.html', context=context)


def post_delete(request):
    # post_pk에 해당하는 Post에 대한 delete요청만을 받음
    # 처리완료 후에는 post_list페이지로 redirect
    pass


def comment_create(request, post_pk):
    # POST요청을 받아 Commemnt객체를 생성 후 post_detail 페이지로 redirect
    pass


def comment_modify(request, post_pk):
    pass


def comment_delete(request, post_pk, comment_pk):
    pass


def post_anyway(request):
    return redirect('post:post_list')
