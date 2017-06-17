from django.contrib.auth import authenticate, login as django_login, logout as django_logout, get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm

User = get_user_model()


def login(request):
    # member/login.html 생성
    # username, password, button이 있는 HTML
    # POST요청이 올 경우 좌측 코드를 기반으로 로그인 완료 후 post_list로 이동
    # 실해할 경우 HttpResponse로 'Login invalid!' 띄어주기

    # member/urls.py 생성
    # /member/login/으로 접근시 이 view로 오도록 설정
    # config/urls.py에 member/urls.py를 include
    #   member/urls.py에 app_name설정으로 namespace지정
    if request.method == 'POST':
        # 요청받은 POST데이터에서 username, password키가 가진 값들을
        # username, password변수에 할당 (문자열)
        # username = request.POST['username']
        # password = request.POST['password']
        # authenticate함수를 사용해서 User객체를 얻어 user에 할당
        # 인증에 실패할 경우 user변수에는 None이 할당됨
        # user = authenticate(
        #     request,
        #     username=username,
        #     password=password,
        # )
        # if user is not None:
        # # Django의 session을 이용해 이번 request와 user객체를 사용해 로그인 처리
        #     # 이후의 request/response에서는 사용자가 인증된 상태로 통신이 이루어진다
        #     django_login(request, user)
        #     # 로그인 완료 후에는 post_list뷰로 리다이렉트 처리
        #     return redirect('post:post_list')
        # # user변수가 None일 경우 (username 또는 password가 틀려 인증에 실패한 경우)

        # Form 클래스 사용시
        # Bound form 생성
        form = LoginForm(data=request.POST)
        # Bound form의 유효성을 검증 통과하면 true bool 반환
        if form.is_valid():
            user = form.cleaned_data['user']
            django_login(request, user)
            # 일반적인 경우에는 post_list로 이동하지만,
            # GET parameter의 next속성값이 있을 경우 해당 URL로 이동
            next = request.GET.get('next')
            if next:
                return redirect(next)
            return redirect('post:post_list')


        # user변수가 None이 아닐 경우 (정상적으로 인증되어 User객체를 얻은 경우)
        #
    # get 요청이 왔을 경우, 단순 로그인 Form 보여주기
    else:
        # 만약 이미 로그인 된 상태일 경우에는
        # post_list로 redirect
        # 아닐경우 login.html을 render해서 리턴
        if request.user.is_authenticated:
            return redirect('post:post_list')
        form = LoginForm()  # unbound form
        context = {
            'form': form,
        }
        return render(request, 'member/login.html', context=context)


        # render, redirect, httpresponse, ??


def logout(request):
    # 로그아웃되면 post_list로 redirect
    django_logout(request)
    return redirect('post:post_list')


def signup(request):
    if request.method == "POST":
        #     username = request.POST['username']
        #     password1 = request.POST['password1']
        #     password2 = request.POST['password2']
        #     if User.objects.filter(username=username).exists():
        #         return HttpResponse('Username is already exist')
        #     elif password1 != password2:
        #         return HttpResponse('Password and Password check are not equal')
        #     user = User.objects.create_user(
        #         username=username,
        #         password=password1
        #     )
        form = SignupForm(data=request.POST)
        if form.is_valid():
            user = form.create_user()
            # if User.objects.filter(username=username).exists():
            #         return HttpResponse('Username is already exist')
            #     elif password1 != password2:
            #         return HttpResponse('Password and Password check are not equal')
            #     user = User.objects.create_user(
            #         username=username,
            #         password=password1
            #     )
            #
            django_login(request, user)
            return redirect('post:post_list')

    else:
        form = SignupForm()
    context = {
        'form': form,
    }
    return render(request, 'member/signup.html', context)

# url은 /member/signup/$
# member/signup.html을 사용
#   username, password1, password2를 받아 회원가입
#   이미 유저가 존재하는지 검사
#   password1, 2가 일치하는지 검사
#   각각의 경우를 검사해서 틀릴 경우 오류메시지 리턴
#   가입에 성공시 로그인시키고 post_list로 리다이렉트
